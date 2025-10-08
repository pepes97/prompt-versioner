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
                    <div style="flex: 1; cursor: pointer;" onclick="Versions.load('${p.name}')">
                        <div class="prompt-name">${p.name}</div>
                        <div class="prompt-meta">
                            ${p.version_count} versions • Latest: ${p.latest_version}
                        </div>
                    </div>
                    <button 
                        class="btn btn-secondary" 
                        style="padding: 0.25rem 0.75rem; font-size: 0.75rem;"
                        onclick="event.stopPropagation(); ExportImport.exportSingle('${p.name}')"
                    >
                        Export
                    </button>
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
    }
};

// Expose functions globally for inline handlers
window.filterPrompts = () => Prompts.filter();
window.sortPrompts = () => Prompts.sort();