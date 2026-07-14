import requests


def detect_platform(url):

    try:

        if not url.startswith("http"):
            url="https://" + url


        r=requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )


        html=r.text.lower()



        # Shopify

        shopify=[
            "cdn.shopify.com",
            "shopify.theme",
            "shopify-section",
            "shopify.shop",
            "/cart.js"
        ]


        for item in shopify:

            if item in html:
                return "Shopify"



        # WooCommerce

        woo=[
            "woocommerce",
            "wc-ajax",
            "wp-content/plugins/woocommerce"
        ]


        for item in woo:

            if item in html:
                return "WooCommerce"



        # Magento

        if "magento" in html:
            return "Magento"



        # Wix

        if "wixstatic" in html:
            return "Wix"



        # Squarespace

        if "squarespace" in html:
            return "Squarespace"



        return "Unknown"



    except Exception:

        return "Unreachable"
