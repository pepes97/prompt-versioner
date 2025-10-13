# Web Dashboard

Access **Prompt Versioner**'s web interface for visual prompt management and monitoring.

## 🌐 Quick Start

```python
from prompt_versioner import PromptVersioner

# Initialize with web dashboard support
pv = PromptVersioner(project_name="my-project", enable_git=False)

# Start the web dashboard
pv.start_dashboard(host="127.0.0.1", port=8080)
```

Then open your browser to: `http://localhost:8080`

## 🎛️ Dashboard Features

### Main Dashboard
- **Overview**: See all your prompts and their latest versions
- **Metrics**: Performance statistics
- **Version History**: Browse version changes over time
- **Comparisons**: Side-by-side version comparisons

### Prompt Management
- **View Prompts**: Browse all system and user prompts
- **Export**: Download prompt files
- **Annotations**: Add notes and documentation

### Performance Monitoring
- **Real-time Metrics**: Live performance data
- **Quality Trends**: Track quality scores over time
- **Cost Analysis**: Monitor usage costs

## 🚀 Starting the Dashboard

### Basic Setup

```python
from prompt_versioner import PromptVersioner

# Initialize versioner
pv = PromptVersioner(project_name="my-project")

# Start dashboard on default port (5000)
pv.start_dashboard()
print("Dashboard running at http://localhost:5000")
```

### Custom Configuration

```python
# Custom host and port
pv.start_dashboard(
    host="0.0.0.0",  # Allow external access
    port=8080,
    debug=False,      # Set True for development
    auto_open=True    # Automatically open browser
)
```

### Production Setup

```python
# Production configuration
pv.start_dashboard(
    host="0.0.0.0",
    port=80,
    debug=False,
    threaded=True,
    ssl_context="production"  # Enable HTTPS
)
```

## 📊 Dashboard Views

### Prompts Overview
```
┌─────────────────────────────────────────────────┐
│ 📝 PROMPTS OVERVIEW                            │
├─────────────────────────────────────────────────┤
│ customer_service  v2.1.0  ↗️ 0.92 quality      │
│ code_reviewer     v1.1.0  ↗️ 0.89 quality      │
│ summarizer        v1.2.0  ↘️ 0.85 quality      │
└─────────────────────────────────────────────────┘
```

### Version Details
```
┌─────────────────────────────────────────────────┐
│ 🔍 customer_service v2.1.0                     │
├─────────────────────────────────────────────────┤
│ Created: 2024-01-15 14:30                      │
│ Calls: 1,247                                   │
│ Avg Quality: 0.92                              │
│ Avg Latency: 425ms                             │
│ Success Rate: 98.4%                            │
│                                                 │
│ [View Code] [Edit] [Export] [Compare]          │
└─────────────────────────────────────────────────┘
```

## 🔧 Dashboard Configuration

### Custom Styling

The dashboard supports custom CSS and themes:

```python
# Custom dashboard configuration
dashboard_config = {
    "theme": "dark",           # "light" or "dark"
    "custom_css": "path/to/custom.css",
    "logo_url": "/static/logo.png",
    "title": "My AI Dashboard",
    "auto_refresh": 30,        # Refresh every 30 seconds
}

pv.start_dashboard(config=dashboard_config)
```

## 🔗 API Integration

### REST API Endpoints

The dashboard exposes REST API endpoints:

```bash
# Get all prompts
GET /api/prompts

# Get specific prompt versions
GET /api/prompts/{name}/versions

# Get metrics
GET /api/prompts/{name}/versions/{version}/metrics

# Create new version
POST /api/prompts/{name}/versions

# Update version
PUT /api/prompts/{name}/versions/{version}
```

### JavaScript Integration

```javascript
// Fetch prompt data from dashboard API
async function getPromptData(name) {
    const response = await fetch(`/api/prompts/${name}`);
    const data = await response.json();
    return data;
}

// Update metrics in real-time
async function updateMetrics(name, version) {
    const response = await fetch(`/api/prompts/${name}/versions/${version}/metrics`);
    const metrics = await response.json();

    // Update your custom UI
    updateDashboard(metrics);
}
```

## 🎯 Use Cases

### Development Workflow
1. **Edit prompts** through the web interface
2. **Test versions** with live preview
3. **Monitor performance** with real-time charts
4. **Compare versions** side-by-side

### Team Collaboration
1. **Share dashboards** with team members
2. **Add annotations** for documentation
3. **Review changes** before deployment
4. **Track team metrics** and progress

### Production Monitoring
1. **Monitor live performance** 24/7
2. **Set up alerts** for quality degradation
3. **Track costs** and usage patterns
4. **Analyze errors** and issues

## 🛠️ Advanced Features

### Custom Widgets

Create custom dashboard widgets:

```python
# Custom widget example
def create_custom_widget(pv):
    """Create a custom dashboard widget"""

    widget_data = {
        "title": "Cost Analysis",
        "type": "chart",
        "data": get_cost_analysis_data(pv),
        "refresh_interval": 60
    }

    return widget_data

# Register custom widget
pv.dashboard.add_widget("cost_analysis", create_custom_widget)
```

### Data Export

Export dashboard data:

```python
# Export dashboard data
dashboard_data = pv.dashboard.export_data(
    format="json",
    include_metrics=True,
    date_range="last_30_days"
)

# Save to file
with open("dashboard_export.json", "w") as f:
    json.dump(dashboard_data, f, indent=2)
```

### Embedding

Embed dashboard views in other applications:

```html
<!-- Embed specific chart -->
<iframe src="http://localhost:5000/embed/metrics/customer_service/2.1.0"
        width="100%" height="400">
</iframe>

<!-- Embed full dashboard -->
<iframe src="http://localhost:5000/embed/dashboard"
        width="100%" height="600">
</iframe>
```

## 🔒 Security Considerations

### Access Control
- Enable authentication for production use
- Use HTTPS for secure connections
- Implement role-based access control
- Regular security updates

### Data Protection
- Sensitive data masking
- Audit logs for all changes
- Backup and recovery procedures
- Compliance with data regulations

## 🎯 Best Practices

### 1. Regular Monitoring
- Check dashboard daily for production systems
- Set up automated alerts for issues
- Review performance trends weekly

### 2. Team Usage
- Train team members on dashboard features
- Establish workflows for prompt updates
- Document important changes and decisions

### 3. Performance
- Use appropriate refresh intervals
- Optimize for your network bandwidth
- Cache frequently accessed data

### 4. Maintenance
- Regular updates and backups
- Monitor dashboard performance
- Clean up old data periodically

## 🚀 Getting Started Checklist

1. ✅ **Start Dashboard**: `pv.start_dashboard()`
2. ✅ **Browse Prompts**: View your existing prompts
3. ✅ **Check Metrics**: Review performance data
4. ✅ **Create Version**: Make changes through web UI
5. ✅ **Set Monitoring**: Configure alerts and thresholds
6. ✅ **Share Access**: Invite team members if needed

## 📚 Next Steps

- [Version Management](version-management.md) - Learn about version control
- [Metrics Tracking](metrics-tracking.md) - Understand performance metrics
- [A/B Testing](ab-testing.md) - Compare versions systematically
