async function searchBusinesses() {

const postcode = document
.getElementById("postcode")
.value
.trim();


const status = document.getElementById("status");
const results = document.getElementById("results");


results.innerHTML = "";


if (!postcode) {

status.innerHTML = "Please enter a postcode prefix";

return;

}


status.innerHTML = "Finding postcode location...";


try {


const geoResponse = await fetch(

`https://nominatim.openstreetmap.org/search?format=json&q=${postcode}, UK`

);


const geoData = await geoResponse.json();



if (!geoData.length) {

status.innerHTML =
"Could not find postcode area";

return;

}



const lat = geoData[0].lat;
const lon = geoData[0].lon;



status.innerHTML =
"Searching OpenStreetMap businesses...";



const query = `

[out:json];

(
node["shop"](around:5000,${lat},${lon});
way["shop"](around:5000,${lat},${lon});

node["amenity"="restaurant"](around:5000,${lat},${lon});
way["amenity"="restaurant"](around:5000,${lat},${lon});

node["amenity"="cafe"](around:5000,${lat},${lon});
way["amenity"="cafe"](around:5000,${lat},${lon});

);

out center;

`;



const osmResponse = await fetch(

"https://overpass-api.de/api/interpreter",

{

method:"POST",

body:query

}

);



const osmData = await osmResponse.json();



status.innerHTML =
`Found ${osmData.elements.length} businesses`;



osmData.elements.forEach(place => {


const tags = place.tags || {};


const name =
tags.name || "Unnamed business";


const category =
tags.shop ||
tags.amenity ||
"Business";


const website =
tags.website ||
tags["contact:website"] ||
"";



results.innerHTML += `

<tr>

<td>${name}</td>

<td>${category}</td>

<td>
${
website
?
`<a href="${website}" target="_blank">${website}</a>`
:
"No website"
}
</td>


<td>
Not checked
</td>


</tr>

`;

});


}

catch(error) {


status.innerHTML =
"Error: " + error.message;


console.error(error);


}

}




function exportCSV() {


const rows = [];


const tableRows =
document.querySelectorAll("#results tr");



if (!tableRows.length) {

alert("No results to export");

return;

}



rows.push([

"Business",
"Category",
"Website",
"Shopify"

]);



tableRows.forEach(row => {


const cells =
row.querySelectorAll("td");


rows.push([

cells[0]?.innerText || "",
cells[1]?.innerText || "",
cells[2]?.innerText || "",
cells[3]?.innerText || ""

]);


});



const csv = rows.map(row =>

row.map(item =>

`"${item.replace(/"/g,'""')}"`

).join(",")

).join("\n");



const blob =
new Blob(

[csv],

{
type:"text/csv"
}

);



const url =
URL.createObjectURL(blob);



const link =
document.createElement("a");


link.href = url;


link.download =
"shopify-store-results.csv";


link.click();


}
