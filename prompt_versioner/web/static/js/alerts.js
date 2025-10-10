/**
 * Performance alerts management
 */

const Alerts = {
    /**
     * Load all alerts from API
     */
    async load() {
        try {
            const alerts = await API.getAllAlerts();

            if (alerts.length === 0) {
                document.getElementById('alerts-section').style.display = 'none';
                return;
            }

            document.getElementById('alerts-section').style.display = 'block';
            this.render(alerts);
        } catch (error) {
            console.error('Error loading alerts:', error);
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
