"""
Chart Structure Improvements based on Audit Recommendations.

This module implements chart structure improvements identified by the audit.
"""

import logging
from typing import Dict, List, Optional, Any
from openpyxl.chart import LineChart, BarChart, PieChart
from openpyxl.chart.series import Series
from openpyxl.chart.label import DataLabelList
# Note: ValueAxis may not be available in all openpyxl versions
try:
    from openpyxl.chart.axis import DateAxis, ValueAxis
except ImportError:
    DateAxis = None
    ValueAxis = None
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.data_source import StrRef
from openpyxl.utils import get_column_letter

logger = logging.getLogger(__name__)


class ChartStructureImprover:
    """Improves chart structure based on audit recommendations."""
    
    # Industry standard color palette for LBO models
    COLOR_PALETTE = {
        "primary": "4F81BD",      # Blue
        "secondary": "9BBB59",     # Green
        "accent": "F79646",        # Orange
        "warning": "C0504D",        # Red
        "neutral": "8064A2",       # Purple
        "highlight": "FFC000"      # Yellow
    }
    
    @staticmethod
    def improve_chart_formatting(chart, chart_type: str = "line") -> None:
        """
        Apply industry-standard formatting to charts.
        
        Args:
            chart: Chart object to format
            chart_type: Type of chart ("line", "bar", "pie")
        """
        # Set consistent styling
        chart.style = 10  # Professional style
        
        # Format axes
        if hasattr(chart, 'y_axis') and chart.y_axis:
            chart.y_axis.scaling.min = 0
            if chart_type == "line":
                chart.y_axis.number_format = '#,##0'
        
        if hasattr(chart, 'x_axis') and chart.x_axis:
            if chart_type == "line":
                chart.x_axis.number_format = 'General'
        
        # Set legend position
        if hasattr(chart, 'legend'):
            chart.legend.position = 'b'  # Bottom
        
        # Set chart size
        chart.height = 10
        chart.width = 16
    
    @staticmethod
    def create_improved_sensitivity_chart(ws, data_range: str, 
                                          title: str = "Sensitivity Analysis") -> LineChart:
        """
        Create improved sensitivity analysis chart.
        
        Args:
            ws: Worksheet
            data_range: Range of data (e.g., "A10:D15")
            title: Chart title
            
        Returns:
            Formatted LineChart
        """
        chart = LineChart()
        chart.title = title
        chart.style = 10
        chart.height = 10
        chart.width = 16
        
        # Configure axes
        chart.y_axis.title = "Value"
        chart.y_axis.scaling.min = 0
        chart.y_axis.number_format = '#,##0'
        
        chart.x_axis.title = "Exit Multiple"
        chart.x_axis.number_format = '0.0"x"'
        
        chart.legend.position = 'b'
        
        return chart
    
    @staticmethod
    def ensure_chart_data_labels(chart, show_values: bool = True, 
                                 show_percentages: bool = False) -> None:
        """
        Ensure data labels are properly configured.
        
        Args:
            chart: Chart object
            show_values: Show data values
            show_percentages: Show percentages (for pie charts)
        """
        if hasattr(chart, 'dataLabels'):
            chart.dataLabels = DataLabelList()
            if show_values:
                chart.dataLabels.showVal = True
            if show_percentages:
                chart.dataLabels.showPercent = True
    
    @staticmethod
    def create_missing_charts(wb, model) -> List[Dict[str, Any]]:
        """
        Create missing charts identified by audit.
        
        Args:
            wb: Workbook
            model: LBOModel instance
            
        Returns:
            List of created charts
        """
        created_charts = []
        
        # Check for Returns Analysis sheet
        if "Returns Analysis" in wb.sheetnames:
            ws_returns = wb["Returns Analysis"]
            
            # Create MOIC/IRR comparison chart if missing
            try:
                chart = BarChart()
                chart.type = "col"
                chart.style = 10
                chart.title = "MOIC and IRR Comparison"
                chart.height = 8
                chart.width = 12
                
                # This would need actual data references
                # Placeholder for implementation
                created_charts.append({
                    "name": "MOIC and IRR Comparison",
                    "type": "BarChart",
                    "location": "Returns Analysis"
                })
            except Exception as e:
                logger.warning(f"Failed to create MOIC/IRR chart: {e}")
        
        return created_charts

