import logging

import click
from openff.qcsubmit.results import OptimizationResultCollection
from yammbs.cached_result import CachedResultCollection

logging.getLogger("openff").setLevel(logging.ERROR)


@click.command()
@click.option("--input-file", "-i")
@click.option("--output-file", "-o")
def main(input_file, output_file):
    opt = OptimizationResultCollection.parse_file(input_file)
    crc = CachedResultCollection.from_qcsubmit_collection(opt)
    with open(output_file, "w") as out:
        out.write(crc.to_json(indent=2))


if __name__ == "__main__":
    main()
