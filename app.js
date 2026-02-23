/* ============================================================
   StockRAG — Frontend JavaScript  v2
   Handles API calls, UI state, history, toasts, and rendering
   ============================================================ */

const API_URL = "http://127.0.0.1:8000/query";  // Same origin via FastAPI

// -----------------------------------------------
// DOM References
// -----------------------------------------------
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');
const charCount = document.getElementById('charCount');
const resultsSection = document.getElementById('resultsSection');
const skeletonSection = document.getElementById('skeletonSection');
const errorBanner = document.getElementById('errorBanner');
const errorText = document.getElementById('errorText');
const errorClose = document.getElementById('errorClose');

// Header
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const docCount = document.getElementById('docCount');

// Answer
const answerQuestion = document.getElementById('answerQuestion');
const answerBody = document.getElementById('answerBody');
const answerMeta = document.getElementById('answerMeta');
const copyAnswerBtn = document.getElementById('copyAnswerBtn');

// Stats
const meanPriceVal = document.getElementById('meanPriceVal');
const volatilityVal = document.getElementById('volatilityVal');
const riskVal = document.getElementById('riskVal');
const trendVal = document.getElementById('trendVal');
const signalVal = document.getElementById('signalVal');

// Docs
const docsCount = document.getElementById('docsCount');
const docsList = document.getElementById('docsList');
const expandAllBtn = document.getElementById('expandAllBtn');

// History
const historyToggleBtn = document.getElementById('historyToggleBtn');
const historyDrawer = document.getElementById('historyDrawer');
const historyOverlay = document.getElementById('historyOverlay');
const historyCloseBtn = document.getElementById('historyCloseBtn');
const historyClearBtn = document.getElementById('historyClearBtn');
const historyList = document.getElementById('historyList');

// Hero metrics
const hmDocs = document.getElementById('hm-docs');
const hmQueries = document.getElementById('hm-queries');

// Toast container
const toastContainer = document.getElementById('toastContainer');

// -----------------------------------------------
// App State
// -----------------------------------------------
let queryHistory = JSON.parse(localStorage.getItem('stockrag_history') || '[]');
let totalQueries = parseInt(localStorage.getItem('stockrag_query_count') || '0');
let docsExpanded = false;
let lastAnswerText = '';

