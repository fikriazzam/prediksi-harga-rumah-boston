import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import base64

# 1. KONFIGURASI HALAMAN STANDARD
st.set_page_config(page_title="Smart House Predictor", layout="wide", initial_sidebar_state="expanded")

# Fungsi pembantu untuk mengubah gambar lokal menjadi format Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    bg_base64 = get_base64_image("bg_header.png")
    logo_base64 = get_base64_image("logo_sidebar.png")
except Exception as e:
    bg_base64 = ""
    logo_base64 = ""

# 2. INJEKSI CSS CUSTOM - BANNER FULL WIDTH & SIDEBAR TETAP SEMPURNA
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', sans-serif !important;
        background-color: #f1f5f9;
    }}

    /* BANNER TETAP MENTOK FULL WIDTH */
    [data-testid="stMainBlockContainer"] {{
        max-width: 100% !important;
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        padding-bottom: 2rem !important;
    }}

    /* Membuat header asli streamlit transparan */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        background-color: transparent !important;
    }}

    /* Tombol pembuka sidebar tetap aman di posisinya */
    [data-testid="stSidebarCollapsedControl"] {{
        left: 20px !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-radius: 8px !important;
        padding: 4px !important;
        top: 15px !important;
        z-index: 999999 !important;
    }}
    
    [data-testid="stSidebarCollapsedControl"] button {{
        color: white !important;
    }}

    /* HERO CARD BANNER FULL WIDTH */
    .hero-card {{
        width: 100%;
        height: 320px;
        position: relative;
        margin-top: -3rem; 
        border-radius: 0 0 24px 24px;
        overflow: hidden;
        background-image: 
            linear-gradient(
                90deg,
                rgba(3,7,18,.95) 0%,
                rgba(15,23,42,.85) 40%,
                rgba(30,64,175,.50) 100%
            ),
            url('data:image/png;base64,{bg_base64}');
        background-size: cover;
        background-position: center;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.1);
    }}

    /* PADDING KONTEN UTAMA KEMBALI ASLI DAN SIMETRIS */
    .main-content-wrapper {{
        padding-left: 3rem;
        padding-right: 3rem;
    }}

    /* SIDEBAR STYLING GRADIENT NAVY */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #071428 0%, #0a1e42 100%) !important;
    }}
    
    [data-testid="stSidebar"] .st-emotion-cache-17l273g, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span {{
        color: #f8fafc !important;
    }}

    /* STYLING FOOTER SIDEBAR */
    .sidebar-premium-footer {{
        width: 100%;
        margin-top: 20px;
        padding: 5px;
    }}

    .sidebar-image-fade-final {{
        width: 100%;
        height: auto;
        display: block;
        border-radius: 12px;
        -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 20%, rgba(0,0,0,1) 100%);
        mask-image: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 20%, rgba(0,0,0,1) 100%);
    }}

    .sidebar-text-style {{
        color: #94a3b8 !important;
        font-size: 12px !important;
        line-height: 1.6 !important;
        text-align: left !important;
        margin-top: 15px !important;
    }}

    /* KPI CARD FLOATING */
    .kpi-card-premium {{
        background: white;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(15,23,42,.06);
        border: 1px solid #eef2ff;
        display: flex;
        align-items: center;
    }}

    .kpi-circle-icon {{
        width: 52px;
        height: 52px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 22px;
        margin-right: 15px;
    }}

    .custom-form-card {{
        background: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(15,23,42,.06);
        border: 1px solid #eef2ff;
    }}

    .prediction-card-premium {{
        background: linear-gradient(135deg, #071a4d, #042f2e);
        padding: 40px 25px;
        border-radius: 24px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(7,26,77,0.25);
    }}

    /* Tombol Hitung */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 14px 20px;
        font-weight: 600;
        font-size: 15px;
        width: 100%;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
        transition: all 0.2s ease;
        margin-top: 15px;
    }}
    div.stButton > button:first-child:hover {{
        background: linear-gradient(135deg, #4f46e5, #4338ca);
        transform: translateY(-1px);
    }}
</style>
""", unsafe_allow_html=True)

# 3. LOAD DATASET & AI MODEL
@st.cache_resource
def load_model():
    with open('model_regresi_boston.pkl', 'rb') as file:
        return pickle.load(file)

@st.cache_data
def load_data():
    return pd.read_csv('BostonHousing (1).csv')

model = load_model()
df = load_data()

# 4. HERO BANNER
st.markdown(f"""
<div class="hero-card">
    <div style="position:absolute; top:45px; right:4rem; background:rgba(255,255,255,.08); backdrop-filter:blur(12px); padding:12px 20px; border-radius:16px; color:white; font-size:13px; font-weight:600; border:1px solid rgba(255,255,255,0.15);">
        📈 Model: Linear Regression
    </div>
    <div style="padding:75px 4rem 0 4rem; color:white;">
        <h1 style="font-size:56px; font-weight:800; margin-bottom:10px; color:white; letter-spacing:-1px;">🏠 Smart House Price Predictor</h1>
        <p style="font-size:22px; opacity:.9; margin-bottom:15px; color:#cbd5e1;">AI-Powered Real Estate Valuation System (Boston Dataset)</p>
        <p style="max-width:750px; opacity:.75; font-size:14px; color:#e2e8f0; line-height:1.5; margin:0;">
            Prediksi harga rumah menggunakan machine learning berdasarkan karakteristik lingkungan dan properti.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# BUNGKUSAN KONTEN UTAMA
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

# 5. KPI CARDS
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #e0e7ff; color: #4f46e5;">📥</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Total Dataset</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">506 <span style="font-size:13px; color:#64748b; font-weight:normal;">Rumah</span></h3></div></div>', unsafe_allow_html=True)
with col_kpi2:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #d1fae5; color: #059669;">💚</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Avg Price</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">$22.5K <span style="font-size:13px; color:#64748b; font-weight:normal;">USD</span></h3></div></div>', unsafe_allow_html=True)
with col_kpi3:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #e0f2fe; color: #0284c7;">📊</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Total Fitur</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">13 <span style="font-size:13px; color:#64748b; font-weight:normal;">Indikator</span></h3></div></div>', unsafe_allow_html=True)
with col_kpi4:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #fef3c7; color: #d97706;">⚡</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Model AI</p><h3 style="margin:0; color:#1e293b; font-size:15px; font-weight:700; margin-top:2px;">Linear Regression</h3></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. LAYOUT UTAMA RASIO (6.5 : 3.5)
col_main_left, col_main_right = st.columns([6.5, 3.5], gap="large")

# === SEKTOR KIRI: FORM SPECIFICATION ===
with col_main_left:
    st.markdown('<div class="custom-form-card"><h3 style="margin:0 0 20px 0; color:#0f172a; font-size:18px; font-weight:700;">🔷 Spesifikasi Properti Anda</h3></div>', unsafe_allow_html=True)
    
    # TRIK PAS DAN BARU: Kita pecah kolom form kiri menjadi sub-kolom kecil [bemper_kosong, wadah_slider_asli]
    # Rasio 0.6 untuk membuat bemper jarak kosong dari sidebar, dan 9.4 untuk wadah slidernya
    sub_col_space, sub_col_form = st.columns([0.6, 9.4])
    
    with sub_col_space:
        st.write("") # Sengaja dikosongkan sebagai benteng pembatas dari sidebar
        
    with sub_col_form:
        # Sekarang seluruh slider ditaruh di sini, dijamin otomatis bergeser ke kanan mengikuti grid Python!
        kamar = st.slider("🛋️ Rata-rata Jumlah Kamar (RM)", min_value=3.5, max_value=8.8, value=6.2, step=0.1)
        ekonomi_rendah = st.slider("📉 % Penduduk Ekonomi Rendah (LSTAT)", min_value=1.1, max_value=37.0, value=12.6, step=0.1)
        kriminalitas = st.slider("🚨 Tingkat Kriminalitas (CRIM)", min_value=0.01, max_value=88.0, value=3.6, step=0.1)
        sungai_charles = st.selectbox("🌊 Dekat Sungai Charles? (CHAS)", options=["Tidak", "Ya"])
        
        sungai_charles_val = 1 if sungai_charles == "Ya" else 0
        btn_hitung = st.button("🔮 Hitung Estimasi Harga Properti")

# === SEKTOR KANAN: CARD PREDIKSI ===
with col_main_right:
    harga_final_usd = None
    if btn_hitung:
        zn, indus, nox, age, dis, rad, tax, ptratio, b = 11.36, 11.14, 0.55, 68.57, 3.80, 9.55, 408.24, 18.46, 356.67
        input_data = np.array([[kriminalitas, zn, indus, sungai_charles_val, nox, kamar, age, dis, rad, tax, ptratio, b, ekonomi_rendah]])
        prediksi = model.predict(input_data)
        harga_final_usd = float(prediksi.flatten()[0]) * 1000

    if harga_final_usd is not None:
        st.markdown(f'<div class="prediction-card-premium"><div style="width:90px; height:90px; border-radius:50%; background:rgba(255,255,255,.08); display:flex; justify-content:center; align-items:center; font-size:42px; margin:auto; margin-bottom:20px;">🏠</div><p style="margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.7; font-weight:600;">Estimasi Harga Rumah Anda</p><h1 style="margin: 15px 0; font-size: 46px; font-weight: 800; color: #10b981; letter-spacing: -0.5px;">${harga_final_usd:,.2f}</h1><p style="margin: 0; font-size: 15px; font-weight: 700; color: #cbd5e1;">USD</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="prediction-card-premium"><div style="width:90px; height:90px; border-radius:50%; background:rgba(255,255,255,.08); display:flex; justify-content:center; align-items:center; font-size:42px; margin:auto; margin-bottom:20px;">🏠</div><p style="margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.7; font-weight:600;">Estimasi Harga Rumah Anda</p><h2 style="margin:15px 0; font-size:42px; color:#10b981; font-weight:800;">$0.00</h2><p style="margin:0; font-size:13px; color:#94a3b8;">Silakan klik tombol di sebelah kiri untuk merilis analisis.</p></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 7. SEKTOR GRAFIK
st.markdown('<div style="background: white; padding: 20px; border-radius: 20px 20px 0 0; border-top: 1px solid #eef2ff; border-left: 1px solid #eef2ff; border-right: 1px solid #eef2ff; margin-bottom: -15px;"><h4 style="margin:0; color:#0f172a; font-size:16px; font-weight:700;">📊 Analisis Tren: Hubungan Jumlah Kamar vs Harga</h4></div>', unsafe_allow_html=True)
col_chart, col_insight = st.columns([6.5, 3.5], gap="medium")
with col_chart:
    fig = px.scatter(df, x="rm", y="medv", color="lstat", labels={"rm": "Rata-rata Jumlah Kamar (RM)", "medv": "Harga Rumah (MEDV)", "lstat": "% Ekonomi Rendah"}, color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font=dict(family="Inter", size=13), title=None, margin=dict(l=10, r=10, t=10, b=10), height=350)
    st.plotly_chart(fig, use_container_width=True)
with col_insight:
    st.markdown('<div style="background: white; padding: 22px; border-radius: 20px; border: 1px solid #eef2ff; height: 350px; box-shadow: 0 10px 30px rgba(15,23,42,.04);"><h5 style="margin-top:0; color:#0f172a; font-size:14px; font-weight:700; display:flex; align-items:center;"><span style="margin-right:8px;">💡</span> Insight Analisis</h5><ul style="margin-top:12px; padding-left:18px; color:#475569; font-size:13px; line-height:1.7;"><li>Semakin banyak <b>jumlah kamar (RM)</b>, kecenderungan harga rumah akan meningkat secara linear.</li><li>Warna titik grafik merepresentasikan persentase <b>penduduk ekonomi rendah (LSTAT)</b> di wilayah tersebut.</li><li>Rumah dengan LSTAT rendah (berwarna ungu tua) umumnya mendominasi klaster harga yang jauh lebih tinggi.</li></ul></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # TUTUP BUNGKUSAN KONTEN UTAMA

# 8. SIDEBAR FOOTER
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

with st.sidebar.container():
    st.markdown(f"""
    <div class="sidebar-premium-footer">
        <img src="data:image/png;base64,{logo_base64}" class="sidebar-image-fade-final">
        <div class="sidebar-text-style">
            <b style="color: #cbd5e1; font-size:13px;">Tentang Aplikasi:</b><br>
            Aplikasi ini dibangun untuk memprediksi harga rumah di wilayah Boston menggunakan model regresi linear.<br><br>
        </div>
    </div>
    """, unsafe_allow_html=True)