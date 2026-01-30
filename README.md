# yammbs-dataset-submission
Input files and scripts for benchmarking OpenFF force fields with yammbs

## Usage

### Running benchmarks in CI

Note: as running benchmarks in CI uses paid AWS images, please ensure you have
discussed your projects and plans with a member of the OpenFF leadership team
before you open a pull request.

0. Create a new branch starting from the `main` branch.
1. Create a new entry in the `submissions` directory, with the general format
   `YYYY-MM-DD-Name`. For example:

   ``` shell
   mkdir submissions/$(date +%Y-%m-%d)-Sage-2.1.0
   ```
2. Add a YAML input file named `input.yaml` in this directory specifying the force field and datasets
   to use for the run.
   
   All paths in the file must be relative to the root of the repository.

   Currently only single datasets are supported.
   Currently only cached datasets are supported.

   If using a new force field file (as in the below example) commit that file to the branch.
   ``` yaml
   forcefield: submissions/2025-10-31-Spooky-FF-v3/spooky-ff-v3.offxml
   datasets:
      - datasets/OpenFF-Industry-Benchmark-Season-1-v1.1/cache.json
   ```

   Force fields can also correspond to built-in force fields recognized by the toolkit, for example:
   
   For example:
   ``` yaml
   forcefield: openff-2.1.0.offxml
   datasets:
      - datasets/OpenFF-Industry-Benchmark-Season-1-v1.1/cache.json
   ```

3. Push your branch and open a PR.
4. Request a review, and get the PR approved.
5. Make a comment of the form `/run-optimization-benchmarks path/to/submission/input.yaml
   [conda-env.yaml]` or `/run-torsion-benchmarks path/to-submission/input.yaml
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
| [GAFF-2.11](submissions/2025-05-07-GAFF) | GAFF-2.11+AM1BCC (via openmmforcefields)                                                  | https://doi.org/10.5281/zenodo.15361197
| [Parsley-1.0.0-unconstrained](submissions/2025-05-07-Parsley-1.0.0)                   | openff_unconstrained-1.0.0.offxml                                                  | https://doi.org/10.5281/zenodo.15361226                                         |
| [smirnoff99Frosst-1.1.0](submissions/2025-05-07-s99f-1.1.0) (note this has hbond constraints))                   | smirnoff99Frosst-1.1.0.offxml                                                  | https://doi.org/10.5281/zenodo.15361270       |
| [Parsley-1.3.1](submissions/2025-05-07-Parsley-1.3.1) (same settings as below)        | openff_unconstrained-1.3.1.offxml                                                  | https://doi.org/10.5281/zenodo.15362656                                                                 |
| [Parsley-1.3.1-unconstrained]                   | openff_unconstrained-1.3.1.offxml                                                  | [10.5281/zenodo.14172472](https://doi.org/10.5281/zenodo.14172472)                                          |
| [Sage-2.0.0](submissions/2024-11-19-Sage-2.0.0) | openff_unconstrained-2.0.0.offxml                                                  | [10.5281/zenodo.14188644](https://doi.org/10.5281/zenodo.14188644)                                          |
| [Sage-2.1.0]                                    | openff-2.1.0.offxml                                                                | [10.5281/zenodo.14053221](https://doi.org/10.5281/zenodo.14053221)                                          |
| [Sage-2.1.0-unconstrained]                      | openff_unconstrained-2.1.0.offxml                                                  | [10.5281/zenodo.14058464](https://doi.org/10.5281/zenodo.14058464)                                          |
| [Sage-2.2.1](submissions/2024-11-21-Sage-2.2.1) | openff_unconstrained-2.2.1.offxml                                                  | [10.5281/zenodo.14200591](https://doi.org/10.5281/zenodo.14200591)                                          |
| [Null-0.0.3](submissions/2024-12-03-Null-0.0.3) | Protein parameter fit, null model v0.0.3, unconstrained                            | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14270907.svg)](https://doi.org/10.5281/zenodo.14270907) |
| [Null-0.0.3-Looser-Priors][nlp]                 | Protein parameter fit, null model v0.0.3, unconstrained with looser torsion priors | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14270934.svg)](https://doi.org/10.5281/zenodo.14270934) |
| [2025-08-13-smee-spice2-systematic-torsion-generation](submissions/2025-08-13-smee-spice2-systematic-torsion-generation)                 | [Fit to SPICE2 using SMEE, with proper torsion types systematically generated from the dataset](https://github.com/fjclark/descent-workflow/tree/main) | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16864755.svg)](https://doi.org/10.5281/zenodo.16864755) |
| [Split vdW N v1](submissions/2025-09-16-split-N-vdW-v1) | Split vdW N parameters, v1 | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17196559.svg)](https://doi.org/10.5281/zenodo.17196559) |
| [Protein-Null-AAQAA3-3-OPC3](submissions/2025-09-19-protein-null-aaqaa3-3-opc3) | Protein NMR fit started from Null-QM | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17163141.svg)](https://doi.org/10.5281/zenodo.17163141)
| [Protein-Null-4-mer-AAQAA3-2-OPC3](submissions/2025-09-19-protein-null-4-mer-aaqaa3-2-opc3) | Protein NMR fit started from Null-4-mer-QM | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17163330.svg)](https://doi.org/10.5281/zenodo.17163330)
| [Protein-Specific-4-mer-AAQAA3-2-OPC3](submissions/2025-09-19-protein-specific-4-mer-aaqaa3-2-opc3) | Protein NMR fit started from Specific-4-mer-QM | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17163328.svg)](https://doi.org/10.5281/zenodo.17163328)
| [Sage-2.1.0 (rerun)](submissions/2025-10-20-Sage-2.1.0) | Re-running Sage 2.1.0 | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17404618.svg)](https://doi.org/10.5281/zenodo.17404618)
| [Sage 2.3.0 RC1](submissions/2025-11-07-Sage-2.3.0-RC1) | Sage 2.3.0 RC1 |[ ![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17555239.svg)](https://doi.org/10.5281/zenodo.17555239)
| [Sage 2.3.0 RC2](submissions/2025-11-07-Sage-2.3.0-RC2) | Sage 2.3.0 RC2 | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17555233.svg)](https://doi.org/10.5281/zenodo.17555233)
| [Rosemary-3.0.0-alpha0](submissions/2025-11-11-Rosemary-alpha0) | openff_no_water_unconstrained-3.0.0-alpha0.offxml | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17584227.svg)](https://doi.org/10.5281/zenodo.17584227)
| [openff-2.2.0-rc1-alkanes](submissions/2026-01-22-Sage-2.2.0-alkanes) | openff-2.2.0-rc1-alkanes.offxml | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18357086.svg)](https://doi.org/10.5281/zenodo.18357086)

<!-- ENDOFTABLE -->

[Sage-2.1.0]: submissions/2024-11-07-Sage-2.1.0
[Sage-2.1.0-unconstrained]: submissions/2024-11-08-Sage-2.1.0-unconstrained
[Parsley-1.3.1-unconstrained]: submissions/2024-11-13-Parsley-1.3.1
[nlp]: submissions/2024-12-03-Null-0.0.3-Looser-Priors


<!-- References -->
[qcsubmit]: https://github.com/openforcefield/openff-qcsubmit
[yammbs]: https://github.com/openforcefield/yammbs
