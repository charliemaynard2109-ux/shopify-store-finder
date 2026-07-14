import requests


def detect_platform(url):


    try:


        response = requests.get(

            url,

            headers={
                "User-Agent":
                "Mozilla/5.0"
            },

            timeout=15

        )


        html = response.text.lower()



    except Exception:


        return "Website Unreachable"



    # Shopify indicators

    shopify_signals = [

        "cdn.shopify.com",

        "shopify.theme",

        "myshopify.com",

        "/products/",

        "shopify-payment-button",

        "shopify-section"

    ]


    for signal in shopify_signals:

        if signal in html:

            return "Shopify"



    # WooCommerce indicators

    woo_signals = [

        "woocommerce",

        "wp-content/plugins/woocommerce",

        "wc-block",

        "add-to-cart"

    ]


    for signal in woo_signals:

        if signal in html:

            return "WooCommerce"



    # Magento

    magento_signals = [

        "magento",

        "mage-cache"

    ]


    for signal in magento_signals:

        if signal in html:

            return "Magento"



    # Wix

    if "wixstatic.com" in html:

        return "Wix"



    # Squarespace

    if "squarespace.com" in html:

        return "Squarespace"



    return "Unknown"
