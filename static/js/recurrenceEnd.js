document.addEventListener("DOMContentLoaded", function () {
  const recurrence = document.getElementById("recurrence");
  const recurrenceEndGroup = document.getElementById("recurrence_end_group");

  function toggleRecurrenceEnd() {
    if (recurrence.value === "none") {
      recurrenceEndGroup.style.display = "none";
      // Optionally clear the value
      recurrenceEndGroup.querySelector("input").value = "";
    } else {
      recurrenceEndGroup.style.display = "";
    }
  }

  recurrence.addEventListener("change", toggleRecurrenceEnd);
  toggleRecurrenceEnd(); // Initial call on page load
});
