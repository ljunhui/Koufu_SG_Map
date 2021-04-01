# %% Import
import geopandas as gpd
import pandas as pd
import numpy as np
import os

""" 
Takes the converted geojson file and returns columns of interest
- Subzone
- Planning area
- Region
- Geometry data (important for choropleths)
"""
# %% Functions


def getArea(file):
    gdf = gpd.read_file(file)
    cols = [
        # "id",
        # "name",
        # "description",
        # "SUBZONE_NO",
        "SUBZONE_N",
        # "SUBZONE_C",
        # "CA_IND",
        "PLN_AREA_N",
        # "PLN_AREA_C",
        "REGION_N",
        # "REGION_C",
        # "INC_CRC",
        # "FMEL_UPD_D",
        "geometry",
    ]
    # epsg 6933 for an equal area estimation
    gdf = gdf.to_crs(epsg=6933)
    gdf = gdf[cols]
    gdf["area_km2"] = gdf.area / 10 ** 6
    return gdf


def getPopulation(file):
    df = pd.read_csv(file)
    df["SZ"] = df["SZ"].str.upper()
    df = df[["SZ", "Pop"]].groupby("SZ", as_index=False).sum()
    return df


def mergeAndWrite(df1, df2, outputfn):
    # Merge both dfs together and some minor cleaning
    mdf = pd.merge(
        df1, df2, how="inner", left_on="SUBZONE_N", right_on="SZ", validate="1:1"
    )
    mdf.columns = mdf.columns.str.lower()
    mdf.drop(columns=["sz"], inplace=True)
    # Decision to cast density as int because float doesn't add value to the conversation
    mdf["pop_density/km2"] = round(mdf["pop"] / mdf["area_km2"], 0).astype(int)
    # exports this to a processed geojson file
    if os.path.isfile(outputfn):
        os.remove(outputfn)
        print(f"Removed the original {outputfn} in the folder.")
    mdf.to_file(outputfn, driver="GeoJSON")
    print(f"A new {outputfn} has been created.")


def main():
    gdf = getArea("./r_boundarydata.geojson")
    popdf = getPopulation("./r_demographicsdata.csv")
    outputfn = "./r2_cleanboundary.geojson"
    mergeAndWrite(gdf, popdf, outputfn)


# %% Main
if __name__ == "__main__":
    main()
    os.system("pause")
