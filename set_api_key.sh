#!/bin/bash
# Script to set OpenAI API key as environment variable
# Usage: source set_api_key.sh
#
# IMPORTANT: Do not commit actual API keys to the repository.
# Replace 'your-api-key-here' with your actual API key when using this script.

export OPENAI_API_KEY='your-api-key-here'

echo "✓ OPENAI_API_KEY environment variable set"
echo "  Note: This is only set for the current shell session"
echo "  To make it permanent, add to your ~/.zshrc or ~/.bashrc file"
echo ""
echo "⚠️  Remember to replace 'your-api-key-here' with your actual API key!"
