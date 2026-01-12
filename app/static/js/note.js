let versionsCache = [];

const API = "";
const token = localStorage.getItem("token");
const params = new URLSearchParams(window.location.search);
const noteId = params.get("id");

if (!token || !noteId) {
  window.location.href = "/static/index.html";
}

/* Navigation */
function back() {
  window.location.href = "/static/notes.html";
}

/* Init */
document.addEventListener("DOMContentLoaded", async () => {
  await loadNote();
  await loadVersions();
});

/* Load Note */
async function loadNote() {
  const res = await fetch(API + `/notes/${noteId}`, {
    headers: { Authorization: "Bearer " + token }
  });

  if (!res.ok) return;

  const note = await res.json();

  document.getElementById("note-title").value = note.title ?? "";
  document.getElementById("note-content").value = note.content ?? "";
  document.getElementById("version-info").innerHTML = "";
}

/* Update Note */
async function updateNote() {
  const title = document.getElementById("note-title").value;
  const content = document.getElementById("note-content").value;

  const res = await fetch(API + `/notes/${noteId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    },
    body: JSON.stringify({ title, content })
  });

  if (!res.ok) return;

  await loadNote();
  await loadVersions();
}

/* Load Versions */
async function loadVersions() {
  const res = await fetch(API + `/notes/${noteId}/versions`, {
    headers: { Authorization: "Bearer " + token }
  });

  if (!res.ok) return;

  versionsCache = await res.json();

  const list = document.getElementById("versions");
  list.innerHTML = "";

  if (versionsCache.length === 0) {
    list.innerHTML = "<li>No versions available</li>";
    return;
  }

  const latestVersionNumber = versionsCache[0].version_number;

  versionsCache.forEach(v => {
    const isLatest = v.version_number === latestVersionNumber;

    const li = document.createElement("li");
    li.classList.add("version-card");

    li.innerHTML = `
      <strong>Version ${v.version_number}</strong><br/>
      <em>${v.title_snapshot ?? ""}</em><br/>

      <button onclick="togglePreview(${v.version_number}, this)">
        Preview
      </button>

      <button onclick="restore(${v.version_number})">
        Restore
      </button>

      <button 
        onclick="deleteVersion(${v.version_number})"
        ${isLatest ? "disabled title='Cannot delete latest version'" : ""}
      >
        Delete
      </button>

      <!-- 👇 PREVIEW CONTAINER (REQUIRED) -->
      <div class="version-preview"></div>
    `;

    list.appendChild(li);
  });
}

/* Preview Version */
function togglePreview(versionNumber, button) {
  const v = versionsCache.find(x => x.version_number === versionNumber);
  if (!v) return;

  const card = button.closest(".version-card");
  const previewBox = card.querySelector(".version-preview");

  document.querySelectorAll(".version-preview.open").forEach(p => {
    if (p !== previewBox) {
      p.classList.remove("open");
      p.innerHTML = "";
      p.closest(".version-card")
        .querySelector("button")
        .innerText = "Preview";
    }
  });

  if (previewBox.classList.contains("open")) {
    previewBox.classList.remove("open");
    previewBox.innerHTML = "";
    button.innerText = "Preview";
    return;
  }

  const date = new Date(v.created_at);

  previewBox.innerHTML = `
    <div class="preview-content">
      <p><strong>Title:</strong> ${v.title_snapshot ?? ""}</p>

      <p><strong>Content:</strong></p>
      <div class="preview-text"></div>

      <p class="preview-meta">
        Created: ${date.toLocaleString()}
      </p>
    </div>
  `;

  const previewText = previewBox.querySelector(".preview-text");
  previewText.textContent = (v.content_snapshot ?? "")
    .replace(/\r\n/g, "\n")
    .trim();


  previewBox.classList.add("open");
  button.innerText = "Hide";
}

/* Restore Version (CREATES NEW) */
async function restore(versionNumber) {
  const res = await fetch(
    API + `/notes/${noteId}/versions/${versionNumber}/restore`,
    {
      method: "POST",
      headers: { Authorization: "Bearer " + token }
    }
  );

  if (!res.ok) return;

  await loadNote();
  await loadVersions();
}

async function deleteVersion(versionNumber) {
  const ok = confirm(
    `Delete version ${versionNumber}? This cannot be undone.`
  );

  if (!ok) return;

  const res = await fetch(
    API + `/notes/${noteId}/versions/${versionNumber}`,
    {
      method: "DELETE",
      headers: { Authorization: "Bearer " + token }
    }
  );

  if (!res.ok) {
    const err = await res.json();
    alert(err.detail || "Failed to delete version");
    return;
  }

  await loadVersions();
}

function highlightDiff(oldText, newText) {
  if (!oldText) return newText;

  const oldWords = oldText.split(" ");
  const newWords = newText.split(" ");

  return newWords
    .map(word =>
      oldWords.includes(word)
        ? word
        : `<span class="diff-added">${word}</span>`
    )
    .join(" ");
}
