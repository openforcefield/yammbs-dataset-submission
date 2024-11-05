## Adding a new dataset
The general steps for adding a new dataset are:
1. Run `download_and_filter_dataset.py` passing as arguments:
   * The dataset name on QCArchive
   * (optional) The number of CPUs to use in [multiprocessing.Pool][pool],
     defaults to 1
   * (optional) The chunk size for [multiprocessing.Pool.imap][imap], defaults
     to 1
2. Move your input file and any log files (if run as a batch job, for example)
   into the created dataset directory
3. Commit the results to the repo
4. Open a PR for review before merging

### Submission script
`submit.sh` is an example Slurm submission script for running
`download_and_filter_dataset.py` on UCI's HPC3. It may need to be modified to
work on other clusters, but please do not include these changes as part of
dataset submission. Basic usage is just `./submit.sh "Name of QCA dataset"`, but
it also supports a few flags to control the time requested (`-t` in hours), the
memory requested (`-m` in GB), the number of CPUs (`-n`), and the [imap][imap]
chunk size (`-c`) as described above. These must come before the name of the
input file on the command line. There's also a "dry run" flag (`-d`) that prints
the generated `sbatch` input instead of running it immediately.

#### Conda environment
The example submission script activates an environment called
`yammbs-dataset-submission`, so you'll need to have one of those available. You
can create such an environment using the provided [env.yaml
file](../devtools/env.yaml).

[pool]: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
[imap]: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.imap
