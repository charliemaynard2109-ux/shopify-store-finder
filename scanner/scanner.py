import json
import requests
import time

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from detector import detect_platform


TARGET_DISTRICT = "CM1"



SEARCH_TERMS = [

    "clothing shop",

    "boutique",

    "gift shop",

    "furniture shop",

    "beauty",

    "jewellery",

    "homeware",

    "sports shop",

    "pet shop",

    "food shop"

]





def find_websites():


    websites = {}


    print(
        "Searching:",
        TARGET_DISTRICT
    )


    with DDGS() as ddgs:


        for term in SEARCH_TERMS:


            query = (
                TARGET_DISTRICT
                +
                " "
                +
                term
                +
                " website"
            )


            print(
                "Query:",
                query
            )


            try:


                results = ddgs.text(

                    query,

                    max_results=20

                )


                for result in results:


                    url = result.get(
                        "href"
                    )


                    title = result.get(
                        "title"
                    )


                    if url and url.startswith(
                        "http"
                    ):


                        websites[url] = title



            except Exception as e:


                print(
                    "Search error:",
                    e
                )



            time.sleep(1)



    print(
        "Websites found:",
        len(websites)
    )


    return websites





def scan_websites(websites):


    output=[]



    for url,title in websites.items():


        print(
            "Checking:",
            url
        )


        platform="Unknown"



        try:


            platform=detect_platform(
                url
            )



        except Exception as e:


            print(
                "Detector error:",
                e
            )



        output.append({

            "business": title,

            "website": url,

            "postcode_area": TARGET_DISTRICT,

            "platform": platform

        })



        time.sleep(0.5)



    return output





def save(results):


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





if __name__=="__main__":


    websites=find_websites()


    results=scan_websites(
        websites
    )


    save(
        results
    )


    print(

        "Saved",

        len(results),

        "businesses"

    )
