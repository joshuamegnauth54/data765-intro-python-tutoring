#!/usr/bin/env python

"""Load GSS data set and convert to a better, open file format."""

import sys
from typing import Optional

import pandas as pd

argc: int = len(sys.argv)

if argc < 2:
    print(f"USAGE:\n\t{sys.argv[0]} PATH-TO-DUMB-STATA [columns...]")
    sys.exit(-1)

# List of columns to use; `None` = all columns
# Columns are the third argument forward
columns: Optional[list[str]] = None
if argc >= 3:
    columns = sys.argv[2:]


gss: pd.DataFrame = pd.read_stata(sys.argv[1], columns=columns)
print(f"Loaded data:\n\t{gss.head()}")

print("Writing parquet to 'gss.parquet'")
gss.write_parquet("gss.parquet")
