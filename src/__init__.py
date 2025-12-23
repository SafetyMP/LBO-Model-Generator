"""
LBO Model Generator Package

A comprehensive tool for generating Leveraged Buyout (LBO) financial models.
"""

__version__ = "1.0.0"
__author__ = "Sage Hart"

from .lbo_model_generator import LBOModel, LBOAssumptions, LBODebtStructure, create_lbo_from_inputs

from .lbo_ai_recommender import LBOModelAIRecommender, recommend_lbo_parameters

from .lbo_ai_validator import LBOModelAIValidator, ValidationResult, ScenarioAnalysis, BenchmarkResult

from .lbo_exceptions import (
    LBOError,
    LBOValidationError,
    LBOConfigurationError,
    LBOAIServiceError,
    LBOExcelExportError,
    LBOCalculationError,
)

from .lbo_constants import LBOConstants

# Logging configuration
try:
    from .lbo_logging import setup_logging, get_logger
except ImportError:
    from lbo_logging import setup_logging, get_logger

# Excel formatting helpers
try:
    from .lbo_excel_helpers import ExcelFormattingHelper
except ImportError:
    from lbo_excel_helpers import ExcelFormattingHelper

# Audit and validation modules
try:
    from .lbo_model_auditor import LBOModelAuditor, AuditReport, AuditFinding
    from .lbo_consistency_helpers import LBOConsistencyHelper
    from .lbo_validation_enhanced import EnhancedLBOValidator, ValidationResult as EnhancedValidationResult
    from .lbo_chart_improvements import ChartStructureImprover
except ImportError:
    LBOModelAuditor = None
    AuditReport = None
    AuditFinding = None
    LBOConsistencyHelper = None
    EnhancedLBOValidator = None
    EnhancedValidationResult = None
    ChartStructureImprover = None

# Excel export classes
try:
    from .lbo_industry_standards import IndustryStandardTemplate
    from .lbo_industry_excel import IndustryStandardExcelExporter
    from .lbo_excel_template import LBOExcelTemplate
except ImportError:
    # Handle direct imports
    try:
        from lbo_industry_standards import IndustryStandardTemplate
        from lbo_industry_excel import IndustryStandardExcelExporter
        from lbo_excel_template import LBOExcelTemplate
    except ImportError:
        IndustryStandardTemplate = None
        IndustryStandardExcelExporter = None
        LBOExcelTemplate = None

__all__ = [
    # Core model classes
    "LBOModel",
    "LBOAssumptions",
    "LBODebtStructure",
    "create_lbo_from_inputs",
    # AI classes
    "LBOModelAIRecommender",
    "recommend_lbo_parameters",
    "LBOModelAIValidator",
    "ValidationResult",
    "ScenarioAnalysis",
    "BenchmarkResult",
    # Exception classes
    "LBOError",
    "LBOValidationError",
    "LBOConfigurationError",
    "LBOAIServiceError",
    "LBOExcelExportError",
    "LBOCalculationError",
    # Constants
    "LBOConstants",
    # Logging
    "setup_logging",
    "get_logger",
    # Excel helpers
    "ExcelFormattingHelper",
    # Excel export classes
    "IndustryStandardTemplate",
    "IndustryStandardExcelExporter",
    "LBOExcelTemplate",  # Alternative format utilities
    # Audit and validation
    "LBOModelAuditor",
    "AuditReport",
    "AuditFinding",
    "LBOConsistencyHelper",
    "EnhancedLBOValidator",
    "EnhancedValidationResult",  # From lbo_validation_enhanced
    "ChartStructureImprover",
]
