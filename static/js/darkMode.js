document.addEventListener("DOMContentLoaded", () => {
  const htmlElement = document.documentElement;
  const switchElement = document.getElementById("darkModeSwitch");

  // Set the default theme to dark if no setting is found in local storage
  const currentTheme = localStorage.getItem("bsTheme") || "light";
  htmlElement.setAttribute("data-bs-theme", currentTheme);

  if (switchElement) {
    switchElement.checked = currentTheme === "dark";

    switchElement.addEventListener("change", function () {
      if (this.checked) {
        htmlElement.setAttribute("data-bs-theme", "dark");
        localStorage.setItem("bsTheme", "dark");
      } else {
        htmlElement.setAttribute("data-bs-theme", "light");
        localStorage.setItem("bsTheme", "light");
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const htmlElement = document.documentElement;
  const fontSwitch = document.getElementById("largeFontSwitch");

  // Set initial state from localStorage
  if (localStorage.getItem("largeFont") === "on") {
    htmlElement.classList.add("large-font");
    if (fontSwitch) fontSwitch.checked = true;
  }

  if (fontSwitch) {
    fontSwitch.addEventListener("change", function () {
      if (this.checked) {
        htmlElement.classList.add("large-font");
        localStorage.setItem("largeFont", "on");
      } else {
        htmlElement.classList.remove("large-font");
        localStorage.setItem("largeFont", "off");
      }
    });
  }
});
