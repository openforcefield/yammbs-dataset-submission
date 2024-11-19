# yammbs-dataset-submission
Input files and scripts for benchmarking OpenFF force fields with yammbs

## Usage

### Running benchmarks in CI
0. Create a new branch starting from the `master` branch.
1. Create a new entry in the `submissions` directory, with the general format
   `YYYY-MM-DD-Name`. For example:

   ``` shell
   mkdir submissions/$(date +%Y-%m-%d)-Sage-2.1.0
   ```
2. Add a YAML input file in this directory specifying the force field and datasets
   to use for the run. For example:
   ``` yaml
   forcefield: openff-2.1.0.offxml
   datasets:
	   - datasets/cache/industry.json
   ```

   All paths should be relative to the root of the repository, and cached
   datasets must be used. Force fields can also correspond to built-in force
   fields recognized by the toolkit (as in the example). Currently only single
   datasets are supported.

3. Push your branch and open a PR.
4. Request a review, and get the PR approved.
5. Make a comment of the form `/run-benchmark path/to/submission
   [conda-env.yaml]` on the PR. The brackets indicate an optional argument. If
   the path to the conda environment is omitted, the default environment will be
   used ([devtools/env.yaml](devtools/env.yaml)).
6. Wait for the benchmarks to finish.
7. Review the results, and update your submission with a README containing a
   link to the Zenodo archive created by CI.
   * An OpenFF admin (probably your PR reviewer) will need to manually publish
     the Zenodo entry before you can do this.
8. Merge your PR!

#### Output

This will produce CSV files corresponding to the DDE, RMSD, TFD, and
internal-coordinate RMSD (ICRMSD) metrics computed by [yammbs][yammbs].

### Generating datasets

See [datasets/README.md](datasets/README.md)

## Benchmark Results

| Submission                    | Description                       | DOI                                                                |
|-------------------------------|-----------------------------------|--------------------------------------------------------------------|
| [Sage-2.1.0]                  | Constrained openff-2.1.0.offxml   | [10.5281/zenodo.14053221](https://doi.org/10.5281/zenodo.14053221) |
| [Sage-2.1.0-unconstrained]    | Unconstrained openff-2.1.0.offxml | [10.5281/zenodo.14058464](https://doi.org/10.5281/zenodo.14058464) |
| [Parsley-1.3.1-unconstrained] | Unconstrained openff-1.3.1.offxml | [10.5281/zenodo.14172472](https://doi.org/10.5281/zenodo.14172472) |

[Sage-2.1.0]: submissions/2024-11-07-Sage-2.1.0
[Sage-2.1.0-unconstrained]: submissions/2024-11-08-Sage-2.1.0-unconstrained
[Parsley-1.3.1-unconstrained]: submissions/2024-11-13-Parsley-1.3.1


<!-- References -->
[qcsubmit]: https://github.com/openforcefield/openff-qcsubmit
[yammbs]: https://github.com/openforcefield/yammbs
