// Pointer-following spotlight on the dark background. Disabled on touch
// devices (no meaningful pointer) and harmless if the element is absent
// on a given page.
const spotlight = document.getElementById("spotlight");

if (spotlight && window.matchMedia("(pointer: fine)").matches) {
    window.addEventListener("pointermove", (event) => {
        document.body.classList.add("pointer-active");
        const xPct = (event.clientX / window.innerWidth) * 100;
        const yPct = (event.clientY / window.innerHeight) * 100;
        spotlight.style.setProperty("--mx", `${xPct}%`);
        spotlight.style.setProperty("--my", `${yPct}%`);
    });
    window.addEventListener("pointerleave", () => {
        document.body.classList.remove("pointer-active");
    });
}