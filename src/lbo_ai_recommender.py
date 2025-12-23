"""
AI-Powered LBO Model Recommender

Uses Large Language Models to analyze business descriptions and recommend
appropriate LBO model parameters.
"""

import json
import os
import logging
from typing import Dict, Optional
import openai
from dataclasses import dataclass

# Handle both package and direct imports
try:
    from .lbo_exceptions import LBOAIServiceError, LBOConfigurationError
    from .lbo_validation import validate_api_key
except ImportError:
    from lbo_exceptions import LBOAIServiceError, LBOConfigurationError
    from lbo_validation import validate_api_key

logger = logging.getLogger(__name__)


@dataclass
class LBORecommendations:
    """Recommended LBO model parameters from AI analysis."""
    entry_ebitda: Optional[float] = None
    entry_multiple: Optional[float] = None
    revenue_growth_rate: Optional[list] = None
    cogs_pct_of_revenue: Optional[float] = None
    sganda_pct_of_revenue: Optional[float] = None
    capex_pct_of_revenue: Optional[float] = None
    tax_rate: Optional[float] = None
    days_sales_outstanding: Optional[float] = None
    days_inventory_outstanding: Optional[float] = None
    days_payable_outstanding: Optional[float] = None
    debt_recommendations: Optional[list] = None
    exit_multiple: Optional[float] = None
    confidence_level: Optional[str] = None
    reasoning: Optional[str] = None


