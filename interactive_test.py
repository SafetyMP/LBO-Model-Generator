#!/usr/bin/env python3
"""
Interactive LBO Model Test Generator

Allows users to test the LBO model generator with minimal input.
Uses AI to fill in missing information based on what the user provides.
"""

import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from lbo_model_generator import create_lbo_from_inputs
from lbo_ai_recommender import LBOModelAIRecommender
from lbo_ai_validator import LBOModelAIValidator
import openai


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80)


def print_section(text):
    """Print a section header."""
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)


def get_user_input(prompt, default=None, required=False, input_type=str):
    """Get user input with optional default and validation."""
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    
    if not required and not default:
        prompt_text += "(press Enter to skip - AI will generate)"
    elif not required and default:
        prompt_text += "(press Enter to use default or AI-generated value)"
    
    while True:
        try:
            value = input(prompt_text).strip()
            
            if not value:
                if default:
                    return default
                elif not required:
                    return None
                else:
                    print("  ⚠️  This field is required. Please enter a value.")
                    continue
            
            # Convert to appropriate type
            if input_type == float:
                # Remove $ and commas for easier input
                value = value.replace('$', '').replace(',', '').replace(' ', '')
                return float(value)
            elif input_type == int:
                # Remove commas for easier input
                value = value.replace(',', '').replace(' ', '')
                return int(value)
            elif input_type == bool:
                return value.lower() in ['y', 'yes', 'true', '1']
            else:
                return value
                
        except ValueError:
            print(f"  ⚠️  Invalid input. Please enter a valid {input_type.__name__}.")
            if input_type in [float, int]:
                print(f"      For numbers, enter without $ or commas (e.g., 35000000 for $35M)")
            continue


def generate_missing_info_with_ai(provided_info):
    """Use AI to generate missing company information."""
    print_section("🤖 Using AI to Generate Missing Information")
    print("Analyzing provided information and generating realistic values...")
    
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Build prompt with what we know
        known_info = []
        if provided_info.get('company_name'):
            known_info.append(f"Company Name: {provided_info['company_name']}")
        if provided_info.get('industry'):
            known_info.append(f"Industry: {provided_info['industry']}")
        if provided_info.get('business_description'):
            known_info.append(f"Business Description: {provided_info['business_description']}")
        if provided_info.get('current_revenue'):
            known_info.append(f"Current Revenue: ${provided_info['current_revenue']:,.0f}")
        if provided_info.get('current_ebitda'):
            known_info.append(f"Current EBITDA: ${provided_info['current_ebitda']:,.0f}")
        
        prompt = f"""Based on the following company information, generate realistic missing details for a Leveraged Buyout (LBO) model.

PROVIDED INFORMATION:
{chr(10).join(known_info) if known_info else "None provided"}

Generate a complete company profile with:
1. Company name (if not provided)
2. Industry sector
3. Detailed business description
4. Current annual revenue (if not provided)
5. Current EBITDA (if not provided)
6. Key business characteristics
7. Growth prospects

Return JSON format:
{{
    "company_name": "...",
    "industry": "...",
    "business_description": "...",
    "current_revenue": 0,
    "current_ebitda": 0,
    "key_characteristics": ["...", "..."],
    "growth_prospects": "..."
}}

Make the company realistic for LBO analysis (mid-market, $10M-$100M revenue range)."""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial analyst creating realistic company profiles for LBO modeling."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        ai_data = json.loads(response.choices[0].message.content)
        
        # Merge with provided info (provided info takes precedence)
        complete_info = {**ai_data, **provided_info}
        
        print("✓ AI-generated information:")
        if not provided_info.get('company_name'):
            print(f"  - Company Name: {complete_info.get('company_name', 'N/A')}")
        if not provided_info.get('industry'):
            print(f"  - Industry: {complete_info.get('industry', 'N/A')}")
        if not provided_info.get('business_description'):
            print(f"  - Business Description: {complete_info.get('business_description', 'N/A')[:100]}...")
        if not provided_info.get('current_revenue'):
            print(f"  - Current Revenue: ${complete_info.get('current_revenue', 0):,.0f}")
        if not provided_info.get('current_ebitda'):
            print(f"  - Current EBITDA: ${complete_info.get('current_ebitda', 0):,.0f}")
        
        return complete_info
        
    except Exception as e:
        print(f"⚠️  Error generating AI information: {e}")
        print("   Using default values instead...")
        return provided_info


