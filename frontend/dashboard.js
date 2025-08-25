async function loadIdeas() {
  let token = localStorage.getItem("token");
  let res = await fetch("http://backend:8000/ideas", {
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
