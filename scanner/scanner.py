import requests
import json
import time
from detector import detect_platform


# UK postcode prefixes
POSTCODES = [
    "AB","AL","B","BA","BB","BD","BH","BL","BN","BR","BS",
    "BT","CA","CB","CF","CH","CM","CO","CR","CT","CV",
    "CW","DA","DD","DE","DG","DH","DL","DN","DT","DY",
    "E","EC","EH","EN","EX","FK","FY","G","GL","GU",
    "HA","HD","HG","HP","HR","HS","HX","IG","IP","IV",
    "KA","KT","KW","KY","L","LA","LD","LE","LL","LN",
    "LS","LU","M","ME","MK","ML","N","NE","NG","NN",
    "NP","NR","NW","OL","OX","PA","PE","PH","PL",
    "PO","PR","RG","RH","RM","S","SA","SE","SG",
    "SK","SL","SM","SN","SO","SP","SR","SS","ST",
    "SW","SY","TA","TD","TF","TN","TQ","TR","TS",
    "TW","UB","WA","WC","WD","WF","WN","WR","WS",
    "WV","YO","ZE"
]


def find_businesses(prefix):

    print("Searching:", prefix)


    query = f"""

[out:json][timeout:60];

area["ISO3166-1"="GB"]->.uk;

(
node["shop"](area.uk);
way["shop"](area.uk);

node["craft"](area.uk);
way["craft"](area.uk);

node["office"](area.uk);
way["office"](area.uk);

);

out center;

"""


    try:

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            timeout=120
        )


        data=response.json()


    except Exception as e:

        print("OSM error:", e)
        return []



    businesses=[]


    for item in data.get("elements", []):


        tags=item.get("tags", {})


        name=tags.get("name")


        website=(
            tags.get("website")
            or
            tags.get("contact:website")
        )


        if not name:

            continue


        if not website:

            continue



        print(
            "Checking:",
            name,
            website
        )


        platform=detect_platform(website)



        businesses.append({

            "business": name,

            "address":
            tags.get("addr:street",""),

            "postcode":
            prefix,

            "website":
            website,

            "platform":
            platform

        })


        time.sleep(0.5)



    return businesses





def main():


    all_businesses=[]


    for postcode in POSTCODES:


        results=find_businesses(postcode)


        all_businesses.extend(results)


        print(
            postcode,
            "found",
            len(results)
        )



    with open(
        "../database.json",
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            all_businesses,
            file,
            indent=2,
            ensure_ascii=False
        )



    print(
        "COMPLETE:",
        len(all_businesses),
        "businesses saved"
    )



if __name__=="__main__":

    main()
