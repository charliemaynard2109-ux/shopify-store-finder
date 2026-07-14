import json
import time
import os
import requests

from bs4 import BeautifulSoup

from detector import detect_platform

from postcode_batches import POSTCODE_BATCHES



BATCH = os.environ.get(
    "BATCH",
    "batch1"
)


TARGET_DISTRICTS = POSTCODE_BATCHES[BATCH]



SEARCH_TERMS = [

    "shop",
    "boutique",
    "online shop",
    "clothing",
    "jewellery",
    "gift shop",
    "furniture",
    "beauty",
    "pet shop",
    "homeware",
    "independent retailer"

]



BAD_DOMAINS = [

    "facebook.com",
    "instagram.com",
    "tripadvisor.com",
    "yell.com",
    "yelp.com",
    "google.com",
    "linkedin.com",
    "youtube.com",
    "pinterest.com"

]





def clean_url(url):


    for bad in BAD_DOMAINS:

        if bad in url.lower():

            return False


    return True





def bing_search(query):


    print(
        "Searching:",
        query
    )


    try:


        response = requests.get(

            "https://www.bing.com/search",

            params={

                "q": query,

                "count": 20

            },

            headers={

                "User-Agent":
                "Mozilla/5.0"

            },

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



    results=[]



    for item in soup.select(
        "li.b_algo h2 a"
    ):


        link=item.get(
            "href"
        )


        if link and link.startswith("http"):

            results.append(
                link
            )



    return results





def find_websites(district):


    websites=set()



    for term in SEARCH_TERMS:


        query = (

            district

            +

            " "

            +

            term

            +

            " website"

        )



        links = bing_search(
            query
        )



        for link in links:


            if clean_url(link):

                websites.add(
                    link
                )



        time.sleep(2)



    print(

        district,

        "websites found:",

        len(websites)

    )



    return websites





def ecommerce_score(platform):


    scores={

        "Shopify":100,

        "WooCommerce":90,

        "Magento":85,

        "Wix":60,

        "Squarespace":60,

        "Unknown":20,

        "Website Unreachable":0

    }


    return scores.get(

        platform,

        0

    )





def load_existing_database():


    try:


        with open(

            "../database.json",

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    except:


        return []





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





def scan_websites(websites, district):


    results=[]



    for url in websites:


        print(

            "Scanning:",

            url

        )



        detected = detect_platform(
            url
        )



        if isinstance(
            detected,
            dict
        ):


            platform = detected.get(
                "platform",
                "Unknown"
            )


            confidence = detected.get(
                "confidence",
                0
            )


        else:


            platform = detected

            confidence = 0




        results.append({

            "postcode_area":
            district,

            "website":
            url,

            "platform":
            platform,

            "confidence":
            confidence,

            "score":
            ecommerce_score(
                platform
            )

        })



        time.sleep(1)



    return results





def main():


    existing = load_existing_database()



    existing_urls=set()



    for item in existing:

        existing_urls.add(

            item.get(
                "website"
            )

        )



    new_results=[]



    for district in TARGET_DISTRICTS:


        print(

            "===================="

        )


        print(

            "Scanning district:",

            district

        )


        websites=find_websites(
            district
        )



        results=scan_websites(

            websites,

            district

        )



        for item in results:


            if item["website"] not in existing_urls:


                new_results.append(
                    item
                )



                existing_urls.add(
                    item["website"]
                )



    combined = existing + new_results



    combined.sort(

        key=lambda x:x.get(
            "score",
            0
        ),

        reverse=True

    )



    save_database(
        combined
    )



    print(

        "Added",

        len(new_results),

        "new businesses"

    )


    print(

        "Total database:",

        len(combined)

    )





if __name__ == "__main__":

    main()
