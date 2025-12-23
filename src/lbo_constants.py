"""
Constants for LBO Model Generator.
Extracts magic numbers and hard-coded values for better maintainability.
"""


class LBOConstants:
    """Constants used throughout the LBO model generator."""

    # Default financial ratios
    DEFAULT_TAX_RATE = 0.25
    DEFAULT_DSO = 45.0
    DEFAULT_DIO = 30.0
    DEFAULT_DPO = 30.0

    # Default transaction costs
    DEFAULT_TRANSACTION_EXPENSES_PCT = 0.03  # 3% of EV
    DEFAULT_FINANCING_FEES_PCT = 0.02  # 2% of total debt

    # Default operating assumptions
    DEFAULT_COGS_PCT = 0.70
    DEFAULT_SGANDA_PCT = 0.15
    DEFAULT_CAPEX_PCT = 0.03
    DEFAULT_DEPRECIATION_PCT_OF_PPE = 0.10

    # Estimation ratios (when initial values not provided)
    DEFAULT_PPE_TO_REVENUE_RATIO = 0.3
    DEFAULT_DEPRECIATION_TO_REVENUE_RATIO = 0.015
    DEFAULT_AMORTIZATION_TO_REVENUE_RATIO = 0.005

    # Default exit assumptions
    DEFAULT_EXIT_YEAR = 5
    DEFAULT_EXIT_MULTIPLE = 7.5

    # Calculation parameters
    MAX_IRR_ITERATIONS = 100
    IRR_EPSILON = 1e-6
    MAX_IRR_RATE = 10.0  # 1000% max to prevent unrealistic rates

    # Balance sheet validation
    BALANCE_SHEET_TOLERANCE = 1.0  # Allow $1 rounding difference

    # Cash flow validation
    CASH_FLOW_TOLERANCE = 0.01

    # Equity validation thresholds
    MIN_EQUITY_TO_EV_RATIO = 0.1  # Warn if equity < 10% of EV
    WARN_NEGATIVE_EQUITY = True

    # Working capital days limits
    MIN_WORKING_CAPITAL_DAYS = 0
    MAX_WORKING_CAPITAL_DAYS = 365

    # Percentage limits
    MIN_PERCENTAGE = 0.0
    MAX_PERCENTAGE = 1.0

    # Excel export constants
    EXCEL_THOUSANDS_DIVISOR = 1000  # Convert values to thousands for Excel display

    # Rounding constants
    DECIMAL_PLACES = 2  # Round all financial values to 2 decimal places
