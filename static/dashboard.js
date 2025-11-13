/**
 * US30 Trading Bot Dashboard - JavaScript
 * Real-time updates and interactions
 */

// Global state
const dashboardState = {
    priceHistory: [],
    updateInterval: 2000, // 2 seconds
    refreshTimer: null,
};

/**
 * Initialize dashboard
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    
    // Initial data fetch
    updateDashboard();
    
    // Set up periodic updates
    dashboardState.refreshTimer = setInterval(updateDashboard, dashboardState.updateInterval);
    
    // Update timestamp
    updateTimestamp();
    setInterval(updateTimestamp, 1000);
    
    console.log('Dashboard initialized');
});

/**
 * Update entire dashboard
 */
async function updateDashboard() {
    try {
        const response = await fetch('/api/dashboard');
        const data = await response.json();
        
        updatePrice(data);
        updateAccount(data);
        updatePositions(data);
        updateStrategies(data);
        updateStatistics(data);
        updateBotStatus(data);
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
        updateBotStatusError();
    }
}

/**
 * Update price display
 */
function updatePrice(data) {
    const priceEl = document.getElementById('currentPrice');
    const changeEl = document.getElementById('priceChange');
    
    if (priceEl && data.current_price) {
        priceEl.textContent = formatPrice(data.current_price);
        
        // Update price history for chart
        dashboardState.priceHistory.push(data.current_price);
        if (dashboardState.priceHistory.length > 100) {
            dashboardState.priceHistory.shift();
        }
    }
    
    if (changeEl) {
        const changePct = data.price_change_pct || 0;
        const change = data.price_change || 0;
        const sign = change >= 0 ? '+' : '';
        const display = `${sign}${change.toFixed(2)} (${sign}${changePct.toFixed(2)}%)`;
        
        changeEl.textContent = display;
        changeEl.className = 'price-change' + (changePct >= 0 ? '' : ' negative');
    }
    
    updatePriceChart();
}

/**
 * Update account information
 */
function updateAccount(data) {
    const balance = data.account_balance || 0;
    const equity = data.equity || 0;
    const freeMargin = data.free_margin || 0;
    const usedMargin = data.used_margin || 0;
    const marginLevel = data.margin_level || 0;
    
    setElementText('balance', formatCurrency(balance));
    setElementText('equity', formatCurrency(equity));
    setElementText('freeMargin', formatCurrency(freeMargin));
    setElementText('usedMargin', formatCurrency(usedMargin));
    setElementText('marginLevel', formatPercent(marginLevel));
}

/**
 * Update open positions
 */
function updatePositions(data) {
    const tickets = data.open_tickets || [];
    
    // Update count badge
    const countEl = document.querySelector('.count-badge');
    if (countEl) {
        countEl.textContent = tickets.length;
    }
    
    // Update positions list (cards)
    updatePositionsList(tickets);
    
    // Update positions table
    updatePositionsTable(tickets);
}

/**
 * Update positions list view
 */
function updatePositionsList(tickets) {
    const listEl = document.getElementById('positionsList');
    if (!listEl) return;
    
    if (tickets.length === 0) {
        listEl.innerHTML = '<div class="empty-state">No open positions</div>';
        return;
    }
    
    let html = '';
    tickets.forEach(ticket => {
        const isPositive = ticket.profit_loss >= 0;
        const plClass = isPositive ? 'positive' : 'negative';
        const typeClass = ticket.type === 'BUY' ? 'buy' : 'sell';
        
        html += `
            <div class="position-item">
                <span class="position-type ${typeClass}">${ticket.type}</span>
                <div class="position-info">
                    <div><strong>Ticket #${ticket.ticket}</strong></div>
                    <div>${ticket.symbol} | Vol: ${ticket.volume}</div>
                </div>
                <div class="position-pl ${plClass}">
                    ${formatCurrency(ticket.profit_loss)}
                    <br/>
                    (${formatPercent(ticket.profit_loss_pct)})
                </div>
            </div>
        `;
    });
    
    listEl.innerHTML = html;
}

/**
 * Update positions table
 */
