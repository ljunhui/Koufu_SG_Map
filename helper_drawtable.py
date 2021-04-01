# %% Import libraries
import pandas as pd
import numpy as np
import geopandas as gpd

# %% Functions
def createOutletPivot(filename):
    df = pd.read_csv(filename)
    # Group by all the brands according to their planning areas.
    groupdf = df.groupby(
        by=["pln_area_n", "brand"], as_index=False, dropna=False
    ).count()
    # Pivot it around for readability
    pivotdf = (
        groupdf.pivot(index="pln_area_n", columns="brand", values="postalcode")
        .reset_index()
        .fillna(0)
    )
    return pivotdf


def createPlanningArea(filename):
    gdf = gpd.read_file(filename)
    pagdf = gdf.dissolve(by="pln_area_n", aggfunc="sum")
    pagdf["pop_density/km2"] = (round(pagdf["pop"] / pagdf["area_km2"], 0)).astype(int)
    pagdf = pagdf.reset_index().drop(columns="geometry")
    pagdf = pd.DataFrame(pagdf)
    return pagdf


def mergeDF(pivotdf, pagdf):
    mdf = pd.merge(pagdf, pivotdf, how="outer", on="pln_area_n").fillna(0)
    mdf.iloc[:, 4:] = mdf.iloc[:, 4:].astype(int)
    mdf["area_km2"] = mdf["area_km2"].apply(lambda x: round(x, 2))
    return mdf


def main():
    pivotdf = createOutletPivot("./data/r2b_outletgeocode.csv")
    padf = createPlanningArea("./data/r2_cleanboundary.geojson")
    mdf = mergeDF(pivotdf, padf)
    mdf.rename(
        columns={
            "pln_area_n": "Planning Area",
            "area_km2": "Area (km2)",
            "pop": "Population",
            "pop_density/km2": "Population Density (/km2)",
        },
        inplace=True,
    )
    mdf = mdf.sort_values(by=["Population Density (/km2)"], ascending=False)
    return mdf


# %% Main execute
if __name__ == "__main__":
    main()

# %%