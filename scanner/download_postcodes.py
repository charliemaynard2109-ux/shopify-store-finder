import requests
import os


URL = "https://www.getthedata.com/downloads/open_postcode_geo.csv.zip"


print("Downloading postcode database...")


response = requests.get(
    URL,
    timeout=300
)


if response.status_code != 200:
    raise Exception(
        f"Download failed: {response.status_code}"
    )


os.makedirs(
    "../data",
    exist_ok=True
)


with open(
    "../data/postcodes.zip",
    "wb"
) as file:

    file.write(
        response.content
    )


print("Download complete")
