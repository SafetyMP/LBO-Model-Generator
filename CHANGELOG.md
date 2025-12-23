# Changelog

All notable changes to the LBO Model Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-23

### Added
- **Streamlit Web Dashboard**: Complete interactive web interface for LBO modeling
  - Multi-page navigation (Dashboard, Assumptions, Analysis, Help)
  - Real-time validation and feedback
  - Interactive visualizations (Plotly charts)
  - Sensitivity analysis with tornado charts
  - Scenario comparison (Base/High/Low)
  - Enhanced visualizations (equity waterfall, returns attribution)
  - Break-even analysis
  - Excel and PDF export capabilities
  - Multiple debt instruments support (Senior + Subordinated)
  - Test case loading (AlphaCo, DataCore, SentinelGuard, VectorServe)
  - Cache management for performance optimization
  - AI-powered features integration (with API key)

- **Streamlit Modules**: Modular architecture for dashboard components
  - `app_config.py`: Configuration and session state management
  - `app_utils.py`: Utility functions and caching
  - `app_visualizations.py`: Visualization functions
  - `app_analysis.py`: Advanced analysis functions
  - `app_export.py`: Export functionality (Excel, PDF)
  - `app_performance.py`: Performance optimization
  - `app_ui.py`: UI helper functions

- **Documentation**:
  - Streamlit Dashboard Guide (`docs/guides/STREAMLIT_DASHBOARD.md`)
  - Test case comparison report (`STREAMLIT_TEST_COMPARISON.md`)
  - Sidebar navigation guide (`SIDEBAR_NAVIGATION_GUIDE.md`)
  - Sidebar troubleshooting guide (`SIDEBAR_TROUBLESHOOTING.md`)

- **Testing**:
  - Test case comparison script (`compare_streamlit_test.py`)
  - Streamlit module unit tests (`tests/test_streamlit_modules.py`)

- **Dependencies**:
  - `streamlit>=1.28.0` for web dashboard
  - `plotly>=5.17.0` for interactive visualizations
  - `reportlab>=4.0.0` for PDF export

### Changed
- Updated `README.md` with Streamlit dashboard information
- Enhanced `requirements.txt` with Streamlit dependencies
- Improved code organization with modular Streamlit components
- Updated `src/__init__.py` to export `calculate_lbo` function

### Fixed
- Sidebar visibility issues (config.toml and page config)
- OpenAI API key loading from environment variables and Streamlit secrets
- PDF export dependency (reportlab installation)
- Import path issues in Streamlit execution context
- Debt instrument handling in Streamlit UI

## [1.0.0] - 2024

### Added
- Initial release of LBO Model Generator
- Core LBO modeling functionality
- Excel export capabilities
- AI integration (10 features)
- CLI interface
- Comprehensive documentation

### Features
- Complete financial statement generation
- Multiple debt instrument support
- Returns analysis (IRR, MOIC)
- Industry-standard Excel formatting
- AI-powered recommendations and validation
- Scenario analysis
- Market benchmarking

---

## Version History

- **1.1.0** (2025-12-23): Streamlit dashboard release
- **1.0.0** (2024): Initial release

---

## Upgrade Notes

### From 1.0.0 to 1.1.0

1. **Install new dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Streamlit dashboard**:
   ```bash
   streamlit run app.py
   ```

3. **API key configuration** (for AI features):
   - Set `OPENAI_API_KEY` environment variable, or
   - Configure in `.streamlit/secrets.toml`

4. **CLI usage unchanged**: All existing CLI functionality remains available

---

## Future Roadmap

### Planned Features
- [ ] User authentication and saved scenarios
- [ ] Collaborative editing
- [ ] Advanced chart customization
- [ ] More export formats (PowerPoint, Word)
- [ ] Integration with external data sources
- [ ] Mobile-responsive dashboard
- [ ] Real-time collaboration

### Known Issues
- See [GitHub Issues](https://github.com/SafetyMP/LBO-Model-Generator/issues)

---

*For detailed information about each release, see the [GitHub Releases](https://github.com/SafetyMP/LBO-Model-Generator/releases) page.*

