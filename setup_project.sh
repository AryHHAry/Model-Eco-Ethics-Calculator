# setup_project.sh - Complete project setup script

#!/bin/bash

echo "🚀 AI Model Eco & Ethics Calculator - Project Setup"
echo "=================================================="
echo ""

# Create project directory structure
echo "📁 Creating project structure..."
mkdir -p ai-eco-calculator
cd ai-eco-calculator

# Create subdirectories
mkdir -p tests
mkdir -p docs
mkdir -p exports
mkdir -p .streamlit

echo "✓ Project structure created"
echo ""

# Create .streamlit/config.toml
echo "⚙️ Creating Streamlit configuration..."
cat > .streamlit/config.toml << 'EOF'
[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
EOF

echo "✓ Streamlit config created"
echo ""

# Initialize git
echo "🔧 Initializing Git repository..."
git init
echo "✓ Git initialized"
echo ""

# Create first commit
echo "💾 Creating initial commit..."
git add .
git commit -m "Initial commit: Project structure setup"
echo "✓ Initial commit created"
echo ""

# Print next steps
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Copy all project files to this directory"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Run application: streamlit run app.py"
echo "4. Create GitHub repository and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-eco-calculator.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "🌍 Ready to calculate AI environmental impact!"