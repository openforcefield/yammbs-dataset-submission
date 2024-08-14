industry.json: download.py
	python download.py "OpenFF Industry Benchmark Season 1 v1.1" -o $@ -p

tm-supp.json: download.py
	python download.py \
"OpenFF Torsion Multiplicity Optimization Benchmarking Coverage Supplement v1.0" \
--output-file $@ --pretty-print

tm-supp0.json: download.py
	python download.py \
	"OpenFF Torsion Benchmark Supplement v1.0" --output-file $@ --pretty-print

NPROCS := 1
CHUNKSIZE := 1
filtered-%.json: %.json filter.py
	python filter.py -i $< -o $@ -c .cache/$$$$ -n $(NPROCS) -z $(CHUNKSIZE)

cache/%.json: %.json cache_dataset.py
	mkdir -p cache
	python cache_dataset.py -i $< -o $@
