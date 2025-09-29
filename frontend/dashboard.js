async function loadIdeas() {
  const API_BASE = "/api";
  let token = localStorage.getItem("token");
  let res = await fetch(`${API_BASE}/ideas`, {
    headers: {"Authorization": "Bearer " + token}
  });
  let data = await res.json();
  let ul = document.getElementById("ideas");
  ul.innerHTML = "";
  data.forEach(idea => {
    let li = document.createElement("li");
    li.innerText = idea.short_desc + " (" + idea.status + ")";
    ul.appendChild(li);
  });
}
