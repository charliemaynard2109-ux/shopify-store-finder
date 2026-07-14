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


    response = requests.get(
        url,
        timeout=30
    )


    data = response.json()


    results = []


    for item in data.get("result", []):

        if isinstance(item, dict):

            results.append(
                item.get("postcode")
            )

        else:

            results.append(
                item
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


    response = requests.get(
        url,
        timeout=20
    )


    data = response.json()


    if data.get("status") != 200:

        return None



    result = data["result"]


    return (
        result["latitude"],
        result["longitude"]
    )





def find_businesses(postcodes, district):


    businesses=[]

    checked=set()



    for postcode in postcodes:


        coords=get_coordinates(
            postcode
        )


        if not coords:
            continue



        lat,lon=coords



        query=f"""

[out:json][timeout:25];

(
node["shop"](around:500,{lat},{lon});
way["shop"](around:500,{lat},{lon});

);

out center;

"""


        try:

            response=requests.post(

                "https://overpass-api.de/api/interpreter",

                data=query,

                timeout=40

            )


            data=response.json()


        except Exception as e:

            print(
                "Overpass error:",
                e
            )

            continue




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



            if name in checked:
                continue



            checked.add(
                name
            )



            website = (
                tags.get("website")
                or ""
            )


            platform="Not Checked"



            if website:

                platform=detect_platform(
                    website
                )



            businesses.append({

                "business": name,

                "postcode": district,

                "website": website,

                "platform": platform

            })


            print(
                name,
                platform
            )


        time.sleep(0.5)



    return businesses





if __name__=="__main__":


    district = TARGET_DISTRICT


    postcodes = get_postcodes(
        district
    )


    businesses = find_businesses(
        postcodes,
        district
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
