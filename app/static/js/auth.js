const API = "";

function saveToken(token) {
  localStorage.setItem("token", token);
  window.location.href = "/static/notes.html";
}

async function login() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    document.getElementById("error").innerText =
      "Email and password are required";
    return;
  }

  const res = await fetch(API + "/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({
      username: email,
      password: password
    })
  });

  if (!res.ok) {
    const err = await res.json();
    document.getElementById("error").innerText =
      err.detail || "Login failed";
    return;
  }

  const data = await res.json();
  saveToken(data.access_token);
}


async function register() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    document.getElementById("error").innerText =
      "Email and password are required";
    return;
  }

  const res = await fetch(API + "/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (!res.ok) {
    const err = await res.json();
    document.getElementById("error").innerText =
      err.detail || "Registration failed";
    return;
  }
  
  login();
}
