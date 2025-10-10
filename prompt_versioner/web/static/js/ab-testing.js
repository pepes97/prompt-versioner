/**
 * A/B Testing comparison logic
 */

const ABTesting = {
    /**
     * Load A/B test options for a prompt
     */
    async loadOptions(promptName) {
        try {
            const versions = await API.getABTestOptions(promptName);

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
    },

    /**
     * Run A/B test comparison
     */
    async run() {
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
            const data = await API.compareVersions(Versions.currentPrompt, versionA, versionB, metric);
            this.renderResults(data, versionA, versionB, metric);
        } catch (error) {
            resultsDiv.innerHTML = '<div class="empty-state"><h3>Error running comparison</h3></div>';
        }
    },

    /**
     * Render A/B test results
     */
    renderResults(data, versionA, versionB, metric) {
        const metricLabels = {
            'quality_score': 'Quality Score',
            'cost': 'Cost (USD)',
            'latency': 'Latency (ms)',
            'accuracy': 'Accuracy'
        };

        const metricLabel = metricLabels[metric];
        const isWinnerA = data.winner === versionA;

        const resultsDiv = document.getElementById('ab-test-results');
        resultsDiv.innerHTML = `
            <div class="ab-comparison">
                <div class="ab-version-card ${isWinnerA ? 'winner' : ''}">
                    ${isWinnerA ? '<div class="ab-winner-badge">🏆 Winner</div>' : ''}
                    <h3 style="color: #38bdf8; margin-bottom: 1rem;">Version A: ${versionA}</h3>
                    <div style="font-size: 2rem; font-weight: bold; color: #38bdf8; margin-bottom: 1rem;">
                        ${Utils.formatMetricValue(data.value_a, metric)}
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
                        ${Utils.formatMetricValue(data.value_b, metric)}
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
    }
};

// Expose globally
window.runABTest = () => ABTesting.run();
