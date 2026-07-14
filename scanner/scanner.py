import json
import time
import requests
from bs4 import BeautifulSoup

from detector import detect_platform


TARGET_DISTRICT = "CM1"


SEARCH_TERMS = [

    "shop",
    "boutique",
    "online shop",
    "clothing",
    "jewellery",
    "gift shop",
    "furniture",
    "beauty",
    "pet shop"

]


BAD_DOMAINS = [

    "facebook.com",
    "instagram.com",
    "tripadvisor.com",
    "yell.com",
    "google.com",
    "linkedin.com",
    "youtube.com"

]



def clean_url(url):

    for bad in BAD_DOMAINS:

        if bad in url:

            return False


    return True





def bing_search(query):


    print(
        "Searching:",
        query
    )


    url = "https://www.bing.com/search"


    params = {

        "q": query,

        "count": 20

    }


    headers = {

        "User-Agent":
        "Mozilla/5.0"

    }


    try:


        response = requests.get(

            url,

            params=params,

            headers=headers,

            timeout=30

        )


        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )



    except Exception as e:


        print(
            "Search error:",
            e
        )

        return []



    links=[]



    for item in soup.select("li.b_algo h2 a"):


        href=item.get(
            "href"
        )


        if href and href.startswith("http"):

            links.append(
                href
            )


    return links





def find_websites():


    websites=set()


    for term in SEARCH_TERMS:


        query=f"{TARGET_DISTRICT} {term} website"


        results=bing_search(
            query
        )


        for url in results:


            if clean_url(url):

                websites.add(
                    url
                )


        time.sleep(2)



    print(

        "Websites found:",

        len(websites)

    )


    return websites





def score(platform):


    scores={

        "Shopify":100,

        "WooCommerce":90,

        "Magento":80,

        "Wix":60,

        "Squarespace":60,

        "Unknown":20

    }


    return scores.get(

        platform,

        0

    )





def main():


    websites=find_websites()


    results=[]



    for url in websites:


        print(
            "Scanning:",
            url
        )


        platform=detect_platform(
            url
        )


        results.append({

            "postcode_area":
            TARGET_DISTRICT,

            "website":
            url,

            "platform":
            platform,

            "score":
            score(platform)

        })



        time.sleep(1)



    results.sort(

        key=lambda x:x["score"],

        reverse=True

    )



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





if __name__=="__main__":

    main()
