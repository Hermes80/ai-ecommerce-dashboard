document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/portfolio")
        .then(res => res.json())
        .then(data => renderPortfolio(data))
        .catch(err => {
            console.error("Portfolio error:", err);
        });
});

function renderBucket(containerId, items, emptyMessage) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!items || !items.length) {
        container.innerHTML = `<p class="text-muted">${emptyMessage}</p>`;
        return;
    }

    let html = "";

    items.forEach(it => {
        html += `
        <div class="card mb-2">
          <div class="card-body">
            <h5 class="card-title">${it.title}</h5>
            <p class="card-text">
              Price: $${it.price.toFixed(2)}<br>
              Score: ${it.score}<br>
              Margin: ${it.margin_percent}%<br>
              Demand (orders): ${it.demand}<br>
              Competitors: ${it.competitors}<br>
              Estimated Profit: $${it.profit_estimate.toFixed(2)}<br>
              Tags: ${it.tags.join(", ")}
            </p>
          </div>
        </div>
        `;
    });

    container.innerHTML = html;
}

function renderExternal(containerId, items) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!items || !items.length) {
        container.innerHTML = `<p class="text-muted">No external opportunities detected yet.</p>`;
        return;
    }

    let html = "";

    items.forEach(it => {
        html += `
        <div class="card mb-2">
          <div class="card-body">
            <h5 class="card-title">${it.title}</h5>
            <p class="card-text">
              Price: $${it.price.toFixed(2)}<br>
              Note: ${it.note}
            </p>
            <a href="${it.url}" target="_blank" class="btn btn-sm btn-outline-primary">View on eBay</a>
          </div>
        </div>
        `;
    });

    container.innerHTML = html;
}

function renderPortfolio(data) {
    renderBucket("core-list", data.core, "No core winners yet. Give the AI time with real sales.");
    renderBucket("growth-list", data.growth, "No growth picks yet.");
    renderBucket("risky-list", data.risky, "No risky items identified yet.");
    renderExternal("external-list", data.external_opportunities);
}
