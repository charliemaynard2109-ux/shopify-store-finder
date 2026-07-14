import requests
import json
import os
import time

from detector import detect_platform


# CHANGE THIS EACH RUN
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


    try:

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            timeout=150
        )

        data=response.json()


    except Exception as e:

        print(
            "Overpass failed:",
            e
        )

        return []



    businesses=[]


    for item in data.get("elements", []):


        tags=item.get(
            "tags",
            {}
        )


        name=tags.get(
            "name"
        )


        website=(
            tags.get("website")
            or
            tags.get("contact:website")
        )


        if not name or not website:

            continue



        print(
            "Checking",
            name
        )


        platform=detect_platform(
            website
        )



        businesses.append({

            "business":name,

            "postcode_area":area,

            "website":website,

            "platform":platform

        })


        time.sleep(0.5)



    return businesses





def save_results(new_results):


    file="../database.json"



    if os.path.exists(file):

        with open(file) as f:

            database=json.load(f)


    else:

        database=[]



    existing={
        x["website"]
        for x in database
    }



    for item in new_results:

        if item["website"] not in existing:

            database.append(item)



    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            database,
            f,
            indent=2
        )



    print(
        "Database total:",
        len(database)
    )





if __name__=="__main__":


    results=get_businesses(
        POSTCODE_AREA
    )


    save_results(
        results
    )


    print(
        "Finished"
    )
