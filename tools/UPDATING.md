# How the shop copy is updated

Source of truth: the "BearSt Allergen Matrix" Claude artifact
https://claude.ai/artifact/HZvok4XeMvPcty6uGcPcmw (edited by staff with the Edit button).

To refresh this site:
1. Read the artifact's current HTML (Artifact tool, action "read") and save it.
2. For every `/_blob/<id>` referenced in it, fetch that asset (Artifact read with `path: <id>`)
   and save it as `<photo-dir>/<id>.jpg`. Photos already in `photos/` can be reused.
3. Run `python3 tools/build_shop.py <artifact.html> <photo-dir> <out-dir>`.
4. Copy `<out-dir>/index.html` and `<out-dir>/photos/` over the repo root, commit, push to `main`.
GitHub Pages then serves https://mf994.github.io/bearst-allergens/ within a minute or two.
