document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/suppliers")
        .then(res => res.json())
        .then(data => renderSuppliers(data));
});

function renderSuppliers(data) {
    const container = document.getElementById("supplier-results");

    if (!data || !data.results || data.results.length === 0) {
        container.innerHTML = "<p>No supplier recommendations yet. Run AI Engine or enable Auto Source.</p>";
        return;
    }

    let html = "";

    data.results.forEach(item => {
        html += `
        <div class="card mb-3">
            <div class="card-header"><strong>${item.category}</strong> — ${item.order_count} recent orders</div>
            <div class="card-body">
                <p>Suggested Supplier Searches:</p>
                <ul>
                    ${item.suppliers.map(s => `
                        <li>
                            <a href="${s.search_url}" target="_blank">
                                ${s.platform} ↗
                            </a>
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>
        `;
    });

    container.innerHTML = html;
}
