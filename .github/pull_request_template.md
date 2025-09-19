## Submission Checklist
- [ ] Created a new directory in the `submissions` directory containing the YDS input file and optionally a force field `.offxml` file
- [ ] Triggered the benchmark workflow with a PR comment of the form `/run-optimization-benchmarks path/to/submission/input.yaml` or `/run-torsion-benchmarks path/to/submission/input.yaml`
- [ ] Waited for the workflow to finish and a comment with `Job status: success` to be posted
- [ ] Reviewed the results committed by the workflow
- [ ] Published the corresponding Zenodo entry and retrieved the DOI
- [ ] Added the Zenodo DOI to the table in the main README
- [ ] Ready to merge!
