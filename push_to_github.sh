#!/bin/bash
# Script to push LBO Model Generator to GitHub

set -e

echo "🚀 Pushing LBO Model Generator to GitHub..."
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "⚠️  No changes to commit"
else
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: LBO Model Generator v1.0.0

- Complete LBO financial modeling tool
- AI-powered recommendations and validation
- Industry-standard Excel export
- Comprehensive test suite
- Full documentation
- Apache 2.0 License"
fi

# Set branch to main
echo "🌿 Setting branch to main..."
git branch -M main

# Add remote (if not already added)
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/SafetyMP/LBO-Model-Generator.git
else
    echo "🔗 Remote already configured"
    git remote set-url origin https://github.com/SafetyMP/LBO-Model-Generator.git
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
echo ""
echo "⚠️  You may need to authenticate with GitHub"
echo ""

git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🔗 Repository: https://github.com/SafetyMP/LBO-Model-Generator"

