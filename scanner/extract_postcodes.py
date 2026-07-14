import zipfile
import os


zip_path = "../data/postcodes.zip"

output = "../data/postcodes.csv"


print("Extracting postcode file...")


with zipfile.ZipFile(zip_path) as z:

    csv_files = [
        file for file in z.namelist()
        if file.endswith(".csv")
    ]


    if not csv_files:
        raise Exception(
            "No CSV file found in ZIP"
        )


    with z.open(csv_files[0]) as source:

        with open(
            output,
            "wb"
        ) as target:

            target.write(
                source.read()
            )


print("Postcodes extracted")
