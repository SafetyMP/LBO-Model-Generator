"""
Custom exception classes for LBO Model Generator.
"""


class LBOError(Exception):
    """Base exception for LBO model errors."""

    pass


class LBOValidationError(LBOError):
    """Raised when model assumptions fail validation."""

    pass


class LBOConfigurationError(LBOError):
    """Raised when configuration is invalid or missing."""

    pass


class LBOAIServiceError(LBOError):
    """Raised when AI service calls fail."""

    pass


class LBOExcelExportError(LBOError):
    """Raised when Excel export fails."""

    pass


class LBOCalculationError(LBOError):
    """Raised when financial calculations fail."""

    pass
