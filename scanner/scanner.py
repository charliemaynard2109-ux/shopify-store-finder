import json
import time

from ddgs import DDGS

from detector import detect_platform


TARGET_DISTRICT = "CM1"


SEARCH_TERMS = [

    "clothing shop",
    "boutique",
    "gift shop",
    "furniture shop",
    "beauty salon",
    "jewellery",
    "homeware",
    "sports shop",
    "pet shop",
    "food shop",
    "independent shop",
    "online store"

]



def find_websites():

    websites = {}


    print(
        "Searching:",
        TARGET_DISTRICT
    )


    try:

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


                    results = list(
                        ddgs.text(
                            query,
                            max_results=20
                        )
                    )


                    print(
                        "Results returned:",
                        len(results)
                    )



                    for result in results:


                        url = (

                            result.get("href")

                            or

                            result.get("url")

                        )


                        title = (

                            result.get("title")

                            or

                            "Unknown Business"

                        )


                        if url and url.startswith("http"):


                            websites[url] = title



                except Exception as e:


                    print(
                        "Search error:",
                        e
                    )



                time.sleep(1)



    except Exception as e:


        print(
            "DDGS error:",
            e
        )



    print(
        "Websites found:",
        len(websites)
    )



    print(
        "Sample websites:"
    )


    for site in list(websites.keys())[:10]:

        print(
            site
        )


    return websites





def scan_websites(websites):


    results=[]



    for url, title in websites.items():


        print(
            "Checking:",
            url
        )


        platform="Unknown"



        try:


            platform = detect_platform(
                url
            )


        except Exception as e:


            print(
                "Detector error:",
                e
            )


            platform="Error"



        results.append({

            "business": title,

            "postcode_area": TARGET_DISTRICT,

            "website": url,

            "platform": platform

        })



        time.sleep(0.5)



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





if __name__ == "__main__":


    websites = find_websites()


    results = scan_websites(
        websites
    )


    save_database(
        results
    )


    print(

        "Saved",

        len(results),

        "businesses"

    )