// -----------------------------------------------
// TOAST SYSTEM
// -----------------------------------------------
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = {
        success: '✓',
        error: '✕',
        info: 'ℹ',
    };

    toast.innerHTML = `<span>${icons[type] || 'ℹ'}</span><span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('hiding');
        toast.addEventListener('animationend', () => toast.remove(), { once: true });
    }, duration);
}

// -----------------------------------------------
// TICKER TAPE
// -----------------------------------------------
const TICKERS = [
    { sym: 'RELIANCE', price: '2,987.40', change: '+1.24%', up: true },
    { sym: 'TCS', price: '4,012.80', change: '+0.56%', up: true },
    { sym: 'HDFC BANK', price: '1,654.25', change: '-0.38%', up: false },
    { sym: 'INFOSYS', price: '1,890.60', change: '+2.10%', up: true },
    { sym: 'ICICI BANK', price: '1,234.50', change: '-0.15%', up: false },
    { sym: 'ADANI ENT', price: '2,556.90', change: '+0.88%', up: true },
    { sym: 'WIPRO', price: '478.35', change: '-0.72%', up: false },
    { sym: 'SBI', price: '720.10', change: '+1.45%', up: true },
    { sym: 'HCL TECH', price: '1,543.70', change: '+0.34%', up: true },
    { sym: 'BAJAJ FIN', price: '7,204.00', change: '-1.08%', up: false },
    { sym: 'NIFTY 50', price: '22,150.40', change: '+0.67%', up: true },
    { sym: 'SENSEX', price: '73,042.20', change: '+0.55%', up: true },
];

function buildTickerTape() {
    const tape = document.getElementById('tickerTape');
    const items = [...TICKERS, ...TICKERS];  // duplicate for infinite loop
    const inner = document.createElement('div');
    inner.className = 'ticker-inner';

    items.forEach(t => {
        const el = document.createElement('div');
        el.className = 'ticker-item';
        const changeClass = t.up ? 'up' : 'down';
        const arrow = t.up ? '▲' : '▼';
        el.innerHTML = `
      <span style="color:var(--text-secondary);font-weight:600">${t.sym}</span>
      <span style="color:var(--text-primary)">${t.price}</span>
      <span class="${changeClass}">${arrow} ${t.change}</span>
    `;
        inner.appendChild(el);
    });

    tape.appendChild(inner);
}

// -----------------------------------------------
// HEALTH CHECK
// -----------------------------------------------
async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (!res.ok) throw new Error('not ok');
        const data = await res.json();

        if (data.status === 'healthy') {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'System Online';

            const count = data.documents_indexed ?? 0;
            docCount.textContent = count;
            if (hmDocs) hmDocs.textContent = count.toLocaleString();

            // animate doc counter
            animateCounter(docCount, count, 1000);
        } else {
            statusDot.className = 'status-dot degraded';
            statusText.textContent = 'Degraded';
        }
    } catch {
        statusDot.className = 'status-dot error';
        statusText.textContent = 'Offline';
        showToast('Backend is offline. Some features may not work.', 'error', 5000);
    }
}

// -----------------------------------------------
// INPUT HANDLING
// -----------------------------------------------
queryInput.addEventListener('input', () => {
    const len = queryInput.value.length;
    charCount.textContent = `${len} / 500`;
    charCount.className = 'query-hint';
    if (len >= 450) charCount.classList.add('near-limit');
    if (len >= 495) { charCount.classList.remove('near-limit'); charCount.classList.add('at-limit'); }
    submitBtn.disabled = len < 3;
});

queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        if (!submitBtn.disabled) handleSubmit();
    }
});

// Chip clicks
document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
        queryInput.value = chip.dataset.query;
        queryInput.dispatchEvent(new Event('input'));
        queryInput.focus();
        queryInput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
});

// Close error banner
errorClose.addEventListener('click', () => { errorBanner.hidden = true; });

// Submit button
submitBtn.addEventListener('click', handleSubmit);

// Expand All toggle
expandAllBtn?.addEventListener('click', () => {
    docsExpanded = !docsExpanded;
    expandAllBtn.textContent = docsExpanded ? 'Collapse All' : 'Expand All';
    document.querySelectorAll('.doc-content').forEach(el => {
        el.classList.toggle('expanded', docsExpanded);
    });
    document.querySelectorAll('.doc-expand-toggle').forEach(btn => {
        btn.textContent = docsExpanded ? '▲ Show less' : '▼ Show more';
    });
});

// Copy answer button
copyAnswerBtn?.addEventListener('click', async () => {
    if (!lastAnswerText) return;
    try {
        await navigator.clipboard.writeText(lastAnswerText);
        copyAnswerBtn.classList.add('copied');
        copyAnswerBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Copied!`;
        showToast('Answer copied to clipboard!', 'success');
        setTimeout(() => {
            copyAnswerBtn.classList.remove('copied');
            copyAnswerBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> Copy`;
        }, 2500);
    } catch {
        showToast('Could not copy. Try manually selecting the text.', 'error');
    }
});

// -----------------------------------------------
// HISTORY DRAWER
// -----------------------------------------------
historyToggleBtn?.addEventListener('click', openHistory);
historyCloseBtn?.addEventListener('click', closeHistory);
historyOverlay?.addEventListener('click', closeHistory);

historyClearBtn?.addEventListener('click', () => {
    queryHistory = [];
    localStorage.setItem('stockrag_history', JSON.stringify(queryHistory));
    renderHistory();
    showToast('History cleared.', 'info');
});

function openHistory() {
    historyDrawer.hidden = false;
    historyOverlay.hidden = false;
    renderHistory();
    document.body.style.overflow = 'hidden';
}

function closeHistory() {
    historyDrawer.hidden = true;
    historyOverlay.hidden = true;
    document.body.style.overflow = '';
}

function saveHistory(query) {
    const entry = { query, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    // Avoid duplicate consecutive entries
    if (queryHistory.length > 0 && queryHistory[0].query === query) return;
    queryHistory.unshift(entry);
    if (queryHistory.length > 20) queryHistory.pop();
    localStorage.setItem('stockrag_history', JSON.stringify(queryHistory));
}

function renderHistory() {
    historyList.innerHTML = '';
    if (queryHistory.length === 0) {
        historyList.innerHTML = '<li class="history-empty">No queries yet. Ask something!</li>';
        return;
    }
    queryHistory.forEach((entry) => {
        const li = document.createElement('li');
        li.className = 'history-item';
        li.innerHTML = `
      <div>
        <div class="history-item-text">${escapeHtml(entry.query)}</div>
        <div class="history-item-time">${entry.time}</div>
      </div>
    `;
        li.addEventListener('click', () => {
            queryInput.value = entry.query;
            queryInput.dispatchEvent(new Event('input'));
            closeHistory();
            queryInput.focus();
        });
        historyList.appendChild(li);
    });
}

// -----------------------------------------------
// SUBMIT HANDLER
// -----------------------------------------------
async function handleSubmit() {
    const query = queryInput.value.trim();
    if (!query || query.length < 3) return;

    // Update counters
    totalQueries++;
    localStorage.setItem('stockrag_query_count', totalQueries);
    if (hmQueries) hmQueries.textContent = totalQueries;

    setLoadingState(true);
    hideError();
    resultsSection.hidden = true;
    skeletonSection.hidden = false;

    // Auto-scroll to skeleton
    skeletonSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        const res = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, n_results: 3 }),
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Server error ${res.status}`);
        }

        const data = await res.json();
        saveHistory(query);
        renderResults(data, query);
        showToast('Answer ready!', 'success', 2500);

    } catch (err) {
        showError(`Query failed: ${err.message || 'Unknown error'}`);
        showToast(`Error: ${err.message}`, 'error', 4000);
    } finally {
        setLoadingState(false);
        skeletonSection.hidden = true;
    }
}

