from functools import cache

import qcportal  # noqa
from openff.interchange.exceptions import UnassignedValenceError
from openff.toolkit import ForceField, Molecule
from tqdm import tqdm
from yammbs.inputs import QCArchiveDataset

FF = ForceField("openff-2.1.0.offxml")


@cache
def all_assigned(smiles):
    mol = Molecule.from_mapped_smiles(smiles, allow_undefined_stereo=True)
    mol.assign_partial_charges("gasteiger")
    try:
        FF.create_interchange(mol.to_topology(), charge_from_molecules=[mol])
    except UnassignedValenceError:
        return False

    return True


with open("filtered-industry.json") as inp:
    crc = QCArchiveDataset.model_validate_json(inp.read())

print("init: ", len(crc.qm_molecules))

crc = QCArchiveDataset(
    qm_molecules=[
        res
        for res in tqdm(crc.qm_molecules)
        if all_assigned(res.mapped_smiles)
    ]
)

print("final: ", len(crc.qm_molecules))

with open("filtered-industry.json", "w") as out:
    out.write(crc.model_dump_json())
