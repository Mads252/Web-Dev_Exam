// Simple HTML escaping helper to avoid XSS when rendering user-controlled strings.
function escapeHtml(str) {
  if (typeof str !== "string") return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Generic helper to send a form with fetch and delegate the response
// to a callback. This keeps the search logic reusable and testable.
function server(url, method, data_source_selector, function_after_fetch) {
  const form = document.querySelector(data_source_selector);
  if (!form) return;

  const formData = new FormData(form);

  fetch(url, {
    method: method,
    body: formData
  })
    .then(res => res.text())
    .then(data => {
      function_after_fetch(data);
    })
    .catch(err => {
      console.error("Server error", err);
    });
}

// Debounced search trigger: validates input, clears results on empty,
// and only calls the server when there is an actual query.
function get_search_results(url, method, data_source_selector, function_after_fetch) {
  const txt_search_for = document.querySelector("#txt_search_for");
  const box = document.querySelector("#search_results");

  if (!txt_search_for || !box) return false;

  if (txt_search_for.value.trim() === "") {
    box.innerHTML = "";
    box.classList.add("d-none");
    return false;
  }

  server(url, method, data_source_selector, function_after_fetch);
}

// Parses JSON from the backend and renders the search result dropdown.
// Uses escapeHtml to protect against XSS when showing usernames/display names.
function parse_search_results(data_from_server) {
  let data;
  try {
    data = JSON.parse(data_from_server);
  } catch (e) {
    console.error("Could not parse JSON", e, data_from_server);
    return;
  }

  const box = document.querySelector("#search_results");
  if (!box) return;

  const noResultsText = box.dataset.noResultsText || "No users found";

  if (!data || data.length === 0) {
    box.innerHTML = `<div class="search-result search-result--empty">${escapeHtml(noResultsText)}</div>`;
    box.classList.remove("d-none");
    return;
  }

  let users_html = "";
  data.forEach(user => {
    const avatar_path = user.avatar_filename
      ? `/static/uploads/avatars/${encodeURIComponent(user.avatar_filename)}`
      : "/static/images/unknown.jpg";

    const displayName = escapeHtml(user.display_name || user.username);
    const username = escapeHtml(user.username);
    const profileUrl = `/profile/${encodeURIComponent(user.username)}`;

    users_html += `
      <button
        type="button"
        class="search-result"
        onclick="window.location.href='${profileUrl}'"
      >
        <img
          src="${avatar_path}"
          class="search-result__avatar"
          alt="${username} avatar"
        >
        <div class="search-result__info">
          <span class="search-result__name">${displayName}</span>
          <span class="search-result__username">@${username}</span>
        </div>
      </button>
    `;
  });

  box.innerHTML = users_html;
  box.classList.remove("d-none");
}

document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector("#txt_search_for");
  const box = document.querySelector("#search_results");
  if (!input || !box) return;

  let searchTimeout;

  // Debounce user input so we don't spam the server on every keystroke.
  input.addEventListener("input", function () {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(function () {
      get_search_results(
        "/api/search-users",
        "POST",
        "#frm_search",
        parse_search_results
      );
    }, 250);
  });

  // Hide the dropdown when clicking outside of it or the input.
  document.addEventListener("click", function (evt) {
    if (!box) return;
    if (!box.contains(evt.target) && evt.target !== input) {
      box.innerHTML = "";
      box.classList.add("d-none");
    }
  });

  // Allow closing the dropdown with Escape for better UX/accessibility.
  input.addEventListener("keydown", function (evt) {
    if (evt.key === "Escape") {
      box.innerHTML = "";
      box.classList.add("d-none");
      input.blur();
    }
  });
});
