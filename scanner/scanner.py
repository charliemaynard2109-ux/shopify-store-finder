import requests
import json

from detector import detect_platform



POSTCODE="CM1"


def find_businesses(postcode):


    query=f"""

[out:json];

area["name"="{postcode}"]->.searchArea;

(
node["shop"](area.searchArea);
node["name"](area.searchArea);
way["shop"](area.searchArea);
);

out center;

"""



    url="https://overpass-api.de/api/interpreter"


    response=requests.post(
        url,
        data=query
    )


    data=response.json()


    businesses=[]


    for item in data["elements"]:


        tags=item.get("tags",{})


        name=tags.get("name")


        website=tags.get("website")



        if name and website:


            platform=detect_platform(
                website
            )


            businesses.append({

                "business":name,

                "address":
                tags.get("addr:street",""),

                "postcode":
                postcode,

                "website":
                website,

                "platform":
                platform

            })


    return businesses




results=find_businesses(POSTCODE)



with open(
"../database.json",
"w",
encoding="utf8"
) as f:


    json.dump(
        results,
        f,
        indent=2
    )


print(
"Saved",
len(results),
"businesses"
)
