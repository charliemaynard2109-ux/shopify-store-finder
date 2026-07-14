let businesses=[];


fetch("database.json")
.then(res=>res.json())
.then(data=>{
businesses=data;
});


function searchBusinesses(){


let postcode=document
.getElementById("postcode")
.value
.toUpperCase();


let platform=document
.getElementById("platform")
.value;



let results=businesses.filter(x=>{


let postcodeMatch =
x.postcode &&
x.postcode.startsWith(postcode);



let platformMatch =
platform==="all" ||
x.platform===platform;



return postcodeMatch && platformMatch;


});


display(results);


}



function display(data){


let table=document.getElementById("results");

table.innerHTML="";


data.forEach(x=>{


table.innerHTML += `

<tr>

<td>${x.business}</td>

<td>${x.address || ""}</td>

<td>
<a href="${x.website}" target="_blank">
${x.website}
</a>
</td>

<td>${x.platform}</td>

</tr>


`;


});


}



function downloadCSV(){


let csv="Business,Address,Website,Platform\n";


businesses.forEach(x=>{


csv += `"${x.business}","${x.address}","${x.website}","${x.platform}"\n`;


});


let blob=new Blob([csv],{type:"text/csv"});


let url=URL.createObjectURL(blob);


let a=document.createElement("a");

a.href=url;

a.download="businesses.csv";

a.click();


}
