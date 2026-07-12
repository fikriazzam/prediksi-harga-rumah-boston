import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import base64
import sys
import numpy

# 1. KONFIGURASI HALAMAN (Wide Mode)
st.set_page_config(page_title="Smart House Predictor", layout="wide", initial_sidebar_state="expanded")

# Fungsi pembantu untuk mengubah gambar lokal menjadi format Base64 agar bisa dibaca CSS murni Streamlit
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load gambar lokal ke base64
try:
    bg_base64 = get_base64_image("bg_header.png")
    logo_base64 = get_base64_image("logo_sidebar.png")
except Exception as e:
    bg_base64 = ""
    logo_base64 = ""

# 2. INJEKSI CSS CUSTOM UTAMAKAN KEMIRIPAN 100% DENGAN MOCKUP
st.markdown(f"""
<style>
    /* Mengubah background utama aplikasi */
    .stApp {{
        background-color: #f3f4f6;
    }}

    /* Mengubah warna latar belakang Sidebar menjadi Navy Gelap */
    [data-testid="stSidebar"] {{
        background-color: #0b1329 !important;
    }}
    
    /* Mengubah warna teks menu di sidebar agar putih/terang */
    [data-testid="stSidebar"] .st-emotion-cache-17l273g, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span {{
        color: #f8fafc !important;
    }}

    /* PERBAIKAN: Memaksa warna teks label Slider dan Selectbox menjadi Gelap Kontras */
    .stSlider label, .stSelectbox label, 
    [data-testid="stWidgetLabel"] p,
    .st-emotion-cache-zt5igj p,
    .st-emotion-cache-zt5igj span {{
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }}

    /* Desain Tombol Hitung Sesuai Contoh Ungu Gradasi */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 14px 20px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        transition: all 0.2s ease;
    }}
    
    div.stButton > button:first-child:hover {{
        background: linear-gradient(135deg, #4f46e5, #4338ca);
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.4);
    }}

    /* Merapikan padding container */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# 3. LOAD DATASET & AI MODEL
@st.cache_resource
def load_model():
    # 1. Buat jembatan manipulasi objek sebelum pickle membaca model
    import sys
    import types
    import numpy as np

    # Membuat modul bayangan 'numpy._core' dan 'numpy._core.numeric'
    core = types.ModuleType('numpy._core')
    sys.modules['numpy._core'] = core
    sys.modules['numpy._core.numeric'] = core
    
    # Memetakan fungsi yang dicari oleh model lama ke fungsi Numpy 1.x yang setara
    core.numeric = np
    core.dtype = np.dtype

    # 2. Baru lakukan load model dengan aman
    with open('model_regresi_boston.pkl', 'rb') as file:                
        return pickle.load(file)

@st.cache_data
def load_data():
    return pd.read_csv('BostonHousing (1).csv')

model = load_model()
df = load_data()

# 4. HERO SECTION DENGAN GAMBAR BACKGROUND LOKAL BERGAYA PREMIUM
st.markdown(f"""
<div style="
    position: relative;
    padding: 55px 30px;
    border-radius: 20px;
    background-image: linear-gradient(rgba(11, 19, 41, 0.82), rgba(29, 78, 216, 0.82)), url('data:image/png;base64,{bg_base64}');
    background-size: cover;
    background-position: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
">
    <div style="position: absolute; top: 20px; right: 30px; background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; color: #34d399;">
        📈 Model: Linear Regression
    </div>
    <h1 style='margin: 0; font-size: 34px; font-weight: 800; letter-spacing: -0.5px;'>🏠 Smart House Price Predictor</h1>
    <p style='margin: 5px 0 0 0; opacity: 0.9; font-size: 16px;'>AI-Powered Real Estate Valuation System (Boston Dataset)</p>
    <p style='margin: 15px 0 0 0; opacity: 0.7; font-size: 14px; font-style: italic;'>Prediksi harga rumah berdasarkan karakteristik lingkungan dan properti Anda</p>
</div>
""", unsafe_allow_html=True)

# 5. KARTU INDIKATOR (KPI CARDS - 4 KOTAK BERJEJER PERSIS MOCKUP)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
    <div style="background: white; padding: 18px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); display: flex; align-items: center; border: 1px solid #e5e7eb;">
        <div style="background: #e0e7ff; padding: 12px; border-radius: 50%; margin-right: 15px; font-size: 22px;">📊</div>
        <div>
            <p style="margin:0; font-size:12px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Total Dataset</p>
            <h3 style="margin:2px 0 0 0; color:#1e293b; font-size:24px; font-weight:700;">506 <span style="font-size:14px; color:#64748b; font-weight:normal;">Rumah</span></h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div style="background: white; padding: 18px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); display: flex; align-items: center; border: 1px solid #e5e7eb;">
        <div style="background: #d1fae5; padding: 12px; border-radius: 50%; margin-right: 15px; font-size: 22px;">💵</div>
        <div>
            <p style="margin:0; font-size:12px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Rata-rata Harga</p>
            <h3 style="margin:2px 0 0 0; color:#1e293b; font-size:24px; font-weight:700;">$22.5K <span style="font-size:14px; color:#64748b; font-weight:normal;">USD</span></h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div style="background: white; padding: 18px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); display: flex; align-items: center; border: 1px solid #e5e7eb;">
        <div style="background: #e0f2fe; padding: 12px; border-radius: 50%; margin-right: 15px; font-size: 22px;">🔢</div>
        <div>
            <p style="margin:0; font-size:12px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Total Fitur</p>
            <h3 style="margin:2px 0 0 0; color:#1e293b; font-size:24px; font-weight:700;">13 <span style="font-size:14px; color:#64748b; font-weight:normal;">Indikator</span></h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div style="background: white; padding: 18px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); display: flex; align-items: center; border: 1px solid #e5e7eb;">
        <div style="background: #fef3c7; padding: 12px; border-radius: 50%; margin-right: 15px; font-size: 22px;">🤖</div>
        <div>
            <p style="margin:0; font-size:12px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Model AI</p>
            <h3 style="margin:2px 0 0 0; color:#1e293b; font-size:18px; font-weight:700; line-height:1.2; margin-top:5px;">Linear Reg</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. TATA LETAK KOLOM UTAMA (Membagi Halaman Menjadi Kiri [Form] dan Kanan [Hasil])
col_main_left, col_main_right = st.columns([5.5, 4.5], gap="large")

# === SEKTOR KIRI: FORM SPECIFICATION CARD ===
with col_main_left:
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #e5e7eb; margin-bottom: 15px;">
        <h3 style="margin:0; color:#1e3a8a; font-size:20px; font-weight:700; display:flex; align-items:center;">
            <span style="margin-right:10px;">🧬</span> Spesifikasi Properti Anda
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Input sliders dimasukkan ke dalam container kolom kiri secara presisi
    kamar = st.slider("🛋️ Rata-rata Jumlah Kamar (RM)", min_value=3.5, max_value=8.8, value=6.2, step=0.1)
    ekonomi_rendah = st.slider("📉 % Penduduk Ekonomi Rendah (LSTAT)", min_value=1.1, max_value=37.0, value=12.6, step=0.1)
    kriminalitas = st.slider("🚨 Tingkat Kriminalitas (CRIM)", min_value=0.01, max_value=88.0, value=3.6, step=0.1)
    sungai_charles = st.selectbox("🌊 Dekat Sungai Charles? (CHAS)", options=["Tidak", "Ya"])
    
    sungai_charles_val = 1 if sungai_charles == "Ya" else 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    btn_hitung = st.button("📋 Hitung Estimasi Harga Properti")

# === SEKTOR KANAN: HIGHLIGHT PREDIKSI CARD ===
with col_main_right:
    harga_final_usd = None
    
    if btn_hitung:
        zn, indus, nox, age, dis, rad, tax, ptratio, b = 11.36, 11.14, 0.55, 68.57, 3.80, 9.55, 408.24, 18.46, 356.67
        input_data = np.array([[
            kriminalitas, zn, indus, sungai_charles_val, nox, 
            kamar, age, dis, rad, tax, ptratio, b, ekonomi_rendah
        ]])
        prediksi = model.predict(input_data)
        harga_final_usd = float(prediksi.flatten()[0]) * 1000

    if harga_final_usd is not None:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0f172a, #111827);
            padding: 40px 25px;
            border-radius: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            border: 1px solid #1f2937;
            position: relative;
            overflow: hidden;
        ">
            <p style='margin: 0; font-size: 15px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; font-weight:600;'>Estimasi Harga Rumah Anda</p>
            <h1 style='margin: 15px 0; font-size: 50px; font-weight: 800; color: #10b981; letter-spacing: -1px;'>${harga_final_usd:,.2f}</h1>
            <p style='margin: 0; font-size: 16px; font-weight: 700; color: #f3f4f6;'>USD</p>
            <div style="margin-top: 20px; background: rgba(255,255,255,0.05); padding: 10px 15px; border-radius: 10px; font-size: 13px; color: #9ca3af; border: 1px solid rgba(255,255,255,0.05);">
                ✨ Berdasarkan data dan model AI, estimasi harga rumah Anda adalah sebagai berikut.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0f172a, #111827);
            padding: 52px 25px;
            border-radius: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            border: 1px solid #1f2937;
        ">
            <div style="font-size: 35px; margin-bottom: 5px;">🏠</div>
            <h2 style="margin:0; font-size:36px; color:#cbd5e1; font-weight:800;">$0.00</h2>
            <p style="margin:10px 0 0 0; font-size:14px; color:#9ca3af;">Silakan klik tombol "Hitung Estimasi Harga Properti" di sebelah kiri untuk merilis hasil analisis.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 7. SEKTOR GRAFIK & ANALISIS TREN DATA INSIGHT
st.markdown("""
<div style="background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #e5e7eb; margin-bottom: 15px;">
    <h4 style="margin:0; color:#1e293b; font-size:18px; font-weight:700;">📊 Analisis Tren: Hubungan Jumlah Kamar vs Harga</h4>
</div>
""", unsafe_allow_html=True)

col_chart, col_insight = st.columns([6.5, 3.5], gap="medium")

with col_chart:
    fig = px.scatter(
        df, 
        x="rm", 
        y="medv", 
        color="lstat",
        labels={"rm": "Rata-rata Jumlah Kamar (RM)", "medv": "Harga Rumah (MEDV)", "lstat": "% Ekonomi Rendah"},
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    # KONFIGURASI YANG AMAN DAN BEBAS ERROR
    fig.update_layout(
        # Ditambah tingginya menjadi 380 agar teks tidak berhimpitan/tabrakan
        margin=dict(l=40, r=10, t=10, b=50), 
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color='#1e293b',  # Memaksa warna teks menjadi gelap kontras
            size=11
        )
    )
    
    # Menggunakan theme=None agar warna font gelap kita aktif
    st.plotly_chart(fig, width="stretch", theme=None)

with col_insight:
    st.markdown("""
    <div style="background: #f8fafc; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; height: 320px;">
        <h5 style="margin-top:0; color:#0f172a; font-size:15px; font-weight:700; display:flex; align-items:center;">
            <span style="margin-right:8px;">💡</span> Insight Analisis
        </h5>
        <ul style="margin-top:10px; padding-left:20px; color:#475569; font-size:13.5px; line-height:1.7;">
            <li>Semakin banyak <b>jumlah kamar (RM)</b>, kecenderungan harga rumah akan meningkat secara linear.</li>
            <li>Warna titik grafik merepresentasikan persentase <b>penduduk ekonomi rendah (LSTAT)</b> di wilayah tersebut.</li>
            <li>Rumah dengan LSTAT rendah (berwarna ungu tua) umumnya mendominasi klaster harga yang jauh lebih tinggi.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 8. SIDEBAR DEKORASI BAWAH (MENAMPILKAN LOGO DAN TEKS STRUKTUR)
st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_sidebar.png", width="stretch")
st.sidebar.markdown(f"""
<div style="color: #64748b; font-size: 13px; padding: 10px 5px; line-height: 1.6;">
    <b>Tentang Aplikasi:</b><br>
    Aplikasi ini dibangun untuk memprediksi harga rumah di wilayah Boston menggunakan model regresi linear.<br><br>
    <span style="font-size: 11px; opacity: 0.7;">Dibuat dengan ❤️ menggunakan Streamlit</span>
</div>
""", unsafe_allow_html=True)
