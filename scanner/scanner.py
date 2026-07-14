import json
import time

from ddgs import DDGS

from detector import detect_platform



TARGET_DISTRICT = "CM1"



BAD_DOMAINS = [

    "facebook.com",

    "instagram.com",

    "tripadvisor.com",

    "yell.com",

    "yelp.com",

    "google.com",

    "linkedin.com",

    "wikipedia.org"

]



SEARCH_TERMS = [

    "shop",

    "boutique",

    "store",

    "online shop",

    "gift shop",

    "clothing",

    "jewellery",

    "furniture",

    "beauty",

    "pet shop"

]





def valid_domain(url):


    for bad in BAD_DOMAINS:

        if bad in url:

            return False


    return True





def find_websites():


    websites={}


    with DDGS() as ddgs:


        for term in SEARCH_TERMS:


            query=f"{TARGET_DISTRICT} {term} shop"


            print(
                query
            )


            results=list(

                ddgs.text(

                    query,

                    max_results=20

                )

            )



            for result in results:


                url=(

                    result.get("href")

                    or

                    result.get("url")

                )


                title=result.get(

                    "title",

                    "Unknown"

                )


                if url and url.startswith("http"):


                    if valid_domain(url):

                        websites[url]=title



            time.sleep(1)



    return websites





def ecommerce_score(platform):


    if platform=="Shopify":

        return 100


    if platform=="WooCommerce":

        return 90


    if platform in [

        "Magento",

        "Wix",

        "Squarespace"

    ]:

        return 70



    return 20





def main():


    websites=find_websites()


    output=[]



    for url,title in websites.items():


        print(
            "Scanning",
            url
        )


        platform=detect_platform(
            url
        )


        score=ecommerce_score(
            platform
        )


        output.append({

            "business":title,

            "website":url,

            "postcode_area":TARGET_DISTRICT,

            "platform":platform,

            "score":score

        })



        time.sleep(0.5)




    output.sort(

        key=lambda x:x["score"],

        reverse=True

    )



    with open(

        "../database.json",

        "w",

        encoding="utf8"

    ) as f:


        json.dump(

            output,

            f,

            indent=2

        )



    print(

        "Saved",

        len(output),

        "businesses"

    )




if __name__=="__main__":

    main()
