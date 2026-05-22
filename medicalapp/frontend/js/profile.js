document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("profileForm");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const profileData = {
      name: document.getElementById("name").value,

      birthday: document.getElementById("birthday").value,

      gender: document.getElementById("gender").value,

      age: document.getElementById("age").value,

      weight: document.getElementById("weight").value,

      height: document.getElementById("height").value,
    };

    localStorage.setItem("profile", JSON.stringify(profileData));

    alert("Profile Saved Successfully");

    window.location.href = "dashboard.html";
  });
});
