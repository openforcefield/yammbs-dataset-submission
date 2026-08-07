# Combined dataset

This dataset was created by combining the following already-downloaded QCArchive datasets with `combine_downloaded_datasets.py`:

- `OpenFF-NSP-Optimization-Set-1-Nitrogen-v4.0` (2720 molecules)
- `OpenFF-NSP-Optimization-Set-1-Phosphorus-v4.0` (2544 molecules)
- `OpenFF-NSP-Optimization-Set-1-Sulfur-v4.0` (3232 molecules)

Total: 8496 molecules.

Generated on 2026-08-04.

The `cache.json` in this directory is the union of the source datasets' `cache.json` files and is the file that should be used for benchmark runs.
