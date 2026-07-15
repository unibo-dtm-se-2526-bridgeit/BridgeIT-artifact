const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

document.getElementById("check-health").addEventListener("click", async () => {
    setStamp("pending", "Checking...");

    try {
        const data = await apiGet("/health");
        setStamp("ok", `Backend: ${data.status}`);
    } catch (error) {
        setStamp("error", "Could not reach the backend");
        console.error(error);
    }
});