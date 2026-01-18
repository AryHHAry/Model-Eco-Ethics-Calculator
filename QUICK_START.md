# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Download Files
Save these essential files to a folder:
- `app.py` (main application)
- `requirements.txt` (dependencies)
- `README.md` (documentation)

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
streamlit run app.py
```

### Step 4: Open Browser
Navigate to: http://localhost:8501

**That's it! You're ready to calculate AI environmental impact.**

---

## 📊 First Calculation Example

### Small Language Model (7B params)
1. Set **Model Parameters**: 7 billion
2. Set **Training Hours**: 1000
3. Set **Tokens per Day**: 10,000,000
4. Click **"🔍 Calculate Impact"**

**Expected Results:**
- CO₂: ~5,000 kg
- Water: ~16,000 L
- Cost: ~$18,000
- Ethical Risk: 4/10

### Large Language Model (175B params)
1. Set **Model Parameters**: 175 billion
2. Set **Training Hours**: 50,000
3. Set **Tokens per Day**: 100,000,000
4. Select **Hardware**: NVIDIA H100
5. Click **"🔍 Calculate Impact"**

**Expected Results:**
- CO₂: ~590,000 kg
- Water: ~1,770,000 L
- Cost: ~$4,200,000
- Ethical Risk: 8/10

---

## 🌍 Deploy to Cloud (3 options)

### Option A: Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Connect repository
4. Deploy! ✨

**Time: 5 minutes**

### Option B: Render.com
1. Push code to GitHub
2. Create Render account
3. New Web Service → Connect repo
4. Deploy automatically

**Time: 10 minutes**

### Option C: Railway.app
1. Push code to GitHub
2. Create Railway account
3. New Project → Import repo
4. Deploy

**Time: 10 minutes**

---

## 🔧 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow calculations
**Solution:** This is normal - calculations are instant. If UI is slow, check internet connection for assets.

---

## 💾 Export Your Results

After calculation:
1. Scroll to "📥 Export Results"
2. Click **"Download JSON"** for complete data
3. Or click **"Download CSV"** for spreadsheet

---

## 📧 Need Help?

**Email:** aryhharyanto@proton.me

**Common Questions:**
- How accurate are estimates? → Educational approximations, ±30-50%
- Can I use for production? → Yes, but get professional audit for compliance
- Is my data stored? → No, everything runs locally in your browser
- Can I modify the code? → Yes, but keep attribution

---

## 🎯 Next Steps

1. ✅ Read `WHITE_PAPER.md` for methodology details
2. ✅ View `PRESENTATION.html` for quick overview
3. ✅ Check `README.md` for full documentation
4. ✅ Deploy to cloud for team access
5. ✅ Share with colleagues interested in AI sustainability

---

**Version:** 1.0.0  
**Author:** Ary HH (aryhharyanto@proton.me)  
**License:** Proprietary - Educational Use