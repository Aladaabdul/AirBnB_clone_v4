const HOST = "0.0.0.0";
const amen = {};

$(document).ready(function () {
    // Event listener for the span next to the "Reviews" heading
    $("h2:contains('Reviews') + span").click(function () {
	    // Toggle between showing and hiding reviews
        if ($(this).text() === 'Show') {
            fetchReviews(); // Fetch and display reviews
		$(this).text('Hide'); // Change the text to "Hide"
        } else {
            $(".reviews").empty(); // Remove all review elements from the DOM
            $(this).text('Show'); // Change the text to "Show"
        }
    });
);
        // Update the h4 tag inside the div Locations with the list of States or Cities checked
        const objNames = Object.keys(amen);
        $(".locations h4").text(objNames.sort().join(", "));
    });

    apiStatus();
    fetchPlaces();

    // Add event listener for the button click
    $("button").click(function () {
        searchPlaces(); // Call a function to handle the search
    });
});

function apiStatus() {
    const apiUrl = "http://0.0.0.0:5001/api/v1/status/";
    $.get(apiUrl, function (data, status) {
        if (data.status === "OK" && status === "success") {
            $("#api_status").addClass("available");
        } else {
            $("#api_status").removeClass("available");
        }
    });
}

function fetchPlaces() {
    const PLACES_URL = `http://${HOST}:5001/api/v1/places_search/`;
    $.ajax({
        url: PLACES_URL,
        type: "POST",
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify({}),
        success: function (response) {
            displayPlaces(response); // Call a function to display places
        },
        error: function (error) {
            console.log(error);
        },
    });
}

// New function to handle search with amenities, states, and cities
function searchPlaces() {
    const PLACES_URL = `http://${HOST}:5001/api/v1/places_search/`;
    $.ajax({
        url: PLACES_URL,
        type: "POST",
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify({ amenities: Object.values(amen) }), // Pass amenities
        success: function (response) {
            displayPlaces(response); // Call a function to display places
        },
        error: function (error) {
            console.log(error);
        },
    });
}

// New function to display places
function displayPlaces(response) {
    $("SECTION.places").empty(); // Clear existing places
    for (const r of response) {
        const article = [
            "<article>",
            '<div class="title_box">',
            `<h2>${r.name}</h2>`,
            `<div class="price_by_night">$${r.price_by_night}</div>`,
            "</div>",
            '<div class="information">',
            `<div class="max_guest">${r.max_guest} Guest(s)</div>`,
            `<div class="number_rooms">${r.number_rooms} Bedroom(s)</div>`,
            `<div class="number_bathrooms">${r.number_bathrooms} Bathroom(s)</div>`,
            "</div>",
            '<div class="description">',
            `${r.description}`,
            "</div>",
            "</article>",
        ];
        $("SECTION.places").append(article.join(""));
    }
}
