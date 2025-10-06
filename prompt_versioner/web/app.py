"""Web dashboard for prompt versioner."""

from flask import Flask, render_template_string, jsonify, send_file, request
from typing import Any
from pathlib import Path
import tempfile

# HTML template for the dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Prompt Versioner Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        /* ===== DARK MODE (default) ===== */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 20px;
            transition: background-color 0.3s, color 0.3s;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { font-size: 2.5rem; margin-bottom: 2rem; color: #38bdf8; }
        h2 { font-size: 1.5rem; margin: 2rem 0 1rem; color: #94a3b8; }
        
        /* Theme toggle */
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            transition: background 0.3s, border-color 0.3s;
            z-index: 1000;
        }
        .theme-toggle:hover {
            background: #334155;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #1e293b;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #334155;
            transition: background 0.3s, border-color 0.3s;
        }
        .stat-label { color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem; }
        .stat-value { font-size: 2rem; font-weight: bold; color: #38bdf8; }
        .stat-sublabel { color: #64748b; font-size: 0.75rem; margin-top: 0.25rem; }
        
        .prompt-list {
            background: #1e293b;
            border-radius: 8px;
            border: 1px solid #334155;
            overflow: hidden;
            transition: background 0.3s, border-color 0.3s;
        }
        .prompt-item {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #334155;
            cursor: pointer;
            transition: background 0.2s;
        }
        .prompt-item:hover { background: #334155; }
        .prompt-item:last-child { border-bottom: none; }
        .prompt-name { font-size: 1.125rem; font-weight: 600; color: #38bdf8; }
        .prompt-meta { color: #94a3b8; font-size: 0.875rem; margin-top: 0.25rem; }
        
        .version-list {
            background: #1e293b;
            border-radius: 8px;
            border: 1px solid #334155;
            margin-top: 1rem;
            transition: background 0.3s, border-color 0.3s;
        }
        .version-item {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #334155;
        }
        .version-item:last-child { border-bottom: none; }
        .version-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .version-tag {
            background: #0ea5e9;
            color: #fff;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.875rem;
            font-weight: 600;
        }
        .version-time { color: #64748b; font-size: 0.875rem; }
        
        .model-badge {
            display: inline-block;
            background: #8b5cf6;
            color: #fff;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: 8px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.75rem;
            margin: 1rem 0;
            padding: 1rem;
            background: #0f172a;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .metric-item { text-align: center; }
        .metric-label {
            color: #64748b;
            font-size: 0.75rem;
            margin-bottom: 0.25rem;
        }
        .metric-value {
            color: #38bdf8;
            font-size: 1.25rem;
            font-weight: 600;
        }
        .metric-unit {
            color: #94a3b8;
            font-size: 0.75rem;
            margin-left: 0.25rem;
        }
        
        .prompt-content {
            background: #0f172a;
            padding: 1rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            white-space: pre-wrap;
            margin-top: 0.5rem;
            line-height: 1.6;
            transition: background 0.3s;
        }
        .prompt-label {
            color: #38bdf8;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .diff-added {
            background: rgba(34, 197, 94, 0.2);
            color: #86efac;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: 500;
        }
        .diff-removed {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            padding: 2px 4px;
            border-radius: 3px;
            text-decoration: line-through;
            font-weight: 500;
        }
        .diff-badge {
            display: inline-block;
            background: #f59e0b;
            color: #fff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: 8px;
        }
        .diff-info {
            color: #94a3b8;
            font-size: 0.875rem;
            margin-top: 0.5rem;
            font-style: italic;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #94a3b8;
        }
        
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: #64748b;
        }
        .empty-state h3 { color: #94a3b8; margin-bottom: 0.5rem; }
        
        /* ===== LIGHT MODE ===== */
        body.light-mode {
            background: #f8fafc;
            color: #1e293b;
        }
        body.light-mode h1 { color: #0284c7; }
        body.light-mode h2 { color: #475569; }
        
        body.light-mode .theme-toggle {
            background: #e2e8f0;
            border-color: #cbd5e1;
        }
        body.light-mode .theme-toggle:hover {
            background: #cbd5e1;
        }
        
        body.light-mode .stat-card {
            background: #ffffff;
            border-color: #e2e8f0;
        }
        body.light-mode .stat-label { color: #64748b; }
        body.light-mode .stat-value { color: #0284c7; }
        body.light-mode .stat-sublabel { color: #94a3b8; }
        
        body.light-mode .prompt-list {
            background: #ffffff;
            border-color: #e2e8f0;
        }
        body.light-mode .prompt-item {
            border-bottom-color: #e2e8f0;
        }
        body.light-mode .prompt-item:hover {
            background: #f1f5f9;
        }
        body.light-mode .prompt-name { color: #0284c7; }
        body.light-mode .prompt-meta { color: #64748b; }
        
        body.light-mode .version-list {
            background: #ffffff;
            border-color: #e2e8f0;
        }
        body.light-mode .version-item {
            border-bottom-color: #e2e8f0;
        }
        body.light-mode .version-time { color: #94a3b8; }
        
        body.light-mode .metrics-grid {
            background: #f8fafc;
        }
        body.light-mode .metric-label { color: #94a3b8; }
        body.light-mode .metric-value { color: #0284c7; }
        body.light-mode .metric-unit { color: #64748b; }
        
        body.light-mode .prompt-content {
            background: #f8fafc;
            color: #1e293b;
        }
        body.light-mode .prompt-label { color: #0284c7; }
        
        body.light-mode .diff-added {
            background: rgba(34, 197, 94, 0.15);
            color: #15803d;
        }
        body.light-mode .diff-removed {
            background: rgba(239, 68, 68, 0.15);
            color: #dc2626;
        }
        body.light-mode .diff-info { color: #64748b; }
        
        body.light-mode .loading { color: #64748b; }
        body.light-mode .empty-state { color: #94a3b8; }
        body.light-mode .empty-state h3 { color: #64748b; }

        body.light-mode #search-input,
        body.light-mode #sort-select {
            background: #ffffff;
            border-color: #e2e8f0;
            color: #1e293b;
        }

        /* Annotations */
        .annotations-section {
            margin-top: 1rem;
            padding: 1rem;
            background: #0f172a;
            border-radius: 4px;
            border: 1px solid #334155;
            transition: background 0.3s, border-color 0.3s;
        }

        .annotations-header {
            color: #38bdf8;
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .annotation-item {
            padding: 0.75rem;
            background: #1e293b;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            border-left: 3px solid #38bdf8;
            transition: background 0.3s;
        }

        .annotation-item:last-child {
            margin-bottom: 0;
        }

        .annotation-author {
            font-size: 0.75rem;
            color: #94a3b8;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .annotation-text {
            color: #e2e8f0;
            font-size: 0.875rem;
            line-height: 1.5;
        }

        .annotation-time {
            font-size: 0.7rem;
            color: #64748b;
            margin-top: 0.25rem;
        }

        .annotation-badge {
            display: inline-block;
            background: #38bdf8;
            color: #0f172a;
            padding: 0.125rem 0.5rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        /* Light mode */
        body.light-mode .annotations-section {
            background: #f8fafc;
            border-color: #e2e8f0;
        }

        body.light-mode .annotation-item {
            background: #ffffff;
            border-left-color: #0284c7;
        }

        body.light-mode .annotation-author {
            color: #64748b;
        }

        body.light-mode .annotation-text {
            color: #1e293b;
        }

        body.light-mode .annotation-time {
            color: #94a3b8;
        }

        body.light-mode .annotation-badge {
            background: #0284c7;
            color: #ffffff;
        }
        
        /* AB Test */
        body.light-mode #version-a-select,
        body.light-mode #version-b-select,
        body.light-mode #metric-select {
            background: #ffffff;
            border-color: #e2e8f0;
            color: #1e293b;
        }

        .ab-comparison {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 2rem;
            margin-top: 1rem;
        }

        .ab-version-card {
            background: #1e293b;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #334155;
        }

        .ab-version-card.winner {
            border: 2px solid #10b981;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }

        .ab-vs {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: #64748b;
        }

        .ab-winner-badge {
            background: #10b981;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 0.5rem;
        }

        body.light-mode .ab-version-card {
            background: #ffffff;
            border-color: #e2e8f0;
        }

        body.light-mode .ab-version-card.winner {
            border-color: #10b981;
        }

        /* Alerts section */
        .alerts-section {
            margin: 2rem 0;
        }
        .alert-card {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
        }
        .alert-card.warning {
            background: rgba(251, 191, 36, 0.1);
            border-color: rgba(251, 191, 36, 0.3);
        }
        .alert-card.info {
            background: rgba(59, 130, 246, 0.1);
            border-color: rgba(59, 130, 246, 0.3);
        }
        .alert-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .alert-type {
            font-weight: 600;
            color: #ef4444;
            text-transform: uppercase;
            font-size: 0.875rem;
        }
        .alert-message {
            color: #e2e8f0;
            margin-bottom: 0.5rem;
        }
        .alert-details {
            font-size: 0.875rem;
            color: #94a3b8;
        }

        body.light-mode .alert-card {
            background: rgba(239, 68, 68, 0.05);
        }
        body.light-mode .alert-type {
            color: #dc2626;
        }
        body.light-mode .alert-message {
            color: #1e293b;
        }

        /* Export/Import */
        .btn {
            background: #0ea5e9;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 600;
            transition: background 0.3s;
        }
        .btn:hover { background: #0284c7; }
        .btn-secondary {
            background: #475569;
        }
        .btn-secondary:hover { background: #334155; }

        body.light-mode .btn-secondary {
            background: #cbd5e1;
            color: #1e293b;
        }
        body.light-mode .btn-secondary:hover {
            background: #94a3b8;
        }
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
        <span id="theme-icon">🌙</span>
    </button>
    
    <div class="container">
        <h1>🚀 Prompt Versioner Dashboard</h1>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-label">Total Prompts</div>
                <div class="stat-value" id="total-prompts">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Versions</div>
                <div class="stat-value" id="total-versions">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Cost</div>
                <div class="stat-value" id="total-cost">-</div>
                <div class="stat-sublabel">EUR</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Tokens</div>
                <div class="stat-value" id="total-tokens">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Calls</div>
                <div class="stat-value" id="total-calls">-</div>
            </div>
        </div>
        
        <h2>📝 Prompts</h2>

        <!-- Export/Import toolbar -->
        <div style="margin-bottom: 1rem; display: flex; gap: 0.5rem; justify-content: flex-end;">
            <button class="btn btn-secondary" onclick="exportAll()">
                📦 Export All
            </button>
            <button class="btn btn-secondary" onclick="document.getElementById('import-file').click()">
                📥 Import
            </button>
            <input 
                type="file" 
                id="import-file" 
                accept=".json" 
                style="display: none;" 
                onchange="importPrompt()"
            />
        </div>

        <!-- Search and filters -->
        <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <input 
                type="text" 
                id="search-input" 
                placeholder="🔍 Search prompts..." 
                style="flex: 1; min-width: 200px; padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0; font-size: 0.875rem;"
                oninput="filterPrompts()"
            />
            
            <select 
                id="sort-select" 
                style="padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0; font-size: 0.875rem; cursor: pointer;"
                onchange="sortPrompts()"
            >
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="versions-desc">Most Versions</option>
                <option value="versions-asc">Least Versions</option>
                <option value="date-desc">Recently Updated</option>
                <option value="date-asc">Oldest First</option>
            </select>
        </div>

        <div class="prompt-list" id="prompt-list">
            <div class="loading">Loading prompts...</div>
        </div>

        <div id="ab-test-section" style="display: none; margin-top: 2rem;">
            <h2>🧪 A/B Test Comparison</h2>
            
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
                <select id="version-a-select" style="flex: 1; min-width: 150px; padding: 0.5rem; border-radius: 4px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0;">
                    <option value="">Select Version A...</option>
                </select>
                
                <span style="align-self: center; color: #94a3b8;">vs</span>
                
                <select id="version-b-select" style="flex: 1; min-width: 150px; padding: 0.5rem; border-radius: 4px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0;">
                    <option value="">Select Version B...</option>
                </select>
                
                <select id="metric-select" style="flex: 1; min-width: 150px; padding: 0.5rem; border-radius: 4px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0;">
                    <option value="quality_score">Quality Score</option>
                    <option value="cost">Cost (USD)</option>
                    <option value="latency">Latency (ms)</option>
                    <option value="accuracy">Accuracy</option>
                </select>
                
                <button onclick="runABTest()" style="padding: 0.5rem 1.5rem; background: #0ea5e9; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 600;">
                    Compare
                </button>
            </div>
            
            <div id="ab-test-results"></div>
        </div>
        
        <div id="version-section" style="display: none;">
            <h2 id="version-title">Versions</h2>
            <div class="version-list" id="version-list"></div>
        </div>

        <!-- Alerts section -->
        <div class="alerts-section" id="alerts-section" style="display: none;">
            <h2>⚠️ Performance Alerts</h2>
            <div id="alerts-container"></div>
        </div>

        
        
    </div>

    
    
    <script>
        // Theme management
        function initTheme() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            if (savedTheme === 'light') {
                document.body.classList.add('light-mode');
                document.getElementById('theme-icon').textContent = '☀️';
            }
        }
        
        function toggleTheme() {
            const body = document.body;
            const icon = document.getElementById('theme-icon');
            
            if (body.classList.contains('light-mode')) {
                body.classList.remove('light-mode');
                icon.textContent = '🌙';
                localStorage.setItem('theme', 'dark');
            } else {
                body.classList.add('light-mode');
                icon.textContent = '☀️';
                localStorage.setItem('theme', 'light');
            }
        }
        
        let currentPrompt = null;
        
        let allPromptsData = [];

        async function loadPrompts() {
            try {
                const response = await fetch('/api/prompts');
                const data = await response.json();
                
                allPromptsData = data.prompts;
                
                document.getElementById('total-prompts').textContent = data.prompts.length;
                document.getElementById('total-versions').textContent = data.total_versions;
                document.getElementById('total-cost').textContent = data.total_cost?.toFixed(4) || '0.0000';
                document.getElementById('total-tokens').textContent = data.total_tokens?.toLocaleString() || '0';
                document.getElementById('total-calls').textContent = data.total_calls?.toLocaleString() || '0';
                
                renderPrompts(allPromptsData);
            } catch (error) {
                document.getElementById('prompt-list').innerHTML = 
                    '<div class="empty-state"><h3>Error loading prompts</h3></div>';
            }
        }

        function renderPrompts(prompts) {
            const list = document.getElementById('prompt-list');
            
            if (prompts.length === 0) {
                list.innerHTML = `
                    <div class="empty-state">
                        <h3>No prompts found</h3>
                        <p>Try adjusting your search or filters</p>
                    </div>
                `;
                return;
            }
            
            list.innerHTML = prompts.map(p => `
                <div class="prompt-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1; cursor: pointer;" onclick="loadVersions('${p.name}')">
                            <div class="prompt-name">${p.name}</div>
                            <div class="prompt-meta">
                                ${p.version_count} versions • Latest: ${p.latest_version}
                            </div>
                        </div>
                        <button 
                            class="btn btn-secondary" 
                            style="padding: 0.25rem 0.75rem; font-size: 0.75rem;"
                            onclick="event.stopPropagation(); exportSinglePrompt('${p.name}')"
                        >
                            Export
                        </button>
                    </div>
                </div>
            `).join('');
        }

        function filterPrompts() {
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            
            const filtered = allPromptsData.filter(p => 
                p.name.toLowerCase().includes(searchTerm) ||
                p.latest_version.toLowerCase().includes(searchTerm)
            );
            
            renderPrompts(filtered);
        }

        function sortPrompts() {
            const sortBy = document.getElementById('sort-select').value;
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            
            let filtered = allPromptsData.filter(p => 
                p.name.toLowerCase().includes(searchTerm) ||
                p.latest_version.toLowerCase().includes(searchTerm)
            );
            
            switch(sortBy) {
                case 'name-asc':
                    filtered.sort((a, b) => a.name.localeCompare(b.name));
                    break;
                case 'name-desc':
                    filtered.sort((a, b) => b.name.localeCompare(a.name));
                    break;
                case 'versions-desc':
                    filtered.sort((a, b) => b.version_count - a.version_count);
                    break;
                case 'versions-asc':
                    filtered.sort((a, b) => a.version_count - b.version_count);
                    break;
                case 'date-desc':
                    filtered.sort((a, b) => new Date(b.latest_timestamp) - new Date(a.latest_timestamp));
                    break;
                case 'date-asc':
                    filtered.sort((a, b) => new Date(a.latest_timestamp) - new Date(b.latest_timestamp));
                    break;
            }
            
            renderPrompts(filtered);
        }
        
        async function loadVersions(promptName) {
            currentPrompt = promptName;
            document.getElementById('version-title').textContent = `Versions of "${promptName}"`;
            document.getElementById('version-section').style.display = 'block';
            
            const list = document.getElementById('version-list');
            list.innerHTML = '<div class="loading">Loading versions...</div>';
            
            try {
                // Carica versioni con diff
                const response = await fetch(`/api/prompts/${promptName}/versions/with-diffs`);
                const versions = await response.json();
                
                list.innerHTML = versions.map(v => {
                    let metricsHtml = '';
                    if (v.metrics_summary && v.metrics_summary.call_count > 0) {
                        metricsHtml = `
                            <div class="metrics-grid">
                                <div class="metric-item">
                                    <div class="metric-label">Calls</div>
                                    <div class="metric-value">${v.metrics_summary.call_count}</div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-label">Avg Tokens</div>
                                    <div class="metric-value">${Math.round(v.metrics_summary.avg_total_tokens || 0)}</div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-label">Total Cost</div>
                                    <div class="metric-value">€${(v.metrics_summary.total_cost || 0).toFixed(4)}</div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-label">Avg Latency</div>
                                    <div class="metric-value">${Math.round(v.metrics_summary.avg_latency || 0)}<span class="metric-unit">ms</span></div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-label">Quality</div>
                                    <div class="metric-value">${((v.metrics_summary.avg_quality || 0) * 100).toFixed(0)}<span class="metric-unit">%</span></div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-label">Success Rate</div>
                                    <div class="metric-value">${((v.metrics_summary.success_rate || 0) * 100).toFixed(0)}<span class="metric-unit">%</span></div>
                                </div>
                            </div>
                        `;
                    }
                    
                    let diffBadge = '';
                    if (v.has_changes) {
                        diffBadge = `<span class="diff-badge">Modified</span>`;
                    }
                    
                    let modelBadge = '';
                    if (v.model_name) {
                        modelBadge = `<span class="model-badge">${v.model_name}</span>`;
                    }

                    let annotationsHtml = '';
                    if (v.annotations && v.annotations.length > 0) {
                        const annotationItems = v.annotations.map(ann => `
                            <div class="annotation-item">
                                <div class="annotation-author">${escapeHtml(ann.author)}</div>
                                <div class="annotation-text">${escapeHtml(ann.text)}</div>
                                <div class="annotation-time">${new Date(ann.timestamp).toLocaleString()}</div>
                            </div>
                        `).join('');
                        
                        annotationsHtml = `
                            <div class="annotations-section">
                                <div class="annotations-header">
                                    💬 Comments
                                    <span class="annotation-badge">${v.annotations.length}</span>
                                </div>
                                ${annotationItems}
                            </div>
                        `;
                    }
                    
                    const systemPromptHtml = renderDiff(v.system_diff);
                    const userPromptHtml = renderDiff(v.user_diff);
                    
                    return `
                        <div class="version-item">
                            <div class="version-header">
                                <div>
                                    <span class="version-tag">${v.version}</span>${modelBadge}${diffBadge}
                                </div>
                                <span class="version-time">${new Date(v.timestamp).toLocaleString()}</span>
                            </div>
                            ${v.git_commit ? `<div class="prompt-meta">Git: ${v.git_commit}</div>` : ''}
                            ${v.has_changes ? `<div class="diff-info">📝 ${v.diff_summary}</div>` : `<div class="diff-info">🎉 ${v.diff_summary}</div>`}
                            ${metricsHtml}
                            ${annotationsHtml}
                            <div style="margin-top: 1rem;">
                                <div class="prompt-label">System Prompt:</div>
                                <div class="prompt-content">${systemPromptHtml}</div>
                            </div>
                            <div style="margin-top: 1rem;">
                                <div class="prompt-label">User Prompt:</div>
                                <div class="prompt-content">${userPromptHtml}</div>
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                list.innerHTML = '<div class="empty-state"><h3>Error loading versions</h3></div>';
            }

            // Load A/B test options
            loadABTestOptions(promptName);
        }

        async function loadABTestOptions(promptName) {
            try {
                const response = await fetch(`/api/prompts/${promptName}/ab-tests`);
                const versions = await response.json();
                
                if (versions.length >= 2) {
                    document.getElementById('ab-test-section').style.display = 'block';
                    
                    const selectA = document.getElementById('version-a-select');
                    const selectB = document.getElementById('version-b-select');
                    
                    selectA.innerHTML = '<option value="">Select Version A...</option>' +
                        versions.map(v => `<option value="${v.version}">${v.version} (${v.call_count} calls)</option>`).join('');
                    
                    selectB.innerHTML = '<option value="">Select Version B...</option>' +
                        versions.map(v => `<option value="${v.version}">${v.version} (${v.call_count} calls)</option>`).join('');
                    
                    // Pre-select first two versions
                    if (versions.length >= 2) {
                        selectA.value = versions[1].version;
                        selectB.value = versions[0].version;
                    }
                } else {
                    document.getElementById('ab-test-section').style.display = 'none';
                }
            } catch (error) {
                console.error('Failed to load A/B test options:', error);
            }
        }

        async function runABTest() {
            const versionA = document.getElementById('version-a-select').value;
            const versionB = document.getElementById('version-b-select').value;
            const metric = document.getElementById('metric-select').value;
            
            if (!versionA || !versionB) {
                alert('Please select both versions');
                return;
            }
            
            if (versionA === versionB) {
                alert('Please select different versions');
                return;
            }
            
            const resultsDiv = document.getElementById('ab-test-results');
            resultsDiv.innerHTML = '<div class="loading">Running comparison...</div>';
            
            try {
                const response = await fetch(
                    `/api/prompts/${currentPrompt}/compare?version_a=${versionA}&version_b=${versionB}&metric=${metric}`
                );
                const data = await response.json();
                
                const metricLabels = {
                    'quality_score': 'Quality Score',
                    'cost': 'Cost (USD)',
                    'latency': 'Latency (ms)',
                    'accuracy': 'Accuracy'
                };
                
                const metricLabel = metricLabels[metric];
                const isWinnerA = data.winner === versionA;
                
                resultsDiv.innerHTML = `
                    <div class="ab-comparison">
                        <div class="ab-version-card ${isWinnerA ? 'winner' : ''}">
                            ${isWinnerA ? '<div class="ab-winner-badge">🏆 Winner</div>' : ''}
                            <h3 style="color: #38bdf8; margin-bottom: 1rem;">Version A: ${versionA}</h3>
                            <div style="font-size: 2rem; font-weight: bold; color: #38bdf8; margin-bottom: 1rem;">
                                ${formatMetricValue(data.value_a, metric)}
                            </div>
                            <div style="color: #94a3b8; font-size: 0.875rem;">
                                <div>Calls: ${data.call_count_a}</div>
                                <div>Avg Cost: $${(data.summary_a.avg_cost || 0).toFixed(4)}</div>
                                <div>Avg Latency: ${Math.round(data.summary_a.avg_latency || 0)}ms</div>
                                <div>Success Rate: ${((data.summary_a.success_rate || 0) * 100).toFixed(0)}%</div>
                            </div>
                        </div>
                        
                        <div class="ab-vs">vs</div>
                        
                        <div class="ab-version-card ${!isWinnerA ? 'winner' : ''}">
                            ${!isWinnerA ? '<div class="ab-winner-badge">🏆 Winner</div>' : ''}
                            <h3 style="color: #38bdf8; margin-bottom: 1rem;">Version B: ${versionB}</h3>
                            <div style="font-size: 2rem; font-weight: bold; color: #38bdf8; margin-bottom: 1rem;">
                                ${formatMetricValue(data.value_b, metric)}
                            </div>
                            <div style="color: #94a3b8; font-size: 0.875rem;">
                                <div>Calls: ${data.call_count_b}</div>
                                <div>Avg Cost: $${(data.summary_b.avg_cost || 0).toFixed(4)}</div>
                                <div>Avg Latency: ${Math.round(data.summary_b.avg_latency || 0)}ms</div>
                                <div>Success Rate: ${((data.summary_b.success_rate || 0) * 100).toFixed(0)}%</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #1e293b; border-radius: 8px;">
                        <div style="font-size: 1.25rem; color: #94a3b8; margin-bottom: 0.5rem;">
                            ${metricLabel} Improvement
                        </div>
                        <div style="font-size: 3rem; font-weight: bold; color: #10b981;">
                            ${data.improvement_percent.toFixed(1)}%
                        </div>
                        <div style="color: #64748b; font-size: 0.875rem; margin-top: 0.5rem;">
                            ${data.winner} performs better on ${metricLabel.toLowerCase()}
                        </div>
                    </div>
                `;
            } catch (error) {
                resultsDiv.innerHTML = '<div class="empty-state"><h3>Error running comparison</h3></div>';
            }
        }

        async function loadAllAlerts() {
            try {
                const response = await fetch('/api/alerts');
                const alerts = await response.json();
                
                if (alerts.length === 0) {
                    document.getElementById('alerts-section').style.display = 'none';
                    return;
                }
                
                document.getElementById('alerts-section').style.display = 'block';
                
                const container = document.getElementById('alerts-container');
                container.innerHTML = alerts.map(alert => {
                    const icon = getAlertIcon(alert.type);
                    const severity = getAlertSeverity(alert.change_percent, alert.threshold);
                    
                    return `
                        <div class="alert-card ${severity}">
                            <div class="alert-header">
                                <span class="alert-type">${icon} ${alert.type.replace('_', ' ')}</span>
                                <span class="prompt-meta">${alert.prompt_name}</span>
                            </div>
                            <div class="alert-message">${alert.message}</div>
                            <div class="alert-details">
                                ${alert.baseline_version} → ${alert.current_version} | 
                                Baseline: ${alert.baseline_value.toFixed(4)} | 
                                Current: ${alert.current_value.toFixed(4)}
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                console.error('Error loading alerts:', error);
            }
        }

        function getAlertIcon(type) {
            const icons = {
                'cost_increase': '💰',
                'latency_increase': '⏱️',
                'quality_decrease': '📉',
                'error_rate_increase': '❌'
            };
            return icons[type] || '⚠️';
        }

        function getAlertSeverity(changePercent, threshold) {
            const change = Math.abs(changePercent);
            if (change > threshold * 2) return 'error';
            if (change > threshold * 1.5) return 'warning';
            return 'info';
        }

        function formatMetricValue(value, metric) {
            if (metric === 'cost') {
                return `$${value.toFixed(4)}`;
            } else if (metric === 'latency') {
                return `${Math.round(value)}ms`;
            } else if (metric === 'quality_score' || metric === 'accuracy') {
                return `${(value * 100).toFixed(1)}%`;
            }
            return value.toFixed(2);
        }
        
        function renderDiff(diffSegments) {
            if (!diffSegments || diffSegments.length === 0) {
                return '';
            }
            
            return diffSegments.map(segment => {
                const text = escapeHtml(segment.text);
                if (segment.type === 'added') {
                    return `<span class="diff-added">${text}</span>`;
                } else if (segment.type === 'removed') {
                    return `<span class="diff-removed">${text}</span>`;
                } else {
                    return text;
                }
            }).join(' ');
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        async function exportAll() {
            try {
                const response = await fetch('/api/export-all');
                if (!response.ok) throw new Error('Export failed');
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'all_prompts.zip';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                
                showNotification('All prompts exported successfully', 'success');
            } catch (error) {
                showNotification('Export failed: ' + error.message, 'error');
            }
        }

        async function exportSinglePrompt(promptName) {
            try {
                const response = await fetch(`/api/prompts/${promptName}/export`);
                if (!response.ok) throw new Error('Export failed');
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${promptName}_export.json`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                
                showNotification(`Exported "${promptName}"`, 'success');
            } catch (error) {
                showNotification('Export failed: ' + error.message, 'error');
            }
        }

        async function importPrompt() {
            const fileInput = document.getElementById('import-file');
            const file = fileInput.files[0];
            
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch('/api/prompts/import', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) throw new Error('Import failed');
                
                const result = await response.json();
                showNotification(
                    `Imported: ${result.imported} versions, Skipped: ${result.skipped}`,
                    'success'
                );
                
                // Reload prompts
                loadPrompts();
            } catch (error) {
                showNotification('Import failed: ' + error.message, 'error');
            } finally {
                fileInput.value = ''; // Reset input
            }
        }

        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 80px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                background: ${type === 'success' ? '#10b981' : '#ef4444'};
                color: white;
                font-weight: 600;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                z-index: 1001;
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        // Initialize theme and load data
        initTheme();
        loadPrompts();
        loadAllAlerts();
    </script>
</body>
</html>
"""


def create_inline_diff(old_text: str, new_text: str) -> list:
    """Create word-level inline diff for highlighting.
    
    Args:
        old_text: Previous text
        new_text: New text
        
    Returns:
        List of dicts with 'type' and 'text' for each segment
    """
    import difflib
    
    old_words = old_text.split()
    new_words = new_text.split()
    
    diff_result = []
    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diff_result.append({
                'type': 'unchanged',
                'text': ' '.join(new_words[j1:j2])
            })
        elif tag == 'delete':
            diff_result.append({
                'type': 'removed',
                'text': ' '.join(old_words[i1:i2])
            })
        elif tag == 'insert':
            diff_result.append({
                'type': 'added',
                'text': ' '.join(new_words[j1:j2])
            })
        elif tag == 'replace':
            diff_result.append({
                'type': 'removed',
                'text': ' '.join(old_words[i1:i2])
            })
            diff_result.append({
                'type': 'added',
                'text': ' '.join(new_words[j1:j2])
            })
    
    return diff_result


def create_app(versioner: Any) -> Flask:
    """Create Flask app for dashboard.
    
    Args:
        versioner: PromptVersioner instance
        
    Returns:
        Flask app
    """
    app = Flask(__name__)
    app.versioner = versioner

    @app.route('/')
    def index() -> str:
        """Render dashboard."""
        return render_template_string(DASHBOARD_TEMPLATE)

    @app.route('/api/prompts')
    def get_prompts() -> Any:
        """Get all prompts with metadata."""
        prompts = app.versioner.list_prompts()
        
        prompt_data = []
        total_versions = 0
        total_cost = 0.0
        total_tokens = 0
        total_calls = 0
        
        for name in prompts:
            versions = app.versioner.list_versions(name)
            total_versions += len(versions)
            
            # Aggregate metrics across all versions
            for v in versions:
                summary = app.versioner.storage.get_metrics_summary(v['id'])
                if summary:
                    total_cost += summary.get('total_cost', 0) or 0
                    total_tokens += summary.get('total_tokens_used', 0) or 0
                    total_calls += summary.get('call_count', 0) or 0
            
            latest = versions[0] if versions else None
            prompt_data.append({
                'name': name,
                'version_count': len(versions),
                'latest_version': latest['version'] if latest else 'N/A',
                'latest_timestamp': latest['timestamp'] if latest else None,
            })
        
        return jsonify({
            'prompts': prompt_data,
            'total_versions': total_versions,
            'total_cost': round(total_cost, 4),
            'total_tokens': total_tokens,
            'total_calls': total_calls,
        })

    @app.route('/api/prompts/<n>/versions')
    def get_versions(name: str) -> Any:
        """Get all versions of a prompt with metrics."""
        versions = app.versioner.list_versions(name)
        
        # Enrich with metrics summary
        for v in versions:
            v['metrics_summary'] = app.versioner.storage.get_metrics_summary(v['id'])
        
        return jsonify(versions)

    @app.route('/api/prompts/<name>/versions/with-diffs')
    def get_versions_with_diffs(name: str) -> Any:
        """Get all versions with diffs from previous version."""
        from prompt_versioner.diff import DiffEngine
        
        versions = app.versioner.list_versions(name)
        
        if not versions:
            return jsonify([])
        
        # Enrich with metrics and diffs
        for i, v in enumerate(versions):
            v['metrics_summary'] = app.versioner.storage.get_metrics_summary(v['id'])
            
            metrics_list = app.versioner.storage.get_metrics(v['id'])
            model_name = None
            if metrics_list:
                # Get most common model from metrics
                model_names = [m.get('model_name') for m in metrics_list if m.get('model_name')]
                if model_names:
                    # Use most recent model
                    model_name = model_names[0]
            v['model_name'] = model_name

            annotations = app.versioner.storage.get_annotations(v['id'])
            v['annotations'] = annotations  # ✅ Aggiungi annotations
            
            # Calculate diff from previous version
            if i < len(versions) - 1:
                prev_version = versions[i + 1]
                
                diff = DiffEngine.compute_diff(
                    old_system=prev_version['system_prompt'],
                    old_user=prev_version['user_prompt'],
                    new_system=v['system_prompt'],
                    new_user=v['user_prompt'],
                )
                
                v['has_changes'] = diff.total_similarity < 1.0
                v['diff_summary'] = diff.summary
                v['system_similarity'] = diff.system_similarity
                v['user_similarity'] = diff.user_similarity
                
                v['system_diff'] = create_inline_diff(
                    prev_version['system_prompt'],
                    v['system_prompt']
                )
                v['user_diff'] = create_inline_diff(
                    prev_version['user_prompt'],
                    v['user_prompt']
                )
            else:
                v['has_changes'] = False
                v['diff_summary'] = "Initial version"
                v['system_diff'] = [{'type': 'unchanged', 'text': v['system_prompt']}]
                v['user_diff'] = [{'type': 'unchanged', 'text': v['user_prompt']}]

        
        return jsonify(versions)

    @app.route('/api/prompts/<n>/versions/<version>')
    def get_version_detail(name: str, version: str) -> Any:
        """Get a specific version with metrics summary."""
        v = app.versioner.get_version(name, version)
        if v:
            # Get metrics summary
            metrics_summary = app.versioner.storage.get_metrics_summary(v['id'])
            metrics_list = app.versioner.storage.get_metrics(v['id'])
            
            v['metrics_summary'] = metrics_summary
            v['metrics_history'] = metrics_list
            return jsonify(v)
        return jsonify({'error': 'Version not found'}), 404
    
    @app.route('/api/prompts/<n>/stats')
    def get_prompt_stats(name: str) -> Any:
        """Get aggregated stats across all versions of a prompt."""
        versions = app.versioner.list_versions(name)
        
        if not versions:
            return jsonify({'error': 'Prompt not found'}), 404
        
        total_calls = 0
        total_cost = 0.0
        total_tokens = 0
        all_latencies = []
        all_quality_scores = []
        models_used = set()
        
        version_stats = []
        
        for v in versions:
            summary = app.versioner.storage.get_metrics_summary(v['id'])
            if summary and summary.get('call_count', 0) > 0:
                total_calls += summary.get('call_count', 0)
                total_cost += summary.get('total_cost', 0)
                total_tokens += summary.get('total_tokens_used', 0)
                
                if summary.get('avg_latency'):
                    all_latencies.append(summary['avg_latency'])
                if summary.get('avg_quality'):
                    all_quality_scores.append(summary['avg_quality'])
                
                # Get individual metrics for model names
                metrics = app.versioner.storage.get_metrics(v['id'])
                for m in metrics:
                    if m.get('model_name'):
                        models_used.add(m['model_name'])
                
                version_stats.append({
                    'version': v['version'],
                    'timestamp': v['timestamp'],
                    'summary': summary,
                })
        
        return jsonify({
            'name': name,
            'total_versions': len(versions),
            'total_calls': total_calls,
            'total_cost_eur': round(total_cost, 4),
            'total_tokens': total_tokens,
            'avg_latency_ms': round(sum(all_latencies) / len(all_latencies), 2) if all_latencies else 0,
            'avg_quality_score': round(sum(all_quality_scores) / len(all_quality_scores), 2) if all_quality_scores else 0,
            'models_used': list(models_used),
            'version_stats': version_stats,
        })

    @app.route('/api/prompts/<name>/ab-tests')
    def get_ab_tests(name: str) -> Any:
        """Get available versions for A/B testing.
        
        Returns versions with enough metrics to compare.
        """
        versions = app.versioner.list_versions(name)
        
        # Filter versions with metrics
        testable_versions = []
        for v in versions:
            summary = app.versioner.storage.get_metrics_summary(v['id'])
            if summary and summary.get('call_count', 0) >= 5:  # Need at least 5 calls
                testable_versions.append({
                    'version': v['version'],
                    'timestamp': v['timestamp'],
                    'call_count': summary['call_count'],
                    'avg_quality': summary.get('avg_quality', 0),
                    'avg_cost': summary.get('avg_cost', 0),
                    'avg_latency': summary.get('avg_latency', 0),
                })
        
        return jsonify(testable_versions)
    
    @app.route('/api/prompts/<name>/compare')
    def compare_versions_api(name: str) -> Any:
        """Compare two versions with A/B test style analysis."""
        version_a = request.args.get('version_a')
        version_b = request.args.get('version_b')
        metric = request.args.get('metric', 'quality_score')
        
        if not version_a or not version_b:
            return jsonify({'error': 'Missing version_a or version_b'}), 400
        
        v_a = app.versioner.get_version(name, version_a)
        v_b = app.versioner.get_version(name, version_b)
        
        if not v_a or not v_b:
            return jsonify({'error': 'Version not found'}), 404
        
        summary_a = app.versioner.storage.get_metrics_summary(v_a['id'])
        summary_b = app.versioner.storage.get_metrics_summary(v_b['id'])
        
        metrics_a = app.versioner.storage.get_metrics(v_a['id'])
        metrics_b = app.versioner.storage.get_metrics(v_b['id'])
        
        # Extract metric values for comparison
        metric_map = {
            'quality_score': 'avg_quality',
            'cost': 'avg_cost',
            'latency': 'avg_latency',
            'accuracy': 'avg_accuracy'
        }
        
        summary_metric = metric_map.get(metric, 'avg_quality')
        
        value_a = summary_a.get(summary_metric, 0) if summary_a else 0
        value_b = summary_b.get(summary_metric, 0) if summary_b else 0
        
        # Determine winner (lower is better for cost/latency, higher for quality/accuracy)
        if metric in ['cost', 'latency']:
            winner = 'a' if value_a < value_b else 'b'
            improvement = abs(value_b - value_a) / value_a * 100 if value_a > 0 else 0
        else:
            winner = 'a' if value_a > value_b else 'b'
            improvement = abs(value_b - value_a) / value_a * 100 if value_a > 0 else 0
        
        return jsonify({
            'version_a': version_a,
            'version_b': version_b,
            'metric': metric,
            'summary_a': summary_a,
            'summary_b': summary_b,
            'value_a': value_a,
            'value_b': value_b,
            'winner': version_b if winner == 'b' else version_a,
            'improvement_percent': improvement,
            'call_count_a': summary_a.get('call_count', 0) if summary_a else 0,
            'call_count_b': summary_b.get('call_count', 0) if summary_b else 0,
        })

    @app.route('/api/prompts/<name>/diff')
    def get_diff(name: str) -> Any:
        """Get diff between two versions."""
        name = request.args.get('name')
        v1 = request.args.get('version1')
        v2 = request.args.get('version2')
        
        if not all([name, v1, v2]):
            return jsonify({'error': 'Missing parameters'}), 400
        
        try:
            diff = app.versioner.diff(name, v1, v2)
            return jsonify({
                'summary': diff.summary,
                'system_similarity': diff.system_similarity,
                'user_similarity': diff.user_similarity,
                'total_similarity': diff.total_similarity,
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        
    @app.route('/api/prompts/<name>/alerts')
    def get_alerts(name: str) -> Any:
        """Get performance alerts for a prompt."""
        from prompt_versioner.monitoring import PerformanceMonitor
        
        versions = app.versioner.list_versions(name)
        if len(versions) < 2:
            return jsonify([])
        
        monitor = PerformanceMonitor(app.versioner)
        
        # Check latest vs previous
        latest = versions[0]
        previous = versions[1]
        
        alerts = monitor.check_regression(
            name=name,
            current_version=latest["version"],
            baseline_version=previous["version"],
            thresholds={
                "cost": 0.20,
                "latency": 0.30,
                "quality": -0.10,
                "error_rate": 0.05
            }
        )
        
        # Convert alerts to dict
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                "type": alert.alert_type.value,
                "message": alert.message,
                "metric_name": alert.metric_name,
                "baseline_value": alert.baseline_value,
                "current_value": alert.current_value,
                "change_percent": alert.change_percent,
                "threshold": alert.threshold,
                "current_version": alert.current_version,
                "baseline_version": alert.baseline_version
            })
        
        return jsonify(alerts_data)
    
    @app.route('/api/alerts')
    def get_all_alerts() -> Any:
        """Get all performance alerts across all prompts."""
        from prompt_versioner.monitoring import PerformanceMonitor
        
        all_alerts = []
        prompts = app.versioner.list_prompts()
        monitor = PerformanceMonitor(app.versioner)
        
        for prompt_name in prompts:
            versions = app.versioner.list_versions(prompt_name)
            if len(versions) < 2:
                continue
            
            latest = versions[0]
            previous = versions[1]
            
            alerts = monitor.check_regression(
                name=prompt_name,
                current_version=latest["version"],
                baseline_version=previous["version"]
            )
            
            for alert in alerts:
                all_alerts.append({
                    "prompt_name": prompt_name,
                    "type": alert.alert_type.value,
                    "message": alert.message,
                    "metric_name": alert.metric_name,
                    "baseline_value": alert.baseline_value,
                    "current_value": alert.current_value,
                    "change_percent": alert.change_percent,
                    "threshold": alert.threshold,
                    "current_version": alert.current_version,
                    "baseline_version": alert.baseline_version
                })
        
        return jsonify(all_alerts)
    
    @app.route('/api/prompts/<name>/export')
    def export_prompt_endpoint(name: str) -> Any:
        """Export a prompt to JSON file."""
        try:
            # Create temporary file
            temp_file = Path(tempfile.gettempdir()) / f"{name}.json"
            app.versioner.export_prompt(name, temp_file, format="json", include_metrics=True)
            
            return send_file(
                temp_file,
                as_attachment=True,
                download_name=f"{name}_export.json",
                mimetype='application/json'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/import', methods=['POST'])
    def import_prompt_endpoint() -> Any:
        """Import a prompt from uploaded JSON file."""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Save to temporary file
            temp_file = Path(tempfile.gettempdir()) / file.filename
            file.save(temp_file)
            
            # Import
            result = app.versioner.import_prompt(temp_file, overwrite=False)
            
            # Cleanup
            temp_file.unlink()
            
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/export-all')
    def export_all_endpoint() -> Any:
        """Export all prompts as ZIP."""
        import zipfile
        
        try:
            # Create temp directory
            temp_dir = Path(tempfile.gettempdir()) / "prompt_export"
            temp_dir.mkdir(exist_ok=True)
            
            # Export all prompts
            app.versioner.export_all(temp_dir, format="json")
            
            # Create ZIP
            zip_path = Path(tempfile.gettempdir()) / "all_prompts.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for json_file in temp_dir.glob("*.json"):
                    zipf.write(json_file, json_file.name)
            
            # Cleanup temp files
            for json_file in temp_dir.glob("*.json"):
                json_file.unlink()
            temp_dir.rmdir()
            
            return send_file(
                zip_path,
                as_attachment=True,
                download_name="all_prompts.zip",
                mimetype='application/zip'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app
