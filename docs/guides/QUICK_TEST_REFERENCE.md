# Quick Test Reference Card

## 🚀 Quick Start

```bash
cd lbo_model_generator
python3 interactive_test.py
```

## 📋 What Information to Provide

### Minimum Required: **NONE!**
You can press Enter for everything and AI will generate a complete company.

### Recommended Information (Optional)

| Field | Example | What AI Does If Omitted |
|-------|---------|------------------------|
| **Company Name** | "TechWave Solutions" | Generates realistic name |
| **Industry** | "SaaS Software" | Infers from description |
| **Business Description** | "Cloud PM software for SMEs" | Creates detailed description |
| **Current Revenue** | `35000000` | Estimates based on company |
| **Current EBITDA** | `7000000` | Estimates from revenue & margins |

## 💡 Usage Patterns

### Pattern 1: Zero Input (AI Does Everything)
```
Company Name: [Enter]
Industry: [Enter]
Description: [Enter]
Revenue: [Enter]
EBITDA: [Enter]
```
**Result:** AI creates complete realistic company profile

### Pattern 2: Company Name Only
```
Company Name: Acme Corp
Industry: [Enter]
Description: [Enter]
Revenue: [Enter]
EBITDA: [Enter]
```
**Result:** AI generates industry, description, and financials

### Pattern 3: Industry + Description
```
Company Name: [Enter]
Industry: Manufacturing
Description: Industrial equipment manufacturer
Revenue: [Enter]
EBITDA: [Enter]
```
**Result:** AI generates company name and estimates financials

### Pattern 4: Financials Only
```
Company Name: [Enter]
Industry: [Enter]
Description: [Enter]
Revenue: 50000000
EBITDA: 10000000
```
**Result:** AI generates company profile matching the financials

### Pattern 5: Everything Provided
```
Company Name: TechWave Solutions
Industry: SaaS Software
Description: Cloud project management for SMEs
Revenue: 35000000
EBITDA: 7000000
```
**Result:** AI still optimizes LBO parameters (multiples, growth, debt)

## 🎯 What You Get

1. **Complete LBO Model** with all financial statements
2. **Returns Analysis** (IRR, MOIC)
3. **Excel Export** (optional) with professional formatting
4. **AI Validation** (optional) with recommendations

## ⚙️ Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key (optional but recommended)
export OPENAI_API_KEY='your-key-here'

# 3. Run interactive test
python3 interactive_test.py
```

## 📝 Input Format

- **Text fields:** Just type and press Enter
- **Numbers:** Enter without commas or $ signs
  - ✅ `35000000` (correct)
  - ❌ `$35,000,000` (wrong)
  - ❌ `35M` (wrong)
- **Skip fields:** Press Enter to let AI generate

## 🔍 Example Output

```
Key Results:
  Exit Year: 5
  Exit EBITDA: $22,423,000
  Exit Enterprise Value: $156,961,000
  Exit Equity Value: $204,929,000
  Equity Invested: $18,500,000
  MOIC: 11.08x
  IRR: 61.77%
```

## ❓ Common Questions

**Q: Do I need to provide all information?**  
A: No! Provide what you have. AI fills the rest.

**Q: What if I don't have an API key?**  
A: Tool still works but uses default values instead of AI-generated ones.

**Q: Can I change values after AI generates them?**  
A: Yes, review the configuration summary before generating the model.

**Q: How accurate are AI-generated values?**  
A: They're based on industry standards and best practices, but always review them.

## 🎓 Tips

1. **Start simple** - Try with minimal input first
2. **Provide industry** - Helps AI generate more accurate assumptions
3. **Review before generating** - Check the configuration summary
4. **Use validation** - Run AI validation for feedback
5. **Save configurations** - Note down values you like for future use

