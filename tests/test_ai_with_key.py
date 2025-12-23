"""
Test AI Recommendations with API Key
Run this script after setting OPENAI_API_KEY environment variable
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from lbo_ai_recommender import LBOModelAIRecommender, recommend_lbo_parameters
    from lbo_model_generator import create_lbo_from_inputs
except ImportError:
    print("Error: Required modules not found. Make sure lbo_ai_recommender.py is available.")
    sys.exit(1)

def test_with_api_key():
    """Test AI recommendations with actual API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("=" * 80)
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("=" * 80)
        print("\nTo run this test:")
        print("1. Get an OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Set it as an environment variable:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("3. Run this script again")
        print("\nAlternatively, use test_ai_mock.py for a demonstration without API key.")
        return False
    
    print("=" * 80)
    print("AI RECOMMENDATIONS TEST (WITH API KEY)")
    print("=" * 80)
    # Security: Do not log API key, even partially
    print("\n⚠️  WARNING: This will make real API calls and may incur costs.")
    print("   Press Ctrl+C to cancel, or wait 5 seconds to continue...\n")
    
    try:
        import time
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        return False
    
    try:
        # Test 1: Basic recommendation
        print("\n" + "-" * 80)
        print("TEST 1: Basic AI Recommendation")
        print("-" * 80)
        
        recommender = LBOModelAIRecommender(api_key=api_key)
        
        # Load AI-generated test company
        from pathlib import Path
        test_company_file = Path(__file__).parent / "ai_test_company.json"
        if test_company_file.exists():
            with open(test_company_file, 'r') as f:
                company_data = json.load(f)
            business_description = company_data.get('business_description', '')
            company_name = company_data.get('company_name', 'Test Company')
            industry = company_data.get('industry', 'SaaS')
            current_revenue = company_data.get('current_revenue', 35_000_000)
            current_ebitda = company_data.get('current_ebitda', 7_000_000)
        else:
            # Fallback
            business_description = """
            TechCorp is a SaaS company providing project management software for mid-market
            companies. Founded in 2018, they have grown to $15M annual recurring revenue 
            with 35% EBITDA margins. The company serves 500+ customers with strong retention 
            rates of 95%. They are looking to expand sales and marketing to accelerate growth.
            """
            company_name = "TechCorp"
            industry = "SaaS Software"
            current_revenue = 15_000_000
            current_ebitda = 5_250_000
        
        print(f"Company: {company_name}")
        print(f"Industry: {industry}")
        print("\nBusiness Description:")
        print(business_description.strip())
        print("\n🔄 Getting AI recommendations...")
        
        recommendations = recommender.recommend_parameters(
            business_description,
            current_revenue=current_revenue,
            current_ebitda=current_ebitda,
            industry=industry
        )
        
        print("✓ Recommendations received!")
        print("\n" + "=" * 80)
        print("AI RECOMMENDATIONS")
        print("=" * 80)
        print(json.dumps(recommendations, indent=2))
        
        # Test 2: Explanation
        print("\n" + "=" * 80)
        print("EXPLANATION")
        print("=" * 80)
        explanation = recommender.explain_recommendations(recommendations)
        print(explanation)
        
        # Test 3: Create model from recommendations
        print("\n" + "=" * 80)
        print("TEST 2: Model Generation from AI Recommendations")
        print("=" * 80)
        print("\n🔄 Creating LBO model from AI recommendations...")
        
        model = create_lbo_from_inputs(recommendations)
        returns = model.calculate_returns()
        
        print("✓ Model generated successfully!")
        print("\nReturns Analysis:")
        print(f"  Exit Year:              {returns['exit_year']}")
        print(f"  Exit EBITDA:            ${returns['exit_ebitda']:,.0f}")
        print(f"  Exit Enterprise Value:  ${returns['exit_ev']:,.0f}")
        print(f"  Exit Equity Value:      ${returns['exit_equity_value']:,.0f}")
        print(f"  Equity Invested:        ${returns['equity_invested']:,.0f}")
        print(f"  MOIC:                   {returns['moic']:.2f}x")
        print(f"  IRR:                    {returns['irr']:.2f}%")
        
        # Test 4: Convenience function
        print("\n" + "=" * 80)
        print("TEST 3: Convenience Function")
        print("=" * 80)
        
        recommendations2 = recommend_lbo_parameters(
            "Manufacturing company with $50M revenue and 15% EBITDA margin",
            current_revenue=50_000_000,
            current_ebitda=7_500_000,
            industry="Manufacturing",
            api_key=api_key
        )
        
        print("✓ Convenience function works!")
        print(f"  Entry Multiple: {recommendations2.get('entry_multiple', 'N/A')}")
        print(f"  Revenue Growth: {recommendations2.get('revenue_growth_rate', [])[:3]}")
        
        print("\n" + "=" * 80)
        print("✓ ALL TESTS PASSED")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import json
    success = test_with_api_key()
    sys.exit(0 if success else 1)
