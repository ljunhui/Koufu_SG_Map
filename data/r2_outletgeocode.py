# %% Import libraries
import pandas as pd
import re
import os
from ast import literal_eval
from geopy import GoogleV3

# You'll have to use your own credentials!
from credentials import google_api_key

""" 
Takes the raw outlet data and returns a cleaned up df with 4 columns
- brand
- postal code
- address
- geocode data returned from Google Places API
"""

# %% Functions
def clean(file):
    """
    Takes the raw outlet data to process it into 3 cols
    1. brand
    2. postalcode
    3. address

    Please note. There is an additional step here where dropna is used.
    """
    df = pd.read_csv(file)

    def _getPostalCode(row):
        """
        For each row in the df, find the col with postalcode
        """
        patt = r"\d{6}"
        for value in row:
            mo = re.search(patt, str(value))
            if mo:
                # Instead of returning value here, I did this monster
                # because Outlet Yishun 747's postalcode had \xa0 in it.
                # It's a unicode thing, note to self for future learning.
                return str(f"Singapore {mo.group()}")

    # Create tmp series to insert into the df. Purpose is for re-ordering cols.
    tmp = df.iloc[:, 3:].apply(lambda x: _getPostalCode(x), axis=1)
    df.insert(1, "postalcode", tmp)

    # Trim the other columns
    df = df.iloc[:, 0:5]
    # Create an address col combining the 3 columns
    df["address"] = df["0"] + " " + df["1"] + " " + df["2"]
    # Final cleaning of df
    df.drop(columns=["0", "1", "2"], inplace=True)
    df.dropna(subset=["postalcode"], inplace=True)
    return df


def getGeoCodeGoogle(addr, postalcode):
    """
    Takes addr and postal code from df to return [addr, (lat, lng)]
    - Search postalcode first, then addr if it fails.
    - Split the postal code to just numbers since region is already specified.
    """
    geoObj = GoogleV3(api_key=google_api_key)
    postalcode = postalcode.split()[-1]
    result = geoObj.geocode(postalcode, region="sg")
    if result != None:
        print(f"{postalcode} found.")
        return (result[0], result[1])
    else:
        print("Postalcode didn't work, using addr instead.")
        result = geoObj.geocode(addr, region="sg")
        print(f"{addr} found.")
        return (result[0], result[1])


def furtherProcessing(df):
    # Splitting up the results of the GeoCode
    df["retaddr"] = df["geocode"].apply(lambda x: x[0])
    df["lat"] = df["geocode"].apply(lambda x: x[1][0])
    df["lng"] = df["geocode"].apply(lambda x: x[1][1])
    df.drop(columns=["geocode"], inplace=True)
    return df


def saveFile(df, outputfn):
    if os.path.isfile(outputfn):
        os.remove(outputfn)
    df.to_csv(outputfn, index=False)
    print(f"{outputfn} saved.")


def main():
    filename = "r_outletsdata.csv"
    outputfn = "r2_outletgeocode.csv"

    # Apply the geocode function
    df = clean(filename)
    df["geocode"] = df.apply(
        lambda x: getGeoCodeGoogle(x["address"], x["postalcode"]), axis=1
    )
    df = furtherProcessing(df)

    saveFile(df, outputfn)
    os.system("pause")


# %% Main
if __name__ == "__main__":
    main()
