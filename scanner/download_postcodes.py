import requests
import zipfile
import io
import os


url = "https://parlvid.mysociety.org/os/pc/pc-complete.csv"


print("Downloading postcode data...")


r = requests.get(
    url,
    timeout=120
)


if r.status_code != 200:
    raise Exception("Postcode download failed")


os.makedirs(
    "../data",
    exist_ok=True
)


with open(
    "../data/postcodes.csv",
    "wb"
) as f:

    f.write(
        r.content
    )


print(
    "Postcode database downloaded"
)