// -----------------------------------------------
// RENDER RESULTS
// -----------------------------------------------
function renderResults(data, query) {
    const startTime = performance.now();

    // Question
    answerQuestion.textContent = `"${data.question}"`;

    // Answer
    const rawAnswer = data.answer || 'No answer generated.';
    lastAnswerText = rawAnswer;
    answerBody.textContent = '';

    // Typewriter effect for answer
    typewriterEffect(answerBody, rawAnswer, 12);

    // Meta (timing)
    const elapsed = Math.round(performance.now() - startTime);
    answerMeta.textContent = `Generated in ~${elapsed}ms · ${data.results.length} docs retrieved`;

    // Stats
    const a = data.analysis || {};
    if (a.status) {
        meanPriceVal.textContent = 'N/A';
        volatilityVal.textContent = 'N/A';
        riskVal.textContent = 'N/A';
        trendVal.textContent = 'N/A';
        signalVal.textContent = 'N/A';
    } else {
        setStatWithAnimation(meanPriceVal, a.mean_price != null
            ? `₹${a.mean_price.toLocaleString('en-IN')}` : '—');
        setStatWithAnimation(volatilityVal, a.volatility != null
            ? a.volatility.toFixed(2) : '—');
        setStatWithAnimation(riskVal, stripBrackets(a.risk_level || '—'));
        setStatWithAnimation(trendVal, stripBrackets(a.trend || '—'));

        const sig = stripBrackets(a.trading_signal || '—');
        setStatWithAnimation(signalVal, sig);
        signalVal.className = 'stat-value signal-value';
        if (sig.toLowerCase().includes('sell') || sig.toLowerCase().includes('bear')) {
            signalVal.classList.add('bearish');
        }
    }

    // Documents
    docsList.innerHTML = '';
    docsCount.textContent = `${data.results.length} found`;
    docsExpanded = false;
    if (expandAllBtn) expandAllBtn.textContent = 'Expand All';

    if (data.results.length === 0) {
        docsList.innerHTML = `<div class="glass-panel" style="padding:24px;text-align:center;color:var(--text-muted)">No relevant documents found. Try different keywords.</div>`;
    } else {
        data.results.forEach((r, i) => {
            docsList.appendChild(buildDocCard(r, i));
        });
    }

    // Show results
    resultsSection.hidden = false;
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Typewriter animation
function typewriterEffect(el, text, speed = 14) {
    el.textContent = '';
    let i = 0;
    const interval = setInterval(() => {
        el.textContent += text[i++];
        if (i >= text.length) clearInterval(interval);
    }, speed);
}

// Flash animation when stats update
function setStatWithAnimation(el, value) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(6px)';
    el.textContent = value;
    requestAnimationFrame(() => {
        el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
    });
    setTimeout(() => { el.style.transition = ''; }, 500);
}

