async function searchStores(){

    const postcode = document
    .getElementById("postcode")
    .value
    .toUpperCase();


    const response = await fetch("../data/stores.json");

    const stores = await response.json();


    const results = stores.filter(store =>
    store.postcode.startsWith(postcode)
    );


    let html="";


    if(results.length===0){

    html="<p>No stores found.</p>";

    }
    else {

    results.forEach(store=>{

    html += `

    <div class="card">

    <h3>${store.business}</h3>

    <p>${store.website}</p>

    <p>
    Shopify:
    ${store.shopify ? "✅ Yes" : "❌ No"}
    </p>

    </div>

    `;

    });

    }


    document.getElementById("results").innerHTML=html;

    }
