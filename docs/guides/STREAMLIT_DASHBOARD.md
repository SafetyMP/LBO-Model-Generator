# Streamlit Dashboard Guide

## Overview

The LBO Model Generator includes a comprehensive Streamlit web dashboard for interactive LBO modeling and analysis. The dashboard provides an intuitive interface for configuring assumptions, viewing results, performing sensitivity analysis, and exporting models.

## Features

### 🎯 Core Features

- **Interactive Assumptions Configuration**: Easy-to-use sliders and inputs for all LBO parameters
- **Real-time Validation**: Instant feedback on assumption reasonableness
- **Multi-page Navigation**: Organized into Dashboard, Assumptions, Analysis, Help, and Comparison pages
- **Multiple Debt Instruments**: Support for Senior + Subordinated debt structures
- **Sensitivity Analysis**: Built-in scenario comparison and tornado charts
- **Enhanced Visualizations**: Equity waterfall, returns attribution, and financial statement trends
- **Export Capabilities**: Excel export, PDF summary, and JSON configuration export/import
- **AI Integration**: AI-powered validation and recommendations (requires API key)
- **Break-even Analysis**: Calculate minimum values needed for target returns

### 📊 Dashboard Pages

#### 1. Dashboard (`1_📊_Dashboard.py`)
- High-level metrics display (IRR, MOIC, Exit Metrics)
- Key financial statement visualizations
- Excel and PDF export buttons
- Quick status overview

#### 2. Assumptions (`2_⚙️_Assumptions.py`)
- Complete input configuration interface
- Test case loading (AlphaCo, DataCore, SentinelGuard, VectorServe)
- Multiple debt instrument configuration
- Working capital assumptions
- Transaction fees configuration
- Real-time validation feedback

#### 3. Analysis (`3_📈_Analysis.py`)
- Sensitivity analysis with tornado charts
- Scenario comparison (Base/High/Low)
- Enhanced visualizations:
  - Equity waterfall chart
  - Returns attribution
  - Financial statement trends
- Break-even analysis

#### 4. Help (`4_ℹ️_Help.py`)
- Comprehensive documentation
- Best practices guide
- FAQ section
- Troubleshooting tips

## Installation

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt
```

Required packages:
- `streamlit>=1.28.0`
- `plotly>=5.17.0`
- `reportlab>=4.0.0` (for PDF export)
- `pandas>=2.0.0`
- `numpy>=1.24.0`

### OpenAI API Key (Optional)

For AI features, configure your API key:

**Option 1: Environment Variable**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Option 2: Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
[openai]
api_key = "your-api-key-here"
```

## Quick Start

### 1. Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### 2. Configure Assumptions

1. Navigate to the **Assumptions** page (via sidebar)
2. Load a test case or configure manually:
   - Entry Multiple: 5.0x - 15.0x
   - Leverage Ratio: 2.0x - 7.0x
   - Revenue Growth: 0% - 20%
   - EBITDA Margin: 10% - 40%
   - Entry EBITDA: Your company's EBITDA
   - Exit Multiple: Expected exit multiple

3. Configure debt structure:
   - **Single Instrument**: Simple single debt tranche
   - **Senior + Subordinated**: Multiple debt tranches with different rates and schedules

4. Set working capital assumptions (DSO, DIO, DPO)

5. Click **"Calculate LBO Model"**

### 3. View Results

Navigate to the **Dashboard** page to see:
- Equity IRR and MOIC
- Exit metrics (Exit EV, Exit Equity Value, Exit Cash)
- Debt paydown summary
- Financial statement trends

### 4. Perform Analysis

Go to the **Analysis** page for:
- Sensitivity analysis
- Scenario comparison
- Enhanced visualizations
- Break-even analysis

### 5. Export Results

From the Dashboard page:
- **Excel Export**: Full LBO model with all financial statements
- **PDF Summary**: Executive summary report with key metrics

## Architecture

### Module Structure

```
streamlit_modules/
├── app_config.py          # Configuration and session state
├── app_utils.py           # Utility functions and caching
├── app_visualizations.py  # All visualization functions
├── app_analysis.py        # Advanced analysis (break-even, etc.)
├── app_export.py          # Export functionality (Excel, PDF)
├── app_performance.py     # Performance optimization
└── app_ui.py              # UI helper functions

pages/
├── 1_📊_Dashboard.py       # Main dashboard
├── 2_⚙️_Assumptions.py    # Input configuration
├── 3_📈_Analysis.py       # Analysis and visualizations
└── 4_ℹ️_Help.py           # Help and documentation
```

### Key Components

#### Session State Management
- Centralized in `app_config.py`
- Stores current results, inputs, and UI state
- Persists across page navigation

#### Caching
- `@st.cache_data` decorator for expensive calculations
- Cache management UI for clearing when needed
- Improves performance for repeated calculations

