async function apiErrorMessage(response) {
    let data = null;

    try {
        data = await response.clone().json();
    } catch (_error) {
        // The response may not contain JSON.
    }

    if (data && data.error && data.error.message) {
        return data.error.message;
    }

    if (response.status === 404) {
        return "Requirement not found. Check the requirement id and try again.";
    }

    if (response.status === 409) {
        return "This action is not allowed for the requirement's current status.";
    }

    if (response.status === 400 || response.status === 422) {
        return "The request is incomplete or invalid. Check the entered data and try again.";
    }

    return `Request failed with status ${response.status}.`;
}

const API_BASE_URL = "http://127.0.0.1:8000";

async function apiPost(path, body) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    if (!response.ok) {
        throw new Error(await apiErrorMessage(response));
    }
    return response.json();
}

async function apiGet(path) {
    const response = await fetch(`${API_BASE_URL}${path}`);
    if (!response.ok) {
        throw new Error(await apiErrorMessage(response));
    }
    return response.json();
}