function buildDocCard(r, index) {
    const card = document.createElement('div');
    card.className = 'doc-card';
    card.setAttribute('role', 'listitem');

    const rel = r.relevance;
    let relClass = 'relevance-low';
    if (rel >= 65) relClass = 'relevance-high';
    else if (rel >= 40) relClass = 'relevance-med';

    const sourceLabel = r.source ? truncate(r.source, 60) : 'NIFTY Market Data';
    const dateLabel = r.date !== 'Unknown' ? r.date : 'N/A';

    card.innerHTML = `
    <div class="doc-card-header">
      <div class="doc-badge">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        Document ${index + 1}
      </div>
      <span class="relevance-pill ${relClass}" title="Semantic similarity">
        ${rel.toFixed(1)}% match
      </span>
    </div>
    <div class="doc-meta">
      <div class="doc-meta-item">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
        ${dateLabel}
      </div>
      <div class="doc-meta-item">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
        ${sourceLabel}
      </div>
    </div>
    <div class="doc-content" id="docContent${index}">${escapeHtml(r.content)}</div>
    <button class="doc-expand-toggle" data-idx="${index}">▼ Show more</button>
  `;

    // Wire up expand toggle for this card
    const toggleBtn = card.querySelector('.doc-expand-toggle');
    const contentEl = card.querySelector('.doc-content');
    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const expanded = contentEl.classList.toggle('expanded');
        toggleBtn.textContent = expanded ? '▲ Show less' : '▼ Show more';
    });

    return card;
}

// -----------------------------------------------
// UI HELPERS
// -----------------------------------------------
function setLoadingState(loading) {
    submitBtn.classList.toggle('loading', loading);
    submitBtn.disabled = loading;
    queryInput.disabled = loading;
}

function showError(msg) {
    errorText.textContent = msg;
    errorBanner.hidden = false;
}

function hideError() {
    errorBanner.hidden = true;
}

function stripBrackets(str) {
    return str.replace(/[\[\]]/g, '').trim();
}

function truncate(str, len) {
    return str.length > len ? str.slice(0, len) + '…' : str;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// -----------------------------------------------
// Animated number counter
// -----------------------------------------------
function animateCounter(el, target, duration = 800) {
    const start = performance.now();
    const from = parseInt(el.textContent) || 0;
    function step(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(from + (target - from) * eased);
        if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

// -----------------------------------------------
// KEYBOARD SHORTCUTS
// -----------------------------------------------
document.addEventListener('keydown', (e) => {
    // ESC closes history drawer
    if (e.key === 'Escape') {
        if (!historyDrawer.hidden) closeHistory();
        if (!errorBanner.hidden) errorBanner.hidden = true;
    }
    // Ctrl+K focuses the input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        queryInput.focus();
        queryInput.select();
    }
});

// -----------------------------------------------
// INIT
// -----------------------------------------------
(async function init() {
    buildTickerTape();

    // Set query count from storage
    if (hmQueries) hmQueries.textContent = totalQueries;

    // Check health
    await checkHealth();

    // Re-check health every 30 seconds
    setInterval(checkHealth, 30_000);

    // Keyboard shortcut hints
    queryInput.title = 'Press Ctrl+Enter (or Cmd+Enter) to submit · Ctrl+K to focus';

    // Render any existing history (populates drawer when opened)
    renderHistory();
})();

function fakeDemoResponse() {
    showAnswer({
        answer: "This is a demo MVP UI. Backend API will be integrated in the production version.",
        mean_price: "₹2,450",
        volatility: "Medium",
        risk: "Moderate",
        trend: "Bullish",
        signal: "BUY",
        docs: [
            { source: "NIFTY 50 Report", content: "Market shows strong bullish momentum driven by IT and Banking stocks." },
            { source: "Economic Survey", content: "GDP growth outlook remains positive, boosting investor confidence." }
        ]
    });
}
