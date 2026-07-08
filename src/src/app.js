function displayResults(filter="all") {

    const table = document.getElementById("results");

    table.innerHTML = "";

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

        let website = item.website 
        ? `<a href="${item.website}" target="_blank">${item.website}</a>`
        : "No website";


        table.innerHTML +=
        "<tr>" +
        "<td>" + item.name + "</td>" +
        "<td>" + item.address + "</td>" +
        "<td>" + item.type + "</td>" +
        "<td>" + item.phone + "</td>" +
        "<td>" + website + "</td>" +
        "<td>" + item.shopify + "</td>" +
        "</tr>";

    });

}
