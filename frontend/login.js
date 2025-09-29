async function login() {
  const API_BASE = "/api";
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password})
  });
  let data = await res.json();
  if (data.access_token) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("username", username);
    console.log("Login successful, token stored.");
    window.location.href = "dashboard.html";
  } else {
    document.getElementById("msg").innerText = data.detail;
  }
}
