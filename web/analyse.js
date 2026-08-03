const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("analyse-form");
const requirementIdInput = document.getElementById("requirement-id");
const analyseButton = document.getElementById("analyse-button");
const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");
const resultSection = document.getElementById("result");
const resultQuality = document.getElementById("result-quality");
const resultIssues = document.getElementById("result-issues");
const resultStatus = document.getElementById("result-status");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

function renderIssues(issues) {
    resultIssues.innerHTML = "";
    if (!issues || issues.length === 0) {
        const p = document.createElement("p");
        p.className = "panel-description";
        p.textContent = "No issues found.";
        resultIssues.appendChild(p);
        return;
    }
    const list = document.createElement("ul");
    issues.forEach((issue) => {
        const item = document.createElement("li");
        item.textContent = issue;
        list.appendChild(item);
    });
    resultIssues.appendChild(list);
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const requirementId = requirementIdInput.value.trim();
    if (!requirementId) {
        return;
    }

    analyseButton.disabled = true;
    resultSection.hidden = true;
    setStamp("pending", "Analysing…");

    try {
        const response = await fetch(
            `${API_BASE_URL}/requirements/${encodeURIComponent(requirementId)}/analyse`,
            { method: "POST" }
        );
        const data = await response.json();

        if (!response.ok) {
            const message = data && data.error ? data.error.message : "Request failed.";
            setStamp("error", message);
            return;
        }

        setStamp("ok", "Analysis complete");
        resultQuality.textContent = `Quality indication: ${data.analysis.quality_indication}`;
        renderIssues(data.analysis.issues);
        resultStatus.textContent = `Requirement status is now: ${data.status}`;
        resultSection.hidden = false;
    } catch (error) {
        setStamp("error", "Could not reach the backend");
        console.error(error);
    } finally {
        analyseButton.disabled = false;
    }
});
