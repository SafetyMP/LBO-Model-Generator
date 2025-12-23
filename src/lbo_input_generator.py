"""
Interactive LBO Model Input Generator

Provides a command-line interface and JSON configuration for generating LBO models.
Includes AI-powered recommendations based on business descriptions.
"""

import json
import sys
import os
import logging
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

# Handle both package and direct imports
try:
    from .lbo_model_generator import create_lbo_from_inputs, LBOModel, LBOAssumptions, LBODebtStructure
    from .lbo_exceptions import LBOError, LBOAIServiceError, LBOValidationError, LBOConfigurationError
    from .lbo_validation import validate_json_input, validate_output_path, sanitize_filename
except ImportError:
    from lbo_model_generator import create_lbo_from_inputs, LBOModel, LBOAssumptions, LBODebtStructure
    from lbo_exceptions import LBOError, LBOAIServiceError, LBOValidationError, LBOConfigurationError
    from lbo_validation import validate_json_input, validate_output_path, sanitize_filename

# Configure logging
logger = logging.getLogger(__name__)

try:
    try:
        from .lbo_ai_recommender import LBOModelAIRecommender, recommend_lbo_parameters
    except ImportError:
        from lbo_ai_recommender import LBOModelAIRecommender, recommend_lbo_parameters
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: AI recommendations not available. Install openai package: pip install openai")


def create_input_template() -> Dict:
    """Create a template input configuration."""
    return {
        "company_name": "Example Company",
        "entry_ebitda": 10000,
        "entry_multiple": 6.5,
        "existing_debt": 0,
        "existing_cash": 500,
        "transaction_expenses_pct": 0.03,
        "financing_fees_pct": 0.02,
        "revenue_growth_rate": [0.05, 0.05, 0.05, 0.05, 0.05],
        "debt_instruments": [
            {
                "name": "Senior Debt",
                "interest_rate": 0.08,
                "ebitda_multiple": 1.0,
                "amortization_schedule": "amortizing",
                "amortization_periods": 5
            },
            {
                "name": "Subordinated Debt",
                "interest_rate": 0.12,
                "ebitda_multiple": 2.0,
                "amortization_schedule": "bullet"
            }
        ],
        "cogs_pct_of_revenue": 0.70,
        "sganda_pct_of_revenue": 0.15,
        "depreciation_pct_of_ppe": 0.10,
        "capex_pct_of_revenue": 0.03,
        "tax_rate": 0.25,
        "days_sales_outstanding": 45.0,
        "days_inventory_outstanding": 30.0,
        "days_payable_outstanding": 30.0,
        "initial_ppe": 0,
        "initial_ar": 0,
        "initial_inventory": 0,
        "initial_ap": 0,
        "min_cash_balance": 0,
        "exit_year": 5,
        "exit_multiple": 7.5,
        "starting_revenue": 50000
    }


def _collect_ai_recommendations(config: Dict) -> None:
    """Collect AI-powered recommendations and merge into config."""
    print("AI-POWERED RECOMMENDATIONS")
    print("-" * 80)
    use_ai_recs = input("Would you like AI-powered recommendations? (y/n): ").lower() == 'y'
    
    if not use_ai_recs:
        return
    
    print("\nPlease describe your business:")
    business_description = input("Business description: ")
    
    current_revenue = None
    revenue_input = input("Current annual revenue ($, optional): ")
    if revenue_input:
        try:
            current_revenue = float(revenue_input)
        except (ValueError, TypeError):
            pass
    
    current_ebitda = None
    ebitda_input = input("Current EBITDA ($, optional): ")
    if ebitda_input:
        try:
            current_ebitda = float(ebitda_input)
        except (ValueError, TypeError):
            pass
    
    industry = input("Industry sector (optional): ") or None
    
    print("\n🔄 Analyzing business and generating recommendations...")
    try:
        recommender = LBOModelAIRecommender()
        ai_recommendations = recommender.recommend_parameters(
            business_description,
            current_revenue=current_revenue,
            current_ebitda=current_ebitda,
            industry=industry
        )
        
        print("\n" + recommender.explain_recommendations(ai_recommendations))
        
        use_recs = input("\nUse these AI recommendations as defaults? (y/n): ").lower() == 'y'
        if use_recs:
            config.update({k: v for k, v in ai_recommendations.items() if k != '_ai_metadata'})
            print("✓ AI recommendations loaded. You can modify any values below.\n")
            print("=" * 80)
            print()
    except Exception as e:
        print(f"⚠️  Error getting AI recommendations: {e}")
        print("Continuing with manual input...\n")


