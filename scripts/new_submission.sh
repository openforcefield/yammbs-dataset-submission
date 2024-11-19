#!/bin/bash

sub_name=${1?no submission name given}
sub_dir=submissions/$(date +%F)-${sub_name}

mkdir -p ${sub_dir}

cat > ${sub_dir}/input.yaml <<INP
forcefield: openff_unconstrained-2.1.0.offxml
datasets:
    - datasets/OpenFF-Industry-Benchmark-Season-1-v1.1/cache.json
INP

sed -i "/ENDOFTABLE/i | [$sub_name]($sub_dir) | TODO | [TODO](https://doi.org/TODO) |" README.md
