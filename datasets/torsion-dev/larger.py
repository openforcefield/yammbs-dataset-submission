from openff.qcsubmit.results import TorsionDriveResultCollection
from yammbs.torsion.inputs import QCArchiveTorsionDataset

dspath = "/home/brent/omsf/projects/valence-fitting/02_curate-data/datasets/combined-td.json"
td = TorsionDriveResultCollection.parse_file(dspath)

ytd = QCArchiveTorsionDataset.from_qcsubmit_collection(td)

with open("larger.json", "w") as out:
    out.write(ytd.model_dump_json())
