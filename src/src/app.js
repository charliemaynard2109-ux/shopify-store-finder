let businesses = [];


async function searchBusinesses() {

    const postcode = document
        .getElementById("postcode")
        .value
        .trim()
        .toUpperCase();

    const status = document.getElementById("status");
    const results = document.getElementById("results");

    results.innerHTML = "";
    businesses = [];

    if (!postcode) {
        status.innerHTML = "Enter a postcode prefix";
        return;
    }


    status.innerHTML = "Finding postcode area...";


    try {

        const geo = await fetch(
            `https://nominatim.openstreetmap.org/search?format=json&q=${postcode}, UK`
        );


        const geoData = await geo.json();


        if (!geoData.length) {

            status.innerHTML = "Postcode not found";
            return;

        }


        const lat = geoData[0].lat;
        const lon = geoData[0].lon;



        status.innerHTML = "Searching businesses...";



        const query = `

        [out:json];

        (
          nwr["name"]["shop"](around:5000,${lat},${lon});
          nwr["name"]["amenity"](around:5000,${lat},${lon});
          nwr["name"]["office"](around:5000,${lat},${lon});
          nwr["name"]["craft"](around:5000,${lat},${lon});
        );

        out tags center;

        `;



        const response = await fetch(
            "https://overpass-api.de/api/interpreter",
            {
                method:"POST",
                body:query
            }
        );


        const data = await response.json();



        data.elements.forEach(place => {


            const tags = place.tags || {};

            const website =
                tags.website ||
                tags["contact:website"] ||
                tags.url ||
                tags["contact:url"] ||
                "";


            const address = [

                tags["addr:housenumber"],
                tags["addr:street"],
                tags["addr:city"],
                tags["addr:postcode"]

            ]
            .filter(Boolean)
            .join(" ");



            businesses.push({

                name: tags.name || "Unknown",

                address:
                address || "Not listed",

                type:
                tags.shop ||
                tags.amenity ||
                tags.office ||
                tags.craft ||
                "Business",

                phone:
                tags.phone ||
                tags["contact:phone"] ||
                "",

                website: website,

                shopify:"Unknown"

            });



        });



        displayResults();


        status.innerHTML =
        `Found ${businesses.length} businesses`;



    } catch(error) {

        console.error(error);

        status.innerHTML =
        "Error loading businesses";

    }

}





function displayResults(filter="all") {


    const table =
    document.getElementById("results");


    table.innerHTML="";



    businesses
    .filter(item => {


        if(filter==="shopify")
            return item.shopify==="YES";


        if(filter==="nonshopify")
            return item.shopify==="NO";


        if(filter==="nowebsite")
            return !item.website;


        if(filter==="unknown")
            return item.shopify==="Unknown";


        return true;


    })
    .forEach(item => {


        table.innerHTML += `

        <tr>

        <td>${item.name}</td>

        <td>${item.address}</td>

        <td>${item.type}</td>

        <td>${item.phone}</td>

        <td>
        ${
            item.website
            ?
            `<a href="${item.website}" target="_blank">${item.website}</a>`
            :
            "No website"
        }
        </td>


        <td>${item.shopify}</td>


        </tr>

        `;


    });


}





function filterResults(){

    const filter =
    document.getElementById("filter").value;


    displayResults(filter);

}





async function scanShopify(){


    const status =
    document.getElementById("status");


    status.innerHTML =
    "Scanning websites...";



    for (let business of businesses){


        if(!business.website){

            business.shopify="Unknown";
            continue;

        }



        try {


            const response =
            await fetch(business.website);



            const html =
            await response.text();



            if(

                html.includes("cdn.shopify.com") ||
                html.includes("Shopify.theme") ||
                html.includes("shopify-payment-button") ||
                html.includes("checkout.shopify.com")

            ){

                business.shopify="YES";

            } else {

                business.shopify="NO";

            }



        } catch {

            business.shopify="Unknown";

        }


    }


    displayResults();


    status.innerHTML =
    "Shopify scan complete";


}





function exportCSV(){


    if(!businesses.length){

        alert("No results");
        return;

    }



    let csv =

    "Business,Address,Type,Phone,Website,Shopify\n";



    businesses.forEach(item=>{


        csv +=

        `"${item.name}","${item.address}","${item.type}","${item.phone}","${item.website}","${item.shopify}"\n`;


    });



    const blob =
    new Blob([csv],
    {
        type:"text/csv"
    });



    const link =
    document.createElement("a");


    link.href =
    URL.createObjectURL(blob);


    link.download =
    "shopify-store-results.csv";


    link.click();


}
