#!/usr/bin/env python

"""Wrangle student data sets from raw GSS."""

import pandas as pd
import sys
from typing import Literal
from loaders.cleaners import recode_ethnic, recode_partyid, recode_degree, recode_degree_binary, recode_small_features

argc: int = len(sys.argv)
if argc < 2:
    print(f"USAGE:\n\t{sys.argv[0]} PATH-TO-GSS-CSV MODE")
    print("MODE: raw OR students")
    sys.exit(-1)

# Path to GSS and script task
path: str = sys.argv[1]
mode: str = sys.argv[2]

if mode == "raw":
    df: pd.DataFrame = pd.read_csv(path, usecols=["year", "age", "coninc", "degree", "sex", "race", "partyid", "region",
                                                  "othlang", "ethnic", "letin1a", "talkspvs", "vstrat", "vpsu", "wtssnrps", "wtssall"], engine="pyarrow", low_memory=False)

    print("Writing to ./gss_filtered.csv")
    df.to_csv("gss_filtered.csv", index=False)
elif mode == "students":
    df: pd.DataFrame = pd.read_csv(path, engine="pyarrow", low_memory=False)

    print("Recoding variables")
    df["ethnic"] = recode_ethnic(df["ethnic"]).astype("category")
    df["partyid"] = recode_partyid(df["partyid"]).astype("category")
    df["degree"] = recode_degree(df["degree"]).astype("category")
    df = recode_small_features(df)

    print("Writing wrangled data set.")
    df.to_csv("gss_wrangled.csv", index=False)

    print("Creating student specific data sets")
    gss_saf = df.copy(True)
    gss_theo, df = df, None

else:
    raise ValueError(f"Incorrect mode: {mode}")
