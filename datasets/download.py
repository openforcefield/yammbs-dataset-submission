import click
from openff.qcsubmit.results import OptimizationResultCollection
from qcportal import PortalClient


@click.command()
@click.argument("dsname")
@click.option("--output-file", "-o", default=None)
@click.option("--pretty-print", "-p", is_flag=True)
def main(dsname, output_file, pretty_print):
    client = PortalClient("https://api.qcarchive.molssi.org:443/")
    ds = OptimizationResultCollection.from_server(client, dsname)
    with open(output_file, "w") as out:
        if pretty_print:
            out.write(ds.json(indent=2))
        else:
            out.write(ds.json())


if __name__ == "__main__":
    main()
