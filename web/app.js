const API_BASE_URL = "http://127.0.0.1:8000";

const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

document.getElementById("check-health").addEventListener("click", async () => {
    setStamp("pending", "Checking...");

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            throw new Error(`Backend responded with status ${response.status}`);
        }
        const data = await response.json();
        setStamp("ok", `Backend: ${data.status}`);
    } catch (error) {
        setStamp("error", "Could not reach the backend");
        console.error(error);
    }
});