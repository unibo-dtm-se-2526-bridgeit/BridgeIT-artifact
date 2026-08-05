const API_BASE_URL = "http://127.0.0.1:8000";

// Info disclosure (KISS: description hidden by default, one click to
// reveal instead of always taking up space on the page).
const infoToggle = document.getElementById("info-toggle");
const infoPanel = document.getElementById("info-panel");
infoToggle.addEventListener("click", () => {
    const isOpen = infoPanel.classList.toggle("is-open");
    infoToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
});

const form = document.getElementById("analyse-form");
const requirementIdInput = document.getElementById("requirement-id");
const analyseButton = document.getElementById("analyse-button");
const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");
const resultSection = document.getElementById("result");
const resultLogo = document.getElementById("result-logo");
const resultHeading = document.getElementById("result-heading");
const resultQuality = document.getElementById("result-quality");
const resultIssues = document.getElementById("result-issues");
const resultStatus = document.getElementById("result-status");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

// The logo itself is the signal: whole bridge (deck connected) when the
// requirement is ready, an unfinished bridge (no deck, no wordmark) when
// it still needs work -- never a fabricated score, since
// quality_indication only ever has these two real values.
function renderResult(qualityIndication, issues) {
    const isReady = qualityIndication === "ready_for_validation";

    resultLogo.src = isReady ? "assets/logo.png" : "assets/logo-incomplete.png";
    resultLogo.alt = isReady ? "BridgeIT — complete bridge" : "BridgeIT — unfinished bridge";

    if (isReady) {
        resultHeading.textContent = "This requirement is ready for validation.";
        resultQuality.textContent =
            "Gemini did not find anything blocking — a Business Analyst can now review it in the Validate page.";
        resultIssues.innerHTML = "";
        return;
    }

    resultHeading.textContent = "This requirement still needs clarification.";
    resultQuality.textContent =
        "The bridge isn't finished yet — here's what's missing, and why it matters:";
    resultIssues.innerHTML = "";
    const list = document.createElement("ul");
    (issues || []).forEach((issue) => {
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
        renderResult(data.analysis.quality_indication, data.analysis.issues);
        resultStatus.textContent = `Requirement status is now: ${data.status}`;
        resultSection.hidden = false;
    } catch (error) {
        setStamp("error", "Could not reach the backend");
        console.error(error);
    } finally {
        analyseButton.disabled = false;
    }
});
