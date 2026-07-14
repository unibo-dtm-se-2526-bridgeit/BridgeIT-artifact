const API_BASE_URL = "http://127.0.0.1:8000";

document.getElementById("check-health").addEventListener("click", async () => {
    const resultElement = document.getElementById("health-result");
    resultElement.textContent = "Checking...";

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        resultElement.textContent = `Backend says: ${data.status}`;
    } catch (error) {
        resultElement.textContent = "Could not reach the backend.";
        console.error(error);
    }
});