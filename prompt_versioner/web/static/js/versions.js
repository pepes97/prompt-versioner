/**
 * Version display and diff management
 */

const Versions = {
    currentPrompt: null,

    /**
     * Load versions for a specific prompt
     */
    async load(promptName) {
        this.currentPrompt = promptName;
        document.getElementById('version-title').textContent = `Versions of "${promptName}"`;
        document.getElementById('version-section').style.display = 'block';
        
        const list = document.getElementById('version-list');
        list.innerHTML = '<div class="loading">Loading versions...</div>';
        
        try {
            const versions = await API.getVersionsWithDiffs(promptName);
            this.render(versions);
            ABTesting.loadOptions(promptName);
        } catch (error) {
            list.innerHTML = '<div class="empty-state"><h3>Error loading versions</h3></div>';
        }
    },

    /**
     * Render version list with diffs and metrics
     */
    render(versions) {
        const list = document.getElementById('version-list');
        
        list.innerHTML = versions.map(v => {
            const metricsHtml = this.renderMetrics(v.metrics_summary);
            const diffBadge = v.has_changes ? '<span class="diff-badge">Modified</span>' : '';
            const modelBadge = v.model_name ? `<span class="model-badge">${v.model_name}</span>` : '';
            const annotationsHtml = this.renderAnnotations(v.annotations);
            const systemPromptHtml = Utils.renderDiff(v.system_diff);
            const userPromptHtml = Utils.renderDiff(v.user_diff);
            
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
    },

    /**
     * Render metrics grid
     */
    renderMetrics(summary) {
        if (!summary || summary.call_count === 0) {
            return '';
        }

        return `
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">Calls</div>
                    <div class="metric-value">${summary.call_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Avg Tokens</div>
                    <div class="metric-value">${Math.round(summary.avg_total_tokens || 0)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Total Cost</div>
                    <div class="metric-value">€${(summary.total_cost || 0).toFixed(4)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Avg Latency</div>
                    <div class="metric-value">${Math.round(summary.avg_latency || 0)}<span class="metric-unit">ms</span></div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Quality</div>
                    <div class="metric-value">${((summary.avg_quality || 0) * 100).toFixed(0)}<span class="metric-unit">%</span></div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value">${((summary.success_rate || 0) * 100).toFixed(0)}<span class="metric-unit">%</span></div>
                </div>
            </div>
        `;
    },

    /**
     * Render annotations/comments
     */
    renderAnnotations(annotations) {
        if (!annotations || annotations.length === 0) {
            return '';
        }

        const items = annotations.map(ann => `
            <div class="annotation-item">
                <div class="annotation-author">${Utils.escapeHtml(ann.author)}</div>
                <div class="annotation-text">${Utils.escapeHtml(ann.text)}</div>
                <div class="annotation-time">${new Date(ann.timestamp).toLocaleString()}</div>
            </div>
        `).join('');
        
        return `
            <div class="annotations-section">
                <div class="annotations-header">
                    💬 Comments
                    <span class="annotation-badge">${annotations.length}</span>
                </div>
                ${items}
            </div>
        `;
    }
};

// Expose globally
window.loadVersions = (name) => Versions.load(name);