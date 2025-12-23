# Streamlit Configuration

## API Key Setup

To use AI features in the Streamlit app, you need to configure your OpenAI API key.

### Option 1: Streamlit Secrets (Recommended)

1. Copy the example file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml` and add your API key:
   ```toml
   [openai]
   api_key = "your-actual-api-key-here"
   ```

3. The file `.streamlit/secrets.toml` is already in `.gitignore` and will not be committed.

### Option 2: Environment Variable

Set the environment variable before running Streamlit:
```bash
export OPENAI_API_KEY="your-actual-api-key-here"
streamlit run app.py
```

Or on Windows:
```cmd
set OPENAI_API_KEY=your-actual-api-key-here
streamlit run app.py
```

### Security Notes

- **Never commit** your actual API key to version control
- The `.streamlit/secrets.toml` file is in `.gitignore`
- Use environment variables in production deployments
- Rotate your API key if it's ever exposed

