#!/usr/bin/env bash
set -e

# Deploy script for technommy.github.io
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Preparing Technommy GitHub Pages deployment..."

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
  git init -b main
  git config user.name "Technommy Lab"
  git config user.email "research@gworky.com"
fi

git add -A
git commit -m "feat: launch Technommy authoritative compute economics research portal" || echo "No changes to commit"

# Check if remote exists
if ! git remote | grep -q origin; then
  echo "Adding remote origin..."
  git remote add origin https://github.com/technommy/technommy.github.io.git
fi

echo "Pushing to technommy.github.io on GitHub..."
git push -u origin main --force

echo "✅ Deployed! GitHub Pages will be live at https://technommy.github.io/"