def get_lbo_parameters_from_ai(company_info):
    """Get LBO model parameters from AI based on company information."""
    print_section("📊 Getting AI-Generated LBO Parameters")
    
    try:
        recommender = LBOModelAIRecommender()
        
        recommendations = recommender.recommend_parameters(
            company_info.get('business_description', ''),
            current_revenue=company_info.get('current_revenue'),
            current_ebitda=company_info.get('current_ebitda'),
            industry=company_info.get('industry')
        )
        
        print("✓ AI recommendations received:")
        print(f"  - Entry EBITDA: ${recommendations.get('entry_ebitda', 0):,.0f}")
        print(f"  - Entry Multiple: {recommendations.get('entry_multiple', 0):.1f}x")
        print(f"  - Revenue Growth (Year 1): {recommendations.get('revenue_growth_rate', [0])[0]*100:.1f}%")
        print(f"  - Debt Instruments: {len(recommendations.get('debt_instruments', []))}")
        
        return recommendations
        
    except Exception as e:
        print(f"⚠️  Error getting AI recommendations: {e}")
        return None


def main():
    """Main interactive test function."""
    print_header("LBO Model Generator - Interactive Test")
    print("\nThis tool allows you to test the LBO model generator with minimal input.")
    print("You can provide as much or as little information as you have.")
    print("AI will fill in the missing details based on what you provide.")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  WARNING: OPENAI_API_KEY not set")
        print("   AI features will not be available.")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        use_ai = False
    else:
        print(f"\n✓ OpenAI API key found (format: {api_key[:7]}...{api_key[-4:]})")
        use_ai = True
    
    # Collect user information
    print_section("📝 Company Information")
    print("Provide as much information as you have. Press Enter to skip and let AI generate it.")
    print()
    
    company_info = {}
    
    # Basic company info
    company_info['company_name'] = get_user_input("Company Name", required=False)
    company_info['industry'] = get_user_input("Industry Sector", required=False)
    
    print("\nBusiness Description:")
    print("  (Enter a description of the business, or press Enter to skip)")
    business_desc = input("  Description: ").strip()
    if business_desc:
        company_info['business_description'] = business_desc
    
    # Financial metrics (optional)
    print("\nFinancial Metrics (optional):")
    print("  Note: Enter numbers without $ or commas (e.g., 35000000 for $35M)")
    revenue_input = get_user_input("Current Annual Revenue ($)", input_type=float, required=False)
    if revenue_input:
        company_info['current_revenue'] = revenue_input
    
    ebitda_input = get_user_input("Current EBITDA ($)", input_type=float, required=False)
    if ebitda_input:
        company_info['current_ebitda'] = ebitda_input
    
    # Use AI to fill in missing information
    if use_ai:
        # Generate missing company info
        if not all([company_info.get('company_name'), 
                   company_info.get('industry'), 
                   company_info.get('business_description')]):
            company_info = generate_missing_info_with_ai(company_info)
        
        # Get LBO parameters from AI
        lbo_config = get_lbo_parameters_from_ai(company_info)
        
        if not lbo_config:
            print("\n⚠️  Could not get AI recommendations. Using defaults...")
            lbo_config = {}
    else:
        print("\n⚠️  AI not available. Using default values...")
        lbo_config = {}
    
    # Merge company info with LBO config
    final_config = {
        **company_info,
        **lbo_config
    }
    
    # Ensure required fields have defaults
    if 'entry_ebitda' not in final_config or not final_config['entry_ebitda']:
        final_config['entry_ebitda'] = final_config.get('current_ebitda', 10000) or 10000
    if 'entry_multiple' not in final_config or not final_config['entry_multiple']:
        final_config['entry_multiple'] = 6.5
    if 'revenue_growth_rate' not in final_config or not final_config['revenue_growth_rate']:
        final_config['revenue_growth_rate'] = [0.05] * 5
    if 'starting_revenue' not in final_config or not final_config['starting_revenue']:
        final_config['starting_revenue'] = final_config.get('current_revenue', 50000) or 50000
    if 'exit_year' not in final_config:
        final_config['exit_year'] = 5
    if 'exit_multiple' not in final_config or not final_config['exit_multiple']:
        final_config['exit_multiple'] = final_config.get('entry_multiple', 6.5) + 0.5
    
    # Remove non-LBO fields
    lbo_fields = [
        'entry_ebitda', 'entry_multiple', 'existing_debt', 'existing_cash',
        'transaction_expenses_pct', 'financing_fees_pct', 'revenue_growth_rate',
        'debt_instruments', 'cogs_pct_of_revenue', 'sganda_pct_of_revenue',
        'capex_pct_of_revenue', 'tax_rate', 'days_sales_outstanding',
        'days_inventory_outstanding', 'days_payable_outstanding', 'exit_year',
        'exit_multiple', 'starting_revenue'
    ]
    
    model_config = {k: v for k, v in final_config.items() if k in lbo_fields}
    
    # Show configuration summary
    print_section("📋 Model Configuration Summary")
    print(f"Company: {company_info.get('company_name', 'N/A')}")
    print(f"Industry: {company_info.get('industry', 'N/A')}")
    print(f"Entry EBITDA: ${model_config.get('entry_ebitda', 0):,.0f}")
    print(f"Entry Multiple: {model_config.get('entry_multiple', 0):.1f}x")
    print(f"Revenue Growth: {model_config.get('revenue_growth_rate', [0])[0]*100:.1f}% (Year 1)")
    print(f"Debt Instruments: {len(model_config.get('debt_instruments', []))}")
    
    # Confirm before generating
    print()
    proceed = get_user_input("Generate LBO model with this configuration? (y/n)", input_type=bool, default=True)
    
    if not proceed:
        print("\n❌ Model generation cancelled.")
        return
    
    # Generate model
    print_section("🔄 Generating LBO Model")
    try:
        model = create_lbo_from_inputs(model_config)
        
        # Calculate returns
        returns = model.calculate_returns()
        
        print("✓ Model generated successfully!")
        print()
        print("Key Results:")
        print(f"  Exit Year: {returns['exit_year']}")
        print(f"  Exit EBITDA: ${returns['exit_ebitda']:,.0f}")
        print(f"  Exit Enterprise Value: ${returns['exit_ev']:,.0f}")
        print(f"  Exit Equity Value: ${returns['exit_equity_value']:,.0f}")
        print(f"  Equity Invested: ${returns['equity_invested']:,.0f}")
        print(f"  MOIC: {returns['moic']:.2f}x")
        print(f"  IRR: {returns['irr']:.2f}%")
        
        # Export to Excel
        print()
        export = get_user_input("Export to Excel? (y/n)", input_type=bool, default=True)
        
        if export:
            output_file = get_user_input("Output filename", default="output/interactive_test.xlsx")
            
            # Ensure output directory exists
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            company_name = company_info.get('company_name', 'LBO Model')
            model.export_to_excel(str(output_path), company_name=company_name)
            
            print(f"\n✓ Excel file created: {output_file}")
        
        # Optional AI validation
        if use_ai:
            print()
            validate = get_user_input("Run AI validation on the model? (y/n)", input_type=bool, default=False)
            
            if validate:
                print_section("🔍 Running AI Validation")
                try:
                    validator = LBOModelAIValidator()
                    validation_result = model.validate_with_ai(
                        industry=company_info.get('industry'),
                        api_key=api_key
                    )
                    
                    if validation_result.get('is_valid'):
                        print("✓ AI validation passed")
                    else:
                        print("⚠️  AI validation found issues:")
                        for error in validation_result.get('errors', []):
                            print(f"  ❌ {error}")
                        for warning in validation_result.get('warnings', []):
                            print(f"  ⚠️  {warning}")
                    
                    if validation_result.get('suggestions'):
                        print("\n💡 Suggestions:")
                        for suggestion in validation_result.get('suggestions', [])[:5]:
                            print(f"  • {suggestion}")
                            
                except Exception as e:
                    print(f"⚠️  Validation error: {e}")
        
        print_section("✅ Test Complete")
        print("Model generated and tested successfully!")
        
    except Exception as e:
        print(f"\n❌ Error generating model: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

