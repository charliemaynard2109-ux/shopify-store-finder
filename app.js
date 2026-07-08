document.getElementById("searchButton").addEventListener("click", function(){

const postcode=document.getElementById("postcode").value;

document.getElementById("results").innerHTML=

"Searching for businesses near <strong>"+postcode+"</strong>...";

});
