from pathlib import Path
import copy, json, subprocess, tempfile, yaml
ROOT=Path(__file__).resolve().parents[2]

def load(p): return yaml.safe_load((ROOT/p).read_text(encoding="utf-8"))

def test_native_v2_function_contract():
    f=load("schemas/model-format.yaml")["function_instance"]
    assert f["id_scope"] == "parent_object"
    assert set(f["optional_fields"]) >= {"id","description","required"}
    assert "function_id_is_optional_and_local_to_parent_in_v2" in f["rules"]

def test_legacy_v1_snapshot_still_forbids_id():
    f=load("compatibility/ea-stodjare-v1/schemas/model-format.yaml")["function_instance"]
    assert f["optional_fields"] == ["description"]
    assert "function_has_no_global_id_in_v1" in f["rules"]

def test_validator_accepts_local_ids_and_rejects_duplicates():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        subprocess.run(["cp","-a",str(ROOT)+"/.",str(td)],check=True)
        mp=td/"project-manifest.json"
        m=json.loads(mp.read_text())
        # hashes become stale when fixture is edited; remove integrity inventory for focused semantic validation
        m["files"]=[]
        mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n")
        p=td/"model/it-support.yaml"
        d=yaml.safe_load(p.read_text())
        obj={
            "id":"ITS-999", "type":"it_support", "name":"Teststöd",
            "description":"Testobjekt för lokal funktionsidentitet.",
            "status":"candidate",
            "provenance":[{"evidence_type":"proposed","rationale":"Testfixture"}],
            "functions":[{"id":"F01","name":"A","required":True},{"id":"F02","name":"B"}],
        }
        d["objects"]=[obj]
        p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
        r=subprocess.run(["python3",str(td/"scripts/validate_project.py"),"--project-root",str(td)],capture_output=True,text=True)
        assert "STR-FUN" not in r.stdout+r.stderr
        d=yaml.safe_load(p.read_text()); d["objects"][0]["functions"][1]["id"]="F01"; p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
        r=subprocess.run(["python3",str(td/"scripts/validate_project.py"),"--project-root",str(td)],capture_output=True,text=True)
        assert "STR-FUN-003" in r.stdout+r.stderr
