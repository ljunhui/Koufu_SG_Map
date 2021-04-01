# %% Import
import pandas as pd
import numpy as np
import geopandas as gpd
import folium

# %% Functions
def cleanedGeoDF(filename, target_col):
    gdf = gpd.read_file(filename)
    nan_limit = 2500

    # Hacky method of exploding the geometry collection in the gdf and dissolving it again
    # to create MultiPolygons because GeoJSON tooltips doesn't play nice.
    # See JURONG ISLAND AND BUKOM
    gdf = gdf.explode()
    gdf = gdf.dissolve(by="subzone_n", as_index=False)
    s = gdf[target_col]
    s.mask(s < nan_limit, np.nan, inplace=True)
    gdf["area_km2"] = gdf["area_km2"].round(2)
    return gdf


def createBaseMap():
    startpoint = (1.3521, 103.8198)
    sg_map = folium.Map(
        location=startpoint,
        zoom_start=12,
        control_scale=True,
        # prefer_canvas=True,
        min_zoom=12,
    )

    return sg_map


def createChoropleth(gdf, map_obj, target_col, fill_color, bins):

    # Add a choropleth layer
    choropleth_layer = folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=["subzone_n", target_col],
        key_on="feature.properties.subzone_n",
        fill_color=fill_color,
        line_weight=0.3,
        name="Choropleth Layer",
        fill_opacity=0.6,
        nan_fill_color="black",
        nan_fill_opacity=0.15,
        bins=bins,
        overlay=True,
        control=False,
        legend_name=f"Subzones of Planning Areas grouped by their {target_col}",
        reset=True,
    ).add_to(map_obj)

    # Add tooltips to each subzone
    style_function = lambda x: {
        "fillColor": "white",
        "fillOpacity": 0,
        "weight": 0,
    }

    highlight_function = lambda x: {
        "fillColor": "black",
        "fillOpacity": 0.2,
    }

    folium.GeoJson(
        gdf,
        tooltip=folium.GeoJsonTooltip(
            fields=[
                "pln_area_n",
                "subzone_n",
                "area_km2",
                "pop",
                "pop_density/km2",
            ],
            aliases=[
                "Planning Area",
                "Subzone Name",
                "Area (km2)",
                "Population",
                "Population Density (/km2)",
            ],
            localize=True,
            style="background-color: rgba(255,255,255,0.75);",
        ),
        style_function=style_function,
        highlight_function=highlight_function,
    ).add_to(choropleth_layer)
    return map_obj


def loopcreatePoints(map_obj, outletdf_path):
    outletdf = pd.read_csv(outletdf_path)

    def _createPoints(brand, color, df, map_obj, show):
        """
        Taking the arg brand, create a new df of only that brand.
        - Create a new layer
        - Add all the coordinates of the outlets belonging to that brand and plot points
        - Push it to the specified map object.
        """
        new_df = df[df["brand"] == brand]

        brand_layer = folium.FeatureGroup(
            name=f"{brand} Layer", overlay=True, control=True, show=show
        )
        for brand, address, lat, lng in zip(
            new_df["brand"], new_df["address"], new_df["lat"], new_df["lng"]
        ):
            folium.CircleMarker(
                location=(lat, lng),
                radius=10,
                tooltip=f"<b>Brand:</b> {brand} <br><b>Address:</b> {address}",
                color=color,
                weight=1,
                fill=color,
                fill_opacity=1,
            ).add_to(brand_layer)

            folium.Marker(
                location=(lat + 0.00001, lng + 0.00001),
                tooltip=f"<b>Brand:</b> {brand} <br><b>Address:</b> {address}",
                icon=folium.DivIcon(
                    html=f"""<div style="font-weight: 700;color: white">{brand[0]}</div>"""
                ),
            ).add_to(brand_layer)

        brand_layer.add_to(map_obj)

    brands = {
        "Koufu": "red",
        "Cookhouse": "darkred",
        "Rasapura": "beige",
        "ForkSpoon": "green",
        "HappyHawkers": "orange",
        "Gourmet": "lightred",
        "R&B": "lightgreen",
        "1983NY": "lightgray",
        "Supertea": "darkgreen",
        "1983CT": "gray",
        "Elemen": "darkpurple",
        "Grove": "purple",
    }
    for brand, color in brands.items():
        if brand in [
            "Koufu",
            "Cookhouse",
            "Rasapura",
            "ForkSpoon",
            "HappyHawkers",
            "Gourmet",
        ]:
            _createPoints(
                brand=brand, color=color, df=outletdf, map_obj=map_obj, show=True
            )
        else:
            _createPoints(
                brand=brand, color=color, df=outletdf, map_obj=map_obj, show=False
            )
    return map_obj


def displayAndSave(map_obj, save_map):
    folium.LayerControl().add_to(map_obj)
    if save_map == True:
        map_obj.save("map.html")
    display(map_obj)


def main():
    # I can change this value to make changes to what kind of choropleth to be presented
    target_col = "pop_density/km2"

    # Creates the geodataframe
    gdf = cleanedGeoDF("./data/r2_cleanboundary.geojson", target_col)
    # Create the base map object
    sg_map = createBaseMap()
    # Add choropleth layer
    sg_map = createChoropleth(gdf, sg_map, target_col, "Reds", bins=5)
    # Add the outlet points
    sg_map = loopcreatePoints(sg_map, "./data/r2b_outletgeocode.csv")

    # This should be the last function
    displayAndSave(sg_map, save_map=True)


# %% Main Execute
if __name__ == "__main__":
    main()
# %%
