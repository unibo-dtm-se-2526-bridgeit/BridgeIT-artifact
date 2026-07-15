const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

document.getElementById("create-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = document.getElementById("requirement-text").value.trim();
    if (!text) {
        return;
    }

    setStamp("pending", "Submitting...");

    try {
        const requirement = await apiPost("/requirements", { text });
        setStamp("ok", `Created: ${requirement.status}`);
        window.location.href = `requirements.html?id=${requirement.id}`;
    } catch (error) {
        setStamp("error", "Could not submit the requirement");
        console.error(error);
    }
});