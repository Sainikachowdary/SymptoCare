document.addEventListener("DOMContentLoaded", () => {
  const symptomBtn = document.getElementById("symptomBtn");
  const historyBtn = document.getElementById("historyBtn");
  const logoutBtn = document.getElementById("logoutBtn");

  if (symptomBtn) {
    symptomBtn.onclick = () => {
      window.location.href = "./symptoChecker.html";
    };
  }

  if (historyBtn) {
    historyBtn.onclick = () => {
      window.location.href = "./history.html";
    };
  }

  if (logoutBtn) {
    logoutBtn.onclick = () => {
      localStorage.clear();

      window.location.href = "./login.html";
    };
  }
});
