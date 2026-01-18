# setup_project.ps1 - Windows PowerShell setup script

Write-Host "🚀 AI Model Eco & Ethics Calculator - Project Setup" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

# Create project directory structure
Write-Host "📁 Creating project structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "ai-eco-calculator" | Out-Null
Set-Location "ai-eco-calculator"

# Create subdirectories
New-Item -ItemType Directory -Force -Path "tests" | Out-Null
New-Item -ItemType Directory -Force -Path "docs" | Out-Null
New-Item -ItemType Directory -Force -Path "exports" | Out-Null
New-Item -ItemType Directory -Force -Path ".streamlit" | Out-Null

Write-Host "✓ Project structure created" -ForegroundColor Green
Write-Host ""

# Create .streamlit/config.toml
Write-Host "⚙️ Creating Streamlit configuration..." -ForegroundColor Yellow
$configContent = @"
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
"@

$configContent | Out-File -FilePath ".streamlit\config.toml" -Encoding UTF8
Write-Host "✓ Streamlit config created" -ForegroundColor Green
Write-Host ""

# Initialize git
Write-Host "🔧 Initializing Git repository..." -ForegroundColor Yellow
git init
Write-Host "✓ Git initialized" -ForegroundColor Green
Write-Host ""

# Print next steps
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Copy all project files to this directory"
Write-Host "2. Install dependencies: pip install -r requirements.txt"
Write-Host "3. Run application: streamlit run app.py"
Write-Host "4. Create GitHub repository and push:"
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/ai-eco-calculator.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "🌍 Ready to calculate AI environmental impact!" -ForegroundColor Green