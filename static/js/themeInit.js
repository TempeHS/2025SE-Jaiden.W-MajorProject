(function () {
  const theme = localStorage.getItem("bsTheme") || "light";
  document.documentElement.setAttribute("data-bs-theme", theme);

  if (localStorage.getItem("largeFont") === "on") {
    document.documentElement.classList.add("large-font");
  }
})();
