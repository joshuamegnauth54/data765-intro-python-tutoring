#!/usr/bin/env python

"""Wrangle student data sets from raw GSS."""

import sys

import pandas as pd

from loaders.cleaners import (
    recode_age,
    recode_degree,
    recode_degree_binary,
    recode_ethnic,
    recode_letin_binary,
    recode_partyid,
    recode_small_features,
)

argc: int = len(sys.argv)
if argc < 2:
    print(f"USAGE:\n\t{sys.argv[0]} PATH-TO-GSS-CSV MODE")
    print("MODE: raw OR students")
    sys.exit()

# Path to GSS and script task
path: str = sys.argv[1]
mode: str = sys.argv[2]

safiya_vars: list[str] = [
    "year",
    "age",
    "degree",
    "sex",
    "race",
    "partyid",
    "othlang",
    "letin1a",
    "coninc",
    "vstrat",
    "vpsu",
    "wtssnrps",
]
safiya_vars_add: list[str] = ["decrease_imm", "hs_or_college"]
theo_vars: list[str] = [
    "year",
    "age",
    "degree",
    "sex",
    "race",
    "region",
    "ethnic",
    "coninc",
    "talkspvs",
    "vstrat",
    "vpsu",
    "wtssall",
]
theo_vars_add: list[str] = ["coninc_quantiles", "hs_or_college", "age_cat"]

if mode == "raw":
    gss: pd.DataFrame = pd.read_csv(
        path,
        usecols=[set(*safiya_vars, *theo_vars)],
        engine="pyarrow",
    )

    print("Writing to ./gss_filtered.csv")
    gss.to_csv("gss_filtered.csv", index=False)
elif mode == "students":
    gss: pd.DataFrame = pd.read_csv(
        path,
        engine="pyarrow",
        dtype={
            "ethnic": "Int64",
            "partyid": "Int64",
            "degree": "Int64",
            "sex": "Int64",
            "othlang": "Int64",
            "race": "Int64",
            "region": "Int64",
            "talkspvs": "Int64",
            "letin1a": "Int64",
        },
    )

    print("Recoding variables")
    gss["ethnic"] = gss["ethnic"].map(recode_ethnic).astype("category")
    gss["partyid"] = gss["partyid"].map(recode_partyid).astype("category")
    gss["hs_or_college"] = gss["degree"].map(recode_degree_binary).astype("category")
    gss["degree"] = gss["degree"].map(recode_degree).astype("category")
    gss = recode_small_features(gss)
    gss["decrease_imm"] = gss["letin1a"].map(recode_letin_binary).astype("category")
    gss["age_cat"] = gss["age"].map(recode_age).astype("category")

    print("Writing wrangled data set.")
    gss.to_csv("gss_wrangled.csv", index=False)

    print("Creating student specific data sets")
    gss_saf: pd.DataFrame = gss[safiya_vars + safiya_vars_add]
    gss_theo: pd.DataFrame = gss[theo_vars + theo_vars_add]

    print("Writing student data sets to CSV")
    gss_saf.to_csv("safiya_clean.csv", index=False)
    gss_theo.to_csv("theo_clean.csv", index=False)

else:
    raise ValueError(f"Incorrect mode: {mode}")
