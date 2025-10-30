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
- **Multi-Model Comparison**: Compare performance across different LLM models with automatic "best model" badges

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

### Model Performance Comparison

When you test the same prompt with multiple models, the dashboard automatically shows:

```
┌─────────────────────────────────────────────────┐
│ 🤖 MODEL PERFORMANCE COMPARISON                │
├─────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────┐      │
│ │ gpt-4o          │  │ claude-3-sonnet │      │
│ │ ⚡ Fastest      │  │ ⭐ Best Quality │      │
│ │ 250 calls       │  │ 250 calls       │      │
│ │ €0.0245         │  │ €0.0315         │      │
│ │ 450-1850ms      │  │ 520-2100ms      │      │
│ │ Avg: 156 tokens │  │ Avg: 142 tokens │      │
│ │ Quality: 95.2%  │  │ Quality: 96.1%  │      │
│ └─────────────────┘  └─────────────────┘      │
│                                                 │
│ ┌─────────────────┐  ┌─────────────────┐      │
│ │ gpt-4o-mini     │  │ gemini-pro      │      │
│ │ 💰 Cheapest     │  │ ✅ Most Reliable│      │
│ │ 250 calls       │  │ 250 calls       │      │
│ │ €0.0035         │  │ €0.0055         │      │
│ │ 380-1520ms      │  │ 410-1680ms      │      │
│ │ Avg: 149 tokens │  │ Avg: 138 tokens │      │
│ │ Quality: 92.8%  │  │ Quality: 93.5%  │      │
│ └─────────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

The system automatically identifies and highlights:
- ⚡ **Fastest**: Lowest average latency
- 💰 **Cheapest**: Lowest cost per call
- ⭐ **Best Quality**: Highest quality score
- ✅ **Most Reliable**: Highest success rate

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