class LBOModelAIRecommender:
    """AI-powered recommender for LBO model parameters."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize AI recommender.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        # Validate API key
        try:
            self.api_key = validate_api_key(api_key)
        except LBOConfigurationError as e:
            raise LBOConfigurationError(str(e)) from e
        
        # Security: Do not set global API key, only use client instance
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def _get_system_message(self) -> str:
        """Get system message for AI recommendations."""
        return (
            "You are a financial modeling expert specializing in leveraged buyouts (LBOs). "
            "Analyze business descriptions and provide realistic LBO model parameters "
            "based on industry standards, company characteristics, and market conditions."
        )
    
    def _call_recommendation_api(self, prompt: str) -> Dict:
        """Call OpenAI API for recommendations."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_message()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        recommendations_json = response.choices[0].message.content
        return json.loads(recommendations_json)
    
    def _handle_recommendation_errors(self, e: Exception) -> None:
        """Handle errors during recommendation generation."""
        if isinstance(e, openai.OpenAIError):
            logger.error(f"OpenAI API error: {e}", exc_info=True)
            raise LBOAIServiceError(f"OpenAI API error: {str(e)}") from e
        elif isinstance(e, json.JSONDecodeError):
            logger.error(f"JSON decode error: {e}", exc_info=True)
            raise LBOAIServiceError(f"Invalid JSON response from AI: {str(e)}") from e
        else:
            logger.error(f"Unexpected error getting AI recommendations: {e}", exc_info=True)
            raise LBOAIServiceError(f"Error getting AI recommendations: {str(e)}") from e
    
    def recommend_parameters(self, business_description: str, 
                           current_revenue: Optional[float] = None,
                           current_ebitda: Optional[float] = None,
                           industry: Optional[str] = None) -> Dict:
        """
        Generate LBO model parameter recommendations from business description.
        
        Args:
            business_description: Natural language description of the business
            current_revenue: Current annual revenue (if known)
            current_ebitda: Current EBITDA (if known)
            industry: Industry sector (if known)
        
        Returns:
            Dictionary with recommended parameters matching LBO input format
        """
        prompt = self._create_recommendation_prompt(
            business_description, current_revenue, current_ebitda, industry
        )
        
        try:
            recommendations = self._call_recommendation_api(prompt)
            return self._parse_recommendations(recommendations)
        except Exception as e:
            self._handle_recommendation_errors(e)
    
    def _create_recommendation_prompt(self, business_description: str,
                                     current_revenue: Optional[float],
                                     current_ebitda: Optional[float],
                                     industry: Optional[str]) -> str:
        """Create prompt for AI analysis."""
        prompt = f"""Analyze the following business description and provide recommended parameters for a Leveraged Buyout (LBO) model.

BUSINESS DESCRIPTION:
{business_description}
"""
        
        if industry:
            prompt += f"\nINDUSTRY: {industry}"
        
        if current_revenue:
            prompt += f"\nCURRENT ANNUAL REVENUE: ${current_revenue:,.0f}"
        
        if current_ebitda:
            prompt += f"\nCURRENT EBITDA: ${current_ebitda:,.0f}"
        
        prompt += """

Provide your analysis and recommendations in the following JSON format. Use realistic, industry-appropriate values based on:
- Company size and growth stage
- Industry characteristics (margins, growth rates, capital intensity)
- Market conditions and comparable transactions
- Typical LBO financing structures for similar businesses

For revenue growth rates, provide 5 years of projections. For EBITDA margins, estimate based on industry norms.
For debt structure, recommend senior debt (typically 1-2x EBITDA, 6-8% interest) and subordinated debt (1-3x EBITDA, 10-14% interest) if appropriate.

Return ONLY valid JSON in this exact format:
{
    "entry_ebitda": 10000,
    "entry_multiple": 6.5,
    "revenue_growth_rate": [0.08, 0.07, 0.06, 0.05, 0.05],
    "cogs_pct_of_revenue": 0.65,
    "sganda_pct_of_revenue": 0.20,
    "capex_pct_of_revenue": 0.04,
    "tax_rate": 0.25,
    "days_sales_outstanding": 45.0,
    "days_inventory_outstanding": 35.0,
    "days_payable_outstanding": 30.0,
    "debt_recommendations": [
        {
            "name": "Senior Debt",
            "ebitda_multiple": 1.5,
            "interest_rate": 0.075,
            "amortization_schedule": "amortizing",
            "amortization_periods": 5
        },
        {
            "name": "Subordinated Debt",
            "ebitda_multiple": 2.0,
            "interest_rate": 0.12,
            "amortization_schedule": "bullet"
        }
    ],
    "exit_multiple": 7.5,
    "confidence_level": "high",
    "reasoning": "Brief explanation of key recommendations..."
}

Important considerations:
- Entry multiple should reflect industry and company characteristics (typically 4-10x EBITDA)
- Revenue growth should be realistic for the business stage (mature: 2-5%, growth: 5-15%, high-growth: 15%+)
- EBITDA margins vary by industry (software: 20-40%, manufacturing: 10-20%, services: 15-25%)
- Working capital days depend on business model (B2B longer, B2C shorter)
- Debt structure should be conservative for smaller/riskier businesses
- Exit multiple typically 0.5-1.5x higher than entry multiple
"""
        
        return prompt
    
    def _parse_recommendations(self, ai_response: Dict) -> Dict:
        """Parse AI response into LBO model input format."""
        recommendations = {
            "entry_ebitda": ai_response.get("entry_ebitda"),
            "entry_multiple": ai_response.get("entry_multiple"),
            "revenue_growth_rate": ai_response.get("revenue_growth_rate", [0.05] * 5),
            "cogs_pct_of_revenue": ai_response.get("cogs_pct_of_revenue"),
            "sganda_pct_of_revenue": ai_response.get("sganda_pct_of_revenue"),
            "capex_pct_of_revenue": ai_response.get("capex_pct_of_revenue"),
            "tax_rate": ai_response.get("tax_rate"),
            "days_sales_outstanding": ai_response.get("days_sales_outstanding"),
            "days_inventory_outstanding": ai_response.get("days_inventory_outstanding"),
            "days_payable_outstanding": ai_response.get("days_payable_outstanding"),
            "exit_multiple": ai_response.get("exit_multiple"),
            "debt_instruments": ai_response.get("debt_recommendations", []),
            "_ai_metadata": {
                "confidence_level": ai_response.get("confidence_level"),
                "reasoning": ai_response.get("reasoning")
            }
        }
        
        return recommendations
    
    def explain_recommendations(self, recommendations: Dict) -> str:
        """Generate human-readable explanation of recommendations."""
        metadata = recommendations.get("_ai_metadata", {})
        reasoning = metadata.get("reasoning", "No reasoning provided.")
        confidence = metadata.get("confidence_level", "unknown")
        
        explanation = f"""
AI RECOMMENDATIONS SUMMARY
{'=' * 60}

Confidence Level: {confidence.upper()}

Key Recommendations:
{reasoning}

Recommended Parameters:
- Entry EBITDA: ${recommendations.get('entry_ebitda', 0):,.0f}
- Entry Multiple: {recommendations.get('entry_multiple', 0):.1f}x
- Exit Multiple: {recommendations.get('exit_multiple', 0):.1f}x
- Revenue Growth (5-year avg): {sum(recommendations.get('revenue_growth_rate', [0])) / len(recommendations.get('revenue_growth_rate', [1])) * 100:.1f}%

Operating Metrics:
- COGS: {recommendations.get('cogs_pct_of_revenue', 0) * 100:.1f}% of revenue
- SG&A: {recommendations.get('sganda_pct_of_revenue', 0) * 100:.1f}% of revenue
- CapEx: {recommendations.get('capex_pct_of_revenue', 0) * 100:.1f}% of revenue

Working Capital:
- DSO: {recommendations.get('days_sales_outstanding', 0):.0f} days
- DIO: {recommendations.get('days_inventory_outstanding', 0):.0f} days
- DPO: {recommendations.get('days_payable_outstanding', 0):.0f} days

Debt Structure:
"""
        
        for debt in recommendations.get("debt_instruments", []):
            explanation += f"- {debt.get('name', 'Debt')}: {debt.get('ebitda_multiple', 0):.1f}x EBITDA, "
            explanation += f"{debt.get('interest_rate', 0) * 100:.1f}% interest, "
            explanation += f"{debt.get('amortization_schedule', 'bullet')}\n"
        
        explanation += "\n" + "=" * 60
        explanation += "\n\nNote: These are AI-generated recommendations based on general industry patterns."
        explanation += "\nPlease review and adjust based on specific company circumstances and market conditions."
        
        return explanation


