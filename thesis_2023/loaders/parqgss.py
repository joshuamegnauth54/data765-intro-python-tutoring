#!/usr/bin/env python

"""Load GSS data set and convert to a better, open file format."""

import sys
from pathlib import Path
from typing import Optional

import pandas as pd

argc: int = len(sys.argv)

if argc < 2:
    print(f"USAGE:\n\t{sys.argv[0]} PATH-TO-DUMB-STATA [columns...]")
    sys.exit(0)

# List of columns to use; `None` = all columns
# Columns are the third argument forward
columns: Optional[list[str]] = None
if argc >= 3:
    columns = sys.argv[2:]

# Read in GSS from whatever crappy format it was distributed in
# If it's a CSV, I don't really need to do anything with it
path: Path = Path(sys.argv[1])
gss: Optional[pd.DataFrame | pd.StataReader] = None

match path.suffix:
    case ".dta":
        gss = pd.read_stata(path, columns=columns)
    case ".sas7bdat":
        with pd.read_sas(path, iterator=True) as reader:
            # TextFileReader is an Iterable, so type checking complaints are spurious
            # read_sas doesn't have a columns argument
            gss = pd.concat(map(lambda df: df[columns], reader))
    case ".sav":
        gss = pd.read_spss(path, usecols=columns, dtype_backend="pyarrow")
    case _:
        print(f"{path.suffix} isn't supported")
        sys.exit(0)


assert isinstance(gss, pd.DataFrame)
print(f"Loaded data:\n\t{gss.head()}")

print("Writing parquet to 'gss.parquet'")
gss.write_parquet("gss.parquet")
