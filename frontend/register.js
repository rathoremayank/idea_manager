async function register() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let res = await fetch("http://backend:8000/register", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password})
  });
  let data = await res.json();
  document.getElementById("msg").innerText = data.msg || data.detail;
  if (data.msg === "User registered") {
    setTimeout(() => {
      window.location.href = "login.html"; // redirect to login
    }, 1000);
  }
}
