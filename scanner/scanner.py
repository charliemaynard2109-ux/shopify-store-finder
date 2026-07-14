import requests
import json
import time

from detector import detect_platform


POSTCODE_AREA = "CM"


def get_businesses(area):

    print("Scanning:", area)


    query = f"""
[out:json][timeout:60];

(
  node["shop"](50.0,-6.0,58.7,2.0);
  way["shop"](50.0,-6.0,58.7,2.0);
);

out center;
"""


    try:

        response = requests.post(
            "https://overpass.kumi.systems/api/interpreter",
            data=query,
            headers={
                "User-Agent":"ShopifyFinder/1.0"
            },
            timeout=120
        )


        print(
            "Overpass status:",
            response.status_code
        )


        if response.status_code != 200:

            print(
                response.text[:500]
            )

            return []



        data=response.json()



    except Exception as e:

        print(
            "Overpass error:",
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

            "business":name,

            "postcode_area":area,

            "website":website,

            "platform":platform

        })


        print(
            name,
            platform
        )


        time.sleep(0.2)



    return businesses





def save_results(results):


    with open(
        "../database.json",
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )





if __name__=="__main__":


    results=get_businesses(
        POSTCODE_AREA
    )


    save_results(
        results
    )


    print(
        "Saved",
        len(results),
        "businesses"
    )
