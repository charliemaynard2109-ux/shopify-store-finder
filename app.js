async function searchBusinesses() {

    const postcode = document
        .getElementById("postcode")
        .value
        .toUpperCase()
        .trim();


    const results = document.getElementById("results");


    if (!postcode) {

        results.innerHTML = `
        <tr>
            <td colspan="3">
                Please enter a postcode prefix
            </td>
        </tr>
        `;

        return;

    }


    const response = await fetch("businesses.json");

    const businesses = await response.json();


    const matches = businesses.filter(business =>
        business.postcode.startsWith(postcode)
    );


    results.innerHTML = "";


    if (matches.length === 0) {

        results.innerHTML = `
        <tr>
            <td colspan="3">
                No businesses found
            </td>
        </tr>
        `;

        return;

    }


    matches.forEach(business => {


        results.innerHTML += `

        <tr>

            <td>
                ${business.name}
            </td>

            <td>
                <a href="${business.website}" target="_blank">
                ${business.website}
                </a>
            </td>

            <td>
                Checking...
            </td>

        </tr>

        `;


    });


}
