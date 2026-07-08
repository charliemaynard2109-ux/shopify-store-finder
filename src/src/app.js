function findStore() {

    const input = document.getElementById("storeInput").value;

    const result = document.getElementById("result");


    if (!input) {

        result.innerHTML = "Please enter a store URL.";

        return;

    }


    result.innerHTML = `

        <h3>Store Found</h3>

        <p>
        Checking:
        <strong>${input}</strong>
        </p>

        <p>
        Shopify detection module ready.
        </p>

    `;

}
