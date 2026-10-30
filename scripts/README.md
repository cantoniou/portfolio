Both scripts use only the Python standard library (3.9+).

- `refresh_openalex.py` — rewrites the `openalex` block of `data/metrics.json` from the OpenAlex API. `--dry-run` prints the changes without writing.
- `check_consistency.py` — cross-checks the data files; exit code 1 if anything needs fixing.
