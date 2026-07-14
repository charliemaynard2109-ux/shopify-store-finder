import requests
import json
import time

from detector import detect_platform


TARGET_DISTRICT = "CM1"



def get_postcodes(district):

    print(
        "Finding postcodes for:",
        district
    )


    url = (
        "https://api.postcodes.io/postcodes/"
        + district
        + "/autocomplete"
    )


    try:

        response = requests.get(
            url,
            timeout=30
        )

        data = response.json()


    except Exception as e:

        print(
            "Postcode lookup error:",
            e
        )

        return []



    results = []


    for item in data.get("result", []):

        if isinstance(item, dict):

            postcode = item.get(
                "postcode"
            )

        else:

            postcode = item


        if postcode:

            results.append(
                postcode
            )


    print(
        "Postcodes found:",
        len(results)
    )


    return results





def get_coordinates(postcode):


    url = (
        "https://api.postcodes.io/postcodes/"
        + postcode
    )


    try:

        response = requests.get(
            url,
            timeout=20
        )

        data = response.json()


    except Exception:

        return None



    if data.get("status") != 200:

        return None



    result = data.get(
        "result"
    )


    if not result:

        return None



    return (

        result.get("latitude"),

        result.get("longitude")

    )





def query_overpass(lat, lon):


    query = f"""

[out:json][timeout:25];

(
node["shop"](around:300,{lat},{lon});
way["shop"](around:300,{lat},{lon});

node["craft"](around:300,{lat},{lon});
way["craft"](around:300,{lat},{lon});

);

out center;

"""



    servers = [

        "https://overpass.kumi.systems/api/interpreter",

        "https://overpass.private.coffee/api/interpreter",

        "https://overpass-api.de/api/interpreter"

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

                timeout=60

            )



            if response.status_code != 200:

                continue



            if not response.text.strip():

                continue



            return response.json()



        except Exception as e:


            print(
                "Failed:",
                server,
                str(e)
            )


            continue



    return None





def find_businesses(postcodes, district):


    businesses=[]

    checked=set()



    for index, postcode in enumerate(postcodes):


        print(
            "Checking postcode:",
            postcode,
            index + 1,
            "/",
            len(postcodes)
        )



        coords=get_coordinates(
            postcode
        )


        if not coords:

            continue



        lat, lon = coords



        data=query_overpass(
            lat,
            lon
        )



        if not data:

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

                    platform=detect_platform(
                        website
                    )

                except Exception:

                    platform="Error"



            businesses.append({

                "business": name,

                "postcode_area": district,

                "website": website,

                "platform": platform

            })



            print(

                name,

                platform

            )



        time.sleep(0.3)



    return businesses





def save_database(results):


    with open(

        "../database.json",

        "w",

        encoding="utf8"

    ) as file:


        json.dump(

            results,

            file,

            indent=2,

            ensure_ascii=False

        )





if __name__ == "__main__":


    district = TARGET_DISTRICT


    postcodes = get_postcodes(
        district
    )


    businesses = find_businesses(

        postcodes,

        district

    )


    save_database(
        businesses
    )


    print(

        "Saved",

        len(businesses),

        "businesses"

    )
