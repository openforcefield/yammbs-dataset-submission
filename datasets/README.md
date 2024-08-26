This directory contains datasets in the JSON-serialized
`OptimizationResultCollection` format from [qcsubmit][qcsubmit], as well as
scripts for retrieving and post-processing them.

| Type      | File                   | Description                                                                    |
|-----------|------------------------|--------------------------------------------------------------------------------|
| Script    | download.py            | Download a named dataset from [qcarchive][qcarchive]                           |
|           | filter.py              | Filter out problematic records from a dataset                                  |
|           | cache_dataset.py       | Convert a `qcsubmit.ResultCollection` into a cached version[^1]                |
|           | submit.sh              | General Slurm script for running Make commands                                 |
|           | Makefile               | Makefile showing how each file is produced                                     |
| Dataset   | industry.json          | OpenFF Industry Benchmark Season 1 v1.1                                        |
|           | tm-supp0.json          | OpenFF Torsion Benchmark Supplement v1.0                                       |
|           | tm-supp.json           | OpenFF Torsion Multiplicity Optimization Benchmarking Coverage Supplement v1.0 |
|           | filtered-tm-supp0.json | Filtered version of tm-supp0.json                                              |
|           | filtered-tm-supp.json  | Filtered version of tm-supp.json                                               |
|           | filtered-industry.json | Filtered version of industry.json                                              |
| Directory | cache                  | Contains cached versions of the datasets                                       |

## Adding a dataset
The summary of steps for adding a new dataset is below, with more detailed
instructions in the following sections.

1. Add a rule to download it to the `Makefile`
2. Run a command like `./submit.sh make cache/filtered-your-dataset.json NPROCS=16
   CHUNKSIZE=32` on HPC3
3. Update the table in the README

### 1. Add a rule to the Makefile
The easiest way to do this is to copy an existing rule. For example, the
existing rule to create `industry.json` is:

``` make
industry.json: download.py
	python download.py "OpenFF Industry Benchmark Season 1 v1.1" -o $@ -p
```

This say `industry.json` depends on the `download.py` script (it will be remade
if `download.py` has changed), and the steps to produce `industry.json` from
`download.py` require running the `download.py` script with the dataset's name,
an output path, and the `-p/--pretty-print` flag for `download.py`. `$@` is a
built-in Make variable set to the "target" or the thing on the left of the colon
in the rule definition. After copying this definition and replacing
`industry.json` with the desired output filename and `"OpenFF Industry Benchmark
Season 1 v1.1"` with the name of your dataset, you should be ready for step 2.

### 2. Run submit.sh
`submit.sh` is a shell script that generates a Slurm script to run on HPC3. As
you can see if you provide the `-h` flag, it takes several options, summarized
in the table below:

| Flag | Description                                      | Default |
|------|--------------------------------------------------|---------|
| -h   | Print usage information and exit                 | False   |
| -d   | Dry run, print Slurm input instead of submitting | False   |
| -t   | Set the requested number of CPU hours            | 72      |
| -m   | Set the requested amount of RAM, in GB           | 32      |
| -n   | Set the requested number of CPUs per task        | 8       |

After these optional arguments, `submit.sh` takes any number of commands, which
are passed directly into the generated Slurm script. For the example invocation
above (`./submit.sh make cache/filtered-your-dataset.json NPROCS=16 CHUNKSIZE=32`), the
generated Slurm script will look like:

``` text
#!/bin/bash
#SBATCH -J filter-dataset
#SBATCH -p standard
#SBATCH -t 72:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32gb
#SBATCH --account dmobley_lab
#SBATCH --export ALL
#SBATCH --constraint=fastscratch
#SBATCH --output=logs/2024-08-14.2719087.out

date
hostname
echo $SLURM_JOB_ID

source ~/.bashrc
mamba activate yammbs-dataset-submission

echo $OE_LICENSE

make cache/filtered-your-dataset.json NPROCS=16 CHUNKSIZE=32

date
```

The Makefile defines "pattern rules" for converting any `*.json` file into its
filtered version `filtered-*.json` (using the `*` shell wildcard instead of the
`%` make pattern wildcard). Similarly, it also defines a rule for creating any
`cache/*.json` from `*.json`, so after only defining a rule to make
`your-dataset.json`, you can still ask Make to build
`cache/filtered-your-dataset.json` to generate the original `your-dataset.json`,
as well as the filtered and cached versions.

### 3. Update README
Currently I have been adding both the plain dataset and the filtered version to
the README, but this is a bit redundant, especially since all of the datasets
have the same filters applied so far.

<!-- Refs -->
[qcsubmit]: https://github.com/openforcefield/openff-qcsubmit
[yammbs]: https://github.com/openforcefield/yammbs
[qcarchive]: https://qcarchive.molssi.org/

[^1]: The "caching" here calls `OptimizationResultCollection.to_records`, which
    contacts QCArchive to retrieve the full dataset and extracts only the fields
    needed by [yammbs][yammbs]. `to_records` can be quite expensive (and
    network-dependent), so this saves a lot of time in repeated `yammbs` runs.
