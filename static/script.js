const form = document.getElementById("predictionForm");
const gaugeFill = document.getElementById("gauge-fill");
const gaugeText = document.getElementById("gauge-text");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const wind_speed = parseFloat(document.querySelector('input[name="wind_speed"]').value);
    const theoretical_power = parseFloat(document.querySelector('input[name="theoretical_power"]').value);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ wind_speed, theoretical_power })
        });

        const result = await response.json();
        if (!result.prediction && result.prediction !== 0) throw new Error("No prediction");

        const prediction = result.prediction;
        const percentage = Math.min((prediction / theoretical_power) * 100, 100);
        gaugeFill.setAttribute("stroke-dasharray", `${percentage}, 100`);

        if (percentage < 40) gaugeFill.setAttribute("stroke", "#27ae60");
        else if (percentage < 70) gaugeFill.setAttribute("stroke", "#f1c40f");
        else gaugeFill.setAttribute("stroke", "#e74c3c");

        gaugeText.textContent = `${prediction} kW`;
    } catch (err) {
        gaugeText.textContent = "Error!";
        console.error(err);
        console.log("Prediction:", prediction, "Percentage:", percentage);

    }
});

// OpenWeather autofill (replace YOUR_API_KEY with real key)
async function getWindSpeed() {
    const apiKey = "YOUR_API_KEY";
    const city = "Amaravati";
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        document.querySelector('input[name="wind_speed"]').value = data.wind.speed;
    } catch(err) {
        console.error("Weather API error:", err);
    }
}

getWindSpeed();
