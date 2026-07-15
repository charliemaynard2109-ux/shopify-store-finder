let businesses = [];



async function loadDatabase() {


    try {


        const response = await fetch(
            "database.json"
        );


        businesses = await response.json();


        console.log(
            "Loaded businesses:",
            businesses.length
        );


    }


    catch(error) {


        console.error(
            "Database load failed:",
            error
        );


    }


}





function searchBusinesses() {


    const postcode = document
        .getElementById("search")
        .value
        .trim()
        .toUpperCase();



    const platform = document
        .getElementById("platformFilter")
        .value;




    const filtered = businesses.filter(item => {



        const postcodeMatch =

            !postcode ||

            (item.postcode_area || "")
            .toUpperCase()
            .includes(postcode);




        const platformMatch =

            platform === "all" ||

            item.platform === platform;




        return postcodeMatch && platformMatch;


    });




    displayResults(filtered);


}






function displayResults(results) {


    const table = document
        .getElementById("results");



    table.innerHTML = "";




    if(results.length === 0) {


        table.innerHTML = `

        <tr>

        <td colspan="6">

        No businesses found

        </td>

        </tr>

        `;


        return;


    }






    results.forEach(item => {



        const row = document.createElement(
            "tr"
        );



        row.innerHTML = `


        <td>
        ${item.business || "Unknown"}
        </td>



        <td>
        ${item.address || ""}
        </td>



        <td>

        ${
            item.website

            ?

            `<a href="${item.website}" target="_blank">
            ${item.website}
            </a>`

            :

            ""

        }

        </td>



        <td>
        ${item.platform || "Unknown"}
        </td>



        <td>
        ${item.confidence || 0}%
        </td>



        <td>
        ${item.score || 0}
        </td>



        `;



        table.appendChild(row);


    });


}






document.addEventListener(
    "DOMContentLoaded",
    function() {



        loadDatabase();




        document
        .getElementById("searchButton")
        .addEventListener(
            "click",
            searchBusinesses
        );



    }
);
