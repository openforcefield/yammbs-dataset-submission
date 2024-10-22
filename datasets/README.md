## Adding a new dataset
The general steps for adding a new dataset are:
1. Prepare an input YAML file specifying
   * The dataset name on QCArchive
   * The chunk size for Python's multiprocessing (32 is a good default)
2. Submit the run on HPC3 with [submit.sh](submit.sh)
3. Move your input file and Slurm log file into the created dataset directory
4. Commit the results to the repo

### Input format
The input file is currently quite simple, just requiring the two fields
mentioned above. For example:

```yaml
ds_name: "OpenFF Industry Benchmark Season 1 v1.1"
chunksize: 32
```

`ds_name` should correspond to an existing optimization dataset on QCArchive.
The other two parameters just need to be non-zero integers and will be passed to
Python's [Pool][pool] and [Pool.imap][imap], respectively.

### Submission script
`submit.sh` is a Slurm-script-generating script. Basic usage is just
`./submit.sh input.yaml`, but it also supports a few flags to control the time
requested (`-t` in hours), the memory requested (`-m` in GB), and the number of
CPUs (`-n`). These must come before the name of the input file on the command
line. There's also "dry run" flag (`-d`) that prints the generated sbatch input
instead of running it immediately.

#### Conda environment
The submission script activates an environment called
`yammbs-dataset-submission`, so you'll need to have one of those available. You
can create such an environment using the provided [env.yaml
file](../devtools/env.yaml).

[pool]: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
[imap]: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.imap
