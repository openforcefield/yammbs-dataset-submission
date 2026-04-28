The files in this folder are generated from the following submissions:

* [`Sage 2.3.0 RC2`](https://github.com/openforcefield/yammbs-dataset-submission/pull/77), same as 2.3.0
* [`Rosemary-alpha0-QM`](https://github.com/openforcefield/yammbs-dataset-submission/pull/111)
* [`Rosemary-alpha0-QM-Freeze`](https://github.com/openforcefield/yammbs-dataset-submission/pull/112)

These files are generated from running `plot.py` as follows:

```shell
$ python plot.py \
    submissions/2026-04-28-Rosemary-alpha0-QM \
    submissions/2026-04-28-Rosemary-alpha0-QM-freeze/ \
    submissions/2025-11-07-Sage-2.3.0-RC2/  \
    -o tmp/
```
