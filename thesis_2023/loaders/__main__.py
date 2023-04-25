#!/usr/bin/env python

"""Wrangle student data sets from raw GSS."""

import sys
from itertools import chain
from typing import Iterable

import pandas as pd

from loaders.cleaners import (
    recode_age,
    recode_degree,
    recode_degree_all,
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

# Features for both data sets
# https://gssdataexplorer.norc.org/gssweighting
weights: list[str] = ["vstrat", "vpsu", "wtsscomp"]
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
] + weights
safiya_vars_add: list[str] = ["coninc_log", "decrease_imm", "hs_or_college"]
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
] + weights
theo_vars_add: list[str] = [
    "age_cat",
    "coninc_log",
    "coninc_quantiles",
    "degree_all",
    "hs_or_college",
]

if mode == "raw":
    print(f"Loading GSS from {path}")
    try:
        gss: pd.DataFrame = pd.read_csv(
            path,
            usecols=set(safiya_vars + theo_vars),
            engine="pyarrow",
        )
    except ValueError:
        print(f"{path} is missing `wtsscomp` - creating the weights instead")

        # Pop wtsscomp
        theo_vars.pop()
        safiya_vars.pop()

        # Append old weights
        theo_vars.append("wtssall")
        safiya_vars.append("wtssps")

        gss = pd.read_csv(path, usecols=set(safiya_vars + theo_vars), engine="pyarrow")
        gss["wtsscomp"] = gss["wtssall"].fillna(gss["wtssps"])

        assert gss["wtsscomp"].isna().sum() == 0
        gss = gss.drop(columns=["wtssall", "wtssps"])

    print("Writing to ./gss_filtered.csv")
    gss.to_csv("gss_filtered.csv", index=False)
elif mode == "students":
    gss: pd.DataFrame = pd.read_csv(
        path,
        engine="pyarrow",
        dtype={
            "year": int,
            "age": "Int64",
            "ethnic": "Int64",
            "partyid": "Int64",
            "degree": "Int64",
            "sex": "Int64",
            "othlang": "Int64",
            "race": "Int64",
            "region": "Int64",
            "talkspvs": "Int64",
            "letin1a": "Int64",
            "coninc": float,
            "vstrat": float,
            "vpsu": float,
            "wtsscomp": float,
        },
    )

    print("Recoding variables")
    gss["ethnic"] = gss["ethnic"].map(recode_ethnic).astype("category")
    gss["partyid"] = gss["partyid"].map(recode_partyid).astype("category")
    gss["hs_or_college"] = gss["degree"].map(recode_degree_binary).astype("category")
    gss["degree_all"] = gss["degree"].map(recode_degree_all).astype("category")
    gss["degree"] = gss["degree"].map(recode_degree).astype("category")
    gss = recode_small_features(gss)
    gss["decrease_imm"] = gss["letin1a"].map(recode_letin_binary).astype("category")
    gss["age_cat"] = gss["age"].map(recode_age).astype("category")

    print("Writing wrangled data set.")
    gss.to_csv("gss_wrangled.csv", index=False)

    # Sort features but place weights at the end
    saf_vars_gen: Iterable = chain(
        (var for var in sorted(safiya_vars + safiya_vars_add) if var not in weights),
        weights,
    )
    theo_vars_gen: Iterable = chain(
        (var for var in sorted(theo_vars + theo_vars_add) if var not in weights),
        weights,
    )

    print("Creating student specific data sets")
    gss_saf: pd.DataFrame = gss[saf_vars_gen].query("year >= 2010")
    valid_ethnic: list[str] = ["Africa", "Mexico"]
    gss_theo: pd.DataFrame = gss[theo_vars_gen].query(
        "(year >= 2008) and (ethnic in @valid_ethnic)"
    )

    print("Writing student data sets to CSV")
    gss_saf.to_csv("safiya_clean.csv", index=False)
    gss_theo.to_csv("theo_clean.csv", index=False)

else:
    raise ValueError(f"Incorrect mode: {mode}")
