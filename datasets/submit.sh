#!/bin/bash

# Usage:
# ./submit.sh COMMAND...
#
# All of the arguments to this script are passed into the body of the sbatch
# invocation below.
#
# Slurm output is saved to logs/$date.$pid.out

usage="Usage: $0 [-h] [-d] [-t CPU_HOURS] [-m GB_MEMORY] [-n NCPUS] CMDS..."

case $# in
	0) echo 'error: no arguments provided'
	   echo $usage
	   exit 1;;
esac

# default options
hours=72
mem=64
cmd=sbatch
ncpus=32

while getopts "hdt:m:n:" arg
do
	case $arg in
		h) echo $usage
		   exit 0;;
		d) cmd=cat;;
		t) hours=$OPTARG;;
		m) mem=$OPTARG;;
		n) ncpus=$OPTARG;;
	esac
done

shift $((OPTIND-1)) # shift off flags to process positionals

infile=${1?No input file provided}

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
#SBATCH -p standard
#SBATCH -t ${hours}:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=${ncpus}
#SBATCH --mem=${mem}gb
#SBATCH --account dmobley_lab
#SBATCH --export ALL
#SBATCH --constraint=fastscratch
#SBATCH --output=${logfile}

date
hostname
echo \$SLURM_JOB_ID

source ~/.bashrc
mamba activate yammbs-dataset-submission

echo "=== CONDA ENV ==="
mamba list
echo

echo \$OE_LICENSE

echo "=== INPUT FILE ==="
cat ${infile}
echo

python new_dataset.py --nprocs ${ncpus} ${infile}

date
INP
