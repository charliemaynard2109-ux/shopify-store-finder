import csv
import json
import requests
import time

from detector import detect_platform


TARGET_DISTRICT = "CM1"


def load_postcodes():


    matches=[]


    with open(
        "../data/postcodes.csv",
        encoding="utf8"
    ) as f:


        reader=csv.DictReader(f)


        for row in reader:


            postcode=row.get(
                "postcode"
            )


            if not postcode:
                continue



            if postcode.startswith(
                TARGET_DISTRICT
            ):

                matches.append(row)



    print(
        "Postcodes found:",
        len(matches)
    )


    return matches





def find_businesses(postcodes):


    businesses=[]


    checked=set()



    for p in postcodes:


        lat=p.get(
            "latitude"
        )

        lon=p.get(
            "longitude"
        )


        if not lat or not lon:
            continue



        query=f"""

[out:json][timeout:30];

(
node["shop"](around:500,{lat},{lon});
way["shop"](around:500,{lat},{lon});

);

out center;

"""


        try:


            r=requests.post(

                "https://overpass-api.de/api/interpreter",

                data=query,

                timeout=60

            )


            data=r.json()


        except Exception:


            continue



        for item in data.get(
            "elements",
            []
        ):


            tags=item.get(
                "tags",
                {}
            )


            name=tags.get(
                "name"
            )


            if not name:
                continue



            key=name.lower()



            if key in checked:
                continue



            checked.add(
                key
            )



            website=(
                tags.get("website")
                or
                ""
            )



            platform="Not Checked"



            if website:

                platform=detect_platform(
                    website
                )



            businesses.append({

                "business":name,

                "postcode":TARGET_DISTRICT,

                "website":website,

                "platform":platform

            })


            print(
                name,
                platform
            )


        time.sleep(0.5)



    return businesses





def main():


    postcodes=load_postcodes()


    businesses=find_businesses(
        postcodes
    )


    with open(
        "../database.json",
        "w",
        encoding="utf8"
    ) as f:


        json.dump(

            businesses,

            f,

            indent=2

        )



    print(

        "Saved",

        len(businesses),

        "businesses"

    )




if __name__=="__main__":

    main()
