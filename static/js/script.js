let combinedChart, map, currentMarker;

function searchCity() {
  const city = document.getElementById("cityInput").value;
  loadWeather(city);
}

document
  .getElementById("cityInput")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Voorkom dat het formulier wordt verzonden als dat het geval is
      searchCity();
    }
  });

function loadWeather(city) {
  fetch(`/weather/${city}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert("Stad niet gevonden");
        return;
      }
      updateWeatherDisplay(city, data);
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Er is een fout opgetreden");
    });
}

function initMap() {
  if (!map) {
    map = L.map("weatherMap").setView([52.3676, 4.9041], 12);
    L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
      {
        attribution: "©OpenStreetMap, ©CartoDB",
        maxZoom: 19,
      }
    ).addTo(map);
    setTimeout(() => {
      map.invalidateSize();
    }, 100);
  }
}

function createCharts(data) {
  console.log("Chart data:", {
    dates: data.forecast.map((day) => day.datum),
    temps: data.forecast.map((day) => day.temp),
    rain: data.forecast.map((day) => day.regen),
    wind: data.forecast.map((day) => day.wind),
  });

  const dates = data.forecast.map((day) => day.datum);
  const temps = data.forecast.map((day) => day.temp);
  const rain = data.forecast.map((day) => day.regen);
  const wind = data.forecast.map((day) => day.wind);

  const chartConfig = {
    type: "line",
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          top: 10,
          right: 25,
          bottom: 10,
          left: 25,
        },
      },
      plugins: {
        legend: {
          display: true,
          position: "right",
          labels: {
            color: "white",
            padding: 20,
            usePointStyle: false,
            boxWidth: 40,
            generateLabels: function (chart) {
              const datasets = chart.data.datasets;
              return datasets.map((dataset) => ({
                text: dataset.label,
                fillStyle: dataset.backgroundColor,
                strokeStyle: dataset.borderColor,
                lineWidth: 2,
                hidden: !chart.isDatasetVisible(datasets.indexOf(dataset)),
                lineCap: "round",
                lineDash: [],
                lineDashOffset: 0,
                index: datasets.indexOf(dataset),
                fontColor: "white",
              }));
            },
          },
        },
      },
      animation: {
        duration: 750,
        easing: "easeInOutQuart",
      },
      scales: {
        temp: {
          type: "linear",
          position: "left",
          ticks: { color: "white" },
          grid: { color: "rgba(255,255,255,0.1)" },
          beginAtZero: true,
        },
        rain: {
          type: "linear",
          position: "right",
          ticks: { color: "white" },
          grid: { display: false },
          beginAtZero: true,
        },
        wind: {
          type: "linear",
          position: "right",
          ticks: { color: "white" },
          grid: { display: false },
          beginAtZero: true,
        },
        x: {
          ticks: { color: "white" },
          grid: { color: "rgba(255,255,255,0.1)" },
        },
      },
    },
  };

  if (combinedChart) combinedChart.destroy();
  combinedChart = new Chart(document.getElementById("combinedChart"), {
    ...chartConfig,
    data: {
      labels: dates,
      datasets: [
        {
          label: "Temperatuur (°C)",
          data: temps,
          borderColor: "#ff6b6b",
          backgroundColor: "rgba(255,107,107,0.2)",
          tension: 0.4,
          yAxisID: "temp",
        },
        {
          label: "Neerslag (mm)",
          data: rain,
          borderColor: "#4dabf7",
          backgroundColor: "rgba(77,171,247,0.2)",
          tension: 0.4,
          yAxisID: "rain",
        },
        {
          label: "Wind (km/u)",
          data: wind,
          borderColor: "#69db7c",
          backgroundColor: "rgba(105,219,124,0.2)",
          tension: 0.4,
          yAxisID: "wind",
        },
      ],
    },
    options: {
      ...chartConfig.options,
      scales: {
        temp: {
          type: "linear",
          position: "left",
          ticks: { color: "white" },
          grid: { color: "rgba(255,255,255,0.1)" },
        },
        rain: {
          type: "linear",
          position: "right",
          ticks: { color: "white" },
          grid: { display: false },
        },
        wind: {
          type: "linear",
          position: "right",
          ticks: { color: "white" },
          grid: { display: false },
        },
        x: {
          ticks: { color: "white" },
          grid: { color: "rgba(255,255,255,0.1)" },
        },
      },
    },
  });
}

function updateWeatherDisplay(city, data) {
  // Update background image
  const cityBackground = document.querySelector(".city-background");
  cityBackground.style.opacity = 0;
  setTimeout(() => {
    cityBackground.style.backgroundImage = `url(${data.city_image})`;
    cityBackground.style.opacity = 1;
  }, 500);

  // Update current weather
  document.getElementById("cityName").textContent = city;
  document.getElementById(
    "temperature"
  ).textContent = `${data.weather.temperatuur}°C`;
  document.getElementById("description").textContent =
    data.weather.beschrijving;
  document.getElementById(
    "humidity"
  ).innerHTML = `<i class="fas fa-tint"></i> ${data.weather.luchtvochtigheid}%`;
  document.getElementById(
    "windspeed"
  ).innerHTML = `<i class="fas fa-wind"></i> ${data.weather.windsnelheid} km/u`;

  // Update forecast
  const forecastContainer = document.getElementById("forecastContainer");
  forecastContainer.innerHTML = data.forecast
    .map(
      (day) => `
        <div class="col">
            <div class="forecast-card text-center">
                <div class="forecast-date">${day.datum}</div>
                <img src="http://openweathermap.org/img/wn/${day.icon}@2x.png" 
                     class="weather-icon" alt="weer icoon">
                <div class="forecast-temp">${day.temp}°C</div>
                <div class="forecast-desc">${day.beschrijving}</div>
            </div>
        </div>
    `
    )
    .join("");

  // Update grafieken
  createCharts(data);

  // Update map location
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${city}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.length > 0) {
        const lat = parseFloat(data[0].lat);
        const lon = parseFloat(data[0].lon);
        map.setView([lat, lon], 12);
        if (currentMarker) {
          map.removeLayer(currentMarker);
        }
        currentMarker = L.marker([lat, lon]).addTo(map);
        map.invalidateSize();
      }
    });
}

// Load default city on page load
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    initMap();
    loadWeather("Amsterdam");
  }, 100);
});
