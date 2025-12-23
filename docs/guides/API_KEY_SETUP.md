# API Key Setup Guide

This guide explains how to set up your OpenAI API key for the LBO Model Generator AI features.

## Quick Setup

### Option 1: Environment Variable (Current Session)

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Option 2: Using the Setup Script

```bash
source set_api_key.sh
```

### Option 3: Permanent Setup (Recommended)

Add to your shell configuration file:

**For zsh (macOS default):**
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Option 4: .env File (Future Support)

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

Note: The `.env` file is already in `.gitignore` for security.

## Verify Setup

Test that your API key is working:

```bash
python3 -c "
import os
import sys
sys.path.insert(0, 'src')
from lbo_validation import validate_api_key
api_key = validate_api_key()
print('✓ API key validated successfully')
"
```

## Security Notes

- ✅ API keys are never logged (even partially)
- ✅ API keys are not stored in code
- ✅ `.env` files are gitignored
- ✅ API key validation checks format before use

## Current Status

Your API key is currently set in the environment and working correctly!

Test it with:
```bash
python3 tests/test_ai_with_key.py
```

