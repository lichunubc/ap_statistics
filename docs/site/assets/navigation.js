/* Whole-book navigation only; no lesson data, analytics, or persistent state. */
(() => {
  "use strict";
  function initialize() {
    const sidebar = document.getElementById("quarto-sidebar");
    if (!sidebar || sidebar.dataset.courseNavigationReady === "true") return;
    sidebar.querySelectorAll(".sidebar-section").forEach(section => {
      const row = section.parentElement.querySelector(":scope > .sidebar-item-container");
      const oldToggle = row && row.querySelector(".sidebar-item-toggle");
      if (!oldToggle || !section.id) return;
      const link = row.querySelector(".sidebar-item-text");
      const title = (link ? link.textContent : "this unit").trim().replace(/\s+/g, " ");
      const unit = (title.match(/^Unit \d+/) || [title])[0];
      const button = document.createElement("button");
      button.type = "button";
      button.className = "sidebar-item-toggle course-unit-toggle";
      button.setAttribute("aria-controls", section.id);
      const arrow = document.createElement("span");
      arrow.className = "course-unit-chevron";
      arrow.setAttribute("aria-hidden", "true");
      arrow.textContent = "›";
      button.append(arrow);
      oldToggle.replaceWith(button);
      // The unit title remains a real link to its landing page. Only the button
      // controls the topic disclosure, so Bootstrap must not also toggle it.
      if (link) {
        link.removeAttribute("data-bs-toggle");
        link.removeAttribute("data-bs-target");
        link.removeAttribute("aria-expanded");
      }
      section.classList.remove("collapse", "collapsing", "show");
      section.classList.add("course-topic-list");
      section.removeAttribute("style");
      function setExpanded(expanded) {
        section.hidden = !expanded;
        button.setAttribute("aria-expanded", String(expanded));
        const label = `${expanded ? "Hide" : "Show"} topics for ${unit}`;
        button.setAttribute("aria-label", label);
        button.title = label;
      }
      setExpanded(false);
      button.addEventListener("click", () => setExpanded(section.hidden));
      // Native buttons supply Enter/Space activation without custom key handling.
    });
    sidebar.dataset.courseNavigationReady = "true";
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
