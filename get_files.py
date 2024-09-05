# read the config file supplied as the first argument and write the associated
# files to stdout

import sys

from config import Config

conf = Config.from_file(sys.argv[1])
print(conf.forcefield)
for ds in conf.datasets:
    print(ds)
