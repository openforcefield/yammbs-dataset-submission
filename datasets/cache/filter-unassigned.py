from functools import cache

import qcportal  # noqa
from openff.interchange.exceptions import UnassignedValenceError
from openff.toolkit import ForceField, Molecule
from tqdm import tqdm
from yammbs.cached_result import CachedResultCollection

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


crc = CachedResultCollection.from_json("filtered-industry.json")
print("init: ", len(crc.inner))

crc.inner = [res for res in tqdm(crc.inner) if all_assigned(res.mapped_smiles)]

print("final: ", len(crc.inner))

with open("filtered-industry.json", "w") as out:
    out.write(crc.to_json(indent=2))
