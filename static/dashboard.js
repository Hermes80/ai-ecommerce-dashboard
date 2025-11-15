let salesChart, orderChart;

async function refreshData() {
    const res = await fetch("/api/data");
    const data = await res.json();

    renderTopStats(data);
    renderChannels(data);
    renderInventory(data);
    renderProfit(data);
    renderCharts(data);
    renderAiLog(data.ai_command_log || []);
}

// ------- TOP STATS (summary cards) -------
function renderTopStats(data) {
    const el = document.getElementById("top-stats");
    el.innerHTML = `
        <div class="col-md-3">
          <div class="card stat-card">
            <h5>$${data.total_sales_today.toFixed(2)}</h5>
            <p>Sales Today</p>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card">
            <h5>${data.orders_today}</h5>
            <p>Orders Today</p>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card">
            <h5>${data.active_listings}</h5>
            <p>Active Listings</p>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card">
            <h5>${data.ai_status}</h5>
            <p>AI Status</p>
            <small class="text-muted">Last sync: ${data.last_sync}</small>
          </div>
        </div>
    `;
}

// ------- CHANNEL CARDS (eBay/Shopify/Amazon) -------
function renderChannels(data) {
    const el = document.getElementById("channels-row");
    const channels = data.channel_stats || {};
    el.innerHTML = "";

    Object.keys(channels).forEach(name => {
        const ch = channels[name];
        el.innerHTML += `
          <div class="col-md-4">
            <div class="card stat-card">
              <h5 class="text-capitalize">${name}</h5>
              <p>Sales Today: $${ch.sales_today.toFixed(2)}</p>
              <p>Orders Today: ${ch.orders_today}</p>
              <p>Active Listings: ${ch.active_listings}</p>
            </div>
          </div>
        `;
    });
}

// ------- INVENTORY TABLE -------
function renderInventory(data) {
    const body = document.getElementById("inventory-body");
    const items = data.inventory || [];
    body.innerHTML = "";

    items.forEach(item => {
        const lowStockClass = item.qty === 0 ? 'table-danger' : (item.qty <= 2 ? 'table-warning' : '');
        body.innerHTML += `
          <tr class="${lowStockClass}">
            <td>${item.sku}</td>
            <td>${item.title}</td>
            <td>${item.channel}</td>
            <td>${item.qty}</td>
            <td>$${item.price.toFixed(2)}</td>
          </tr>
        `;
    });
}

// ------- PROFIT CARDS -------
function renderProfit(data) {
    const el = document.getElementById("profit-cards");
    const p = data.profit_stats || { revenue_today: 0, fees_today: 0, profit_today: 0, margin_percent: 0 };

    el.innerHTML = `
        <div class="col-md-3">
          <div class="card stat-card">
            <h5>$${p.revenue_today.toFixed(2)}</h5>
            <p>Revenue Today</p>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card">
            <h5>$${p.fees_today.toFixed(2)}</h5>
            <p>Fees Today</p>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card">
            <h5>$${p.profit_today.toFixed(2)}</h5>
            <p>Profit Today</p>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card stat-card">
            <h5>${p.margin_percent}%</h5>
            <p>Profit Margin</p>
          </div>
        </div>
    `;
}

// ------- CHARTS -------
function renderCharts(data) {
    const salesCtx = document.getElementById("salesChart");
    const orderCtx = document.getElementById("orderChart");

    if (salesChart) salesChart.destroy();
    if (orderChart) orderChart.destroy();

    salesChart = new Chart(salesCtx, {
        type: 'line',
        data: {
            labels: ["1", "2", "3", "4", "5", "6", "Today"],
            datasets: [{
                label: "Sales",
                data: data.sales_chart || []
            }]
        }
    });

    orderChart = new Chart(orderCtx, {
        type: 'bar',
        data: {
            labels: ["1", "2", "3", "4", "5", "6", "Today"],
            datasets: [{
                label: "Orders",
                data: data.order_chart || []
            }]
        }
    });
}

// ------- AI CONSOLE -------
async function sendAiCommand() {
    const input = document.getElementById("ai-command-input");
    const command = input.value.trim();
    if (!command) return;

    const res = await fetch("/api/ai/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command })
    });

    const result = await res.json();
    renderAiLog(result.log || []);
    input.value = "";
}

function renderAiLog(log) {
    const el = document.getElementById("ai-log");
    el.innerHTML = "";
    log.slice().reverse().forEach(entry => {
        el.innerHTML += `
          <li class="list-group-item">
            <strong>${entry.timestamp}</strong><br>
            ${entry.command}<br>
            <small class="text-muted">Status: ${entry.status}</small>
          </li>
        `;
    });
}

// Load data on page load
refreshData();
