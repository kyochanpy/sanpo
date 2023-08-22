let map
let routingControl
let toggle
let facilities

navigator.geolocation.getCurrentPosition((position) => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    toggle = document.getElementById("toggle")
    facilities = document.getElementById("facilities")

    map = L.map("map").setView([latitude, longitude], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    map.invalidateSize();

    toggle.addEventListener("click", () => {
        console.log("aaa")
        document.body.classList.toggle("show-nav");
        document.body.addEventListener("click", closeNavbar);
    })

    document.getElementById("toiletButton").addEventListener("click", () => sendRequest("toilet", latitude, longitude));
    document.getElementById("stationButton").addEventListener("click", () => sendRequest("station", latitude, longitude));
    document.getElementById("busStopButton").addEventListener("click", () => sendRequest("bus_stop", latitude, longitude));
});

async function sendRequest(facilityType, latitude, longitude) {
    fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            lat: latitude,
            lon: longitude,
            facility_type: facilityType,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.facility.lat === 999) {
            console.warn("周囲に該当施設はありません")
        } else {
            searchRoute(latitude, longitude, data)
        }
    })
    .catch((error) => {
        console.error("エラー:", error);
    });
}

function searchRoute(currentLat, currentLon, facility_dict) {
    if (routingControl) map.removeControl(routingControl);
    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(currentLat, currentLon),
            L.latLng(facility_dict.facility.lat, facility_dict.facility.lon)
        ],
    }).addTo(map);
}

function closeNavbar(e) {
    if (
        document.body.classList.contains("show-nav") &&
        e.target !== toggle &&
        !toggle.contains(e.target) &&
        e.toggle !== facilities &&
        !facilities.contains(e.target)
    ) {
        document.body.classList.toggle("show-nav");
        document.body.removeEventListener("click", closeNavbar);
    } else if (!document.body.classList.contains("show-nav")) {
        document.body.removeEventListener("click", closeNavbar);
    }
}

