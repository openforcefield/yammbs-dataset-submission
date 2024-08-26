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
6. Wait for the benchmarks to finish and merge your PR!

#### Output

This will produce CSV files corresponding to the DDE, RMSD, TFD, and
internal-coordinate RMSD (ICRMSD) metrics computed by [yammbs][yammbs].

### Generating datasets

See [datasets/README.md](datasets/README.md)

<!-- References -->
[qcsubmit]: https://github.com/openforcefield/openff-qcsubmit
[yammbs]: https://github.com/openforcefield/yammbs
