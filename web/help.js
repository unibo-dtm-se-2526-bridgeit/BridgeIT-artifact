// FAQ accordion: each question toggles its own answer independently.
document.querySelectorAll(".faq-question").forEach((button) => {
    const answerId = button.getAttribute("aria-controls");
    const answer = document.getElementById(answerId);

    button.addEventListener("click", () => {
        const isOpen = answer.classList.toggle("is-open");
        button.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
});
