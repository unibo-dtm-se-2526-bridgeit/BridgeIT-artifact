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

// "Edit" only reveals the edited-text field: the decision is sent with the
// separate "Save edited text" button, so no request is made with an empty
// text. Approve/Reject hide the field again.
const editToggle = document.getElementById("edit-toggle");
editToggle.addEventListener("click", () => {
    modifiedTextField.hidden = false;
    editToggle.setAttribute("aria-expanded", "true");
    modifiedTextInput.focus();
});
form.querySelectorAll("button[data-decision]").forEach((button) => {
    button.addEventListener("click", () => {
        if (button.dataset.decision !== "edit") {
            modifiedTextField.hidden = true;
            editToggle.setAttribute("aria-expanded", "false");
        }
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
        if (!body.modified_text) {
            setStamp("error", "Write the edited text before saving.");
            modifiedTextInput.focus();
            return;
        }
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
            const message =
                response.status === 404
                    ? "Requirement not found. Check the requirement id and try again."
                    : response.status === 409
                      ? "This validation decision is not allowed for the requirement's current status."
                      : response.status === 400 || response.status === 422
                        ? "The request is incomplete or invalid. Check the entered data and try again."
                        : data && data.error && data.error.message
                          ? data.error.message
                          : "Request failed. Please try again.";
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
