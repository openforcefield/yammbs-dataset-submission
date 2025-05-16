# yammbs-dataset-submission
Input files and scripts for benchmarking OpenFF force fields with yammbs

## Usage

### Running benchmarks in CI
0. Create a new branch starting from the `main` branch.
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
5. Make a comment of the form `/run-optimization-benchmarks path/to/submission
   [conda-env.yaml]` or `/run-torsion-benchmarks path/to-submission
   [conda-env.yaml]` on the PR. The brackets indicate an optional argument. If
   the path to the conda environment is omitted, the default environment will
   be used ([devtools/env.yaml](devtools/env.yaml)).
6. Wait for the benchmarks to finish.
7. Review the results, and update your submission with a README containing a
   link to the Zenodo archive created by CI.
   * An OpenFF admin (probably your PR reviewer) will need to manually publish
     the Zenodo entry before you can do this.
8. Merge your PR!

#### Output

This will produce CSV files corresponding to the DDE, RMSD, TFD, and
internal-coordinate RMSD (ICRMSD) metrics computed by [yammbs][yammbs].

### Forks

Running from forks is not supported. To gain access to push directly, contact @mattwthompson.

### Generating datasets

See [datasets/README.md](datasets/README.md)

## Benchmark Results

| Submission                                      | Description                                                                        | DOI                                                                                                         |
|-------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| [smirnoff99Frosst-1.1.0](submissions/2025-05-07-s99f-1.1.0) (note this has hbond constraints))                   | smirnoff99Frosst-1.1.0.offxml                                                  | https://doi.org/10.5281/zenodo.15361270       |
| [Parsley-1.3.1](submissions/2025-05-07-Parsley-1.3.1) (same settings as below)        | openff_unconstrained-1.3.1.offxml                                                  | https://doi.org/10.5281/zenodo.15362656                                                                 |
| [Parsley-1.3.1-unconstrained]                   | openff_unconstrained-1.3.1.offxml                                                  | [10.5281/zenodo.14172472](https://doi.org/10.5281/zenodo.14172472)                                          |
| [Sage-2.0.0](submissions/2024-11-19-Sage-2.0.0) | openff_unconstrained-2.0.0.offxml                                                  | [10.5281/zenodo.14188644](https://doi.org/10.5281/zenodo.14188644)                                          |
| [Sage-2.1.0]                                    | openff-2.1.0.offxml                                                                | [10.5281/zenodo.14053221](https://doi.org/10.5281/zenodo.14053221)                                          |
| [Sage-2.1.0-unconstrained]                      | openff_unconstrained-2.1.0.offxml                                                  | [10.5281/zenodo.14058464](https://doi.org/10.5281/zenodo.14058464)                                          |
| [Sage-2.2.1](submissions/2024-11-21-Sage-2.2.1) | openff_unconstrained-2.2.1.offxml                                                  | [10.5281/zenodo.14200591](https://doi.org/10.5281/zenodo.14200591)                                          |
| [Null-0.0.3](submissions/2024-12-03-Null-0.0.3) | Protein parameter fit, null model v0.0.3, unconstrained                            | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14270907.svg)](https://doi.org/10.5281/zenodo.14270907) |
| [Null-0.0.3-Looser-Priors][nlp]                 | Protein parameter fit, null model v0.0.3, unconstrained with looser torsion priors | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14270934.svg)](https://doi.org/10.5281/zenodo.14270934) |
<!-- ENDOFTABLE -->

[Sage-2.1.0]: submissions/2024-11-07-Sage-2.1.0
[Sage-2.1.0-unconstrained]: submissions/2024-11-08-Sage-2.1.0-unconstrained
[Parsley-1.3.1-unconstrained]: submissions/2024-11-13-Parsley-1.3.1
[nlp]: submissions/2024-12-03-Null-0.0.3-Looser-Priors


<!-- References -->
[qcsubmit]: https://github.com/openforcefield/openff-qcsubmit
[yammbs]: https://github.com/openforcefield/yammbs
