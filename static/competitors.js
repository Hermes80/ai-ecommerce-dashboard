function loadCompetitors() {
    const keyword = document.getElementById("comp-keyword").value.trim();
    if (!keyword) return;

    fetch("/api/competitors?keyword=" + encodeURIComponent(keyword))
        .then(res => res.json())
        .then(data => renderCompetitors(data));
}

function renderCompetitors(data) {
    const container = document.getElementById("competitor-results");

    if (!data || !data.items || data.items.length === 0) {
        container.innerHTML = "<p>No competitors found.</p>";
        return;
    }

    let html = "";

    data.items.forEach(c => {
        html += `
        <div class="card mb-2">
          <div class="card-body">
            <h5 class="card-title">${c.title}</h5>
            <p class="card-text">
              Price: $${c.price.toFixed(2)}
            </p>
            <a href="${c.url}" target="_blank" class="btn btn-sm btn-outline-primary">View Listing</a>
          </div>
        </div>
        `;
    });

    container.innerHTML = html;
}
