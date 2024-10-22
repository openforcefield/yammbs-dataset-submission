import argparse
import logging
from collections import defaultdict
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from openff.qcsubmit.results import OptimizationResultCollection
from openff.qcsubmit.results.filters import (
    ConformerRMSDFilter,
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
from qcportal import PortalClient
from tqdm import tqdm
from yammbs.inputs import QCArchiveDataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    ds_name: str
    nprocs: int
    chunksize: int

    @classmethod
    def from_file(cls, filename):
        with open(filename) as inp:
            d = yaml.load(inp, Loader=yaml.Loader)
            return cls(**d)


def download_dataset(client: PortalClient, dsname: str, out_dir: Path):
    """Download the named ``OptimizationResultCollection``, write it to
    ``raw.json`` in ``out_dir`` and return the result collection."""

    ds = OptimizationResultCollection.from_server(client, dsname)
    with open(out_dir / "raw.json", "w") as out:
        out.write(ds.json())

    return ds


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


def filter_dataset(ds, nprocs, chunksize, out_dir):
    ds = ds.filter(
        NoisyFilter(name="RecordStatus"),
        RecordStatusFilter(status=RecordStatusEnum.complete),
        NoisyFilter(name="Connectivity"),
        ConnectivityFilter(tolerance=1.2),
        NoisyFilter(name="ConformerRMSD"),
        ConformerRMSDFilter(),
        NoisyFilter(name="ChargeCheck"),
        ChargeCheckFilter(nprocs=nprocs, chunksize=chunksize),
        NoisyFilter(name="End"),
    )

    with open(out_dir / "filtered.json", "w") as out:
        out.write(ds.json())

    return ds


def main():
    a = argparse.ArgumentParser()
    a.add_argument("input_file")
    args = a.parse_args()

    conf = Config.from_file(args.input_file)
    with TemporaryDirectory() as d:
        client = _CachedPortalClient(
            "https://api.qcarchive.molssi.org:443/", d
        )
        out_dir = Path(conf.ds_name.replace(" ", "-"))
        out_dir.mkdir()

        logger.info(f"Downloading dataset {conf.ds_name} to {out_dir}")
        ds = download_dataset(client, conf.ds_name, out_dir)

        with portal_client_manager(lambda _: client):
            logger.info("Filtering dataset with")
            ds = filter_dataset(ds, conf.nprocs, conf.chunksize)

            logger.info("Converting dataset to yammbs input format")
            ds = QCArchiveDataset.from_qcsubmit_collection(ds)
            with open(out_dir / "cache.json", "w") as out:
                out.write(ds.model_dump_json())


if __name__ == "__main__":
    main()
