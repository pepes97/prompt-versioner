/**
 * Performance alerts management
 */

const Alerts = {
    /**
     * Toggle Alerts section
     */
    toggle() {
        const section = document.getElementById('alerts-section');
        const button = document.getElementById('alerts-toggle-btn');

        if (section.style.display === 'none') {
            section.style.display = 'block';
            button.textContent = '⚠️ Hide Alerts';
            button.classList.add('active');
            // Ricarica gli alert quando viene mostrata la sezione
            this.load();
        } else {
            section.style.display = 'none';
            button.textContent = '⚠️ Show Alerts';
            button.classList.remove('active');
        }
    },

    /**
     * Load all alerts from API
     */
    async load() {
        try {
            const alerts = await API.getAllAlerts();
            const container = document.getElementById('alerts-container');

            if (alerts.length === 0) {
                // Non nascondere la sezione, mostra messaggio di "nessun alert"
                container.innerHTML = '<div class="no-alerts">No performance alerts at this time</div>';
                return;
            }

            this.render(alerts);
        } catch (error) {
            console.error('Error loading alerts:', error);
            const container = document.getElementById('alerts-container');
            container.innerHTML = '<div class="alerts-error">Error loading alerts. Please try again.</div>';
        }
    },

    /**
     * Render alerts list
     */
    render(alerts) {
        const container = document.getElementById('alerts-container');

        container.innerHTML = alerts.map(alert => {
            const icon = Utils.getAlertIcon(alert.type);
            const severity = Utils.getAlertSeverity(alert.change_percent, alert.threshold);

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
    }
};

// Expose function globally
window.toggleAlerts = () => Alerts.toggle();
