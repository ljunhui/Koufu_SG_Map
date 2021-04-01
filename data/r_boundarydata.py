# %% Import
import os
import requests
from zipfile import ZipFile
import kml2geojson

""" 
Logic: 
- If final file does not exist, go to data.gov.sg to download the zip file.
- Extract kml from zip file.
- Convert kml to geojson.
- Remove all other files.
"""
# %% Functions


def downloader(source_url, output_fn):
    """ Creates a zip file from the input url. """
    response = requests.get(source_url)
    with open(output_fn, "wb") as f:
        f.write(response.content)
    print("Zip file downloaded from {}".format(source_url))


def kml_converter(zipfn, outputfn):
    """
    Convert kml file downloaded from data.gov.sg to geojson.
    Geojson is provided in the zipped file but geopandas parses it wrongly.
    The converter should provide a more readable geojson file.
    """
    # Extract the correct file
    archive = ZipFile(zipfn, "r")
    target = zipfn.split("/")[-1].split(".")[-2] + "-kml.kml"
    archive.extract(target)

    # Convert it to geojson
    kml2geojson.convert(target, ".")
    print("KML converted to geojson.")
    new_target = target.split(".")[-2] + ".geojson"
    os.rename(new_target, outputfn)
    print("Converted file renamed.")
    os.remove(target)
    print("Old KML file removed.")


def main():

    source_url = (
        "https://data.gov.sg/dataset/c754450d-ecbd-4b7d-8dc1-c07ee842c6d1/download"
    )
    # Source_fn is hardcoded for now because of the extraction logic in kml_converter.
    source_fn = "./master-plan-2019-subzone-boundary-no-sea.zip"
    target_fn = "r_boundarydata.geojson"
    if os.path.isfile(target_fn):
        os.remove(target_fn)

    downloader(source_url, source_fn)
    print("Download func done.")
    kml_converter(source_fn, target_fn)
    print("Convert func done.")
    os.remove(source_fn)
    print("Zip file has been removed.")


# %% Main
if __name__ == "__main__":
    main()
    os.system("pause")
