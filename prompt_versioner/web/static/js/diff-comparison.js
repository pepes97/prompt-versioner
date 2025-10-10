/**
 * Version Comparison and Diff Management
 */

const DiffComparison = {

    /**
     * Toggle A/B Testing section
     */
    toggleABTesting() {
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
     * Toggle Version Comparison section
     */
    toggleVersionComparison() {
        const section = document.getElementById('diff-section');
        const button = document.getElementById('diff-toggle-btn');

        if (section.style.display === 'none') {
            section.style.display = 'block';
            button.textContent = '🔄 Hide Comparison';
            button.classList.add('active');
            this.loadPromptsForDiff();
        } else {
            section.style.display = 'none';
            button.textContent = '🔄 Compare Versions';
            button.classList.remove('active');
        }
    },

    /**
     * Load prompts for diff comparison (only those with 2+ versions)
     */
    async loadPromptsForDiff() {
        try {
            const response = await fetch('/api/prompts');
            const data = await response.json();

            const select = document.getElementById('diff-prompt-select');
            const versionASelect = document.getElementById('diff-version-a-select');
            const versionBSelect = document.getElementById('diff-version-b-select');
            const resultsDiv = document.getElementById('diff-results');

            // Reset all selectors
            select.innerHTML = '<option value="">Select prompt...</option>';
            versionASelect.innerHTML = '<option value="">📊 Select BASELINE version (old)...</option>';
            versionBSelect.innerHTML = '<option value="">🆚 Select COMPARISON version (new)...</option>';

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
                        const versionsData = await versionsResponse.json();

                        // versionsData is directly an array of versions, not an object with .versions property
                        if (Array.isArray(versionsData) && versionsData.length >= 2) {
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
                    select.appendChild(option);
                });

                // Show message if no prompts have multiple versions
                if (promptsWithMultipleVersions.length === 0) {
                    const option = document.createElement('option');
                    option.value = "";
                    option.textContent = "No prompts with 2+ versions available";
                    option.disabled = true;
                    select.appendChild(option);
                }
            }
        } catch (error) {
            console.error('Error loading prompts for diff:', error);
        }
    },

    /**
     * Load versions for selected prompt in diff
     */
    async loadVersionsForDiff() {
        const promptName = document.getElementById('diff-prompt-select').value;
        const versionASelect = document.getElementById('diff-version-a-select');
        const versionBSelect = document.getElementById('diff-version-b-select');
        const resultsDiv = document.getElementById('diff-results');

        console.log('loadVersionsForDiff called with prompt:', promptName);

        // Clear version selects with clearer labels
        versionASelect.innerHTML = '<option value="">📊 Select BASELINE version (old)...</option>';
        versionBSelect.innerHTML = '<option value="">🆚 Select COMPARISON version (new)...</option>';

        // Clear previous results
        if (resultsDiv) {
            resultsDiv.innerHTML = '';
        }

        if (!promptName) {
            console.log('No prompt name selected, returning');
            return;
        }

        try {
            console.log('Fetching versions for prompt:', promptName);
            const response = await fetch(`/api/prompts/${encodeURIComponent(promptName)}/versions`);
            console.log('Response status:', response.status, response.statusText);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const versions = await response.json();
            console.log('Received versions:', versions);

            if (!Array.isArray(versions)) {
                console.error('Expected array of versions, got:', typeof versions, versions);
                return;
            }

            console.log('Number of versions found:', versions.length);

            // Sort versions by version number (newer first)
            versions.sort((a, b) => {
                const versionA = parseFloat(a.version) || 0;
                const versionB = parseFloat(b.version) || 0;
                return versionB - versionA;
            });

            versions.forEach((version, index) => {
                const model = version.model_name || version.model || 'N/A';
                const isLatest = index === 0;
                const versionLabel = `v${version.version} (${this.formatDate(version.timestamp || version.created_at)}) - ${model}${isLatest ? ' [LATEST]' : ''}`;

                console.log(`Adding version ${version.version} to dropdowns:`, versionLabel);

                const optionA = document.createElement('option');
                optionA.value = version.version;
                optionA.textContent = versionLabel;
                versionASelect.appendChild(optionA);
                console.log('Added to baseline select:', optionA.value, optionA.textContent);

                const optionB = document.createElement('option');
                optionB.value = version.version;
                optionB.textContent = versionLabel;
                versionBSelect.appendChild(optionB);
                console.log('Added to comparison select:', optionB.value, optionB.textContent);
            });

            // Auto-select suggestions if there are at least 2 versions
            if (versions.length >= 2) {
                // Suggest latest as comparison (B) and previous as baseline (A)
                versionBSelect.value = versions[0].version; // Latest
                versionASelect.value = versions[1].version; // Previous
                console.log('Auto-selected versions:', {
                    baseline: versions[1].version,
                    comparison: versions[0].version
                });
            }

            console.log('Version loading completed successfully');
        } catch (error) {
            console.error('Error loading versions for diff:', error);
            console.error('Error details:', error.message, error.stack);
        }
    },

    /**
     * Compare selected versions
     */
    async compareDiffVersions() {
        const promptName = document.getElementById('diff-prompt-select').value;
        const versionA = document.getElementById('diff-version-a-select').value;
        const versionB = document.getElementById('diff-version-b-select').value;
        const resultsDiv = document.getElementById('diff-results');

        if (!promptName || !versionA || !versionB) {
            alert('Please select a prompt, a baseline version, and a comparison version');
            return;
        }

        if (versionA === versionB) {
            alert('Please select different versions for baseline and comparison');
            return;
        }

        this.showLoading(resultsDiv, '🔄 Comparing baseline vs comparison versions...');

        try {
            // Load both versions and diff data in parallel
            const [versionAResponse, versionBResponse, diffResponse] = await Promise.all([
                fetch(`/api/prompts/${encodeURIComponent(promptName)}/versions/${versionA}`),
                fetch(`/api/prompts/${encodeURIComponent(promptName)}/versions/${versionB}`),
                fetch(`/api/prompts/${encodeURIComponent(promptName)}/diff?version1=${versionA}&version2=${versionB}`)
            ]);

            if (!versionAResponse.ok || !versionBResponse.ok) {
                throw new Error('Error loading version data');
            }

            const versionAData = await versionAResponse.json();
            const versionBData = await versionBResponse.json();

            // Debug logging per il confronto
            console.log(`Comparison data loaded:`, {
                promptName,
                versionA: {
                    version: versionA,
                    model_name: versionAData.model_name,
                    model: versionAData.model,
                    id: versionAData.id,
                    data: versionAData
                },
                versionB: {
                    version: versionB,
                    model_name: versionBData.model_name,
                    model: versionBData.model,
                    id: versionBData.id,
                    data: versionBData
                }
            });

            let diffData = null;
            if (diffResponse.ok) {
                diffData = await diffResponse.json();
            }

            const comparison = {
                version_a: versionAData,
                version_b: versionBData,
                diffs: diffData
            };

            this.displayDiffResults(comparison);
        } catch (error) {
            console.error('Error comparing versions:', error);
            this.showError(resultsDiv, 'Error loading comparison', error.message);
        }
    },

    /**
     * Display diff comparison results
     */
    displayDiffResults(comparison) {
        const resultsDiv = document.getElementById('diff-results');

        if (!comparison || !comparison.version_a || !comparison.version_b) {
            this.showError(resultsDiv, 'No comparison data available', 'Please select valid versions to compare.');
            return;
        }

        const { version_a, version_b, diffs } = comparison;

        // Calculate detailed word-level diff for display (version_a = baseline, version_b = comparison)
        const systemDiff = this.calculateDetailedDiff(
            version_a.system_prompt || '',
            version_b.system_prompt || ''
        );
        const userDiff = this.calculateDetailedDiff(
            version_a.user_prompt || '',
            version_b.user_prompt || ''
        );

        // Create comparison using template
        const template = document.getElementById('diff-comparison-template');
        const clone = template.content.cloneNode(true);

        // Populate baseline version (A)
        const baselineCard = clone.querySelector('.diff-version-card.baseline');
        baselineCard.querySelector('.version-number').textContent = version_a.version;
        baselineCard.querySelector('.version-date').textContent = this.formatDate(version_a.timestamp || version_a.created_at);
        baselineCard.querySelector('.version-model-badge').textContent = version_a.model_name || version_a.model || 'N/A';
        baselineCard.querySelector('.system-prompt-content').textContent = version_a.system_prompt || 'N/A';
        baselineCard.querySelector('.user-prompt-content').textContent = version_a.user_prompt || 'N/A';

        // Populate comparison version (B)
        const comparisonCard = clone.querySelector('.diff-version-card.comparison');
        comparisonCard.querySelector('.version-number').textContent = version_b.version;
        comparisonCard.querySelector('.version-date').textContent = this.formatDate(version_b.timestamp || version_b.created_at);
        comparisonCard.querySelector('.version-model-badge').textContent = version_b.model_name || version_b.model || 'N/A';
        comparisonCard.querySelector('.system-prompt-content').textContent = version_b.system_prompt || 'N/A';
        comparisonCard.querySelector('.user-prompt-content').textContent = version_b.user_prompt || 'N/A';

        // Add changes section
        const changesSection = clone.querySelector('.diff-changes-section');
        const changesElement = this.createDiffChanges(systemDiff, userDiff, diffs);

        // Add metrics comparison
        this.populateMetricsComparison(changesElement, version_a, version_b);

        changesSection.appendChild(changesElement);

        resultsDiv.innerHTML = '';
        resultsDiv.appendChild(clone);
    },

    /**
     * Create diff changes section using templates
     */
    createDiffChanges(systemDiff, userDiff, diffStats) {
        if (!systemDiff.hasChanges && !userDiff.hasChanges) {
            const template = document.getElementById('no-changes-template');
            return template.content.cloneNode(true);
        }

        const template = document.getElementById('diff-changes-template');
        const clone = template.content.cloneNode(true);

        // Show system changes if any
        if (systemDiff.hasChanges) {
            const systemSection = clone.querySelector('.system-changes-section');
            systemSection.style.display = 'block';
            const systemChangesContainer = systemSection.querySelector('.system-changes');
            systemChangesContainer.innerHTML = ''; // Clear previous content
            this.populateWordLevelDiff(systemChangesContainer, systemDiff);
        }

        // Show user changes if any
        if (userDiff.hasChanges) {
            const userSection = clone.querySelector('.user-changes-section');
            userSection.style.display = 'block';
            const userChangesContainer = userSection.querySelector('.user-changes');
            userChangesContainer.innerHTML = ''; // Clear previous content
            this.populateWordLevelDiff(userChangesContainer, userDiff);
        }

        // Show similarity stats if available
        if (diffStats && diffStats.summary) {
            const similaritySection = clone.querySelector('.similarity-section');
            similaritySection.style.display = 'block';

            if (diffStats.system_similarity !== undefined) {
                clone.querySelector('.system-similarity').textContent = `${(diffStats.system_similarity * 100).toFixed(1)}%`;
            }
            if (diffStats.user_similarity !== undefined) {
                clone.querySelector('.user-similarity').textContent = `${(diffStats.user_similarity * 100).toFixed(1)}%`;
            }
            if (diffStats.total_similarity !== undefined) {
                clone.querySelector('.total-similarity').textContent = `${(diffStats.total_similarity * 100).toFixed(1)}%`;
            }
        }

        return clone;
    },

    /**
     * Calculate word-level and character-level diff between two texts
     */
    calculateDetailedDiff(oldText, newText) {
        if (oldText === newText) {
            return { hasChanges: false, chunks: [{ type: 'unchanged', content: oldText }] };
        }

        // Split texts into words while preserving whitespace
        const oldWords = this.splitIntoWords(oldText);
        const newWords = this.splitIntoWords(newText);

        const chunks = [];
        let oldIndex = 0;
        let newIndex = 0;

        while (oldIndex < oldWords.length || newIndex < newWords.length) {
            if (oldIndex >= oldWords.length) {
                // Only new words left - all added
                chunks.push({ type: 'added', content: newWords.slice(newIndex).join('') });
                break;
            } else if (newIndex >= newWords.length) {
                // Only old words left - all removed
                chunks.push({ type: 'removed', content: oldWords.slice(oldIndex).join('') });
                break;
            } else if (oldWords[oldIndex] === newWords[newIndex]) {
                // Words are the same
                chunks.push({ type: 'unchanged', content: oldWords[oldIndex] });
                oldIndex++;
                newIndex++;
            } else {
                // Words are different - find next matching point
                const nextMatch = this.findNextMatch(oldWords, newWords, oldIndex, newIndex);

                if (nextMatch.oldNext === -1 && nextMatch.newNext === -1) {
                    // No more matches - rest is all changed
                    const oldRest = oldWords.slice(oldIndex).join('');
                    const newRest = newWords.slice(newIndex).join('');

                    if (oldRest) chunks.push({ type: 'removed', content: oldRest });
                    if (newRest) chunks.push({ type: 'added', content: newRest });
                    break;
                } else {
                    // Add removed content
                    if (nextMatch.oldNext > oldIndex) {
                        const removedContent = oldWords.slice(oldIndex, nextMatch.oldNext).join('');
                        chunks.push({ type: 'removed', content: removedContent });
                    }

                    // Add added content
                    if (nextMatch.newNext > newIndex) {
                        const addedContent = newWords.slice(newIndex, nextMatch.newNext).join('');
                        chunks.push({ type: 'added', content: addedContent });
                    }

                    oldIndex = nextMatch.oldNext;
                    newIndex = nextMatch.newNext;
                }
            }
        }

        return {
            hasChanges: chunks.some(chunk => chunk.type !== 'unchanged'),
            chunks: chunks
        };
    },

    /**
     * Split text into words while preserving whitespace
     */
    splitIntoWords(text) {
        if (!text) return [];

        const words = [];
        let currentWord = '';

        for (let i = 0; i < text.length; i++) {
            const char = text[i];

            if (/\s/.test(char)) {
                // Whitespace character
                if (currentWord) {
                    words.push(currentWord);
                    currentWord = '';
                }
                words.push(char);
            } else if (/[.,!?;:()[\]{}'""]/.test(char)) {
                // Punctuation
                if (currentWord) {
                    words.push(currentWord);
                    currentWord = '';
                }
                words.push(char);
            } else {
                // Regular character
                currentWord += char;
            }
        }

        if (currentWord) {
            words.push(currentWord);
        }

        return words;
    },

    /**
     * Find next matching point between two word arrays
     */
    findNextMatch(oldWords, newWords, oldStart, newStart) {
        const maxLookAhead = Math.min(10, Math.min(oldWords.length - oldStart, newWords.length - newStart));

        for (let distance = 1; distance <= maxLookAhead; distance++) {
            // Look ahead in old words
            if (oldStart + distance < oldWords.length) {
                const oldWord = oldWords[oldStart + distance];
                for (let j = newStart; j < Math.min(newStart + distance + 3, newWords.length); j++) {
                    if (newWords[j] === oldWord) {
                        return { oldNext: oldStart + distance, newNext: j };
                    }
                }
            }

            // Look ahead in new words
            if (newStart + distance < newWords.length) {
                const newWord = newWords[newStart + distance];
                for (let j = oldStart; j < Math.min(oldStart + distance + 3, oldWords.length); j++) {
                    if (oldWords[j] === newWord) {
                        return { oldNext: j, newNext: newStart + distance };
                    }
                }
            }
        }

        return { oldNext: -1, newNext: -1 };
    },



    /**
     * Format word-level diff with inline highlighting
     */
    /**
     * Populate word-level diff directly in container
     */
    populateWordLevelDiff(container, diff) {
        container.innerHTML = ''; // Clear previous content

        if (!diff.hasChanges) {
            const noChangesDiv = document.createElement('div');
            noChangesDiv.className = 'no-changes-inline';
            noChangesDiv.style.cssText = 'color: #10b981; font-style: italic;';
            noChangesDiv.textContent = 'No changes detected';
            container.appendChild(noChangesDiv);
            return;
        }

        // Create diff content directly in the container
        diff.chunks.forEach(chunk => {
            const span = document.createElement('span');
            span.textContent = chunk.content;
            span.className = chunk.type; // 'added', 'removed', 'unchanged'
            container.appendChild(span);
        });

        // Add summary of changes
        const addedChunks = diff.chunks.filter(c => c.type === 'added');
        const removedChunks = diff.chunks.filter(c => c.type === 'removed');

        if (addedChunks.length > 0 || removedChunks.length > 0) {
            const summaryDiv = document.createElement('div');
            summaryDiv.className = 'diff-summary';
            summaryDiv.style.cssText = 'margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #334155; font-size: 0.8rem; color: #94a3b8;';

            const summaryText = document.createElement('strong');
            summaryText.textContent = 'Summary: ';
            summaryDiv.appendChild(summaryText);

            if (addedChunks.length > 0) {
                const addedText = addedChunks.map(c => c.content).join('').trim();
                const addedWords = addedText.split(/\s+/).filter(w => w.length > 0).length;
                const addedSpan = document.createElement('span');
                addedSpan.style.color = '#10b981';
                addedSpan.textContent = `+${addedWords} words added`;
                summaryDiv.appendChild(addedSpan);
            }

            if (addedChunks.length > 0 && removedChunks.length > 0) {
                summaryDiv.appendChild(document.createTextNode(', '));
            }

            if (removedChunks.length > 0) {
                const removedText = removedChunks.map(c => c.content).join('').trim();
                const removedWords = removedText.split(/\s+/).filter(w => w.length > 0).length;
                const removedSpan = document.createElement('span');
                removedSpan.style.color = '#ef4444';
                removedSpan.textContent = `-${removedWords} words removed`;
                summaryDiv.appendChild(removedSpan);
            }

            container.appendChild(summaryDiv);
        }
    },

    /**
     * Show error message using template
     */
    showError(container, title, message) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('error-message-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.error-title').textContent = title;
        clone.querySelector('.error-text').textContent = message;

        container.appendChild(clone);
    },

    /**
     * Show loading message using template
     */
    showLoading(container, message) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('loading-message-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.loading-text').textContent = message;

        container.appendChild(clone);
    },

    /**
     * Show no content message using template
     */
    showNoContent(container, message) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('no-content-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.no-content-text').textContent = message;

        container.appendChild(clone);
    },

    /**
     * Show A/B test results using template
     */
    showABResults(container, versionA, versionB, versionAData, versionBData, metric, metricA, metricB) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('ab-results-template');
        const clone = template.content.cloneNode(true);

        // Populate version A data
        const versionACard = clone.querySelectorAll('.ab-version-result-card')[0];
        versionACard.querySelector('.ab-version-number').textContent = `v${versionA}`;
        versionACard.querySelector('.ab-metric-value').innerHTML = `${this.getMetricLabel(metric)}: <strong>${this.formatMetricValue(metricA, metric)}</strong>`;

        const modelInfoA = versionACard.querySelector('.ab-model-info');
        if (versionAData.model_name) {
            modelInfoA.textContent = `Model: ${versionAData.model_name}`;
        } else {
            modelInfoA.style.display = 'none';
        }

        // Populate version B data
        const versionBCard = clone.querySelectorAll('.ab-version-result-card')[1];
        versionBCard.querySelector('.ab-version-number').textContent = `v${versionB}`;
        versionBCard.querySelector('.ab-metric-value').innerHTML = `${this.getMetricLabel(metric)}: <strong>${this.formatMetricValue(metricB, metric)}</strong>`;

        const modelInfoB = versionBCard.querySelector('.ab-model-info');
        if (versionBData.model_name) {
            modelInfoB.textContent = `Model: ${versionBData.model_name}`;
        } else {
            modelInfoB.style.display = 'none';
        }

        // Calculate and populate summary
        const improvement = this.calculateImprovement(metricA, metricB, metric);
        const winner = improvement > 0 ? 'B' : 'A';
        const improvementText = Math.abs(improvement).toFixed(2);

        const summary = clone.querySelector('.ab-summary');
        summary.className = `ab-summary ${improvement > 0 ? 'success' : 'error'}`;

        const winnerText = clone.querySelector('.ab-winner-text');
        winnerText.className = `ab-winner-text ${improvement > 0 ? 'success' : 'error'}`;
        winnerText.textContent = `🏆 Winner: Version ${winner}`;

        const improvementTextEl = clone.querySelector('.ab-improvement-text');
        improvementTextEl.textContent = `${improvementText}% ${improvement > 0 ? 'improvement' : 'decline'} in ${this.getMetricLabel(metric).toLowerCase()}`;

        container.appendChild(clone);
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
     * Load versions for selected prompt in A/B testing
     */
    async loadVersionsForAB() {
        const promptName = document.getElementById('ab-prompt-select').value;
        const versionASelect = document.getElementById('ab-version-a-select');
        const versionBSelect = document.getElementById('ab-version-b-select');
        const resultsDiv = document.getElementById('ab-test-results');

        // Clear version selects
        versionASelect.innerHTML = '<option value="">📊 Select Version A (baseline)...</option>';
        versionBSelect.innerHTML = '<option value="">🆚 Select Version B (comparison)...</option>';

        // Clear results
        if (resultsDiv) {
            resultsDiv.innerHTML = '';
        }

        if (!promptName) {
            return;
        }

        try {
            const response = await fetch(`/api/prompts/${promptName}/versions`);
            const versions = await response.json();

            if (Array.isArray(versions)) {
                // Sort versions by creation date (newest first)
                versions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

                versions.forEach((version, index) => {
                    const modelDisplay = version.model_name ? ` (${version.model_name})` : '';

                    const optionA = document.createElement('option');
                    optionA.value = version.version;
                    optionA.textContent = `v${version.version}${modelDisplay}`;
                    versionASelect.appendChild(optionA);

                    const optionB = document.createElement('option');
                    optionB.value = version.version;
                    optionB.textContent = `v${version.version}${modelDisplay}`;
                    versionBSelect.appendChild(optionB);
                });

                // Auto-select the two most recent versions if available
                if (versions.length >= 2) {
                    versionASelect.value = versions[1].version; // Second most recent as baseline
                    versionBSelect.value = versions[0].version; // Most recent as comparison
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
        const metric = document.getElementById('ab-metric-select').value;
        const resultsDiv = document.getElementById('ab-test-results');

        if (!promptName || !versionA || !versionB || !metric) {
            this.showError(resultsDiv, 'Missing Selection', 'Please select prompt, both versions, and a metric');
            return;
        }

        if (versionA === versionB) {
            this.showError(resultsDiv, 'Invalid Selection', 'Please select different versions for comparison');
            return;
        }

        try {
            this.showLoading(resultsDiv, 'Loading A/B test comparison...');

            // Get metrics for both versions
            const [versionAResponse, versionBResponse] = await Promise.all([
                fetch(`/api/prompts/${promptName}/versions/${versionA}`),
                fetch(`/api/prompts/${promptName}/versions/${versionB}`)
            ]);

            const versionAData = await versionAResponse.json();
            const versionBData = await versionBResponse.json();

            // Calculate metric comparison
            const metricA = this.getMetricValue(versionAData, metric);
            const metricB = this.getMetricValue(versionBData, metric);

            const improvement = this.calculateImprovement(metricA, metricB, metric);

            // Display results using template
            this.showABResults(resultsDiv, versionA, versionB, versionAData, versionBData, metric, metricA, metricB);

        } catch (error) {
            console.error('Error running A/B test:', error);
            this.showError(resultsDiv, 'A/B Test Error', 'Error running A/B test. Please try again.');
        }
    },

    /**
     * Helper methods for A/B testing
     */
    getMetricValue(versionData, metric) {
        const summary = versionData.metrics_summary || {};
        switch (metric) {
            case 'quality_score': return summary.avg_quality || 0;
            case 'cost': return summary.total_cost || 0;
            case 'latency': return summary.avg_latency || 0;
            case 'accuracy': return summary.avg_accuracy || 0;
            default: return 0;
        }
    },

    calculateImprovement(valueA, valueB, metric) {
        if (valueA === 0) return 0;

        // For cost and latency, lower is better, so we invert the calculation
        if (metric === 'cost' || metric === 'latency') {
            return ((valueA - valueB) / valueA) * 100;
        } else {
            // For quality_score and accuracy, higher is better
            return ((valueB - valueA) / valueA) * 100;
        }
    },

    getMetricLabel(metric) {
        const labels = {
            'quality_score': 'Quality Score',
            'cost': 'Cost (EUR)',
            'latency': 'Latency (ms)',
            'accuracy': 'Accuracy'
        };
        return labels[metric] || metric;
    },

    formatMetricValue(value, metric) {
        switch (metric) {
            case 'cost': return `€${value.toFixed(4)}`;
            case 'latency': return `${value.toFixed(0)}ms`;
            case 'quality_score':
            case 'accuracy': return value.toFixed(2);
            default: return value.toString();
        }
    },

    /**
     * Populate metrics comparison section
     */
    populateMetricsComparison(changesElement, versionA, versionB) {
        const metricsSection = changesElement.querySelector('.metrics-comparison-section');
        if (!metricsSection) return;

        const metricsA = versionA.metrics_summary || {};
        const metricsB = versionB.metrics_summary || {};

        // Cost comparison (total_cost from metrics summary)
        this.populateMetricComparison(metricsSection, 'cost',
            metricsA.total_cost || 0, metricsB.total_cost || 0,
            (val) => `€${val.toFixed(4)}`, 'lower');

        // Input tokens comparison (avg_input_tokens from metrics summary)
        this.populateMetricComparison(metricsSection, 'input-tokens',
            metricsA.avg_input_tokens || 0, metricsB.avg_input_tokens || 0,
            (val) => Math.round(val).toLocaleString(), 'neutral');

        // Output tokens comparison (avg_output_tokens from metrics summary)
        this.populateMetricComparison(metricsSection, 'output-tokens',
            metricsA.avg_output_tokens || 0, metricsB.avg_output_tokens || 0,
            (val) => Math.round(val).toLocaleString(), 'neutral');

        // Latency comparison (avg_latency from metrics summary)
        this.populateMetricComparison(metricsSection, 'latency',
            metricsA.avg_latency || 0, metricsB.avg_latency || 0,
            (val) => `${val.toFixed(0)}ms`, 'lower');
    },

    /**
     * Populate individual metric comparison
     */
    populateMetricComparison(container, metricName, baselineValue, comparisonValue, formatter, betterDirection) {
        const baselineEl = container.querySelector(`.${metricName}-baseline`);
        const comparisonEl = container.querySelector(`.${metricName}-comparison`);
        const changeEl = container.querySelector(`.${metricName}-change`);

        if (!baselineEl || !comparisonEl || !changeEl) return;

        baselineEl.textContent = formatter(baselineValue);
        comparisonEl.textContent = formatter(comparisonValue);

        // Calculate change
        let changePercent = 0;
        let changeClass = 'neutral';
        let changeText = 'No change';

        if (baselineValue > 0) {
            changePercent = ((comparisonValue - baselineValue) / baselineValue) * 100;

            if (Math.abs(changePercent) < 0.1) {
                changeClass = 'neutral';
                changeText = '±0%';
            } else {
                const sign = changePercent > 0 ? '+' : '';
                changeText = `${sign}${changePercent.toFixed(1)}%`;

                // Determine if change is good or bad based on metric type
                if (betterDirection === 'lower') {
                    changeClass = changePercent < 0 ? 'positive' : 'negative';
                } else if (betterDirection === 'higher') {
                    changeClass = changePercent > 0 ? 'positive' : 'negative';
                } else {
                    changeClass = 'neutral';
                }
            }
        }

        changeEl.textContent = changeText;
        changeEl.className = `metric-change ${changeClass}`;
    },

    /**
     * Format date utility
     */
    formatDate(dateString) {
        if (!dateString) {
            return 'Data non disponibile';
        }

        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                return 'Data non valida';
            }

            return date.toLocaleDateString('it-IT', {
                day: '2-digit',
                month: '2-digit',
                year: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            console.warn('Errore nel formato data:', dateString, error);
            return 'Data non valida';
        }
    },

    /**
     * Escape HTML utility
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Expose functions globally
window.DiffComparison = DiffComparison;
window.toggleABTesting = () => DiffComparison.toggleABTesting();
window.toggleVersionComparison = () => DiffComparison.toggleVersionComparison();
window.loadVersionsForDiff = () => DiffComparison.loadVersionsForDiff();
window.compareDiffVersions = () => DiffComparison.compareDiffVersions();
window.runABTest = () => DiffComparison.runABTest();
