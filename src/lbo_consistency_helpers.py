"""
Consistency Helper Functions for LBO Models.

This module provides helper functions to ensure consistency across test cases
and implement audit recommendations.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class LBOConsistencyHelper:
    """Helper class for ensuring consistency across LBO model configurations."""

    # Standard parameter defaults
    STANDARD_DEFAULTS = {
        "target_exit_debt": 0.0,
        "max_debt_paydown_per_year": 0.0,
        "fcf_conversion_rate": 0.0,
        "transaction_expenses_pct": 0.03,
        "financing_fees_pct": 0.02,
        "depreciation_pct_of_ppe": 0.10,
        "tax_rate": 0.21,
        "days_sales_outstanding": 45.0,
        "days_inventory_outstanding": 30.0,
        "days_payable_outstanding": 30.0,
        "initial_ppe": 0.0,
        "initial_ar": 0.0,
        "initial_inventory": 0.0,
        "initial_ap": 0.0,
        "min_cash_balance": 0.0,
    }

    @staticmethod
    def standardize_config(config: Dict) -> Dict:
        """
        Standardize a configuration by adding missing standard parameters.

        Args:
            config: Configuration dictionary

        Returns:
            Standardized configuration with all standard parameters
        """
        standardized = config.copy()

        # Add missing standard parameters with defaults
        for key, default_value in LBOConsistencyHelper.STANDARD_DEFAULTS.items():
            if key not in standardized:
                standardized[key] = default_value
                logger.debug(f"Added missing parameter {key} with default value {default_value}")

        # Ensure debt instruments have priority if not specified
        if "debt_instruments" in standardized:
            for i, debt in enumerate(standardized["debt_instruments"], 1):
                if "priority" not in debt:
                    debt["priority"] = i
                    logger.debug(f"Added priority {i} to debt instrument {debt.get('name', 'Unknown')}")

        return standardized

    @staticmethod
    def validate_config(config: Dict) -> List[Dict[str, str]]:
        """
        Validate configuration for common issues.

        Args:
            config: Configuration dictionary

        Returns:
            List of validation issues (empty if valid)
        """
        issues = []

        # Check required fields
        required_fields = ["entry_ebitda", "entry_multiple", "revenue_growth_rate", "debt_instruments"]
        for field in required_fields:
            if field not in config:
                issues.append({"severity": "error", "field": field, "message": f"Missing required field: {field}"})

        # Validate entry_ebitda
        if "entry_ebitda" in config:
            if config["entry_ebitda"] <= 0:
                issues.append(
                    {"severity": "error", "field": "entry_ebitda", "message": "entry_ebitda must be positive"}
                )

        # Validate entry_multiple
        if "entry_multiple" in config:
            if config["entry_multiple"] <= 0 or config["entry_multiple"] > 20:
                issues.append(
                    {
                        "severity": "warning",
                        "field": "entry_multiple",
                        "message": f"entry_multiple ({config['entry_multiple']}) is outside typical range (4-12x)",
                    }
                )

        # Validate revenue growth rates
        if "revenue_growth_rate" in config:
            growth_rates = config["revenue_growth_rate"]
            if not isinstance(growth_rates, list) or len(growth_rates) == 0:
                issues.append(
                    {
                        "severity": "error",
                        "field": "revenue_growth_rate",
                        "message": "revenue_growth_rate must be a non-empty list",
                    }
                )
            else:
                for i, rate in enumerate(growth_rates):
                    if rate < -0.5 or rate > 1.0:
                        issues.append(
                            {
                                "severity": "warning",
                                "field": f"revenue_growth_rate[{i}]",
                                "message": f"Revenue growth rate {rate:.1%} is outside typical range (-50% to 100%)",
                            }
                        )

        # Validate debt instruments
        if "debt_instruments" in config:
            total_debt_multiple = 0
            for debt in config["debt_instruments"]:
                if "ebitda_multiple" in debt and debt["ebitda_multiple"]:
                    total_debt_multiple += debt["ebitda_multiple"]
                elif "amount" in debt and debt["amount"] > 0:
                    # Calculate implied multiple
                    if "entry_ebitda" in config and config["entry_ebitda"] > 0:
                        total_debt_multiple += debt["amount"] / config["entry_ebitda"]

            if total_debt_multiple > 7.0:
                issues.append(
                    {
                        "severity": "warning",
                        "field": "debt_instruments",
                        "message": f"Total debt multiple ({total_debt_multiple:.1f}x) is very high (>7.0x)",
                    }
                )
            if total_debt_multiple < 1.0:
                issues.append(
                    {
                        "severity": "warning",
                        "field": "debt_instruments",
                        "message": f"Total debt multiple ({total_debt_multiple:.1f}x) is very low (<1.0x)",
                    }
                )

        # Validate exit assumptions
        if "exit_multiple" in config and "entry_multiple" in config:
            if config["exit_multiple"] < config["entry_multiple"] * 0.5:
                issues.append(
                    {
                        "severity": "warning",
                        "field": "exit_multiple",
                        "message": f"Exit multiple ({config['exit_multiple']:.1f}x) is significantly lower than entry ({config['entry_multiple']:.1f}x)",
                    }
                )

        return issues

    @staticmethod
    def ensure_consistent_structure(config: Dict, include_sub_debt: bool = False) -> Dict:
        """
        Ensure consistent debt structure across configurations.

        Args:
            config: Configuration dictionary
            include_sub_debt: Whether to include subordinated debt (if not present)

        Returns:
            Configuration with consistent structure
        """
        standardized = LBOConsistencyHelper.standardize_config(config)

        # Ensure debt structure consistency
        if "debt_instruments" in standardized:
            _ = any(  # Check for senior debt but don't store result
                "Senior" in d.get("name", "") or "senior" in d.get("name", "").lower()
                for d in standardized["debt_instruments"]
            )
            has_sub = any(
                "Sub" in d.get("name", "") or "sub" in d.get("name", "").lower()
                for d in standardized["debt_instruments"]
            )

            # If include_sub_debt is True and no sub debt exists, add placeholder
            if include_sub_debt and not has_sub:
                # Find senior debt to determine appropriate sub debt
                senior_debt = next((d for d in standardized["debt_instruments"] if "Senior" in d.get("name", "")), None)
                if senior_debt:
                    sub_debt = {
                        "name": "Subordinated Debt",
                        "interest_rate": senior_debt.get("interest_rate", 0.10) + 0.03,  # Typically 3% higher
                        "ebitda_multiple": 0.0,  # Will be set to 0 if not needed
                        "amortization_schedule": "bullet",
                        "priority": 2,
                    }
                    standardized["debt_instruments"].append(sub_debt)
                    logger.info(f"Added placeholder subordinated debt to {standardized.get('company_name', 'Unknown')}")

        return standardized

    @staticmethod
    def compare_configs(config1: Dict, config2: Dict) -> Dict[str, Any]:
        """
        Compare two configurations and identify differences.

        Args:
            config1: First configuration
            config2: Second configuration

        Returns:
            Dictionary with comparison results
        """
        differences = {"missing_in_config1": [], "missing_in_config2": [], "different_values": []}

        all_keys = set(config1.keys()) | set(config2.keys())

        for key in all_keys:
            if key not in config1:
                differences["missing_in_config1"].append(key)
            elif key not in config2:
                differences["missing_in_config2"].append(key)
            elif config1[key] != config2[key]:
                differences["different_values"].append({"key": key, "config1": config1[key], "config2": config2[key]})

        return differences

    @staticmethod
    def standardize_all_configs(config_files: Dict[str, str], output_dir: Optional[str] = None) -> Dict[str, Dict]:
        """
        Standardize all configuration files.

        Args:
            config_files: Dictionary mapping case names to file paths
            output_dir: Optional directory to save standardized configs

        Returns:
            Dictionary of standardized configurations
        """
        standardized = {}

        for case_name, file_path in config_files.items():
            with open(file_path, "r") as f:
                config = json.load(f)

            standardized_config = LBOConsistencyHelper.standardize_config(config)
            standardized_config = LBOConsistencyHelper.ensure_consistent_structure(
                standardized_config, include_sub_debt=False  # Don't force sub debt
            )

            standardized[case_name] = standardized_config

            # Save if output directory specified
            if output_dir:
                output_path = Path(output_dir) / file_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    json.dump(standardized_config, f, indent=2)
                logger.info(f"Saved standardized config for {case_name} to {output_path}")

        return standardized
