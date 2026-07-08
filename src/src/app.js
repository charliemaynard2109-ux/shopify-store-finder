async function searchBusinesses(){

const prefix =
document.getElementById("postcode").value.trim();


const status =
document.getElementById("status");


const results =
document.getElementById("results");


if(!prefix){

status.innerHTML="Enter a postcode prefix";

return;

}


status.innerHTML="Searching OpenStreetMap...";

results.innerHTML="";


// UK postcode prefix approximate search
const geocodeURL =
`https://nominatim.openstreetmap.org/search?format=json&q=${prefix},UK`;


const geoResponse =
await fetch(geocodeURL);


const geo =
await geoResponse.json();


if(!geo.length){

status.innerHTML="Postcode not found";

return;

}


const lat =
geo[0].lat;

const lon =
geo[0].lon;



const query = `

[out:json];

(
node["shop"](around:5000,${lat},${lon});
node["amenity"="restaurant"](around:5000,${lat},${lon});
node["amenity"="cafe"](around:5000,${lat},${lon});
way["shop"](around:5000,${lat},${lon});

);

out center;

`;



const response =
await fetch(
"https://overpass-api.de/api/interpreter",
{
method:"POST",
body:query
});


const data =
await response.json();



status.innerHTML =
`Found ${data.elements.length} businesses`;



data.elements.forEach(place=>{


const tags =
place.tags || {};


const name =
tags.name || "Unknown";


const website =
tags.website || "";


const type =
tags.shop ||
tags.amenity ||
"Business";



let shopify =
"Unknown";


if(
website.includes("shopify")
){

shopify="Likely Shopify";

}



results.innerHTML += `

<tr>

<td>${name}</td>

<td>${type}</td>

<td>
${website ?
`<a href="${website}" target="_blank">${website}</a>`
:
"No website"}
</td>


<td class="${
shopify==="Likely Shopify"
?
"shopify"
:
"no"
}">
${shopify}
</td>


</tr>

`;

});


}
