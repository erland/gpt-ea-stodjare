# CI, release och reproducerbar paketering

## Syfte

EA Stödjare ska kunna valideras, testas, exporteras och paketeras på samma sätt lokalt och i GitHub Actions. Git-taggen är versionskälla för en release.

## Workflows

### `.github/workflows/ci.yml`

Körs på push och pull request. Den:

1. installerar Python-beroenden,
2. installerar Pandoc och LibreOffice,
3. kör strukturell projektvalidering,
4. kör hela pytest-sviten,
5. regenererar Builder Knowledge till temporär katalog och jämför byte för byte,
6. smoke-testar publicerad DOCX/PDF-export.

### `.github/workflows/build-artifacts.yml`

Manuell workflow för att bygga referensartefakter utan att skapa en release. Den genererar:

- Markdown i `working` och `published`,
- Confluence markup i `working` och `published`,
- DOCX/PDF i `working` och `published`.

Artefakterna laddas upp som ett GitHub Actions-artifact.

### `.github/workflows/release.yml`

Körs på taggar som följer `vMAJOR.MINOR.PATCH`, exempelvis `v1.0.0`.

Releasejobbet:

1. validerar taggens format,
2. validerar projektet,
3. kör alla tester,
4. bygger en deterministisk release-zip,
5. packar upp zippen och validerar det packade projektet,
6. laddar upp zip och release-metadata som workflow-artifact,
7. skapar GitHub Release med samma tagg och bifogar filerna.

## Versionskälla

`scripts/package_release.py` löser version i denna ordning:

1. explicit `--version`,
2. miljövariabeln `EA_STODJARE_VERSION`,
3. GitHub-taggen via `GITHUB_REF_NAME`,
4. exakt lokal Git-tag.

I normal release används alltså Git-taggen. Versionsnummer dupliceras inte som en manuellt underhållen releaseversion i projektfilerna.

## Reproducerbar zip

Releasepaketet byggs med:

- deterministiskt sorterad filordning,
- fast ZIP-tidsstämpel,
- fasta filrättigheter,
- deterministisk komprimering,
- exkludering av `.git`, `.pytest_cache`, `__pycache__`, virtuella miljöer och `dist/build`.

För identiskt källträd och identisk version ska två körningar därför ge samma SHA-256.

Varje release skapar dessutom `ea-stodjare-X.Y.Z.release.json` med bland annat arkivets SHA-256 och versionskälla.

## Lokal kontroll

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_project.py --project-root .
python -m pytest -q
```

Dokumentexport kräver dessutom Pandoc och LibreOffice.

Bygg ett releasepaket lokalt, exempelvis:

```bash
python scripts/package_release.py --project-root . --output-dir dist --version v1.0.0
```

I en riktig release bör versionen normalt komma från Git-taggen i stället för `--version`.

## Releaseförfarande

1. Säkerställ att `main` är grön i CI.
2. Skapa och pusha en semantisk tagg, exempelvis `v1.0.0`.
3. Release-workflowen validerar och paketerar automatiskt.
4. GitHub Release skapas endast om validering och tester passerar.

Steg 28 avgör om projektets första faktiska releasekandidat ska märkas `v1.0.0`.