def recommend_lbo_parameters(business_description: str,
                            api_key: Optional[str] = None,
                            current_revenue: Optional[float] = None,
                            current_ebitda: Optional[float] = None,
                            industry: Optional[str] = None,
                            model: str = "gpt-4o-mini") -> Dict:
    """
    Convenience function to get LBO parameter recommendations.
    
    Args:
        business_description: Natural language description of business
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        current_revenue: Current annual revenue
        current_ebitda: Current EBITDA
        industry: Industry sector
        model: OpenAI model to use
    
    Returns:
        Dictionary with recommended LBO parameters
    """
    recommender = LBOModelAIRecommender(api_key=api_key, model=model)
    return recommender.recommend_parameters(
        business_description, current_revenue, current_ebitda, industry
    )


if __name__ == "__main__":
    # Example usage
    example_description = """
    TechCorp is a SaaS company providing project management software for mid-market
    companies. Founded in 2018, they have grown to $15M ARR with 40% EBITDA margins.
    The company serves 500+ customers with strong retention rates. They are looking
    to expand sales and marketing to accelerate growth.
    """
    
    try:
        recommender = LBOModelAIRecommender()
        recommendations = recommender.recommend_parameters(
            example_description,
            current_revenue=15_000_000,
            industry="SaaS Software"
        )
        
        print(recommender.explain_recommendations(recommendations))
        
        # Save recommendations
        with open("ai_recommendations.json", "w") as f:
            json.dump(recommendations, f, indent=2)
        print("\nRecommendations saved to ai_recommendations.json")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nTo use AI recommendations, set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")

