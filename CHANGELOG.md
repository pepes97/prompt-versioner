# Changelog

All notable changes to Prompt Versioner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.6] - 2025-11-05

### Added
- **Model Pricing & Cost Estimation CLI Commands**: Complete pricing management system for LLM models
  - New command `pv models`: List all available models with pricing information
    - Table format with input/output prices per 1M tokens and average cost calculation
    - Sorting options: `--sort-by {name,input,output,total}`
    - Filtering: `--filter TEXT` for case-insensitive substring matching
    - Limit results: `--limit N` to show top N models
    - JSON export: `--format json` for programmatic usage
    - Example cost calculations for top 3 cheapest models
  - New command `pv estimate-cost`: Calculate cost estimates for specific model usage
    - Arguments: `MODEL_NAME INPUT_TOKENS OUTPUT_TOKENS`
    - Option `--calls N` for estimating multiple API calls
    - Detailed breakdown showing cost per call and total cost
    - Validation with helpful error messages for unknown models
  - New command `pv compare-costs`: Compare costs across all models for given token usage
    - Arguments: `INPUT_TOKENS OUTPUT_TOKENS`
    - Option `--top N` to limit results (default: 5)
    - Ranked table with relative cost comparison (e.g., "2.5x")
    - Visual highlighting for top 3 cheapest models
  - **16 supported models** with up-to-date pricing (Claude, GPT, Mistral families)
  - Pricing data in EUR per 1M tokens (both input and output)

### Changed
- **CLI Architecture**:
  - Created new module `prompt_versioner/cli/commands/pricing.py` for pricing commands
  - Updated `prompt_versioner/cli/commands/__init__.py` to register pricing module
  - Improved command organization with dedicated pricing functionality
- **Documentation Structure**:
  - README updated with new CLI commands section showing all pricing commands
  - Added comprehensive pricing documentation: `docs/api-reference/cli/pricing.md`
    - Detailed usage examples for all three commands
    - Complete options reference
    - Common use cases and workflows
    - Tips for cost optimization
  - Enhanced `docs/api-reference/cli/commands.md` with new "Model Pricing & Cost Estimation" category
  - Updated `docs/getting-started/quick-start.md` with cost estimation section
    - Python API examples
    - CLI usage examples
    - Integration with existing metrics tracking
  - Added pricing documentation to `mkdocs.yml` navigation
    - New entry under CLI Reference
    - New entry under Metrics API Reference

### Enhanced
- **PricingManager class** (existing functionality now exposed via CLI):
  - `list_models()`: Get all available models
  - `get_pricing(model_name)`: Retrieve pricing for specific model
  - `calculate_cost()`: Single call cost calculation
  - `estimate_cost()`: Multi-call estimation with breakdown
  - `compare_models()`: Cross-model cost comparison
  - `get_cheapest_model()`: Find most cost-effective option
- **Rich terminal output**: Tables with proper formatting, colors, and visual hierarchy
- **User experience**:
  - Helpful error messages with suggestions
  - Automatic example calculations
  - Progress indicators and info messages
  - Consistent styling across all pricing commands

### Documentation
- Complete API reference for pricing module in `docs/api-reference/metrics/pricing.md`
- Quick start guide updated with cost estimation examples
- README CLI interface section reorganized with categorized commands
- mkdocs navigation structure enhanced with pricing documentation links

### Technical Details
- **Backend**: Leverages existing `PricingManager` from `prompt_versioner.metrics.pricing`
- **CLI Framework**: Built with Click for robust argument parsing and validation
- **Output Formatting**: Rich library for beautiful terminal tables and panels
- **Data Structure**: Default pricing dictionary with extensibility for custom models
- **Currency**: EUR (Euro) pricing for all models
- **Precision**: 6 decimal places for cost calculations to handle micro-costs accurately

### Use Cases Enabled
1. **Budget Planning**: Estimate monthly costs based on expected usage patterns
2. **Model Selection**: Find the most cost-effective model for specific token patterns
3. **Cost Optimization**: Compare providers and models to reduce expenses
4. **Financial Reporting**: Export pricing data in JSON for analysis and reporting
5. **Development**: Quick cost checks during prompt development and testing

