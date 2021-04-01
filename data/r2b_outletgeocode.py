# %% Import libraries
import geopandas as gpd
import pandas as pd
import os

""" 
Last step in processing the outlet data. 
- Using geospatial manipulation, identify the zones within which the outlets belong to.
"""

# %% Functions


def appendZoneInfo(df, geodf):
    # Create a geometry point from the lat-lng coords.
    # To note, pointsfromxy takes long and lat instead,
    # and we must use a starting CRS projects long lat.
    df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat, crs=4326))
    # At this point we must convert CRS to 6933 because geojson is in that format
    df = df.to_crs(epsg=6933)

    mDF = gpd.sjoin(df, geodf, how="left", op="within")
    cols = [
        "brand",
        "postalcode",
        "address",
        # "retaddr",
        "lat",
        "lng",
        "subzone_n",
        "pln_area_n",
        "region_n",
    ]

    return mDF[cols]


def main():
    outletsDF = pd.read_csv("./r2_outletgeocode.csv")
    geoDF = gpd.read_file("./r2_cleanboundary.geojson")

    df = appendZoneInfo(outletsDF, geoDF)

    filename = "./r2b_outletgeocode.csv"
    if os.path.isfile(filename):
        os.remove(filename)
    df.to_csv(filename, index=False)


# %% Main execute
if __name__ == "__main__":
    main()
    os.system("pause")
