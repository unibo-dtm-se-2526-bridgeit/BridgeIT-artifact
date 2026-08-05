const API_BASE_URL = "http://127.0.0.1:8000";

// Info disclosure (KISS: description hidden by default, one click to
// reveal instead of always taking up space on the page).
const infoToggle = document.getElementById("info-toggle");
const infoPanel = document.getElementById("info-panel");
infoToggle.addEventListener("click", () => {
    const isOpen = infoPanel.classList.toggle("is-open");
    infoToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
});

const form = document.getElementById("validate-form");
const requirementIdInput = document.getElementById("requirement-id");
const modifiedTextField = document.getElementById("modified-text-field");
const modifiedTextInput = document.getElementById("modified-text");
const stampElement = document.getElementById("stamp");
const stampValueElement = document.getElementById("stamp-value");
const resultSection = document.getElementById("result");
const resultStatus = document.getElementById("result-status");

function setStamp(state, label) {
    stampElement.className = `stamp stamp--${state}`;
    stampValueElement.textContent = label;
}

// Show the "edited text" field only once the user picks "Edit" -- keeps
// the form simple for the two decisions that don't need it.
form.querySelectorAll("button[data-decision]").forEach((button) => {
    button.addEventListener("click", () => {
        modifiedTextField.hidden = button.dataset.decision !== "edit";
    });
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitter = event.submitter;
    const decision = submitter ? submitter.dataset.decision : null;
    const requirementId = requirementIdInput.value.trim();
    if (!requirementId || !decision) {
        return;
    }

    const body = { decision };
    if (decision === "edit") {
        body.modified_text = modifiedTextInput.value.trim();
    }

    form.querySelectorAll("button[data-decision]").forEach((button) => {
        button.disabled = true;
    });
    resultSection.hidden = true;
    setStamp("pending", "Recording decision…");

    try {
        const response = await fetch(
            `${API_BASE_URL}/requirements/${encodeURIComponent(requirementId)}/validate`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            }
        );
        const data = await response.json();

        if (!response.ok) {
            const message = data && data.error ? data.error.message : "Request failed.";
            setStamp("error", message);
            return;
        }

        setStamp("ok", `Decision recorded: ${decision}`);
        resultStatus.textContent = `Requirement status is now: ${data.status}`;
        resultSection.hidden = false;
    } catch (error) {
        setStamp("error", "Could not reach the backend");
        console.error(error);
    } finally {
        form.querySelectorAll("button[data-decision]").forEach((button) => {
            button.disabled = false;
        });
    }
});
