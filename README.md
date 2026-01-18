# AI Model Eco & Ethics Calculator

Tool sederhana untuk mengestimasi dampak lingkungan (carbon footprint, water usage) dan risiko etika dari training & inference model AI skala besar.

## Features

- ✅ Estimasi CO₂ equivalent dari training & inference
- ✅ Estimasi kebutuhan air untuk cooling data center
- ✅ Ethical risk score berdasarkan ukuran model
- ✅ Perbandingan intuitif (mobil, penerbangan, kolam renang)
- ✅ Support untuk model Dense dan MoE
- ✅ Kustomisasi lokasi data center & hardware

## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## Deploy

### Streamlit Cloud (Gratis)

1. Push code ke GitHub repository
2. Buka <https://streamlit.io/cloud>
3. Connect repository dan deploy

### Alternatif: Hugging Face Spaces

1. Buat Space baru di <https://huggingface.co/spaces>
2. Upload `app.py` dan `requirements.txt`
3. Pilih SDK: Streamlit

## Author

**Ary HH** - <aryhharyanto@proton.me>

Untuk edukasi dampak lingkungan & etika AI

---

⚠️ **Disclaimer:** Estimasi kasar untuk edukasi, bukan pengganti audit professional.