def _collect_transaction_details(config: Dict) -> None:
    """Collect transaction details."""
    print("TRANSACTION DETAILS:")
    print("-" * 80)
    default_ebitda = config.get('entry_ebitda') or "10000"
    config['entry_ebitda'] = float(input(f"Entry EBITDA ($) [{default_ebitda}]: ") or default_ebitda)
    
    default_multiple = config.get('entry_multiple') or "6.5"
    config['entry_multiple'] = float(input(f"Entry Multiple (x EBITDA) [{default_multiple}]: ") or default_multiple)
    
    default_debt = config.get('existing_debt') or "0"
    config['existing_debt'] = float(input(f"Existing Debt ($) [{default_debt}]: ") or default_debt)
    
    default_cash = config.get('existing_cash') or "500"
    config['existing_cash'] = float(input(f"Existing Cash ($) [{default_cash}]: ") or default_cash)
    print()


def _collect_revenue_assumptions(config: Dict) -> None:
    """Collect revenue assumptions."""
    print("REVENUE ASSUMPTIONS:")
    print("-" * 80)
    num_years = int(input("Number of projection years (default 5): ") or "5")
    
    default_growth = config.get('revenue_growth_rate')
    if default_growth:
        growth_str = ", ".join([f"{g*100:.1f}%" for g in default_growth[:num_years]])
        growth_input = input(f"Revenue growth rate per year (% - comma-separated) [{growth_str}]: ") or growth_str.replace("%", "").replace(" ", "")
    else:
        growth_input = input(f"Revenue growth rate per year (% - same for all years or comma-separated): ") or "5"
    
    if ',' in growth_input:
        growth_rates = [float(x.strip()) / 100 for x in growth_input.split(',')]
    else:
        growth_rates = [float(growth_input) / 100] * num_years
    config['revenue_growth_rate'] = growth_rates[:num_years]
    
    default_starting_rev = config.get('starting_revenue') or "0"
    config['starting_revenue'] = float(input(f"Starting Revenue ($, 0 to estimate) [{default_starting_rev}]: ") or default_starting_rev)
    print()


def _collect_debt_structure(config: Dict) -> None:
    """Collect debt structure information."""
    print("DEBT STRUCTURE:")
    print("-" * 80)
    
    ai_debt = config.get('debt_instruments', [])
    if ai_debt:
        print(f"AI recommended {len(ai_debt)} debt instrument(s).")
        use_ai_debt = input("Use AI debt recommendations? (y/n): ").lower() == 'y'
        if use_ai_debt:
            config['debt_instruments'] = ai_debt
            print("✓ Using AI debt recommendations.")
            return
        else:
            num_debt_instruments = int(input("Number of debt instruments: ") or "0")
            debt_instruments = []
    else:
        num_debt_instruments = int(input("Number of debt instruments: ") or "2")
        debt_instruments = []
    
    for i in range(num_debt_instruments):
        print(f"\nDebt Instrument {i+1}:")
        name = input("  Name: ") or f"Debt {i+1}"
        interest_rate = float(input("  Interest Rate (%): ") or "8") / 100
        ebitda_multiple = float(input("  EBITDA Multiple (x, 0 if using fixed amount): ") or "0")
        
        print("  Amortization Schedule:")
        print("    1. Bullet (no payments until maturity)")
        print("    2. Amortizing (equal payments)")
        print("    3. Cash Flow Sweep")
        schedule_choice = input("  Choice (1-3, default 1): ") or "1"
        schedule_map = {"1": "bullet", "2": "amortizing", "3": "cash_flow_sweep"}
        schedule = schedule_map.get(schedule_choice, "bullet")
        
        amort_periods = 5
        if schedule == "amortizing":
            amort_periods = int(input("  Amortization Periods (years): ") or "5")
        
        debt_instruments.append({
            "name": name,
            "interest_rate": interest_rate,
            "ebitda_multiple": ebitda_multiple if ebitda_multiple > 0 else None,
            "amount": float(input("  Fixed Amount ($, if not using EBITDA multiple): ") or "0") if ebitda_multiple == 0 else 0,
            "amortization_schedule": schedule,
            "amortization_periods": amort_periods
        })
    
    config['debt_instruments'] = debt_instruments
    default_equity = config.get('equity_amount') or "0"
    config['equity_amount'] = float(input(f"\nEquity Amount ($, 0 to calculate) [{default_equity}]: ") or default_equity)
    print()


