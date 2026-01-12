const API = "";
const token = localStorage.getItem("token");

if (!token) window.location.href = "/static/index.html";

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/static/index.html";
}

async function fetchNotes() {
  const query = document.getElementById("search")?.value || "";

  const url = query
    ? `/notes/?title=${encodeURIComponent(query)}`
    : `/notes/`;

  const res = await fetch(url, {
    headers: { Authorization: "Bearer " + token }
  });

  if (!res.ok) {
    console.error("Failed to fetch notes");
    return;
  }

  const notes = await res.json();
  const list = document.getElementById("notes");
  list.innerHTML = "";

  if (notes.length === 0) {
    const li = document.createElement("li");
    li.innerText = "No notes found.";
    list.appendChild(li);
    return;
  }

  notes.forEach(n => {
    const li = document.createElement("li");
    li.innerHTML = `<a href="note.html?id=${n.id}">${n.title}</a>`;
    list.appendChild(li);
  });
}

async function createNote() {
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;

  await fetch(API + "/notes/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    },
    body: JSON.stringify({ title, content })
  });

  fetchNotes();
}

fetchNotes();

document.addEventListener("DOMContentLoaded", () => {
  const icon = document.querySelector(".search-icon");
  const input = document.querySelector(".search-input");

  if (icon && input) {
    icon.addEventListener("click", () => input.focus());
  }
});
