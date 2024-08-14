import logging
from collections import defaultdict
from multiprocessing import Pool

import click
from openff.qcsubmit.results import OptimizationResultCollection
from openff.qcsubmit.results.filters import (
    ConnectivityFilter,
    RecordStatusEnum,
    RecordStatusFilter,
    SinglepointRecordFilter,
    T,
)
from openff.qcsubmit.utils import _CachedPortalClient, portal_client_manager
from openff.toolkit.utils.exceptions import (
    ChargeCalculationError,
    ConformerGenerationError,
)
from openff.toolkit.utils.toolkits import OpenEyeToolkitWrapper
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def imap_fn(record_and_molecule):
    """record here is actually only a record.id because the records maintain a
    reference to a PortalClient, which cannot be pickled for multiprocessing.
    """
    record, molecule = record_and_molecule
    try:
        OpenEyeToolkitWrapper().assign_partial_charges(
            molecule, partial_charge_method="am1bccelf10"
        )
    except (ChargeCalculationError, ConformerGenerationError):
        ok = False
    else:
        ok = True

    return record, ok


class ChargeCheckFilter(SinglepointRecordFilter):
    nprocs: int = 1
    chunksize: int = 1

    # this is not needed now that I overrode _apply, and I need to pass along
    # the record_id anyway, but pydantic requires it to be here
    def _filter_function(self, result, record, molecule) -> bool:
        raise NotImplementedError()

    def _apply(self, result_collection: T) -> T:
        """Copy of SinglepointRecordFilter._apply with added logging, progress
        reporting, and eventually parallelism."""

        all_records_and_molecules = defaultdict(list)

        logger.info("starting to_records")

        for record, molecule in result_collection.to_records():
            all_records_and_molecules[record._client.address].append(
                (record.id, molecule)
            )

        logger.info("finished to records")

        filtered_results = {}

        for address, entries in result_collection.entries.items():
            records_and_molecules = all_records_and_molecules[address]

            filtered_ids = []
            with Pool(processes=self.nprocs) as p:
                for record_id, ok in tqdm(
                    p.imap(
                        imap_fn,
                        records_and_molecules,
                        chunksize=self.chunksize,
                    ),
                    total=len(records_and_molecules),
                    desc="Filtering charge errors",
                ):
                    if ok:
                        filtered_ids.append(record_id)

            filtered_results[address] = [
                entry for entry in entries if entry.record_id in filtered_ids
            ]

        result_collection.entries = filtered_results

        return result_collection


class NoisyFilter(SinglepointRecordFilter):
    """A filter that always returns true but can be used for signaling progress
    through a sequence of real filters."""

    name: str

    def _apply(self, result_collection):
        n = result_collection.n_results
        print(f"starting filter: {self.name} on {n} records")
        return super()._apply(result_collection)

    def _filter_function(self, result, record, molecule) -> bool:
        return True


def _main(
    input_file, output_file, pretty_print, cache_dir, nprocs=1, chunksize=1
):
    ds = OptimizationResultCollection.parse_file(input_file)
    client = _CachedPortalClient(
        "https://api.qcarchive.molssi.org:443/", cache_dir=cache_dir
    )
    with portal_client_manager(lambda _: client):
        ds = ds.filter(
            NoisyFilter(name="RecordStatus"),
            RecordStatusFilter(status=RecordStatusEnum.complete),
            NoisyFilter(name="Connectivity"),
            ConnectivityFilter(tolerance=1.2),
            NoisyFilter(name="ChargeCheck"),
            ChargeCheckFilter(nprocs=nprocs, chunksize=chunksize),
            NoisyFilter(name="End"),
        )
    with open(output_file, "w") as out:
        if pretty_print:
            out.write(ds.json(indent=2))
        else:
            out.write(ds.json())

    return ds


@click.command()
@click.option("--input-file", "-i")
@click.option("--output-file", "-o")
@click.option("--pretty-print", "-p", is_flag=True)
@click.option("--cache-dir", "-c")
@click.option("--nprocs", "-n", default=1)
@click.option("--chunksize", "-z", default=1)
def main(input_file, output_file, pretty_print, cache_dir, nprocs, chunksize):
    _main(input_file, output_file, pretty_print, cache_dir, nprocs, chunksize)


if __name__ == "__main__":
    main()