def _collect_operating_assumptions(config: Dict) -> None:
    """Collect operating assumptions."""
    print("OPERATING ASSUMPTIONS:")
    print("-" * 80)
    default_cogs = (config.get('cogs_pct_of_revenue') or 0.70) * 100
    config['cogs_pct_of_revenue'] = float(input(f"COGS as % of Revenue [{default_cogs:.1f}%]: ") or default_cogs) / 100
    
    default_sganda = (config.get('sganda_pct_of_revenue') or 0.15) * 100
    config['sganda_pct_of_revenue'] = float(input(f"SG&A as % of Revenue [{default_sganda:.1f}%]: ") or default_sganda) / 100
    
    default_capex = (config.get('capex_pct_of_revenue') or 0.03) * 100
    config['capex_pct_of_revenue'] = float(input(f"CapEx as % of Revenue [{default_capex:.1f}%]: ") or default_capex) / 100
    
    default_tax = (config.get('tax_rate') or 0.25) * 100
    config['tax_rate'] = float(input(f"Tax Rate (%) [{default_tax:.1f}%]: ") or default_tax) / 100
    print()


def _collect_working_capital(config: Dict) -> None:
    """Collect working capital assumptions."""
    print("WORKING CAPITAL ASSUMPTIONS:")
    print("-" * 80)
    default_dso = config.get('days_sales_outstanding') or 45
    config['days_sales_outstanding'] = float(input(f"Days Sales Outstanding [{default_dso:.0f}]: ") or default_dso)
    
    default_dio = config.get('days_inventory_outstanding') or 30
    config['days_inventory_outstanding'] = float(input(f"Days Inventory Outstanding [{default_dio:.0f}]: ") or default_dio)
    
    default_dpo = config.get('days_payable_outstanding') or 30
    config['days_payable_outstanding'] = float(input(f"Days Payable Outstanding [{default_dpo:.0f}]: ") or default_dpo)
    print()


def _collect_exit_assumptions(config: Dict) -> None:
    """Collect exit assumptions."""
    print("EXIT ASSUMPTIONS:")
    print("-" * 80)
    default_exit_year = config.get('exit_year') or 5
    config['exit_year'] = int(input(f"Exit Year [{default_exit_year}]: ") or default_exit_year)
    
    default_exit_mult = config.get('exit_multiple') or 7.5
    config['exit_multiple'] = float(input(f"Exit Multiple (x EBITDA) [{default_exit_mult}]: ") or default_exit_mult)
    print()


def _collect_optional_assumptions(config: Dict) -> None:
    """Collect optional assumptions."""
    print("OPTIONAL ASSUMPTIONS (press Enter for defaults):")
    print("-" * 80)
    config['transaction_expenses_pct'] = float(input("Transaction Expenses as % of EV (default 3%): ") or "3") / 100
    config['financing_fees_pct'] = float(input("Financing Fees as % of Total Debt (default 2%): ") or "2") / 100
    config['depreciation_pct_of_ppe'] = float(input("Depreciation as % of PP&E (default 10%): ") or "10") / 100
    config['min_cash_balance'] = float(input("Minimum Cash Balance ($, default 0): ") or "0")


