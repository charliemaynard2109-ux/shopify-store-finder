import requests
import json
import time

from detector import detect_platform


TARGET_DISTRICT = "CM1"



def get_boundary(district):

    print(
        "Finding boundary for:",
        district
    )


    url = "https://nominatim.openstreetmap.org/search"


    params = {

        "q": f"{district}, UK",

        "format": "json",

        "polygon_geojson": 1,

        "limit": 1

    }


    response = requests.get(

        url,

        params=params,

        headers={
            "User-Agent":
            "ShopifyBusinessFinder/1.0"
        },

        timeout=30

    )


    data=response.json()



    if not data:

        print(
            "No boundary found"
        )

        return None



    item=data[0]


    if "geojson" not in item:

        print(
            "No polygon available"
        )

        return None



    return item["geojson"]





def search_businesses(boundary):


    print(
        "Searching businesses..."
    )



    coords=json.dumps(
        boundary
    )



    query=f"""

[out:json][timeout:120];

(
nwr["shop"](poly:"{coords}");
nwr["craft"](poly:"{coords}");
);

out center;

"""



    servers=[

        "https://overpass.kumi.systems/api/interpreter",

        "https://overpass.private.coffee/api/interpreter",

        "https://overpass-api.de/api/interpreter"

    ]



    for server in servers:


        try:


            print(
                "Trying",
                server
            )



            response=requests.post(

                server,

                data=query,

                headers={
                    "User-Agent":
                    "ShopifyBusinessFinder/1.0"
                },

                timeout=120

            )



            if response.status_code != 200:

                continue



            return response.json()



        except Exception as e:


            print(
                "Failed:",
                e
            )



    return None





def process_businesses(data):


    results=[]

    checked=set()



    if not data:

        return results



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



        if name.lower() in checked:

            continue



        checked.add(
            name.lower()
        )



        website=(

            tags.get("website")

            or

            tags.get("contact:website")

            or

            ""

        )


        platform="Not Checked"



        if website:


            try:

                platform=detect_platform(
                    website
                )

            except:

                platform="Error"



        results.append({

            "business":name,

            "postcode_area":TARGET_DISTRICT,

            "website":website,

            "platform":platform

        })



        print(
            name,
            platform
        )



    return results





def main():


    boundary=get_boundary(
        TARGET_DISTRICT
    )


    if not boundary:

        return



    data=search_businesses(
        boundary
    )


    results=process_businesses(
        data
    )



    with open(

        "../database.json",

        "w",

        encoding="utf8"

    ) as file:


        json.dump(

            results,

            file,

            indent=2

        )



    print(

        "Saved",

        len(results),

        "businesses"

    )




if __name__=="__main__":

    main()
