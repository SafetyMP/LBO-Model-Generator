"""
Input validation utilities for LBO Model Generator.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Handle both package and direct imports
try:
    from .lbo_exceptions import LBOValidationError, LBOConfigurationError
    from .lbo_constants import LBOConstants
except ImportError:
    from lbo_exceptions import LBOValidationError, LBOConfigurationError
    from lbo_constants import LBOConstants


def validate_output_path(path: str) -> Path:
    """
    Validate and sanitize output file path.

    Args:
        path: Output file path

    Returns:
        Path object

    Raises:
        LBOConfigurationError: If path is invalid
    """
    try:
        path_obj = Path(path).resolve()

        # Check if parent directory exists
        if not path_obj.parent.exists():
            raise LBOConfigurationError(f"Output directory does not exist: {path_obj.parent}")

        # Check if parent directory is writable
        if not os.access(path_obj.parent, os.W_OK):
            raise LBOConfigurationError(f"Output directory is not writable: {path_obj.parent}")

        return path_obj
    except (ValueError, OSError) as e:
        raise LBOConfigurationError(f"Invalid output path: {path}") from e


def _validate_required_fields(config: Dict) -> List[str]:
    """Validate required fields."""
    errors = []
    required_fields = ["entry_ebitda", "entry_multiple", "revenue_growth_rate"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    return errors


def _validate_entry_fields(config: Dict) -> List[str]:
    """Validate entry EBITDA and multiple."""
    errors = []

    if "entry_ebitda" in config:
        if not isinstance(config["entry_ebitda"], (int, float)) or config["entry_ebitda"] <= 0:
            errors.append("entry_ebitda must be a positive number")

    if "entry_multiple" in config:
        if not isinstance(config["entry_multiple"], (int, float)) or config["entry_multiple"] <= 0:
            errors.append("entry_multiple must be a positive number")

    return errors


def _validate_growth_rates(config: Dict) -> List[str]:
    """Validate revenue growth rates."""
    errors = []

    if "revenue_growth_rate" in config:
        if not isinstance(config["revenue_growth_rate"], list):
            errors.append("revenue_growth_rate must be a list")
        elif len(config["revenue_growth_rate"]) == 0:
            errors.append("revenue_growth_rate cannot be empty")
        else:
            for i, rate in enumerate(config["revenue_growth_rate"]):
                if not isinstance(rate, (int, float)):
                    errors.append(f"revenue_growth_rate[{i}] must be a number")
                elif rate < -1 or rate > 1:
                    errors.append(f"revenue_growth_rate[{i}] must be between -1 and 1")

    return errors


def _validate_percentage_fields(config: Dict) -> List[str]:
    """Validate percentage fields."""
    errors = []
    percentage_fields = [
        "cogs_pct_of_revenue",
        "sganda_pct_of_revenue",
        "capex_pct_of_revenue",
        "tax_rate",
        "transaction_expenses_pct",
        "financing_fees_pct",
    ]
    for field in percentage_fields:
        if field in config:
            value = config[field]
            if not isinstance(value, (int, float)):
                errors.append(f"{field} must be a number")
            elif not (LBOConstants.MIN_PERCENTAGE <= value <= LBOConstants.MAX_PERCENTAGE):
                errors.append(f"{field} must be between 0 and 1")
    return errors


def _validate_working_capital_fields(config: Dict) -> List[str]:
    """Validate working capital fields."""
    errors = []
    wc_fields = ["days_sales_outstanding", "days_inventory_outstanding", "days_payable_outstanding"]
    for field in wc_fields:
        if field in config:
            value = config[field]
            if not isinstance(value, (int, float)):
                errors.append(f"{field} must be a number")
            elif not (LBOConstants.MIN_WORKING_CAPITAL_DAYS <= value <= LBOConstants.MAX_WORKING_CAPITAL_DAYS):
                errors.append(
                    f"{field} must be between {LBOConstants.MIN_WORKING_CAPITAL_DAYS} "
                    f"and {LBOConstants.MAX_WORKING_CAPITAL_DAYS}"
                )
    return errors


def _validate_debt_instruments(config: Dict) -> List[str]:
    """Validate debt instruments."""
    errors = []

    if "debt_instruments" in config:
        if not isinstance(config["debt_instruments"], list):
            errors.append("debt_instruments must be a list")
        else:
            for i, debt in enumerate(config["debt_instruments"]):
                if not isinstance(debt, dict):
                    errors.append(f"debt_instruments[{i}] must be a dictionary")
                else:
                    if "name" not in debt:
                        errors.append(f"debt_instruments[{i}] missing 'name' field")
                    if "interest_rate" not in debt:
                        errors.append(f"debt_instruments[{i}] missing 'interest_rate' field")
                    elif not isinstance(debt["interest_rate"], (int, float)) or debt["interest_rate"] < 0:
                        errors.append(f"debt_instruments[{i}].interest_rate must be a non-negative number")

    return errors


def validate_json_input(config: Dict) -> Dict:
    """
    Validate JSON input configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Validated configuration dictionary

    Raises:
        LBOValidationError: If validation fails
    """
    errors = []

    errors.extend(_validate_required_fields(config))
    errors.extend(_validate_entry_fields(config))
    errors.extend(_validate_growth_rates(config))
    errors.extend(_validate_percentage_fields(config))
    errors.extend(_validate_working_capital_fields(config))
    errors.extend(_validate_debt_instruments(config))

    if errors:
        raise LBOValidationError("Input validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    return config


def validate_api_key(api_key: Optional[str] = None) -> str:
    """
    Validate OpenAI API key format.

    Args:
        api_key: API key to validate (or None to get from env)

    Returns:
        Validated API key

    Raises:
        LBOConfigurationError: If API key is invalid
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise LBOConfigurationError(
            "OpenAI API key required. Set OPENAI_API_KEY environment variable " "or pass api_key parameter."
        )

    # Basic format validation (OpenAI keys start with 'sk-')
    if not api_key.startswith("sk-") or len(api_key) < 20:
        raise LBOConfigurationError(
            "Invalid API key format. OpenAI API keys should start with 'sk-' " "and be at least 20 characters long."
        )

    return api_key


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and invalid characters.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename
    """
    # Remove path separators and dangerous characters
    dangerous_chars = ["/", "\\", "..", "<", ">", ":", '"', "|", "?", "*"]
    sanitized = filename
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "_")

    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]

    return sanitized