def interactive_input(use_ai: bool = False) -> Dict:
    """Interactive command-line input collection."""
    print("=" * 80)
    print("LBO Model Generator - Interactive Input")
    print("=" * 80)
    print()
    
    config = {}
    
    if use_ai and AI_AVAILABLE:
        _collect_ai_recommendations(config)
    
    _collect_transaction_details(config)
    _collect_revenue_assumptions(config)
    _collect_debt_structure(config)
    _collect_operating_assumptions(config)
    _collect_working_capital(config)
    _collect_exit_assumptions(config)
    _collect_optional_assumptions(config)
    
    return config


def load_config_from_json(filename: str) -> Dict:
    """Load configuration from JSON file."""
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        
        # Validate the loaded configuration
        return validate_json_input(config)
    except FileNotFoundError:
        raise LBOConfigurationError(f"Configuration file not found: {filename}")
    except json.JSONDecodeError as e:
        raise LBOConfigurationError(f"Invalid JSON in configuration file: {e}")
    except LBOValidationError:
        raise  # Re-raise validation errors
    except Exception as e:
        raise LBOConfigurationError(f"Error loading configuration: {e}") from e


def save_config_to_json(config: Dict, filename: str) -> None:
    """Save configuration to JSON file."""
    try:
        # Sanitize filename
        safe_filename = sanitize_filename(filename)
        
        # Validate output path
        output_path = validate_output_path(safe_filename)
        
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
    except (LBOConfigurationError, LBOValidationError):
        raise  # Re-raise our custom errors
    except Exception as e:
        raise LBOConfigurationError(f"Error saving configuration: {e}") from e