## [0.2.5] - 2025-10-30

### Added
- **Multi-Model Performance Comparison**: Major new feature to test and compare the same prompt across different LLM models
  - Automatic aggregation of metrics by model with weighted averages based on call count
  - Smart identification of best-performing models with visual badges:
    - ⚡ **Fastest**: Model with lowest average latency
    - 💰 **Cheapest**: Model with lowest cost per call
    - ⭐ **Best Quality**: Model with highest quality score
    - ✅ **Most Reliable**: Model with highest success rate
  - New backend method `get_summary_by_model(version_id)` in `storage/metrics.py` for SQL aggregation
  - New API endpoint: `GET /api/prompts/<name>/versions/<version>/models` returning per-model statistics
  - Visual model comparison cards in web dashboard with responsive grid layout
  - Performance Metrics modal section now displays aggregated data across all tested models
  - HTML templates for model cards, badges, loading states, and empty states
- New comprehensive example: `examples/multi_models.py` with realistic multi-model testing simulation
- Complete documentation page: `docs/user-guide/multi-model-comparison.md` with:
  - Step-by-step usage guide
  - API integration examples (OpenAI, Anthropic, Google Gemini)
  - Best practices for model comparison
  - Troubleshooting section

### Changed
- **Web Dashboard UI improvements**:
  - Model Performance Comparison section styled consistently with dashboard design language
  - Unified color scheme and spacing across all components
  - Enhanced visual hierarchy with proper borders and backgrounds
  - Improved hover effects and transitions
- **Code Architecture**:
  - Complete separation of concerns: all HTML moved from JavaScript to templates
  - JavaScript now handles only logic and data manipulation
  - Template-based rendering for all dynamic components
  - Cleaner, more maintainable codebase
- **CSS Styling**:
  - New styles for model comparison cards with full dark/light mode support
  - Consistent badge styling using transparent backgrounds with borders
  - Responsive grid layout with `auto-fit` for flexible column count
  - Improved empty states and loading indicators

### Fixed
- Modal timing issues: Model comparison now loads after modal is in DOM
- Duplicate HTML in JavaScript causing syntax errors
- Template literal issues from incomplete refactoring

### Documentation
- Updated `README.md` with multi-model comparison feature and code examples
- Added "Multi-Model Comparison" to main documentation navigation in `mkdocs.yml`
- Enhanced `docs/index.md` with feature descriptions
- Updated `docs/user-guide/web-dashboard.md` with visual model comparison examples
- Added multi-model benchmarking section to `docs/examples/advanced-workflows.md` with:
  - Complete `ModelBenchmark` class implementation
  - Cross-model prompt optimization patterns
  - Async benchmark execution examples
- Enhanced `docs/examples/best-practices.md` with:
  - Best practices for multi-model tracking
  - Model naming conventions
  - Common pitfalls and how to avoid them
- Improved `examples/multi_models.py` documentation header with clear usage instructions

### Technical Details
- **Backend**: SQL GROUP BY model_name with comprehensive aggregations (COUNT, AVG, SUM, MIN, MAX)
- **Frontend**: Template cloning pattern for dynamic content generation
- **API**: RESTful endpoint returning JSON with models dictionary and total count
- **Performance**: Efficient weighted average calculations for aggregated metrics

## [0.2.4] - 2025-XX-XX

### Previous releases
(Document previous versions here as needed)

## [0.1.0] - 2024-XX-XX

### Added
- Initial release of Prompt Versioner
- Automatic MAJOR/MINOR/PATCH versioning
- Comprehensive metrics tracking (tokens, latency, quality, cost)
- A/B Testing framework
- Web dashboard with dark/light themes
- Git integration support
- CLI interface
- Export/Import functionality
- Team collaboration features (annotations, reviews)
- Performance monitoring and alerting
- REST API endpoints

[Unreleased]: https://github.com/pepes97/prompt-versioner/compare/v0.2.6...HEAD
[0.2.6]: https://github.com/pepes97/prompt-versioner/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/pepes97/prompt-versioner/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/pepes97/prompt-versioner/compare/v0.1.0...v0.2.4
[0.1.0]: https://github.com/pepes97/prompt-versioner/releases/tag/v0.1.0
