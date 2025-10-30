# Changelog

All notable changes to Prompt Versioner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/pepes97/prompt-versioner/compare/v0.2.5...HEAD
[0.2.5]: https://github.com/pepes97/prompt-versioner/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/pepes97/prompt-versioner/compare/v0.1.0...v0.2.4
[0.1.0]: https://github.com/pepes97/prompt-versioner/releases/tag/v0.1.0