#### Validation
- Real-time validation using `EnhancedLBOValidator`
- Displays warnings and errors inline
- Prevents invalid calculations

## Usage Examples

### Example 1: Basic LBO Analysis

```python
# 1. Launch dashboard
streamlit run app.py

# 2. In Assumptions page:
#    - Entry Multiple: 10.0x
#    - Leverage Ratio: 4.0x
#    - Revenue Growth: 12%
#    - EBITDA Margin: 20%
#    - Entry EBITDA: $50,000

# 3. Click "Calculate LBO Model"

# 4. View results in Dashboard
```

### Example 2: Multiple Debt Instruments

```python
# In Assumptions page:
# 1. Select "Senior + Subordinated" debt structure
# 2. Configure:
#    - Senior Debt: 70% @ 7.0%
#    - Subordinated Debt: 30% @ 12.0%
# 3. Calculate and view debt schedule breakdown
```

### Example 3: Sensitivity Analysis

```python
# 1. Calculate base case
# 2. Navigate to Analysis page
# 3. View sensitivity analysis:
#    - Tornado chart showing impact of each assumption
#    - Scenario comparison (Base/High/Low)
#    - Break-even analysis
```

## Configuration

### Streamlit Configuration

The dashboard uses `.streamlit/config.toml` for UI settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[ui]
hideSidebar = false
```

### Cache Management

- Cache is automatically managed by Streamlit
- Use cache management UI in Assumptions page to clear when needed
- Cache persists across page navigation

## Troubleshooting

### Common Issues

**Issue**: Sidebar not visible
- **Solution**: Check `.streamlit/config.toml` has `hideSidebar = false`
- Ensure `st.set_page_config(initial_sidebar_state="expanded")` is set

**Issue**: OpenAI API key not found
- **Solution**: Set `OPENAI_API_KEY` environment variable or configure in `.streamlit/secrets.toml`

**Issue**: PDF export not available
- **Solution**: Install reportlab: `pip install reportlab`

**Issue**: Calculation errors
- **Solution**: Check validation warnings in Assumptions page
- Ensure all inputs are within reasonable ranges
- Review error messages for specific guidance

### Performance Tips

1. **Use caching**: Results are cached automatically
2. **Clear cache**: If assumptions change significantly, clear cache
3. **Debouncing**: Slider updates are debounced to reduce recalculations
4. **Lazy loading**: Visualizations load only when needed

## Best Practices

### Assumption Setting

1. **Start with test cases**: Load a test case to see example configurations
2. **Use validation**: Pay attention to validation warnings
3. **Be realistic**: Use industry-appropriate assumptions
4. **Test scenarios**: Use sensitivity analysis to understand risks

### Analysis Workflow

1. **Base case first**: Calculate and understand base case
2. **Sensitivity analysis**: Identify key value drivers
3. **Scenario planning**: Create High/Base/Low scenarios
4. **Break-even analysis**: Understand minimum requirements
5. **Export results**: Save Excel models and PDF summaries

## Comparison with CLI Tool

| Feature | CLI Tool | Streamlit Dashboard |
|---------|----------|---------------------|
| Input Method | JSON files, CLI args | Interactive UI |
| Visualization | Excel charts | Interactive Plotly charts |
| Sensitivity Analysis | Manual | Built-in |
| Export | Excel only | Excel + PDF |
| AI Features | Full support | Full support |
| Multi-page | N/A | Yes |
| Real-time Validation | Post-calculation | Real-time |

## Advanced Features

### AI-Powered Analysis

With OpenAI API key configured:
- **Validation**: AI-powered assumption validation
- **Recommendations**: Get suggestions for improving assumptions
- **Natural Language Queries**: Ask questions about your model
- **Market Benchmarking**: Compare against industry standards

### Custom Visualizations

The dashboard includes:
- **Equity Waterfall**: Shows value creation breakdown
- **Returns Attribution**: Identifies IRR drivers
- **Tornado Charts**: Sensitivity analysis visualization
- **Financial Trends**: Revenue, EBITDA, FCF over time

### Export Options

1. **Excel Export**: Full LBO model with all statements
2. **PDF Summary**: Executive summary report
3. **JSON Export**: Save configuration for reuse
4. **JSON Import**: Load saved configurations

## Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

### Adding New Features

1. **New visualization**: Add to `streamlit_modules/app_visualizations.py`
2. **New analysis**: Add to `streamlit_modules/app_analysis.py`
3. **New page**: Create in `pages/` directory
4. **New utility**: Add to `streamlit_modules/app_utils.py`

### Testing

```bash
# Run Streamlit-specific tests
pytest tests/test_streamlit_modules.py

# Run comparison script
python compare_streamlit_test.py
```

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Main README](../README.md)
- [Test Case Comparison](../../STREAMLIT_TEST_COMPARISON.md)

