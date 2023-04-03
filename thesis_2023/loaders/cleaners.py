import numpy as np
import pandas as pd
from typing import Literal, TypeAlias

Number: TypeAlias = np.number | float | int | pd.Int64Dtype


def recode_ethnic(ethnic: Number) -> str:
    """Recodes GSS's `ethnic` from magic numbers to strings.

    https://gssdataexplorer.norc.org/variables/5263/vshow

    Parameters
    ----------
    ethnic : Number
        Magic number representing ethnicity.

    Returns
    -------
    Literal[...]
        Ethnicity as a string.

    """

    # [1, 42)
    first_set: list[str] = ["Africa", "Austria", "Canada (French)", "Canada (Other)",
                            "China", "Czechoslovakia", "Denmark", "England and Wales", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland",
                            "Italy", "Japan", "Mexico", "Netherlands", "Norway", "Phillipines", "Poland", "Puerto Rico",
                            "Russia", "Scotland", "Spain", "Sweden", "Switzerland", "West Indies (Unspecified)", "Other", "Native American", "India", "Portugal", "Lithuania", "Yugoslavia", "Romania",
                            "Belgium", "Arabic", "Other Spanish", "West Indies (non-Spanish)", "Other Asian", "Other European"]

    match ethnic:
        case _ if pd.isna(ethnic):
            return pd.NA
        case eth if ethnic in range(1, 42):
            return first_set[eth - 1]
        case 97:
            return "American Only"
        case 101:
            return "Turkey"
        case 202:
            return "Algeria"
        case 203:
            return "Congo"
        case 204:
            return "Egypt"
        case 205:
            return "Ethiopia"
        case 206:
            return "Kenya"
        case 207:
            return "Nigeria"
        case 208:
            return "South Africa"
        case 299:
            return "Other Africa"
        case 301:
            return "South Korea"
        case 302:
            return "Bangladesh"
        case 304:
            return "Pakistan"
        case 306:
            return "Thailand"
        case 307:
            return "Vietnam"
        case 401:
            return "Iran"
        case 402:
            return "Iraq"
        case 403:
            return "Israel"
        case 404:
            return "Jordan"
        case 405:
            return "Saudia Arabia"
        case 406:
            return "Syria"
        case 408:
            return "Yemen"
        case 499:
            return "Other Middle East"
        case 501:
            return "Argentina"
        case 503:
            return "Brazil"
        case 504:
            return "Chile"
        case 505:
            return "Colombia"
        case 506:
            return "Ecuador"
        case 508:
            return "Guyana"
        case 509:
            return "Paraguay"
        case 510:
            return "Peru"
        case 511:
            return "Suriname"
        case 513:
            return "Venezuela"
        case 599:
            return "Other South America"
        case 601:
            return "Belize"
        case 602:
            return "Costa Rica"
        case 603:
            return "El Salvador"
        case 604:
            return "Guatemala"
        case 605:
            return "Honduras"
        case 606:
            return "Nicaragua"
        case 607:
            return "Panama"
        case 699:
            return "Other Central American"
        case 799:
            return "Other North America"
        case 801:
            return "Cuba"
        case 802:
            return "Haiti"
        case 803:
            return "Dominican Republic"
        case 804:
            return "Jamaica"
        case 899:
            return "Other Caribbean"
        case 901:
            return "Australia"
        case 903:
            return "New Zealand"
        case 904:
            return "Samoa"
        case 999:
            return "Other Oceania"
        case _:
            return pd.NA


def recode_partyid(party: Number) -> Literal["Democrat", "Republican", "Other", pd.NA]:
    """Recode GSS's `partyid` variable by collapsing the redundant categories.

    https://gssdataexplorer.norc.org/variables/141/vshow

    Parameters
    ----------
    party : Number
        Sentinel value for GSS's `partyid` variable.

    Returns
    -------
    Literal["Democrat", "Republican", "Other", pd.NA]
        String representing the input's collapsed category.
    """
    match party:
        case _ if pd.isna(party):
            return pd.NA
        case 0 | 1 | 2:
            return "Democrat"
        case 4 | 5 | 6:
            return "Republican"
        case 3 | 7:
            return "Other"
        case _:
            return pd.NA


def recode_degree(degree: Number) -> Literal["No degree", "HS or assoc", "College"]:
    """Recode and collapse degree into strings with less categories.

    Parameters
    ----------
    degree : Number

    Return
    ------
    Literal["No degree", "HS or assoc", "College"]
        Recoded values.
    """

    match degree:
        case _ if pd.isna(degree):
            return pd.NA
        case 0:
            return "No degree"
        case 1 | 2:
            return "HS or assoc"
        case 3 | 4:
            return "College"
        case _:
            return pd.NA


def recode_degree_binary(degree: Number) -> Literal["HS or less", "Some college"]:
    """Recode degree into a binary feature.

    Parameters
    ----------
    degree : Number

    Return
    ------
    Literal["HS or less", "Some college"]
        Recoded values.
    """

    match degree:
        case _ if pd.isna(degree):
            return pd.NA
        case 0 | 1:
            return "HS or less"
        case 2 | 3 | 4:
            return "Some college"
        case _:
            return pd.NA


def recode_small_features(gss: pd.DataFrame) -> pd.DataFrame:
    """Recode a few features that don't require a function.

    Remaps: `sex`, `othlang`, `race`, `region`, `talkspvs`, `letin1a`

    Parameters
    ----------
    gss : pd.DataFrame
        GSS loaded as a DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with recoded values.
    """
    sex: dict[str, str] = {1: "Male", 2: "Female"}
    gss["sex"].astype("Int64").map(sex).astype("category")

    # Does R speak a language other than English or Spanish?
    gss["othlang"] = (
        gss["othlang"].astype("Int64").map(
            {1: "Yes", 2: "No"}).astype("category")
    )

    race: dict[int, str] = {1: "White", 2: "Black", 3: "Other"}
    gss["race"] = gss["race"].astype("Int64").map(race).astype("category")

    gss["region"] = (
        gss["region"]
        .astype("Int64")
        .map(
            dict(
                zip(
                    range(1, 10),
                    [
                        "New England",
                        "Middle Atlantic",
                        "East North Central",
                        "West North Central",
                        "South Atlantic",
                        "East South Atlantic",
                        "West South Central",
                        "Mountain",
                        "Pacific",
                    ],
                )
            )
        )
        .astype("category")
    )

    # This variable is only valid for 2014.
    gss["talkspvs"] = gss["talkspvs"].map(
        dict(
            zip(
                range(1, 6),
                ["Not comfortable at all", "A little",
                 "Somewhat", "Very", "Extremely"],
            )
        )
    )
