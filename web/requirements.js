const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");
const resultElement = document.getElementById("result");
const resultTextElement = document.getElementById("result-text");
const resultIdElement = document.getElementById("result-id");
const idInput = document.getElementById("requirement-id");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

async function loadRequirement(id) {
    if (!id) {
        return;
    }
    resultElement.hidden = false;
    resultTextElement.textContent = "Loading...";
    setStamp("pending", "Looking up...");

    try {
        const requirement = await apiGet(`/requirements/${id}`);
        resultTextElement.textContent = requirement.text;
        resultIdElement.textContent = requirement.id;
        setStamp("ok", requirement.status);
    } catch (error) {
        resultTextElement.textContent = "Requirement not found.";
        resultIdElement.textContent = id;
        setStamp("error", "Not found");
        console.error(error);
    }
}

document.getElementById("lookup-form").addEventListener("submit", (event) => {
    event.preventDefault();
    loadRequirement(idInput.value.trim());
});

// If the page was opened with ?id=..., look it up automatically
// (this is how create.html redirects here after a successful submit).
const params = new URLSearchParams(window.location.search);
const idFromUrl = params.get("id");
if (idFromUrl) {
    idInput.value = idFromUrl;
    loadRequirement(idFromUrl);
}