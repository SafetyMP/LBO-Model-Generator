"""
LBO Model Auditor using OpenAI API.

This module provides comprehensive auditing capabilities for LBO models,
including consistency checks, test case comparisons, and chart structure analysis.
"""

import json
import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class AuditFinding:
    """Represents a single audit finding."""

    severity: str  # "error", "warning", "info"
    category: str  # "consistency", "test_case", "chart", "calculation"
    description: str
    recommendation: str
    affected_cases: List[str] = None


@dataclass
class AuditReport:
    """Complete audit report."""

    findings: List[AuditFinding]
    consistency_score: float
    test_case_alignment: Dict[str, float]
    chart_recommendations: List[Dict[str, Any]]
    overall_recommendations: List[str]


class LBOModelAuditor:
    """Auditor for LBO models using OpenAI API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize auditor with OpenAI API key."""
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package required. Install with: pip install openai")

        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key parameter."
            )

    def audit_model_consistency(self, test_cases: Dict[str, Dict]) -> AuditReport:
        """
        Audit model consistency across test cases.

        Args:
            test_cases: Dictionary of test case names to their configurations

        Returns:
            AuditReport with findings and recommendations
        """
        logger.info("Starting model consistency audit...")

        prompt = self._create_consistency_audit_prompt(test_cases)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert LBO model auditor specializing in financial modeling consistency and best practices.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )

            result = json.loads(response.choices[0].message.content)
            return self._parse_audit_response(result, test_cases)

        except Exception as e:
            logger.error(f"Error in consistency audit: {e}")
            raise

    def audit_test_case_alignment(
        self, case_name: str, config: Dict, target_metrics: Optional[Dict] = None
    ) -> Dict:
        """
        Audit a specific test case against target metrics.

        Args:
            case_name: Name of the test case
            config: Configuration dictionary
            target_metrics: Optional target metrics to compare against

        Returns:
            Dictionary with alignment analysis
        """
        logger.info(f"Auditing test case alignment for {case_name}...")

        prompt = self._create_test_case_audit_prompt(case_name, config, target_metrics)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert LBO model auditor specializing in test case validation and target metric alignment.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=1500,
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            logger.error(f"Error in test case audit: {e}")
            raise

    def audit_chart_structure(self, excel_file_path: str) -> List[Dict[str, Any]]:
        """
        Audit chart structure in Excel file.

        Args:
            excel_file_path: Path to Excel file

        Returns:
            List of chart recommendations
        """
        logger.info(f"Auditing chart structure in {excel_file_path}...")

        try:
            import openpyxl

            wb = openpyxl.load_workbook(excel_file_path, data_only=True)

            chart_info = self._extract_chart_info(wb)
            prompt = self._create_chart_audit_prompt(chart_info)

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in financial model visualization and Excel chart design for LBO models. Always return valid JSON only, no markdown formatting.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )

            content = response.choices[0].message.content
            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in chart audit: {e}")
            logger.debug(
                f"Response content: {response.choices[0].message.content if 'response' in locals() else 'N/A'}"
            )
            # Return default structure
            return {
                "recommendations": [
                    {
                        "chart_name": "All Charts",
                        "issue": "Unable to parse audit response",
                        "recommendation": "Review chart structure manually",
                        "priority": "medium",
                    }
                ],
                "missing_charts": [],
                "overall_structure_score": 0.5,
            }
        except Exception as e:
            logger.error(f"Error in chart audit: {e}", exc_info=True)
            raise

    def _create_consistency_audit_prompt(self, test_cases: Dict[str, Dict]) -> str:
        """Create prompt for consistency audit."""
        prompt = """Analyze the following LBO model test cases for consistency issues, best practices violations, and areas for improvement.

TEST CASES:
"""
        for name, config in test_cases.items():
            prompt += f"\n{name}:\n{json.dumps(config, indent=2)}\n"

        prompt += """
Analyze for:
1. Inconsistencies in debt structure (some have sub debt, some don't)
2. Inconsistent parameter usage (target_exit_debt, fcf_conversion_rate)
3. Calculation methodology issues
4. Missing validations or error handling
5. Best practices violations

Return JSON in this format:
{
    "findings": [
        {
            "severity": "error|warning|info",
            "category": "consistency|test_case|calculation",
            "description": "Detailed description",
            "recommendation": "How to fix",
            "affected_cases": ["case1", "case2"]
        }
    ],
    "consistency_score": 0.85,
    "overall_recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}
"""
        return prompt

    def _create_test_case_audit_prompt(
        self, case_name: str, config: Dict, target_metrics: Optional[Dict]
    ) -> str:
        """Create prompt for test case audit."""
        prompt = f"""Analyze the following LBO model test case for alignment with target metrics and best practices.

CASE: {case_name}
CONFIGURATION:
{json.dumps(config, indent=2)}
"""

        if target_metrics:
            prompt += f"\nTARGET METRICS:\n{json.dumps(target_metrics, indent=2)}\n"

        prompt += """
Analyze for:
1. Alignment with target metrics (if provided)
2. Reasonableness of assumptions
3. Missing required parameters
4. Potential calculation errors
5. Best practices compliance

Return JSON:
{
    "alignment_score": 0.90,
    "issues": [
        {
            "severity": "error|warning|info",
            "description": "Issue description",
            "recommendation": "How to fix"
        }
    ],
    "recommendations": ["rec1", "rec2"]
}
"""
        return prompt

    def _create_chart_audit_prompt(self, chart_info: Dict) -> str:
        """Create prompt for chart audit."""
        chart_info_str = json.dumps(chart_info, indent=2)
        prompt = f"""Analyze the following Excel chart structure for an LBO model and provide recommendations for improvement.

CHART INFORMATION:
{chart_info_str}

Analyze for:
1. Chart type appropriateness
2. Data series organization
3. Axis labeling and formatting
4. Color schemes and visual hierarchy
5. Missing charts or data visualizations
6. Industry standard compliance

Return JSON in this exact format:
{{
    "recommendations": [
        {{
            "chart_name": "Chart name",
            "issue": "Issue description",
            "recommendation": "How to improve",
            "priority": "high|medium|low"
        }}
    ],
    "missing_charts": ["chart1", "chart2"],
    "overall_structure_score": 0.85
}}
"""
        return prompt

    def _extract_chart_title(self, chart) -> str:
        """Extract chart title safely."""
        chart_title = "Untitled"
        try:
            if hasattr(chart, "title") and chart.title:
                if hasattr(chart.title, "text"):
                    chart_title = str(chart.title.text)
                elif hasattr(chart.title, "tx"):
                    if hasattr(chart.title.tx, "rich"):
                        chart_title = "Rich Text Title"
                    elif hasattr(chart.title.tx, "strRef"):
                        chart_title = "Formula Reference"
                    else:
                        chart_title = str(chart.title.tx)
                elif isinstance(chart.title, str):
                    chart_title = chart.title
                else:
                    chart_title = str(chart.title)
        except (AttributeError, TypeError) as e:
            logger.debug(f"Could not extract chart title: {e}")
            chart_title = "Unknown Title"
        except Exception as e:
            logger.warning(f"Unexpected error extracting chart title: {e}", exc_info=True)
            chart_title = "Unknown Title"

        return chart_title

    def _get_chart_series_count(self, chart) -> int:
        """Get chart series count safely."""
        series_count = 0
        try:
            if hasattr(chart, "series"):
                series_count = len(chart.series)
        except (AttributeError, TypeError) as e:
            logger.debug(f"Could not get series count: {e}")
        except Exception as e:
            logger.warning(f"Unexpected error getting series count: {e}", exc_info=True)

        return series_count

    def _extract_charts_from_sheet(self, ws, sheet_name: str) -> List[Dict]:
        """Extract charts from a single worksheet."""
        charts = []

        if not hasattr(ws, "_charts"):
            return charts

        for chart in ws._charts:
            chart_title = self._extract_chart_title(chart)
            series_count = self._get_chart_series_count(chart)

            charts.append(
                {
                    "type": type(chart).__name__,
                    "title": str(chart_title),
                    "series_count": int(series_count),
                }
            )

        return charts

    def _extract_chart_info(self, wb) -> Dict:
        """Extract chart information from workbook."""
        chart_info = {"sheets": [], "total_charts": 0}

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            charts = self._extract_charts_from_sheet(ws, sheet_name)

            if charts:
                chart_info["sheets"].append({"name": str(sheet_name), "charts": charts})
                chart_info["total_charts"] += len(charts)

        return chart_info

    def _parse_audit_response(self, result: Dict, test_cases: Dict) -> AuditReport:
        """Parse audit response into AuditReport."""
        findings = []
        for finding_data in result.get("findings", []):
            findings.append(
                AuditFinding(
                    severity=finding_data.get("severity", "info"),
                    category=finding_data.get("category", "consistency"),
                    description=finding_data.get("description", ""),
                    recommendation=finding_data.get("recommendation", ""),
                    affected_cases=finding_data.get("affected_cases", []),
                )
            )

        return AuditReport(
            findings=findings,
            consistency_score=result.get("consistency_score", 0.0),
            test_case_alignment={},
            chart_recommendations=result.get("chart_recommendations", []),
            overall_recommendations=result.get("overall_recommendations", []),
        )
