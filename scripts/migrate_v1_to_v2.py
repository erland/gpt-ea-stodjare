#!/usr/bin/env python3
"""Safe, deterministic EA Stödjare v1 -> v2 migration engine.

The engine never overwrites the source. It can plan or apply a migration.
Ambiguous semantic changes are preserved explicitly and reported for review.
"""
from __future__ import annotations

import argparse, copy, hashlib, json, shutil, sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ENGINE_VERSION = "1.0"
V1_TYPES = ["driver","goal","principle","capability","it_support","platform_service","platform","standard","solution_pattern","reference_architecture"]
V1_RELATIONS = ["influences","supports","uses","realized_by","governed_by","constrains","depends_on","derived_from","related_to"]
V2_ONLY_RELATIONS = ["provided_by","can_realize"]
DERIVED_DIRS = [Path("docs/generated"), Path("exports/confluence"), Path("exports/document")]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_fingerprint(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        rel = path.relative_to(root).as_posix()
        h.update(rel.encode()); h.update(b"\0"); h.update(sha256(path).encode()); h.update(b"\n")
    return h.hexdigest()


def require_v1(root: Path) -> dict[str, Any]:
    mp = root / "project-manifest.json"
    if not mp.is_file():
        raise ValueError("Källprojektet saknar project-manifest.json")
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    model = manifest.get("model") or {}
    markers = (manifest.get("format"), manifest.get("format_version"), str(model.get("metamodel_version")), str(model.get("relation_model_version")))
    if markers != ("ea-stodjare-project", "1.0", "1.0", "1.0"):
        raise ValueError(f"Källprojektet är inte entydigt legacy v1: {markers}")
    return manifest


def scan(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    model_root = root / str((manifest.get("model") or {}).get("root", "model"))
    objects: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(model_root.glob("*.yaml")):
        data = load_yaml(path)
        if isinstance(data.get("objects"), list):
            objects[str(data.get("object_type"))] = [x for x in data["objects"] if isinstance(x, dict)]
    relations = load_yaml(model_root / "relations.yaml").get("relations", []) if (model_root / "relations.yaml").is_file() else []
    relations = [x for x in relations if isinstance(x, dict)]
    return {"model_root": model_root, "objects": objects, "relations": relations}


def infer_prefix(rows: list[dict[str, Any]], fallback: str) -> str:
    ids = [str(x.get("id")) for x in rows if x.get("id")]
    if not ids: return fallback
    first=ids[0]
    if "-" in first: return first.split("-",1)[0] + "-"
    return fallback


def build_plan(source: Path, manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    s = scan(source, manifest); objects=s["objects"]; rels=s["relations"]
    transforms=[]; issues=[]; attr_ext=[]; custom_types=[]; custom_relations=[]

    all_ids=[str(o.get("id")) for rows in objects.values() for o in rows if o.get("id")]
    all_ids += [str(r.get("id")) for r in rels if r.get("id")]

    cap_scope=[str(o.get("id")) for o in objects.get("capability",[]) if "scope" in o]
    if cap_scope:
        attr_ext.append({"object_type":"capability","attributes":[{"name":"scope","type":"embedded","required":False,"description":"Bevarat legacy v1-scope. Ska granskas och vid entydig boundary migreras till in_scope/out_of_scope."}]})
        transforms.append({"rule":"CAP-BND-001","action":"declared_extension","count":len(cap_scope),"details":"Legacy capability.scope bevaras oförändrat via projektspecifik attributextension.","ids":sorted(cap_scope)})
        issues.append({"code":"MIG-CAP-SCOPE","severity":"review_required","message":"Legacy capability.scope kan innehålla positiv, negativ eller blandad boundary och splittras därför inte automatiskt.","resolution":"Granska scope och migrera endast entydiga delar till in_scope/out_of_scope.","ids":sorted(cap_scope)})

    pls_ids=sorted(str(o.get("id")) for o in objects.get("platform_service",[]) if o.get("id"))
    if pls_ids:
        transforms.append({"rule":"PLS-SEM-001","action":"review_required","count":len(pls_ids),"details":"Plattformstjänster bevaras byte-semantiskt; v2:s realiseringsneutrala definition kräver semantisk granskning.","ids":pls_ids})
        issues.append({"code":"MIG-PLS-SEMANTICS","severity":"review_required","message":"v1 Plattformstjänst hade snävare gemensam/runtime-orienterad semantik än v2.","resolution":"Bekräfta att varje PLS fortfarande beskriver ett stabilt tekniskt erbjudande/funktionalitetskontrakt.","ids":pls_ids})

    plt_ids=sorted(str(o.get("id")) for o in objects.get("platform",[]) if o.get("id"))
    if plt_ids:
        transforms.append({"rule":"PLT-SEM-001","action":"review_required","count":len(plt_ids),"details":"Plattformar bevaras; v2 kräver konceptuell och produktneutral boundary som inte kan antas från v1.","ids":plt_ids})
        issues.append({"code":"MIG-PLT-SEMANTICS","severity":"review_required","message":"v1 Plattform kunde vara konkret teknisk grund/realisering; v2 Plattform är konceptuell produktneutral gruppering.","resolution":"Granska boundary, konsumtionslogik och livscykel innan objektet betraktas som fullt native v2.","ids":plt_ids})

    ambiguous=[]
    for r in rels:
        if r.get("type")=="realized_by" and str(r.get("source","")).startswith("PLS-") and str(r.get("target","")).startswith("PLT-"):
            ambiguous.append(str(r.get("id")))
    if ambiguous:
        custom_relations.append({
            "type":"legacy_realized_by","display_name":"legacy realiseras av",
            "definition":"Bevarad legacy v1-relation PLS→Plattform vars betydelse ännu inte verifierats som konceptuell provided_by eller konkret realisering.",
            "endpoints":[{"source":["platform_service"],"target":["platform"]}],"inverse":None,"provenance_required":True
        })
        transforms.append({"rule":"REL-PROV-001","action":"transformed","count":len(ambiguous),"details":"PLS→PLT realized_by byter endast relationskod till legacy_realized_by; ID, endpoints, status och proveniens bevaras.","ids":sorted(ambiguous)})
        issues.append({"code":"MIG-REALIZED-BY","severity":"review_required","message":"PLS→PLT realized_by kan inte säkert konverteras globalt till provided_by.","resolution":"Klassificera varje relation. Byt till provided_by endast när den faktiskt uttrycker konceptuell hemvist.","ids":sorted(ambiguous)})

    unknown_types=sorted(set(objects)-set(V1_TYPES)-{"None"})
    for typ in unknown_types:
        rows=objects[typ]
        common={"id","type","name","description","status","provenance","aliases","owner","tags","notes"}
        attrs=sorted({k for o in rows for k in o.keys()}-common)
        custom_types.append({"type":typ,"display_name":typ.replace("_"," ").title(),"id_prefix":infer_prefix(rows, typ[:3].upper()+"-"),"definition":"Migrerad projektspecifik legacy-objekttyp; semantik bevarad för fortsatt explicit projektmetamodellering.","attributes":[{"name":a,"type":"embedded","required":False} for a in attrs],"provenance_required":True,"model_file":next((p.name for p in s["model_root"].glob("*.yaml") if load_yaml(p).get("object_type")==typ), typ.replace("_","-")+"s.yaml")})
        transforms.append({"rule":"EXT-OBJ-001","action":"declared_extension","count":len(rows),"details":f"Projektspecifik objekttyp {typ} deklareras inline i v2 project metamodel.","ids":sorted(str(x.get("id")) for x in rows if x.get("id"))})

    enabled_types=[t for t in V1_TYPES if t in objects]
    # Keep canonical v1 types enabled even when their file is currently empty.
    for t in V1_TYPES:
        if t not in enabled_types and any((s["model_root"] / fn).is_file() for fn,tt in {"drivers.yaml":"driver","goals.yaml":"goal","principles.yaml":"principle","capabilities.yaml":"capability","it-support.yaml":"it_support","platform-services.yaml":"platform_service","platforms.yaml":"platform","standards.yaml":"standard","solution-patterns.yaml":"solution_pattern","reference-architectures.yaml":"reference_architecture"}.items() if tt==t): enabled_types.append(t)
    enabled_relations=list(V1_RELATIONS)
    custom_mode=bool(issues or custom_types or custom_relations)
    pm={
      "schema_version":"2.0",
      "project_metamodel":{
        "id":str((manifest.get("project") or {}).get("id","migrated-project"))+"-v2",
        "version":"2.0-migrated",
        "description":"Explicit v2-projektmetamodell skapad av v1→v2-migrationsmotorn. Legacy-semantik som inte säkert kan konverteras är deklarerad och rapporterad för granskning.",
        "base_profile":{"id":"ea-stodjare-v2","version":"2.0","compatibility_mode":"custom" if custom_mode else "native"},
        "object_types":{"enabled":sorted(enabled_types),"disabled":sorted(set(V1_TYPES+["product"])-set(enabled_types)),"custom":custom_types},
        "attribute_extensions":attr_ext,
        "relations":{"enabled":enabled_relations,"disabled":V2_ONLY_RELATIONS,"custom":custom_relations},
        "relation_qualifiers":[],"value_sets":[],"extensions":[],"derived_views":[],
        "presentation":{"contract":"reader-oriented-v1","object_display_pattern":"{name} ({id})","labels":{}},
        "governance":{"change_control":False,"baseline_id":None,"freeze_status":"review"},
        "notes":["Migration bevarar information framför automatisk semantisk normalisering.","Alla review_required-poster i migration/migration-report.yaml ska behandlas före påstående om full native-v2-semantik."]
      }
    }
    source_rev=int((manifest.get("project") or {}).get("revision",0))
    source_fp=tree_fingerprint(source)
    summary={"objects":sum(len(x) for x in objects.values()),"relations":len(rels),"stable_ids":len(all_ids),"review_issues":len(issues),"custom_object_types":len(custom_types),"custom_relations":len(custom_relations)}
    report={"schema_version":"1.0","migration":{
      "engine_version":ENGINE_VERSION,
      "source":{"profile":"ea-stodjare-v1","revision":source_rev,"fingerprint":source_fp},
      "target":{"profile":"ea-stodjare-v2","revision":source_rev+1,"fingerprint":"0"*64},
      "status":"planned",
      "summary":summary,
      "transformations":transforms,
      "issues":issues,
      "information_preservation":{"original_overwritten":False,"stable_ids_preserved":True,"canonical_source_content_deleted":False,"derived_artifacts_may_be_regenerated":True},
      "notes":["Target fingerprint sätts efter materialisering och beräknas utan project-manifest.json och migration-reportens eget fingerprintfält."]
    }}
    return pm,report


def role_for(rel: str) -> str:
    if rel.startswith("model/"): return "canonical_model"
    if rel.startswith("governance/") or rel.startswith("migration/") or rel=="project-metamodel.yaml": return "governance"
    if rel.startswith("schemas/"): return "schema"
    if rel.endswith(".md"): return "documentation_source"
    return "support"


def deterministic_target_fingerprint(root: Path) -> str:
    h=hashlib.sha256()
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name not in {"project-manifest.json","migration-report.yaml"} and "__pycache__" not in x.parts):
        rel=p.relative_to(root).as_posix(); h.update(rel.encode()); h.update(b"\0"); h.update(sha256(p).encode()); h.update(b"\n")
    return h.hexdigest()


def rewrite_manifest(target: Path, source_manifest: dict[str, Any]) -> None:
    m=copy.deepcopy(source_manifest); project=m.setdefault("project",{}); model=m.setdefault("model",{})
    project["revision"]=int(project.get("revision",0))+1; project["lifecycle_status"]="review"
    model["metamodel_version"]="2.0"; model["relation_model_version"]="2.0"; model["model_format_version"]="1.0"; model["provenance_model_version"]="1.0"
    # Step 16 layers are opt-in; migration does not invent market/actual assertions.
    m.pop("information_layers",None)
    files=[]
    for p in sorted(x for x in target.rglob("*") if x.is_file() and x.name!="project-manifest.json" and "__pycache__" not in x.parts):
        rel=p.relative_to(target).as_posix(); files.append({"path":rel,"role":role_for(rel),"required": rel.startswith("model/") or rel in {"project-metamodel.yaml","migration/migration-report.yaml"},"sha256":sha256(p)})
    m["files"]=files
    (target/"project-manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def apply(source: Path, target: Path, repo_root: Path, pm: dict[str, Any], report: dict[str, Any], source_manifest: dict[str, Any], validate: bool=True) -> None:
    if source.resolve()==target.resolve(): raise ValueError("Källprojektet får aldrig vara samma katalog som målprojektet.")
    if target.exists(): raise FileExistsError(f"Målkatalogen finns redan och skrivs inte över: {target}")
    shutil.copytree(source,target)
    removed=[]
    for rel in DERIVED_DIRS:
        p=target/rel
        if p.exists(): shutil.rmtree(p); removed.append(rel.as_posix())
    if removed:
        report["migration"]["transformations"].append({"rule":"DERIVED-001","action":"removed_derived","count":len(removed),"details":"Genererade derivat tas bort från migrationskopian och kan regenereras från den kanoniska modellen.","ids":removed})

    rel_path=target/str((source_manifest.get("model") or {}).get("root","model"))/"relations.yaml"
    data=load_yaml(rel_path)
    for r in data.get("relations",[]) or []:
        if isinstance(r,dict) and r.get("type")=="realized_by" and str(r.get("source","")).startswith("PLS-") and str(r.get("target","")).startswith("PLT-"):
            r["type"]="legacy_realized_by"
    dump_yaml(rel_path,data)
    dump_yaml(target/"project-metamodel.yaml",pm)
    report["migration"]["status"]="applied_with_review_required" if report["migration"]["issues"] else "applied"
    report["migration"]["target"]["fingerprint"]=deterministic_target_fingerprint(target)
    dump_yaml(target/"migration/migration-report.yaml",report)
    rewrite_manifest(target,source_manifest)

    schema=json.loads((repo_root/"schemas/migration-report.schema.json").read_text(encoding="utf-8"))
    errs=list(Draft202012Validator(schema).iter_errors(report))
    if errs: raise ValueError("Migreringsrapporten bryter mot schema: "+"; ".join(e.message for e in errs))
    if validate:
        from validate_project import validate_project
        ctx=validate_project(target,repo_root,check_generated=False)
        if ctx.errors:
            raise ValueError("Migrerat projekt validerar inte:\n"+"\n".join(x.format() for x in ctx.errors))


def main() -> int:
    ap=argparse.ArgumentParser(description="Planera eller genomför säker EA Stödjare v1→v2-migration.")
    ap.add_argument("--source",type=Path,required=True); ap.add_argument("--output",type=Path)
    ap.add_argument("--mode",choices=["plan","apply"],default="plan")
    ap.add_argument("--report",type=Path,help="Skriv planrapport till separat fil i plan-läge.")
    ap.add_argument("--no-validate",action="store_true")
    args=ap.parse_args(); source=args.source.resolve(); repo=Path(__file__).resolve().parents[1]
    try:
        manifest=require_v1(source); pm,report=build_plan(source,manifest)
        if args.mode=="plan":
            text=yaml.safe_dump(report,allow_unicode=True,sort_keys=False)
            if args.report: args.report.write_text(text,encoding="utf-8")
            else: print(text,end="")
            return 0
        if args.output is None: raise ValueError("--output krävs i apply-läge.")
        apply(source,args.output.resolve(),repo,pm,report,manifest,validate=not args.no_validate)
        print(f"Migration skapad: {args.output.resolve()}")
        return 0
    except Exception as exc:
        print(f"ERROR MIG-V1-V2: {exc}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
