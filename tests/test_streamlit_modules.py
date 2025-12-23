"""
Unit tests for Streamlit app modules.

Tests calculation functions, utilities, and validation logic.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_modules.app_utils import (
    calculate_sensitivity_analysis,
    cached_calculate_lbo,
    load_test_case
)
from streamlit_modules.app_analysis import (
    calculate_break_even_exit_multiple,
    calculate_break_even_growth_rate,
    calculate_break_even_margin
)


class TestAppUtils:
    """Test utility functions."""
    
    def test_load_test_case_valid(self, tmp_path):
        """Test loading a valid test case."""
        # Create a test config file
        test_config = {
            "entry_ebitda": 10000,
            "entry_multiple": 10.0,
            "exit_multiple": 12.0,
            "revenue_growth_rate": [0.05, 0.05, 0.05, 0.05, 0.05],
            "tax_rate": 0.25
        }
        
        import json
        test_file = tmp_path / "test_config.json"
        with open(test_file, 'w') as f:
            json.dump(test_config, f)
        
        result = load_test_case(str(test_file))
        assert result is not None
        assert result["entry_ebitda"] == 10000
        assert result["entry_multiple"] == 10.0
    
    def test_load_test_case_invalid(self):
        """Test loading a non-existent test case."""
        result = load_test_case("nonexistent_file.json")
        assert result is None
    
    def test_cached_calculate_lbo_basic(self):
        """Test basic LBO calculation."""
        result = cached_calculate_lbo(
            entry_multiple=10.0,
            leverage_ratio=4.0,
            rev_growth=0.05,
            ebitda_margin=0.20,
            entry_ebitda=10000.0,
            exit_multiple=12.0,
            interest_rate=0.08,
            tax_rate=0.25,
        )
        
        assert result is not None
        assert 'irr' in result
        assert 'moic' in result
        assert 'debt_paid' in result
        assert isinstance(result['irr'], (int, float))
        assert isinstance(result['moic'], (int, float))
    
    def test_calculate_sensitivity_analysis_exit_multiple(self):
        """Test sensitivity analysis for exit multiple."""
        base_results = {
            'irr': 0.20,
            'moic': 2.0,
        }
        
        results = calculate_sensitivity_analysis(
            base_results=base_results,
            variable="Exit Multiple",
            base_entry_multiple=10.0,
            base_exit_multiple=12.0,
            base_rev_growth=0.05,
            base_ebitda_margin=0.20,
            base_leverage_ratio=4.0,
            base_entry_ebitda=10000.0,
            base_interest_rate=0.08,
            base_tax_rate=0.25,
            range_pct=20,
            steps=5,
            dso=45.0,
            dio=30.0,
            dpo=30.0,
            transaction_expenses_pct=0.03,
            financing_fees_pct=0.02,
        )
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert 'Exit Multiple' in results[0]
        assert 'IRR' in results[0]
        assert 'MOIC' in results[0]


class TestAppAnalysis:
    """Test analysis functions."""
    
    def test_break_even_exit_multiple(self):
        """Test break-even exit multiple calculation."""
        result = calculate_break_even_exit_multiple(
            entry_multiple=10.0,
            leverage_ratio=4.0,
            rev_growth=0.05,
            ebitda_margin=0.20,
            entry_ebitda=10000.0,
            target_irr=0.20,
            interest_rate=0.08,
            tax_rate=0.25,
            max_iterations=10,  # Reduced for faster testing
        )
        
        assert result is not None
        assert isinstance(result, (int, float))
        assert result > 0
    
    def test_break_even_growth_rate(self):
        """Test break-even growth rate calculation."""
        result = calculate_break_even_growth_rate(
            entry_multiple=10.0,
            leverage_ratio=4.0,
            ebitda_margin=0.20,
            entry_ebitda=10000.0,
            exit_multiple=12.0,
            target_irr=0.20,
            interest_rate=0.08,
            tax_rate=0.25,
            max_iterations=10,
        )
        
        assert result is not None
        assert isinstance(result, (int, float))
        assert 0 <= result <= 1.0  # Growth rate should be between 0 and 100%
    
    def test_break_even_margin(self):
        """Test break-even margin calculation."""
        result = calculate_break_even_margin(
            entry_multiple=10.0,
            leverage_ratio=4.0,
            rev_growth=0.05,
            entry_ebitda=10000.0,
            exit_multiple=12.0,
            target_irr=0.20,
            interest_rate=0.08,
            tax_rate=0.25,
            max_iterations=10,
        )
        
        assert result is not None
        assert isinstance(result, (int, float))
        assert 0 < result < 1.0  # Margin should be between 0 and 100%


class TestInputValidation:
    """Test input validation logic."""
    
    def test_input_ranges(self):
        """Test that inputs are within valid ranges."""
        # Test with valid inputs
        result = cached_calculate_lbo(
            entry_multiple=10.0,  # Valid: 5-15
            leverage_ratio=4.0,   # Valid: 2-7
            rev_growth=0.05,      # Valid: 0-0.20
            ebitda_margin=0.20,   # Valid: 0.10-0.40
            entry_ebitda=10000.0,
            exit_multiple=12.0,
            interest_rate=0.08,
            tax_rate=0.25,
        )
        
        assert result is not None
    
    def test_edge_cases(self):
        """Test edge cases for calculations."""
        # Test with minimum values
        result = cached_calculate_lbo(
            entry_multiple=5.0,
            leverage_ratio=2.0,
            rev_growth=0.0,
            ebitda_margin=0.10,
            entry_ebitda=1000.0,
            exit_multiple=5.0,
            interest_rate=0.04,
            tax_rate=0.15,
        )
        
        assert result is not None
        assert 'irr' in result
        assert 'moic' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

