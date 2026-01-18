#!/bin/bash

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✓ Git repository initialized"
fi

# Add all files
git add app.py
git add requirements.txt
git add README.md
git add WHITE_PAPER.md
git add PRESENTATION.html
git add PRESENTATION_INSTRUCTIONS.md
git add .gitignore

# Optional files (if you created them)
if [ -f "config.py" ]; then
    git add config.py
fi

if [ -f "utils.py" ]; then
    git add utils.py
fi

if [ -f "test_calculator.py" ]; then
    git add test_calculator.py
fi

if [ -f "Dockerfile" ]; then
    git add Dockerfile
fi

if [ -f "render.yaml" ]; then
    git add render.yaml
fi

if [ -f "railway.json" ]; then
    git add railway.json
fi

if [ -f "DEPLOYMENT.md" ]; then
    git add DEPLOYMENT.md
fi

# Commit with comprehensive message
git commit -m "Production Release v1.0.0: AI Model Eco & Ethics Calculator

🎯 Core Features:
- Complete environmental impact calculator for AI models
- Training & inference CO2 emissions estimation
- Water usage calculation for data center cooling
- Financial cost projections
- Ethical risk scoring (1-10 scale)
- Real-world comparisons (car km, flights, water bottles)
- Interactive visualizations with charts
- Multiple data center locations (8 regions)
- Multiple hardware types (A100, H100, V100, TPU v4/v5)
- Export to JSON and CSV formats

🏗️ Architecture:
- Modular, production-ready code structure
- Separated concerns (Config, Calculator, UI, Reporting)
- Type hints and data classes for maintainability
- Comprehensive error handling
- Session state management
- Easily extensible for future features

📊 Technical Stack:
- Python 3