def _parse_arguments() -> 'argparse.Namespace':
    """Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    import argparse as _argparse
    parser = _argparse.ArgumentParser(description='Generate LBO Model')
    parser.add_argument('--input', '-i', type=str, help='Input JSON file')
    parser.add_argument('--output', '-o', type=str, default='lbo_model.xlsx', help='Output Excel file')
    parser.add_argument('--template', '-t', action='store_true', help='Generate template JSON file')
    parser.add_argument('--interactive', action='store_true', help='Use interactive input')
    parser.add_argument('--ai', action='store_true', help='Enable AI-powered recommendations')
    parser.add_argument('--ai-description', type=str, help='Business description for AI recommendations')
    parser.add_argument('--ai-revenue', type=float, help='Current revenue for AI recommendations')
    parser.add_argument('--ai-ebitda', type=float, help='Current EBITDA for AI recommendations')
    parser.add_argument('--ai-industry', '--industry', type=str, help='Industry for AI recommendations and validation')
    parser.add_argument('--ai-validate', action='store_true', help='Run AI validation on model assumptions')
    parser.add_argument('--ai-review', action='store_true', help='Run AI review on generated Excel model')
    parser.add_argument('--ai-scenarios', action='store_true', help='Generate AI-powered scenario analysis')
    parser.add_argument('--ai-benchmark', action='store_true', help='Benchmark model against market using AI')
    parser.add_argument('--ai-diagnose', action='store_true', help='Use AI to diagnose errors')
    parser.add_argument('--api-key', type=str, help='OpenAI API key (or set OPENAI_API_KEY env var)')
    return parser.parse_args()

def _handle_template_generation() -> None:
    """Handle template generation and exit."""
    template = create_input_template()
    template_file = 'lbo_input_template.json'
    save_config_to_json(template, template_file)
    print(f"Template saved to {template_file}")

def _load_config_from_args(args) -> Optional[Dict]:
    """Load configuration based on command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Configuration dictionary or None if error
    """
    if args.input:
        return load_config_from_json(args.input)
    elif args.interactive:
        config = interactive_input(use_ai=args.ai or False)
        save = input("\nSave configuration to file? (y/n): ")
        if save.lower() == 'y':
            filename = input("Filename (default: lbo_config.json): ") or "lbo_config.json"
            save_config_to_json(config, filename)
            print(f"Configuration saved to {filename}")
        return config
    elif args.ai_description and AI_AVAILABLE:
        print("Generating LBO model from AI recommendations...")
        try:
            config = recommend_lbo_parameters(
                args.ai_description,
                current_revenue=args.ai_revenue,
                current_ebitda=args.ai_ebitda,
                industry=args.ai_industry
            )
            recommender = LBOModelAIRecommender()
            print(recommender.explain_recommendations(config))
            
            ai_config_file = 'lbo_ai_recommendations.json'
            save_config_to_json(config, ai_config_file)
            print(f"\nAI recommendations saved to {ai_config_file}")
            return config
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    return None

def _run_ai_validation(model: 'LBOModel', args) -> None:
    """Run AI validation on model.
    
    Args:
        model: LBO model instance
        args: Command line arguments
    """
    print("\n🔍 Running AI validation...")
    validation_result = model.validate_with_ai(
        industry=getattr(args, 'industry', None),
        api_key=getattr(args, 'api_key', None)
    )
    if not validation_result.get("is_valid", True):
        print("⚠️  Validation Warnings/Errors:")
        for error in validation_result.get("errors", []):
            print(f"  ❌ {error}")
        for warning in validation_result.get("warnings", []):
            print(f"  ⚠️  {warning}")
    else:
        print("✓ AI validation passed")
        if validation_result.get("suggestions"):
            print("💡 Suggestions:")
            for suggestion in validation_result.get("suggestions", [])[:5]:
                print(f"  • {suggestion}")

def _run_ai_review(model: 'LBOModel', output_file: str, args) -> None:
    """Run AI review on generated Excel model.
    
    Args:
        model: LBO model instance
        output_file: Path to output Excel file
        args: Command line arguments
    """
    print("\n🔍 Running AI output review...")
    review_result = model.review_output_with_ai(
        output_file,
        api_key=getattr(args, 'api_key', None)
    )
    if not review_result.get("is_valid", True):
        print("⚠️  Review Findings:")
        for error in review_result.get("errors", []):
            print(f"  ❌ {error}")
        for warning in review_result.get("warnings", []):
            print(f"  ⚠️  {warning}")

def _run_ai_scenarios(model: 'LBOModel', args) -> None:
    """Run AI scenario generation.
    
    Args:
        model: LBO model instance
        args: Command line arguments
    """
    print("\n📊 Generating AI scenarios...")
    scenarios = model.generate_scenarios_with_ai(
        industry=getattr(args, 'industry', None),
        api_key=getattr(args, 'api_key', None)
    )
    print("Scenarios generated:")
    print(f"  Base Case IRR: {scenarios.get('base_case', {}).get('expected_irr', 'N/A'):.1f}%")
    print(f"  High Case IRR: {scenarios.get('high_case', {}).get('expected_irr', 'N/A'):.1f}%")
    print(f"  Low Case IRR: {scenarios.get('low_case', {}).get('expected_irr', 'N/A'):.1f}%")

def _run_ai_benchmark(model: 'LBOModel', args) -> None:
    """Run AI market benchmarking.
    
    Args:
        model: LBO model instance
        args: Command line arguments
    """
    if not (hasattr(args, 'industry') and args.industry):
        return
    
    print("\n📈 Running AI market benchmarking...")
    benchmark = model.benchmark_against_market(
        args.industry,
        api_key=getattr(args, 'api_key', None)
    )
    if benchmark.get("industry_averages"):
        print("Market Benchmarks:")
        for key, value in benchmark.get("industry_averages", {}).items():
            print(f"  {key}: {value}")

def _print_returns_summary(model: 'LBOModel') -> None:
    """Print returns analysis summary.
    
    Args:
        model: LBO model instance
    """
    returns = model.calculate_returns()
    print("\n" + "=" * 80)
    print("RETURNS ANALYSIS")
    print("=" * 80)
    print(f"Exit Year:              {returns['exit_year']}")
    print(f"Exit EBITDA:            ${returns['exit_ebitda']:,.0f}")
    print(f"Exit Enterprise Value:  ${returns['exit_ev']:,.0f}")
    print(f"Exit Equity Value:      ${returns['exit_equity_value']:,.0f}")
    print(f"Equity Invested:        ${returns['equity_invested']:,.0f}")
    print(f"MOIC:                   {returns['moic']:.2f}x")
    irr_pct = returns['irr'] * 100 if returns['irr'] < 1 else returns['irr']
    print(f"IRR:                    {irr_pct:.2f}%")
    print("=" * 80)

def _handle_error_with_ai_diagnosis(error: Exception, model: Optional['LBOModel'], args) -> None:
    """Handle error with optional AI diagnosis.
    
    Args:
        error: Exception that occurred
        model: LBO model instance (may be None if error occurred before model creation)
        args: Command line arguments
    """
    if not args.ai_diagnose:
        return
    
    try:
        import traceback
        traceback_str = traceback.format_exc()
        print("\n🔍 Running AI error diagnosis...")
        
        if model:
            diagnosis = model.diagnose_error_ai(
                str(error),
                traceback_str,
                api_key=getattr(args, 'api_key', None)
            )
        else:
            # If model doesn't exist, create a minimal one for diagnosis
            try:
                temp_model = create_lbo_from_inputs({})
                diagnosis = temp_model.diagnose_error_ai(
                    str(error),
                    traceback_str,
                    api_key=getattr(args, 'api_key', None)
                )
            except (ValueError, KeyError, LBOConfigurationError, LBOAIServiceError, Exception) as e:
                logger.debug(f"AI diagnosis failed: {e}", exc_info=True)
                print("  ⚠️  AI diagnosis unavailable: Model not created")
                return
        
        print("Diagnosis:")
        print(f"  Root Cause: {diagnosis.get('root_cause', 'N/A')}")
        print("  Fix Suggestions:")
        for fix in diagnosis.get('fix_suggestions', []):
            print(f"    • {fix}")
    except LBOAIServiceError as ai_error:
        logger.warning(f"AI diagnosis failed: {ai_error}", exc_info=True)
        print(f"  ⚠️  AI diagnosis unavailable: {ai_error}")
    except Exception as ai_error:
        logger.warning(f"Unexpected error during AI diagnosis: {ai_error}", exc_info=True)
        print(f"  ⚠️  AI diagnosis error: {ai_error}")

def main() -> None:
    """Main entry point."""
    args = _parse_arguments()
    
    if args.template:
        _handle_template_generation()
        return
    
    # Get inputs
    config = _load_config_from_args(args)
    if config is None:
        import argparse as _argparse
        parser = _argparse.ArgumentParser(description='Generate LBO Model')
        print("Error: Must provide --input, --interactive, --template, or --ai-description")
        parser.print_help()
        return
    
    # Generate model
    print("\nGenerating LBO model...")
    model = None
    try:
        model = create_lbo_from_inputs(config)
        
        # Optional AI validation
        if args.ai_validate:
            _run_ai_validation(model, args)
        
        # Validate output path
        try:
            output_path = validate_output_path(args.output)
        except LBOConfigurationError as e:
            logger.error(f"Invalid output path: {e}")
            print(f"\n✗ Invalid output path: {e}")
            sys.exit(1)
        
        model.export_to_excel(
            str(output_path),
            validate_with_ai=args.ai_validate,
            industry=getattr(args, 'industry', None),
            api_key=getattr(args, 'api_key', None)
        )
        print(f"\n✓ Model generated successfully: {args.output}")
        
        # Optional AI review
        if args.ai_review:
            _run_ai_review(model, args.output, args)
        
        # Optional AI scenario generation
        if args.ai_scenarios:
            _run_ai_scenarios(model, args)
        
        # Optional AI benchmarking
        if args.ai_benchmark:
            _run_ai_benchmark(model, args)
        
        # Print summary
        _print_returns_summary(model)
        
    except LBOError as e:
        logger.error(f"LBO model error: {e}", exc_info=True)
        print(f"\n✗ Error generating model: {e}")
        _handle_error_with_ai_diagnosis(e, model, args)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n✗ Unexpected error generating model: {e}")
        _handle_error_with_ai_diagnosis(e, model, args)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

