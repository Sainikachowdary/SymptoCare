async function sendOTP() {
  const phone = document.getElementById("phone").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/auth/send-otp", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        phone: phone,
      }),
    });

    const data = await response.json();

    localStorage.setItem("userPhone", phone);

    alert("OTP Sent");

    window.location.href = "./otp.html";
  } catch (error) {
    console.log(error);

    alert("Error Sending OTP");
  }
}

async function verifyOTP() {
  const phone = localStorage.getItem("userPhone");

  const otp = document.getElementById("otp").value;

  const response = await fetch("http://127.0.0.1:5000/auth/verify-otp", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      phone: phone,
      otp: otp,
    }),
  });

  const data = await response.json();

  if (data.success) {
    alert("Login Successful");

    window.location.href = "./profile.html";
  } else {
    alert("Wrong OTP");
  }
}
