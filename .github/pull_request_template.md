## Submission Checklist
- [ ] Created a new directory in the `submissions` directory containing the YDS input file and optionally a force field `.offxml` file
- [ ] Triggered the benchmark workflow with a PR comment of the form `/run-optimization-benchmarks path/to/submission/input.yaml path/to/environment.yaml Title of any length` or the same with `/run-torsion-benchmarks ...`
  - After the command, the first and second space-separated values are the data input file and conda environment file, respectively. The rest of the comment becomes the title of the Zenodo record.
- [ ] Waited for the workflow to finish and a comment with `Job status: success` to be posted
- [ ] Reviewed the results committed by the workflow
- [ ] Published the corresponding Zenodo entry (contact @mattwthompson, @j-wags, or @lilyminium if you do not have the organization's Zenodo login) and retrieved the DOI
- [ ] Added the Zenodo DOI to the table in the main README
- [ ] Ready to merge!