function updatePositionsTable(tickets) {
    const tbody = document.getElementById('positionsTableBody');
    if (!tbody) return;
    
    if (tickets.length === 0) {
        tbody.innerHTML = '<tr class="empty-row"><td colspan="8" class="empty-state">No open positions</td></tr>';
        return;
    }
    
    let html = '';
    tickets.forEach(ticket => {
        const typeClass = ticket.type === 'BUY' ? 'buy' : 'sell';
        const isPositive = ticket.profit_loss >= 0;
        const plClass = isPositive ? 'text-success' : 'text-danger';
        
        html += `
            <tr class="position-row ${typeClass}">
                <td>#${ticket.ticket}</td>
                <td><strong>${ticket.type}</strong></td>
                <td>${ticket.volume}</td>
                <td>${formatPrice(ticket.entry_price)}</td>
                <td>${formatPrice(ticket.current_price)}</td>
                <td class="${plClass}"><strong>${formatCurrency(ticket.profit_loss)}</strong></td>
                <td class="${plClass}"><strong>${formatPercent(ticket.profit_loss_pct)}</strong></td>
                <td>${formatDateTime(ticket.open_time)}</td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

/**
 * Update active strategies
 */
function updateStrategies(data) {
    const listEl = document.getElementById('strategiesList');
    if (!listEl) return;
    
    const strategies = data.active_strategies || [];
    
    if (strategies.length === 0) {
        listEl.innerHTML = '<div class="empty-state">No active strategies</div>';
        return;
    }
    
    let html = '';
    strategies.forEach(strategy => {
        const displayName = strategy.toUpperCase();
        html += `<div class="strategy-item"><span class="strategy-name">${displayName}</span></div>`;
    });
    
    listEl.innerHTML = html;
}

/**
 * Update statistics
 */
function updateStatistics(data) {
    const pl = data.total_profit_loss || 0;
    const plClass = pl >= 0 ? 'positive' : 'negative';
    
    setElementText('totalPL', formatCurrency(pl), ['stat-value', plClass]);
    setElementText('openOrders', data.open_tickets.length || 0, ['stat-value']);
    setElementText('botStatusText', capitalizeFirst(data.bot_status || 'unknown'), ['stat-value']);
}

/**
 * Update bot status
 */
function updateBotStatus(data) {
    const statusEl = document.getElementById('botStatus');
    if (!statusEl) return;
    
    const status = data.bot_status || 'unknown';
    statusEl.textContent = `● ${capitalizeFirst(status)}`;
    
    if (status === 'error') {
        statusEl.classList.add('error');
    } else {
        statusEl.classList.remove('error');
    }
}

/**
 * Update bot status to error
 */
function updateBotStatusError() {
    const statusEl = document.getElementById('botStatus');
    if (statusEl) {
        statusEl.textContent = '● Error';
        statusEl.classList.add('error');
    }
}

/**
 * Update price chart
 */
function updatePriceChart() {
    const canvas = document.getElementById('priceChart');
    if (!canvas || dashboardState.priceHistory.length < 2) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 5;
    
    // Clear canvas
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, width, height);
    
    // Calculate min/max
    const prices = dashboardState.priceHistory;
    const min = Math.min(...prices);
    const max = Math.max(...prices);
    const range = max - min || 1;
    
    // Draw line chart
    ctx.strokeStyle = '#0ea5e9';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    prices.forEach((price, index) => {
        const x = (index / (prices.length - 1)) * (width - 2 * padding) + padding;
        const y = height - padding - ((price - min) / range) * (height - 2 * padding);
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
}

/**
 * Update timestamp
 */
function updateTimestamp() {
    const el = document.getElementById('timestamp');
    if (el) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { 
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }) + ' UTC';
        el.textContent = timeStr;
    }
}

/* ==================== FORMATTING FUNCTIONS ==================== */

/**
 * Format number as price
 */
function formatPrice(price) {
    if (typeof price !== 'number') price = parseFloat(price) || 0;
    return price.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

/**
 * Format number as currency
 */
function formatCurrency(amount) {
    if (typeof amount !== 'number') amount = parseFloat(amount) || 0;
    return '$' + amount.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

/**
 * Format number as percentage
 */
function formatPercent(value) {
    if (typeof value !== 'number') value = parseFloat(value) || 0;
    const sign = value >= 0 ? '+' : '';
    return sign + value.toFixed(2) + '%';
}

/**
 * Format datetime
 */
function formatDateTime(isoString) {
    if (!isoString) return '--:--';
    try {
        const date = new Date(isoString);
        return date.toLocaleString('en-US', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false,
        });
    } catch {
        return isoString;
    }
}

/**
 * Capitalize first letter
 */
function capitalizeFirst(str) {
    if (typeof str !== 'string') return 'Unknown';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

/* ==================== UTILITY FUNCTIONS ==================== */

/**
 * Set element text content
 */
function setElementText(id, text, classes = []) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = text;
        if (classes.length > 0) {
            el.className = classes.join(' ');
        }
    }
}

/**
 * Add event listener with error handling
 */
function addEventListenerSafe(selector, event, handler) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
        el.addEventListener(event, handler);
    });
}

/* ==================== LIVE UPDATES ==================== */

// Handle window visibility for optimization
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Stop updates when window is hidden
        clearInterval(dashboardState.refreshTimer);
    } else {
        // Resume updates when window becomes visible
        updateDashboard();
        dashboardState.refreshTimer = setInterval(updateDashboard, dashboardState.updateInterval);
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (dashboardState.refreshTimer) {
        clearInterval(dashboardState.refreshTimer);
    }
});

console.log('Dashboard script loaded');
