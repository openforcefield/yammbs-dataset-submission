from dataclasses import dataclass

import yaml


@dataclass
class Config:
    forcefields: list[str]
    datasets: list[str]

    @classmethod
    def from_file(cls, filename):
        with open(filename) as inp:
            d = yaml.load(inp, Loader=yaml.Loader)
            return cls(**d)
