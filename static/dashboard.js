let salesChart, orderChart;

async function refreshData() {
    const res = await fetch("/api/data");
    const data = await res.json();

    renderStats(data);
    renderCharts(data);
}

function renderStats(data) {
    document.getElementById("stats").innerHTML = `
        <div class="col-md-3">
          <div class="card stat-card"><h5>$${data.total_sales_today}</h5><p>Sales Today</p></div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card"><h5>${data.orders_today}</h5><p>Orders Today</p></div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card"><h5>${data.active_listings}</h5><p>Active Listings</p></div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card"><h5>${data.ai_status}</h5><p>AI Status</p></div>
        </div>
    `;
}

function renderCharts(data) {
    const salesCtx = document.getElementById("salesChart");
    const orderCtx = document.getElementById("orderChart");

    if (salesChart) salesChart.destroy();
    if (orderChart) orderChart.destroy();

    salesChart = new Chart(salesCtx, {
        type: 'line',
        data: {
            labels: ["1", "2", "3", "4", "5"],
            datasets: [{
                label: "Sales",
                data: data.sales_chart
            }]
        }
    });

    orderChart = new Chart(orderCtx, {
        type: 'bar',
        data: {
            labels: ["1", "2", "3", "4", "5"],
            datasets: [{
                label: "Orders",
                data: data.order_chart
            }]
        }
    });
}

// load data as soon as the page opens
refreshData();
