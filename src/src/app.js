async function searchBusinesses() {

const postcode = document
.getElementById("postcode")
.value
.trim()
.toUpperCase();


const status =
document.getElementById("status");

const results =
document.getElementById("results");


results.innerHTML = "";


if (!postcode) {

status.innerHTML =
"Please enter a postcode prefix";

return;

}


status.innerHTML =
"Finding postcode area...";


try {


const geoResponse = await fetch(

`https://nominatim.openstreetmap.org/search?format=json&q=${postcode}, UK`

);


const geoData =
await geoResponse.json();



if (!geoData.length) {

status.innerHTML =
"Postcode not found";

return;

}



const lat =
geoData[0].lat;

const lon =
geoData[0].lon;



status.innerHTML =
"Searching businesses...";



const query = `

[out:json];

(
nwr["name"]["shop"](around:3000,${lat},${lon});
nwr["name"]["amenity"](around:3000,${lat},${lon});
nwr["name"]["office"](around:3000,${lat},${lon});
nwr["name"]["craft"](around:3000,${lat},${lon});

);

out tags center;

`;



const osmResponse =
await fetch(

"https://overpass-api.de/api/interpreter",

{

method:"POST",

body:query

}

);



const osmData =
await osmResponse.json();



let count = 0;



osmData.elements.forEach(place => {


const tags =
place.tags || {};



const name =
tags.name || "";



const type =
tags.shop ||
tags.amenity ||
tags.office ||
tags.craft ||
"Business";



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



if (!name) return;



count++;



results.innerHTML += `

<tr>

<td>${name}</td>

<td>${address || "Not listed"}</td>

<td>${type}</td>

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

Unknown

</td>


</tr>

`;



});



status.innerHTML =
`Found ${count} businesses`;



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
"Address",
"Type",
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
cells[3]?.innerText || "",
cells[4]?.innerText || ""

]);



});



const csv =
rows.map(row =>

row.map(value =>

`"${value.replace(/"/g,'""')}"`

).join(",")

).join("\n");



const blob =
new Blob(

[csv],

{
type:"text/csv"
}

);



const link =
document.createElement("a");


link.href =
URL.createObjectURL(blob);


link.download =
"shopify-store-results.csv";


link.click();


}
