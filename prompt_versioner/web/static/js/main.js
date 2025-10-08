/**
 * Main application initialization
 * 
 * This file coordinates all modules and initializes the dashboard
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme
    Theme.init();
    
    // Load initial data
    Prompts.load();
    Alerts.load();
});