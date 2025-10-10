/**
 * A/B Testing comparison logic
 */

const ABTesting = {
    /**
     * Toggle A/B Testing section
     */
    toggle() {
        const section = document.getElementById('ab-test-section');
        const button = document.getElementById('ab-toggle-btn');

        if (section.style.display === 'none') {
            section.style.display = 'block';
            button.textContent = '🧪 Hide A/B Testing';
            button.classList.add('active');
            this.loadPromptsForAB();
        } else {
            section.style.display = 'none';
            button.textContent = '🧪 Enable A/B Testing';
            button.classList.remove('active');
        }
    },

    /**
     * Load prompts for A/B testing (only those with 2+ versions)
     */
    async loadPromptsForAB() {
        try {
            const response = await fetch('/api/prompts');
            const data = await response.json();

            const promptSelect = document.getElementById('ab-prompt-select');
            const versionASelect = document.getElementById('ab-version-a-select');
            const versionBSelect = document.getElementById('ab-version-b-select');
            const resultsDiv = document.getElementById('ab-test-results');

            // Reset all selectors
            promptSelect.innerHTML = '<option value="">Select prompt...</option>';
            versionASelect.innerHTML = '<option value="">📊 Select Version A (baseline)...</option>';
            versionBSelect.innerHTML = '<option value="">🆚 Select Version B (comparison)...</option>';

            // Clear results
            if (resultsDiv) {
                resultsDiv.innerHTML = '';
            }

            if (data.prompts) {
                // Filter prompts that have at least 2 versions
                const promptsWithMultipleVersions = [];

                for (const prompt of data.prompts) {
                    try {
                        const versionsResponse = await fetch(`/api/prompts/${prompt.name}/versions`);
                        const versions = await versionsResponse.json();

                        if (Array.isArray(versions) && versions.length >= 2) {
                            promptsWithMultipleVersions.push(prompt);
                        }
                    } catch (error) {
                        console.warn(`Error checking versions for prompt ${prompt.name}:`, error);
                    }
                }

                // Add only prompts with multiple versions to the select
                promptsWithMultipleVersions.forEach(prompt => {
                    const option = document.createElement('option');
                    option.value = prompt.name;
                    option.textContent = prompt.name;
                    promptSelect.appendChild(option);
                });

                // Show message if no prompts have multiple versions
                if (promptsWithMultipleVersions.length === 0) {
                    const option = document.createElement('option');
                    option.value = "";
                    option.textContent = "No prompts with 2+ versions available";
                    option.disabled = true;
                    promptSelect.appendChild(option);
                }
            }
        } catch (error) {
            console.error('Error loading prompts for A/B testing:', error);
        }
    },

    /**
     * Load versions for A/B testing when prompt is selected
     */
    async loadVersionsForAB() {
        const promptSelect = document.getElementById('ab-prompt-select');
        const selectedPrompt = promptSelect.value;

        if (!selectedPrompt) return;

        try {
            const response = await fetch(`/api/prompts/${selectedPrompt}/versions`);
            const versions = await response.json();

            const versionASelect = document.getElementById('ab-version-a-select');
            const versionBSelect = document.getElementById('ab-version-b-select');

            // Clear version selects with clearer labels
            versionASelect.innerHTML = '<option value="">📊 Select Version A (baseline)...</option>';
            versionBSelect.innerHTML = '<option value="">🆚 Select Version B (comparison)...</option>';

            if (Array.isArray(versions) && versions.length > 0) {
                versions.forEach((version, index) => {
                    const isLatest = index === 0;
                    const model = version.model_config ?
                        (typeof version.model_config === 'string' ?
                            JSON.parse(version.model_config).model || 'Unknown' :
                            version.model_config.model || 'Unknown')
                        : 'Unknown';

                    const versionLabel = `v${version.version} (${this.formatDate(version.timestamp || version.created_at)}) - ${model}${isLatest ? ' [LATEST]' : ''}`;

                    const optionA = document.createElement('option');
                    optionA.value = version.version;
                    optionA.textContent = versionLabel;
                    versionASelect.appendChild(optionA);

                    const optionB = document.createElement('option');
                    optionB.value = version.version;
                    optionB.textContent = versionLabel;
                    versionBSelect.appendChild(optionB);
                });

                // Auto-select latest as A and previous as B if available
                if (versions.length >= 2) {
                    versionASelect.value = versions[0].version;  // Latest
                    versionBSelect.value = versions[1].version;  // Previous
                }
            }
        } catch (error) {
            console.error('Error loading versions for A/B testing:', error);
        }
    },

    /**
     * Run A/B test comparison
     */
    async runABTest() {
        const promptName = document.getElementById('ab-prompt-select').value;
        const versionA = document.getElementById('ab-version-a-select').value;
        const versionB = document.getElementById('ab-version-b-select').value;
        const resultsDiv = document.getElementById('ab-test-results');

        if (!promptName || !versionA || !versionB) {
            this.showError(resultsDiv, 'Missing selection', 'Please select a prompt and both versions for comparison.');
            return;
        }

        if (versionA === versionB) {
            this.showError(resultsDiv, 'Same version selected', 'Please select different versions for A and B.');
            return;
        }

        try {
            // Show loading state
            this.showLoading(resultsDiv, 'Running A/B test comparison...');

            // Fetch version data for both versions
            const [versionAResponse, versionBResponse] = await Promise.all([
                fetch(`/api/prompts/${promptName}/versions/${versionA}`),
                fetch(`/api/prompts/${promptName}/versions/${versionB}`)
            ]);

            const versionAData = await versionAResponse.json();
            const versionBData = await versionBResponse.json();

            // Show A/B test results
            this.showABResults(resultsDiv, versionA, versionB, versionAData, versionBData);

        } catch (error) {
            console.error('Error running A/B test:', error);
            this.showError(resultsDiv, 'A/B test failed', 'Unable to run A/B test comparison.');
        }
    },

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
