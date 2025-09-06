
const API_KEY = '3e72870c74dc724fe5dc03f3f1a38ccb';
const city = 'Mexico City,MX';

const ctxWeather = document.getElementById('weatherChart').getContext('2d');
const weatherChart = new Chart(ctxWeather, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: `Temperatura en ${city} (°C)`,
            data: [],
            backgroundColor: 'rgba(63, 43, 245, 0.49)',
            borderColor: 'rgb(219, 236, 241)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: false },
            x: { }
        }
    }
});

const ctxAccidents = document.getElementById('accidentChart').getContext('2d');
const accidentChart = new Chart(ctxAccidents, {
    type: 'bar',
    data: {
        labels: [], datasets: [{
            label: "Accidentes por Año",
            data: [],
            backgroundColor: 'rgba(241, 25, 108, 0.5)',
            borderColor: 'rgb(250, 248, 248)',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true },
            x: { }
        }
    }
});

async function fetchWeather() {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`);
        const data = await response.json();
        return data.main.temp;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

async function updateWeatherChart() {
    const temperature = await fetchWeather();
    const time = new Date().toLocaleTimeString();
    if (temperature !== null) {
        weatherChart.data.labels.push(time);
        weatherChart.data.datasets[0].data.push(temperature);
        if (weatherChart.data.labels.length > 10) {
            weatherChart.data.labels.shift();
            weatherChart.data.datasets[0].data.shift();
        }
        weatherChart.update();
    }
}

function updateAccidentChart() {
    const currentYear = new Date().getFullYear();
    const years = [];
    const accidents = [];

    for (let i = 0; i < 10; i++) { 
        years.push(currentYear - i);
        accidents.push(Math.floor(Math.random() * 5000) + 1000);
    }

    accidentChart.data.labels = years.reverse(); 
    accidentChart.data.datasets[0].data = accidents.reverse();
    accidentChart.update();
}

updateWeatherChart();
setInterval(updateWeatherChart, 10000);
setInterval(updateAccidentChart, 15000);

function showGraph(type) {
    document.getElementById('weatherChart').style.display = type === 'weather' ? 'block' : 'none';
    document.getElementById('accidentChart').style.display = type === 'accidents' ? 'block' : 'none';
    document.getElementById('graph-title').innerText = type === 'weather' ? 'SKYNET - Temperatura en Tiempo Real' : 'SKYNET - Accidentes en Tiempo Real';
}
