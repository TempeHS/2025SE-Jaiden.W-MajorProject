document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".delete-event-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm("Are you sure you want to delete this event?")) {
        e.preventDefault();
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".leave-team-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm("Are you sure you want to leave this team?")) {
        e.preventDefault();
      }
    });
  });
});
