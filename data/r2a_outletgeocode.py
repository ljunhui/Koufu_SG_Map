# %% Import libraries
import os
import pandas as pd
import re
from geopy import GoogleV3
from credentials import google_api_key
from r2_outletgeocode import getGeoCodeGoogle

""" 
Check returned geocode data against original postal code. Makes a lot of noise if something
went wrong.
"""

# %% Functions


def check(filename):
    """
    Returns a df with latlng columns and a list of problematic indexes
    - Use regex to extract the postal code from the address
    - Validate extracted postal code with the original postal code
    - If errors are found, print out the offending rows and stops the script.
    - Returns a df if no errors are found.
    """
    df = pd.read_csv(filename)

    def _checkMatch(ori, ret):
        patt = r"Singapore \d{6}"
        mo = re.search(patt, ret)
        if not mo:
            return "manualcheck"
        elif mo.group() == ori:
            return 1
        else:
            return 0

    df["check"] = df.apply(lambda x: _checkMatch(x["postalcode"], x["retaddr"]), axis=1)
    # This tells the script what to search for
    err_df = df[df["check"] != 1]
    err_index_list = err_df.index.to_list()

    # Probably a better way to do testing but this works fine in my current use case.
    if len(err_index_list) != 0:
        print("Showing rows that need to be checked\n")
        for index, i in enumerate(err_index_list):
            print(
                f"Item {index} ||| Dataframe Index: {i}: \
                \n--------------------------------"
            )
            print(df.iloc[i].values)
        print(
            "Exiting programme now, please fix the issues shown here before continuing."
        )
        os.system("pause")
        raise SystemExit()
    df.drop(columns=["check"], inplace=True)
    return df


def main():
    filename = "./r2_outletgeocode.csv"
    check(filename)
    print("Postal codes were checked and no issues found, please proceed to next step.")
    os.system("pause")


# %% Main
if __name__ == "__main__":
    main()