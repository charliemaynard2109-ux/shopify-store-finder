async function searchBusinesses(){

const prefix = document.getElementById("postcode").value.trim();
const status = document.getElementById("status");
const results = document.getElementById("results");

results.innerHTML = "";

if(!prefix){
    status.innerHTML = "Enter a postcode prefix";
    return;
}

status.innerHTML = "Finding postcode location...";


try {

const geoURL =
`https://nominatim.openstreetmap.org/search?format=json&q=${prefix}, UK`;


const geoResponse = await fetch(geoURL);


const geo = await geoResponse.json();


console.log("Geocode result:", geo);


if(!geo.length){

status.innerHTML =
"No location found for " + prefix;

return;

}


const lat = geo[0].lat;
const lon = geo[0].lon;


status.innerHTML =
`Location found: ${lat}, ${lon}. Searching businesses...`;



const query = `

[out:json];

(
node["shop"](around:3000,${lat},${lon});
node["amenity"="restaurant"](around:3000,${lat},${lon});
node["amenity"="cafe"](around:3000,${lat},${lon});
way["shop"](around:3000,${lat},${lon});

);

out center;

`;



const response =
await fetch(
"https://overpass-api.de/api/interpreter",
{
method:"POST",
body:query
}
);


const data =
await response.json();


console.log("OSM result:", data);



status.innerHTML =
`Found ${data.elements.length} businesses`;



data.elements.forEach(place=>{


const tags = place.tags || {};


results.innerHTML += `

<tr>

<td>${tags.name || "Unnamed business"}</td>

<td>${tags.shop || tags.amenity || ""}</td>

<td>${tags.website || "No website"}</td>

<td>Checking...</td>

</tr>

`;

});


}

catch(error){

console.error(error);

status.innerHTML =
"Error: " + error.message;

}


}
