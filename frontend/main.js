import { initCanvas } from "./display.js";
import { initDefaultVaules, initInterface } from "./ui.js";

console.log("MAIN");

initInterface();
initCanvas();
initDefaultVaules();

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document
        .querySelectorAll(".tab")
        .forEach((t) => t.classList.remove("active"));

      document
        .querySelectorAll(".tab-content")
        .forEach((c) => c.classList.remove("active"));

      tab.classList.add("active");

      const target = tab.dataset.tab;
      const panel = document.getElementById(target);

      if (panel) panel.classList.add("active");
    });
  });
});
