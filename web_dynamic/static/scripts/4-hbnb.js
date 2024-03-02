const HOST = "0.0.0.0";

$(document).ready(function () {
  const amen = {};

  // Update the change event handler for amenity checkboxes
  $("input[type='checkbox']").change(function () {
    if ($(this).is(":checked"))
      amen[$(this).attr("data-name")] = $(this).attr("data-id");
    else delete amen[$(this).attr("data-name")];
    const objNames = Object.keys(amen);
    $(".amenities h4").text(objNames.sort().join(", "));
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

// New function to handle search with amenities
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
