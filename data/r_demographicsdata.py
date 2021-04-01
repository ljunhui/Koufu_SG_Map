# %% Import
import requests
import os
from zipfile import ZipFile
import pandas as pd
import numpy as np

""" 
- Goes to the url, downloads the zip file found there and saves it.
- Extracts targetfn into the folder then deletes zip file.
- Filters based on the year I set. Only allow 1 year for now.
"""

# %% Functions


def download_extract(inputurl, targetfn):
    response = requests.get(inputurl)
    archivefn = "demographics.zip"
    with open(archivefn, "wb") as f:
        f.write(response.content)
    print(
        "Zip file has been downloaded from {} and renamed as {}.".format(
            inputurl, archivefn
        )
    )

    zipped = ZipFile(archivefn)
    zipped.extract(targetfn)
    zipped.close()
    print("{} has been extracted.".format(targetfn))
    os.remove(archivefn)
    print("{} has been deleted.".format(archivefn))


def filterDataSave(targetfn, years, outputfn):
    df = pd.read_csv(targetfn)
    df = df[df["Time"].isin(years)].reset_index(drop=True)
    df.to_csv(outputfn, index=False)
    print("{} is saved with only the years {}".format(outputfn, years))


def main():
    inputurl = "https://www.singstat.gov.sg/-/media/files/find_data/population/statistical_tables/singapore-residents-by-planning-areasubzone-age-group-sex-and-type-of-dwelling-june-20112020.zip"
    targetfn = "respopagesextod2011to2020.csv"
    outputfn = "r_demographicsdata.csv"

    years = [2020]
    # If output file exists, get rid of it.
    if os.path.isfile(outputfn):
        os.remove(outputfn)

    download_extract(inputurl, targetfn)
    filterDataSave(targetfn, years, outputfn)
    # Clean up the intermediate file
    os.remove(targetfn)


# %% Main
if __name__ == "__main__":
    main()
    os.system("pause")
