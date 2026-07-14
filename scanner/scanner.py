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


    try:

        response = requests.get(

            url,

            params=params,

            headers={
                "User-Agent":
                "ShopifyBusinessFinder/1.0"
            },

            timeout=30

        )


        data = response.json()


    except Exception as e:

        print(
            "Boundary lookup error:",
            e
        )

        return None



    if not data:

        print(
            "No boundary found"
        )

        return None



    if "geojson" not in data[0]:

        print(
            "No polygon returned"
        )

        return None



    return data[0]["geojson"]





def search_businesses(boundary):


    print(
        "Searching businesses..."
    )


    polygon = json.dumps(
        boundary
    )



    query = f"""

[out:json][timeout:180];

(
node["shop"](poly:"{polygon}");
way["shop"](poly:"{polygon}");

node["craft"](poly:"{polygon}");
way["craft"](poly:"{polygon}");

);

out center;

"""



    servers = [

        "https://overpass-api.de/api/interpreter",

        "https://overpass.kumi.systems/api/interpreter",

        "https://overpass.nchc.org.tw/api/interpreter"

    ]



    for server in servers:


        try:


            print(
                "Trying:",
                server
            )


            response = requests.post(

                server,

                data=query,

                headers={

                    "User-Agent":
                    "ShopifyBusinessFinder/1.0"

                },

                timeout=240

            )



            print(
                "Status:",
                response.status_code
            )



            if response.status_code != 200:

                continue



            if not response.text.strip():

                continue



            return response.json()



        except Exception as e:


            print(
                "Server failed:",
                e
            )


            continue



    print(
        "All Overpass servers failed"
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



        key=name.lower()



        if key in checked:

            continue



        checked.add(
            key
        )



        website = (

            tags.get("website")

            or

            tags.get("contact:website")

            or

            ""

        )



        platform="Not Checked"



        if website:


            try:

                platform = detect_platform(
                    website
                )


            except Exception:

                platform="Error"



        results.append({

            "business": name,

            "postcode_area": TARGET_DISTRICT,

            "website": website,

            "platform": platform

        })



        print(

            name,

            "|",

            platform

        )



    return results





def save_database(results):


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





def main():


    boundary = get_boundary(
        TARGET_DISTRICT
    )


    if not boundary:

        print(
            "Stopping - no boundary"
        )

        return



    data = search_businesses(
        boundary
    )


    results = process_businesses(
        data
    )


    save_database(
        results
    )


    print(

        "Saved",

        len(results),

        "businesses"

    )





if __name__ == "__main__":

    main()
