# User Instructions - Interactive LBO Test

## 🎯 Purpose

The Interactive Test tool allows you to quickly test the LBO model generator with minimal effort. You provide what you know, and AI intelligently fills in the rest.

## 📋 Information You Need to Provide

### **Answer: Almost Nothing!**

The tool is designed to work with **zero input** - you can press Enter for everything and AI will generate a complete, realistic company profile.

### What You CAN Provide (All Optional)

#### 1. Company Basics
- **Company Name**: Any name you want to test
- **Industry**: e.g., "SaaS", "Manufacturing", "Healthcare"
- **Business Description**: Brief description of what the company does

#### 2. Financial Information (Optional)
- **Current Revenue**: Annual revenue in dollars (enter as number, no $ or commas)
- **Current EBITDA**: EBITDA in dollars (enter as number, no $ or commas)

## 🚀 How to Run

```bash
cd lbo_model_generator
python3 interactive_test.py
```

## 📝 Step-by-Step Guide

### Step 1: Start the Tool
```bash
python3 interactive_test.py
```

### Step 2: Provide Information (or Skip Everything)

The tool will ask you questions. For each question:

**Option A: Provide Information**
```
Company Name: TechWave Solutions
```

**Option B: Skip (Let AI Generate)**
```
Company Name: [just press Enter]
```

### Step 3: Review AI-Generated Values

After you provide (or skip) all fields, AI will:
1. Generate missing company information
2. Create LBO model parameters
3. Show you a summary

**Review the summary before proceeding!**

### Step 4: Generate Model

Confirm to generate the LBO model. The tool will:
- Create all financial statements
- Calculate returns (IRR, MOIC)
- Show key results

### Step 5: Export (Optional)

Choose to export to Excel for detailed analysis.

### Step 6: Validate (Optional)

Run AI validation to get feedback on your model assumptions.

## 💡 Example Sessions

### Example 1: Zero Input
```
Company Name: [Enter]
Industry: [Enter]
Description: [Enter]
Revenue: [Enter]
EBITDA: [Enter]
```
→ AI creates everything from scratch

### Example 2: Just Company Name
```
Company Name: Acme Manufacturing
Industry: [Enter]
Description: [Enter]
Revenue: [Enter]
EBITDA: [Enter]
```
→ AI generates industry-appropriate profile

### Example 3: Industry + Revenue
```
Company Name: [Enter]
Industry: SaaS Software
Description: [Enter]
Revenue: 50000000
EBITDA: [Enter]
```
→ AI generates company matching SaaS profile and estimates EBITDA

### Example 4: Everything Provided
```
Company Name: TechWave Solutions
Industry: SaaS Software
Description: Cloud project management for SMEs
Revenue: 35000000
EBITDA: 7000000
```
→ AI still optimizes LBO parameters

## ⚠️ Important Notes

### Number Format
- ✅ **Correct**: `35000000` (for $35M)
- ❌ **Wrong**: `$35,000,000`
- ❌ **Wrong**: `35M`
- ❌ **Wrong**: `35,000,000`

Enter numbers as plain digits without currency symbols or commas.

### Skipping Fields
- Press **Enter** to skip any field
- AI will generate realistic values
- You can skip ALL fields if you want

### API Key
- **With API Key**: AI generates intelligent values
- **Without API Key**: Uses default values (less optimal)
- Set with: `export OPENAI_API_KEY='your-key'`

## 📊 What You'll Get

1. **Complete LBO Model**
   - Income Statement
   - Balance Sheet
   - Cash Flow Statement
   - Debt Schedule
   - Returns Analysis

2. **Key Metrics**
   - MOIC (Multiple on Invested Capital)
   - IRR (Internal Rate of Return)
   - Exit Equity Value
   - Exit Enterprise Value

3. **Excel File** (optional)
   - Professional formatting
   - Multiple sheets
   - Interactive formulas
   - Cover page and executive summary

4. **AI Validation** (optional)
   - Feedback on assumptions
   - Warnings and suggestions
   - Industry benchmarking

## 🎓 Best Practices

1. **Start Simple**: Try with zero input first
2. **Provide Industry**: Helps AI generate better assumptions
3. **Review Before Generating**: Check the configuration summary
4. **Use Validation**: Get AI feedback on your model
5. **Save Good Configs**: Note values that work well

## ❓ Troubleshooting

**"Invalid input" error**
- Make sure numbers don't have $ or commas
- Use plain digits: `35000000` not `$35,000,000`

**"API key not set" warning**
- Tool still works but uses defaults
- Set API key for better results: `export OPENAI_API_KEY='key'`

**Model generation fails**
- Check that configuration summary looks reasonable
- Try with different values
- Ensure all required fields have values

## 📚 More Information

- **Full Guide**: See [INTERACTIVE_TEST_GUIDE.md](INTERACTIVE_TEST_GUIDE.md)
- **Quick Reference**: See [QUICK_TEST_REFERENCE.md](QUICK_TEST_REFERENCE.md)
- **Main README**: See [README.md](README.md)

