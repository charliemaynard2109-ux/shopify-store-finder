import requests
import json
import os
import time

from detector import detect_platform


POSTCODE_AREA = "CM"


def get_businesses(area):

    print("Scanning:", area)


    query = f"""

[out:json][timeout:120];

area["name"="{area}"]->.search;

(
node["shop"](area.search);
way["shop"](area.search);

node["craft"](area.search);
way["craft"](area.search);

);

out center;

"""


    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query,
        timeout=150
    )


    data=response.json()


    businesses=[]


    for item in data.get("elements", []):


        tags=item.get("tags", {})


        name=tags.get("name")


        if not name:
            continue


        website = (
            tags.get("website")
            or
            tags.get("contact:website")
            or
            ""
        )


        platform="Not Checked"


        if website:

            platform=detect_platform(
                website
            )


        businesses.append({

            "business": name,

            "postcode_area": area,

            "website": website,

            "platform": platform

        })


        print(
            name,
            platform
        )


    return businesses





def save_results(results):


    with open(
        "../database.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )





if __name__=="__main__":


    results=get_businesses(
        POSTCODE_AREA
    )


    save_results(results)


    print(
        "Saved:",
        len(results)
    )
