# commit_windows.bat - Windows version of commit script

@echo off
echo Starting commit process...

REM Initialize git if needed
if not exist ".git" (
    git init
    echo Git repository initialized
)

REM Add all files
git add app.py
git add requirements.txt
git add README.md
git add WHITE_PAPER.md
git add PRESENTATION.html
git add PRESENTATION_INSTRUCTIONS.md
git add .gitignore

REM Optional files
if exist "config.py" git add config.py
if exist "utils.py" git add utils.py
if exist "test_calculator.py" git add test_calculator.py
if exist "Dockerfile" git add Dockerfile
if exist "render.yaml" git add render.yaml
if exist "railway.json" git add railway.json
if exist "DEPLOYMENT.md" git add DEPLOYMENT.md

REM Commit
git commit -m "Production Release v1.0.0: AI Model Eco & Ethics Calculator - Complete environmental impact calculator for large AI models with training/inference CO2 estimation, water usage, financial costs, ethical risk scoring, and interactive visualizations. Created by Ary HH (aryhharyanto@proton.me)"

echo Committed successfully!
echo.
echo Next steps:
echo 1. Create GitHub repository
echo 2. git remote add origin https://github.com/YOUR_USERNAME/ai-eco-calculator.git
echo 3. git branch -M main
echo 4. git push -u origin main

pause