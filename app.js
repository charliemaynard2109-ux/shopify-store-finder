let businesses = [];


async function loadDatabase() {

    try {

        const response = await fetch("database.json");

        businesses = await response.json();

        console.log(
            "Loaded businesses:",
            businesses.length
        );


    } catch (error) {

        console.error(
            "Database load failed:",
            error
        );

    }

}



function searchBusinesses() {


    const input = document
        .getElementById("search")
        .value
        .trim()
        .toUpperCase();



    const results = businesses.filter(item => {


        const postcode = (
            item.postcode_area || ""
        ).toUpperCase();


        return postcode.includes(input);


    });



    displayResults(results);

}





function displayResults(results) {


    const container = document.getElementById(
        "results"
    );


    container.innerHTML = "";



    if (results.length === 0) {


        container.innerHTML = `

        <div class="no-results">

        No businesses found

        </div>

        `;


        return;

    }




    results.forEach(item => {


        const card = document.createElement(
            "div"
        );


        card.className = "business-card";



        card.innerHTML = `

        <h3>${item.business || "Unknown Business"}</h3>

        <p>
        <strong>Postcode:</strong>
        ${item.postcode_area || ""}
        </p>


        <p>
        <strong>Website:</strong>
        ${
            item.website
            ?
            `<a href="${item.website}" target="_blank">
            ${item.website}
            </a>`
            :
            "No website"
        }
        </p>


        <p>
        <strong>Platform:</strong>
        ${item.platform || "Unknown"}
        </p>


        <p>
        <strong>Confidence:</strong>
        ${item.confidence || 0}%
        </p>


        <p>
        <strong>Score:</strong>
        ${item.score || 0}
        </p>

        `;


        container.appendChild(card);


    });


}





document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadDatabase();


        const button =
            document.getElementById(
                "searchButton"
            );


        if (button) {


            button.addEventListener(
                "click",
                searchBusinesses
            );


        }


    }
);
