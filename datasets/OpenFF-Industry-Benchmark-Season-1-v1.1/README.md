This submission is slightly different from future submissions because of the
changes suggested in
[#7](https://github.com/openforcefield/yammbs-dataset-submission/pull/7).
Namely, the dataset name and `chunksize` are now passed via the command line
rather than being part of a config file (`industry.yaml` in this case). For that
reason, a copy of the version of `download_and_filter_dataset.py` (previously
called `new_dataset.py`) is also included here.

Additionally, the cache file `first1000.json` contains the first 100 entries in
from `cache.json` for testing purposes. This file was produced by manipulating
`cache.json` with `jq`:

``` shell
jq '{qm_molecules: .qm_molecules[:100], tag: .tag, version: .version}' cache.json > first100.json
```

