/**
 * Prompt list management
 */

const Prompts = {
    allData: [],

    /**
     * Load all prompts from API
     */
    async load() {
        const list = document.getElementById('prompt-list');
        list.innerHTML = '<div class="loading">Loading prompts...</div>';

        try {
            const data = await API.getPrompts();

            this.allData = data.prompts;

            // Update stats
            document.getElementById('total-prompts').textContent = data.prompts.length;
            document.getElementById('total-versions').textContent = data.total_versions;
            document.getElementById('total-cost').textContent = data.total_cost?.toFixed(4) || '0.0000';
            document.getElementById('total-tokens').textContent = data.total_tokens?.toLocaleString() || '0';
            document.getElementById('total-calls').textContent = data.total_calls?.toLocaleString() || '0';

            this.render(this.allData);
        } catch (error) {
            console.error('Error loading prompts:', error);
            list.innerHTML = `
                <div class="empty-state">
                    <h3>Error loading prompts</h3>
                    <p>${error.message}</p>
                </div>
            `;
        }
    },

    /**
     * Render prompts list
     */
    render(prompts) {
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
                    <div style="flex: 1; cursor: pointer;" onclick="togglePrompt('${p.name}')">
                        <div class="prompt-name">${p.name}</div>
                        <div class="prompt-meta">
                            ${p.version_count} versions • Latest: ${p.latest_version}
                        </div>
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button
                            class="btn btn-secondary"
                            style="padding: 0.25rem 0.75rem; font-size: 0.75rem;"
                            onclick="event.stopPropagation(); ExportImport.exportSingle('${p.name}')"
                        >
                            Export
                        </button>
                        <button
                            class="delete-prompt-btn"
                            style="padding: 0.25rem 0.5rem; font-size: 0.75rem;"
                            onclick="event.stopPropagation(); deletePrompt('${p.name}')"
                            title="Elimina prompt completo"
                        >
                            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M6.5 7.5V14.5M10 7.5V14.5M13.5 7.5V14.5M3 5.5H17M8.5 3.5H11.5C12.0523 3.5 12.5 3.94772 12.5 4.5V5.5H7.5V4.5C7.5 3.94772 7.94772 3.5 8.5 3.5ZM4.5 5.5V15.5C4.5 16.0523 4.94772 16.5 5.5 16.5H14.5C15.0523 16.5 15.5 16.0523 15.5 15.5V5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    },

    /**
     * Filter prompts by search term
     */
    filter() {
        const searchTerm = document.getElementById('search-input').value.toLowerCase();

        const filtered = this.allData.filter(p =>
            p.name.toLowerCase().includes(searchTerm) ||
            p.latest_version.toLowerCase().includes(searchTerm)
        );

        this.render(filtered);
    },

    /**
     * Sort prompts by selected criteria
     */
    sort() {
        const sortBy = document.getElementById('sort-select').value;
        const searchTerm = document.getElementById('search-input').value.toLowerCase();

        let filtered = this.allData.filter(p =>
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

        this.render(filtered);
    },

    /**
     * Toggle prompt versions display
     */
    togglePrompt(promptName) {
        const versionSection = document.getElementById('version-section');

        // Se le versioni sono già visibili per questo stesso prompt, nascondile (toggle off)
        if (Versions.currentPrompt === promptName && versionSection.style.display === 'block') {
            versionSection.style.display = 'none';
            return;
        }

        // Altrimenti, mostra le versioni per questo prompt (i prompt rimangono visibili)
        versionSection.style.display = 'block';
        Versions.load(promptName);
    },

    /**
     * Delete a prompt and all its versions
     */
    async deletePrompt(promptName) {
        if (!confirm(`Sei sicuro di voler eliminare il prompt "${promptName}" e TUTTE le sue versioni?\n\nQuesta azione è irreversibile!`)) {
            return;
        }

        try {
            const response = await fetch(`/api/prompts/${encodeURIComponent(promptName)}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (data.success) {
                // Nascondi le versioni se erano visibili per questo prompt
                if (Versions.currentPrompt === promptName) {
                    document.getElementById('version-section').style.display = 'none';
                }
                // Ricarica la lista dei prompt
                this.load();
            } else {
                alert('Errore: ' + (data.error || 'Impossibile eliminare il prompt'));
            }
        } catch (error) {
            alert('Errore di rete: ' + error.message);
        }
    },
};

// Expose functions globally for inline handlers
window.filterPrompts = () => Prompts.filter();
window.sortPrompts = () => Prompts.sort();
window.togglePrompt = (name) => Prompts.togglePrompt(name);
window.deletePrompt = (name) => Prompts.deletePrompt(name);
