#!/bin/bash

# Usage:
# ./submit.sh [-h] [-d] [-t CPU_HOURS] [-m GB_MEMORY] [-n NCPUS] [-c CHUNKSIZE] DS_NAME
#
# The required argument DS_NAME should be the name of an optimization dataset on
# QCArchive. The other optional flags control job submission and are described
# below.
#
# -h Print a brief usage message and exit
# -d Print the generated sbatch command and exit instead of invoking sbatch
# -t The number of CPU hours to request via the SBATCH -t flag, defaults to 288
# -m The amount of RAM to request via the SBATCH --mem flag, suffixed with "gb",
#    defaults to 96
# -n The number of CPUs to request via the SBATCH --cpus-per-task flag, defaults
#    to 16
# -c The chunk size to pass to download_and_filter_dataset.py, defaults to 32
#
# Slurm output is saved to logs/$date.$pid.out

usage="Usage: $0 [-h] [-d] [-t CPU_HOURS] [-m GB_MEMORY] [-n NCPUS] [-c CHUNKSIZE] "

case $# in
	0) echo 'error: no arguments provided'
	   echo $usage
	   exit 1;;
esac

# default options
hours=120
mem=96
cmd=sbatch
ncpus=16
chunksize=32

while getopts "hdt:m:n:c:" arg
do
	case $arg in
		h) echo $usage
		   exit 0;;
		d) cmd=cat;;
		t) hours=$OPTARG;;
		m) mem=$OPTARG;;
		n) ncpus=$OPTARG;;
		c) chunksize=$OPTARG;;
	esac
done

shift $((OPTIND-1)) # shift off flags to process positionals

#ds_name=${1?No dataset name provided}i

day=$(date +%Y-%m-%d)
pid=$$

logfile=logs/$day.$pid.out

echo requesting $hours CPU hours, $mem GB RAM, and $ncpus CPUs for cmd:
echo $*
echo saving slurm output to
echo $logfile

$cmd <<INP
#!/bin/bash
#SBATCH -J filter-dataset
#SBATCH -p amilan
#SBATCH --qos=long
#SBATCH -t ${hours}:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=${ncpus}
#SBATCH --mem=${mem}gb
#SBATCH --account ucb500_asc1
#SBATCH --export ALL
#SBATCH --output=${logfile}

date
hostname
echo \$SLURM_JOB_ID

source ~/.bashrc
ml mambaforge
mamba activate yammbs-dataset-submission

echo "=== CONDA ENV ==="
mamba list
echo

echo \$OE_LICENSE

python download_and_filter_dataset.py "OpenFF Lipid Optimization Training Supplement v1.0" --nprocs ${ncpus} --chunksize ${chunksize} 

date
INP
