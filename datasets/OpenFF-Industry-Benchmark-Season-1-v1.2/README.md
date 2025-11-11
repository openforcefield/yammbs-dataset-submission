# OpenFF-Industry-Benchmark-Season-1-v1.2

This dataset differs from *OpenFF Industry Benchmark Season 1 v1.1* with the removal of 29 molecule entries (7 unique molecules) that exhibit 7-member rings with an inverted methylene group causing abnormally high energies. The record IDs from *OpenFF Industry Benchmark Season 1 v1.1* that were removed are:

36957824, 36981509, 36997513, 36959242, 36962955, 36983564, 37008265, 37008890, 36997144, 36991898, 36963231, 36984866, 36961063, 37008819, 36991541, 37008823, 36989631, 36997441, 37015502, 37015507, 36959445, 36976597, 37011034, 36993121, 36982891, 36982892, 36971898, 37008891, 36975868

In this submission we prepare the *OpenFF Industry Benchmark Season 1 v1.2* dataset directly for use using the command: `python new_dataset.py industry.yaml -n <Number of CPUs> > log.txt` and may take many hours, it is recommended to run on a HPC.