"""
Enhanced Validation Functions for LBO Models.

Implements audit recommendations for comprehensive input validation.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Enhanced validation result."""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    score: float  # 0.0 to 1.0


class EnhancedLBOValidator:
    """Enhanced validator implementing audit recommendations."""

    # Realistic ranges for validation
    RANGES = {
        "entry_ebitda": (1000, 1000000),  # $1M to $1B
        "entry_multiple": (3.0, 15.0),  # 3x to 15x
        "exit_multiple": (3.0, 15.0),
        "revenue_growth_rate": (-0.5, 1.0),  # -50% to 100%
        "cogs_pct_of_revenue": (0.0, 0.95),  # 0% to 95%
        "sganda_pct_of_revenue": (0.0, 0.95),
        "tax_rate": (0.0, 0.50),  # 0% to 50%
        "interest_rate": (0.0, 0.30),  # 0% to 30%
        "ebitda_multiple": (0.0, 10.0),  # 0x to 10x per instrument
        "days_sales_outstanding": (0, 365),
        "days_inventory_outstanding": (0, 365),
        "days_payable_outstanding": (0, 365),
    }

    @staticmethod
    def _validate_required_fields(config: Dict) -> List[str]:
        """Validate required fields."""
        errors = []
        required = ["entry_ebitda", "entry_multiple", "revenue_growth_rate", "debt_instruments"]
        for field in required:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        return errors

    @staticmethod
    def _validate_entry_metrics(config: Dict) -> tuple[List[str], List[str]]:
        """Validate entry EBITDA and multiple."""
        errors = []
        warnings = []

        ebitda = config.get("entry_ebitda", 0)
        if ebitda <= 0:
            errors.append("entry_ebitda must be positive")
        elif (
            not EnhancedLBOValidator.RANGES["entry_ebitda"][0]
            <= ebitda
            <= EnhancedLBOValidator.RANGES["entry_ebitda"][1]
        ):
            warnings.append(f"entry_ebitda (${ebitda:,.0f}) is outside typical range")

        entry_mult = config.get("entry_multiple", 0)
        if entry_mult <= 0:
            errors.append("entry_multiple must be positive")
        elif (
            not EnhancedLBOValidator.RANGES["entry_multiple"][0]
            <= entry_mult
            <= EnhancedLBOValidator.RANGES["entry_multiple"][1]
        ):
            warnings.append(f"entry_multiple ({entry_mult:.1f}x) is outside typical range (4-12x)")

        return errors, warnings

    @staticmethod
    def _validate_growth_rates(config: Dict) -> tuple[List[str], List[str]]:
        """Validate revenue growth rates."""
        errors = []
        warnings = []

        growth_rates = config.get("revenue_growth_rate", [])
        if not isinstance(growth_rates, list) or len(growth_rates) == 0:
            errors.append("revenue_growth_rate must be a non-empty list")
        else:
            for i, rate in enumerate(growth_rates):
                if rate < EnhancedLBOValidator.RANGES["revenue_growth_rate"][0]:
                    errors.append(f"revenue_growth_rate[{i}] ({rate:.1%}) is negative beyond -50%")
                elif rate > EnhancedLBOValidator.RANGES["revenue_growth_rate"][1]:
                    warnings.append(f"revenue_growth_rate[{i}] ({rate:.1%}) exceeds 100%")

        return errors, warnings

    @staticmethod
    def _validate_debt_structure(config: Dict, ebitda: float) -> tuple[List[str], List[str]]:
        """Validate debt structure."""
        warnings = []

        debt_instruments = config.get("debt_instruments", [])
        if not isinstance(debt_instruments, list) or len(debt_instruments) == 0:
            warnings.append("No debt instruments specified")
            return [], warnings

        total_debt_multiple = 0
        for i, debt in enumerate(debt_instruments):
            if "interest_rate" in debt:
                ir = debt["interest_rate"]
                if (
                    not EnhancedLBOValidator.RANGES["interest_rate"][0]
                    <= ir
                    <= EnhancedLBOValidator.RANGES["interest_rate"][1]
                ):
                    warnings.append(f"Debt instrument {i} interest rate ({ir:.1%}) is outside typical range")

            if "ebitda_multiple" in debt and debt.get("ebitda_multiple", 0) > 0:
                mult = debt["ebitda_multiple"]
                if mult > EnhancedLBOValidator.RANGES["ebitda_multiple"][1]:
                    warnings.append(f"Debt instrument {i} EBITDA multiple ({mult:.1f}x) is very high")
                total_debt_multiple += mult
            elif "amount" in debt and debt.get("amount", 0) > 0:
                if ebitda > 0:
                    total_debt_multiple += debt["amount"] / ebitda

        if total_debt_multiple > 7.0:
            warnings.append(f"Total debt multiple ({total_debt_multiple:.1f}x) is very high (>7.0x)")
        elif total_debt_multiple < 1.0:
            warnings.append(f"Total debt multiple ({total_debt_multiple:.1f}x) is very low (<1.0x)")

        return [], warnings

    @staticmethod
    def _validate_margins(config: Dict) -> tuple[List[str], List[str], List[str]]:
        """Validate margin assumptions."""
        errors = []
        warnings = []
        info = []

        cogs_pct = config.get("cogs_pct_of_revenue", 0.7)
        sganda_pct = config.get("sganda_pct_of_revenue", 0.15)
        implied_margin = 1 - cogs_pct - sganda_pct

        if implied_margin < 0:
            errors.append(f"COGS% ({cogs_pct:.1%}) + SG&A% ({sganda_pct:.1%}) exceeds 100%")
        elif implied_margin < 0.05:
            warnings.append(f"Implied EBITDA margin ({implied_margin:.1%}) is very low (<5%)")
        elif implied_margin > 0.50:
            info.append(f"Implied EBITDA margin ({implied_margin:.1%}) is very high (>50%)")

        return errors, warnings, info

    @staticmethod
    def _validate_exit_assumptions(config: Dict) -> List[str]:
        """Validate exit assumptions."""
        warnings = []
        exit_mult = config.get("exit_multiple", 7.5)
        entry_mult = config.get("entry_multiple", 0)
        if exit_mult < entry_mult * 0.5:
            warnings.append(f"Exit multiple ({exit_mult:.1f}x) is significantly lower than entry ({entry_mult:.1f}x)")
        return warnings

    @staticmethod
    def validate_comprehensive(config: Dict) -> ValidationResult:
        """
        Comprehensive validation implementing audit recommendations.

        Args:
            config: Configuration dictionary

        Returns:
            ValidationResult with detailed findings
        """
        errors = []
        warnings = []
        info = []

        # Validate required fields
        errors.extend(EnhancedLBOValidator._validate_required_fields(config))
        if errors:
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings, info=info, score=0.0)

        # Validate entry metrics
        entry_errors, entry_warnings = EnhancedLBOValidator._validate_entry_metrics(config)
        errors.extend(entry_errors)
        warnings.extend(entry_warnings)

        # Validate growth rates
        growth_errors, growth_warnings = EnhancedLBOValidator._validate_growth_rates(config)
        errors.extend(growth_errors)
        warnings.extend(growth_warnings)

        # Validate debt structure
        ebitda = config.get("entry_ebitda", 0)
        debt_errors, debt_warnings = EnhancedLBOValidator._validate_debt_structure(config, ebitda)
        errors.extend(debt_errors)
        warnings.extend(debt_warnings)

        # Validate margins
        margin_errors, margin_warnings, margin_info = EnhancedLBOValidator._validate_margins(config)
        errors.extend(margin_errors)
        warnings.extend(margin_warnings)
        info.extend(margin_info)

        # Validate exit assumptions
        exit_warnings = EnhancedLBOValidator._validate_exit_assumptions(config)
        warnings.extend(exit_warnings)

        # Calculate validation score
        score = 1.0
        score -= len(errors) * 0.3
        score -= len(warnings) * 0.1
        score = max(0.0, min(1.0, score))

        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings, info=info, score=score)

    @staticmethod
    def validate_debt_structure(config: Dict) -> Tuple[bool, List[str]]:
        """
        Validate debt structure for consistency and reasonableness.

        Args:
            config: Configuration dictionary

        Returns:
            Tuple of (is_valid, issues)
        """
        issues = []
        debt_instruments = config.get("debt_instruments", [])

        if len(debt_instruments) == 0:
            issues.append("No debt instruments specified")
            return False, issues

        # Check for priority ordering
        priorities = [d.get("priority", 0) for d in debt_instruments]
        if len(set(priorities)) != len(priorities):
            issues.append("Debt instruments have duplicate priorities")

        # Check for reasonable interest rate progression
        interest_rates = [
            (d.get("interest_rate", 0), d.get("priority", 999)) for d in debt_instruments if "interest_rate" in d
        ]
        if len(interest_rates) > 1:
            sorted_rates = sorted(interest_rates, key=lambda x: x[1])
            for i in range(1, len(sorted_rates)):
                if sorted_rates[i][0] < sorted_rates[i - 1][0]:
                    issues.append("Interest rates should increase with priority (senior < subordinated)")

        return len(issues) == 0, issues
