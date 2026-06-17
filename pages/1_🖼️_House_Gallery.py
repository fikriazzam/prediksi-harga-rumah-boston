import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# 1. KONFIGURASI HALAMAN STANDARD
st.set_page_config(page_title="House Gallery - Boston", layout="wide", initial_sidebar_state="expanded")

# Fungsi pembantu untuk load gambar lokal ke base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

bg_base64 = get_base64_image("bg_header.png")
logo_base64 = get_base64_image("logo_sidebar.png")

# 2. INJEKSI CSS CUSTOM - BERSIH & KONSISTEN
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', sans-serif !important;
        background-color: #f1f5f9;
    }}

    /* Menghilangkan padding atas agar header mentok ke langit-langit browser */
    [data-testid="stMainBlockContainer"] {{
        max-width: 100% !important;
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        padding-bottom: 2rem !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    div[data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* Kunci Tombol Panah Buka Sidebar Tetap Muncul */
    [data-testid="stSidebarCollapsedControl"] {{
        left: 20px !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-radius: 8px !important;
        padding: 4px !important;
        top: 15px !important;
        z-index: 999999 !important;
    }}
    [data-testid="stSidebarCollapsedControl"] button {{ color: white !important; }}

    /* HEADER BANNER CARD */
    .hero-card {{
        width: 100%;
        height: 260px;
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
        box-shadow: 0 10px 30px rgba(15,23,42,0.1);
    }}

    .main-content-wrapper {{
        padding-left: 3rem;
        padding-right: 3rem;
    }}

    /* SIDEBAR STYLING GRADIENT NAVY */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #071428 0%, #0a1e42 100%) !important;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{ color: #f8fafc !important; }}

    /* STYLING GRID GALERI RUMAH */
    .house-gallery-card {{
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(15,23,42,0.04);
        border: 1px solid #eef2ff;
        margin-bottom: 25px;
        transition: transform 0.2s ease;
    }}
    .house-gallery-card:hover {{
        transform: translateY(-3px);
    }}
    .badge-category {{
        display: inline-block;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 700;
        border-radius: 6px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    /* KPI METRIC CARDS */
    .kpi-card-premium {{
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(15,23,42,.06);
        border: 1px solid #eef2ff;
        display: flex;
        align-items: center;
    }}
    .kpi-circle-icon {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        margin-right: 15px;
    }}

    /* INFRASTRUKTUR FOOTER SIDEBAR */
    .sidebar-premium-footer {{ width: 100%; margin-top: 20px; padding: 5px; }}
    .sidebar-image-fade-final {{
        width: 100%; height: auto; display: block; border-radius: 12px;
        -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 20%, rgba(0,0,0,1) 100%);
        mask-image: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 20%, rgba(0,0,0,1) 100%);
    }}
    .sidebar-text-style {{ color: #94a3b8 !important; font-size: 12px !important; margin-top: 15px !important; }}
</style>
""", unsafe_allow_html=True)

# 3. DATASET DUMMY DENGAN HARGA YANG DISESUAIKAN BERDASARKAN KRITERIA KLASIFIKASI (MEDV REALISTIC VALUE)
@st.cache_data
def get_gallery_data():
    return [
        {"title": "Luxury Colonial House", "tag": "PREMIUM AREA", "bg": "#e0e7ff", "color": "#4f46e5", "rooms": 7.8, "crime": 0.006, "river": "Near Charles River (CHAS: Ya)", "price": "$50,000", "score": 98, "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=500&auto=format&fit=crop&q=60"},
        {"title": "Modern Riverfront House", "tag": "NEAR RIVER", "bg": "#e0f2fe", "color": "#0369a1", "rooms": 6.9, "crime": 0.015, "river": "Near Charles River (CHAS: Ya)", "price": "$46,800", "score": 94, "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=500&auto=format&fit=crop&q=60"},
        {"title": "Executive Family Home", "tag": "ELITE AREA", "bg": "#d1fae5", "color": "#065f46", "rooms": 7.2, "crime": 0.012, "river": "Standard Area (CHAS: Tidak)", "price": "$44,500", "score": 95, "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=500&auto=format&fit=crop&q=60"},
        {"title": "Grand Victorian House", "tag": "PREMIUM AREA", "bg": "#e0e7ff", "color": "#4f46e5", "rooms": 7.0, "crime": 0.021, "river": "Standard Area (CHAS: Tidak)", "price": "$41,200", "score": 92, "img": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500&auto=format&fit=crop&q=60"},
        {"title": "Contemporary River House", "tag": "NEAR RIVER", "bg": "#e0f2fe", "color": "#0369a1", "rooms": 6.5, "crime": 0.032, "river": "Near Charles River (CHAS: Ya)", "price": "$39,500", "score": 91, "img": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=500&auto=format&fit=crop&q=60"},
        {"title": "Suburban Classic House", "tag": "LOW CRIME", "bg": "#fef3c7", "color": "#92400e", "rooms": 5.8, "crime": 0.009, "river": "Standard Area (CHAS: Tidak)", "price": "$28,500", "score": 88, "img": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=500&auto=format&fit=crop&q=60"},
    ]

houses = get_gallery_data()

# 4. HERO SECTION MENTOK ATAS DENGAN IKON BARU GALERI (🖼️)
st.markdown(f"""
<div class="hero-card">
    <div style="position:absolute; top:45px; right:4rem; background:rgba(255,255,255,.08); backdrop-filter:blur(12px); padding:12px 20px; border-radius:16px; color:white; font-size:13px; font-weight:600; border:1px solid rgba(255,255,255,0.15);">
        🖼️ House Gallery Boston
    </div>
    <div style="padding:75px 4rem 0 4rem; color:white;">
        <h1 style="font-size:46px; font-weight:800; margin-bottom:5px; color:white; letter-spacing:-1px;">🖼️ Galeri Contoh Rumah Boston</h1>
        <p style="font-size:20px; opacity:.9; margin-bottom:10px; color:#cbd5e1;">Explore Premium Residential Properties</p>
        <p style="max-width:750px; opacity:.75; font-size:14px; color:#e2e8f0; line-height:1.5; margin:0;">
            Berikut adalah beberapa contoh arsitektur rumah dan wilayah pinggiran kota Boston berdasarkan kriteria dataset.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# BUNGKUSAN KONTEN UTAMA
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

# 5. KPI METRIC CARDS
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #e0e7ff; color: #4f46e5;">🏠</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Total Property</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">506 <span style="font-size:13px; color:#64748b; font-weight:normal;">Rumah</span></h3></div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #d1fae5; color: #065f46;">⭐</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Premium Area</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">124 <span style="font-size:13px; color:#64748b; font-weight:normal;">Properti</span></h3></div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #e0f2fe; color: #0284c7;">🌊</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Near Charles River</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">35 <span style="font-size:13px; color:#64748b; font-weight:normal;">Properti</span></h3></div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="kpi-card-premium"><div class="kpi-circle-icon" style="background: #fef3c7; color: #d97706;">💰</div><div><p style="margin:0; font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">Avg Price</p><h3 style="margin:0; color:#1e293b; font-size:22px; font-weight:700;">$22.5K <span style="font-size:13px; color:#64748b; font-weight:normal;">USD</span></h3></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. GRID CARDS GALERI UTAMA (3 KOLOM SEJAJAR LANGSUNG TANPA ROW FILTER RADIIO)
col_h1, col_h2, col_h3 = st.columns(3, gap="large")

for idx, h in enumerate(houses):
    target_col = col_h1 if idx % 3 == 0 else (col_h2 if idx % 3 == 1 else col_h3)
    with target_col:
        st.markdown(f"""
        <div class="house-gallery-card">
            <img src="{h['img']}" style="width:100%; height:200px; object-fit:cover;">
            <div style="padding: 20px;">
                <span class="badge-category" style="background:{h['bg']}; color:{h['color']};">{h['tag']}</span>
                <h4 style="margin:5px 0 10px 0; font-size:18px; font-weight:700; color:#0f172a;">{h['title']}</h4>
                <p style="margin:0 0 6px 0; font-size:13px; color:#64748b;">🛋️ Rata-rata Kamar (RM): <b>{h['rooms']}</b></p>
                <p style="margin:0 0 6px 0; font-size:13px; color:#64748b;">🚨 Tingkat Kriminalitas (CRIM): <b>{h['crime']}%</b></p>
                <p style="margin:0 0 15px 0; font-size:13px; color:#64748b;">🌊 {h['river']}</p>
                <hr style="border:0; border-top:1px solid #f1f5f9; margin:10px 0;">
                <div style="display:flex; justify-content:between; align-items:center;">
                    <span style="font-size:20px; font-weight:800; color:#10b981;">{h['price']}</span>
                    <span style="margin-left:auto; background:#f0fdf4; color:#16a34a; font-size:12px; padding:4px 10px; border-radius:20px; font-weight:700;">AI Score {h['score']}/100</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 7. SEKTOR BAWAH: MARKET INSIGHT & GRAFIK DISTRIBUSI HARGA
st.markdown("""
<div style="background: white; padding: 15px 20px; border-radius: 16px 16px 0 0; border-top: 1px solid #eef2ff; border-left: 1px solid #eef2ff; border-right: 1px solid #eef2ff; margin-bottom: -15px;">
    <h4 style="margin:0; color:#0f172a; font-size:16px; font-weight:700;">📊 Analisis Pasar Real Estate Boston</h4>
</div>
""", unsafe_allow_html=True)

col_chart, col_insight = st.columns([6.5, 3.5], gap="medium")

with col_chart:
    chart_data = pd.DataFrame({
        'Harga (Ribu USD)': ['<10K', '10K-20K', '20K-30K', '30K-40K', '40K-50K', '>50K'],
        'Jumlah Rumah': [15, 85, 240, 110, 40, 16]
    })
    fig_bar = px.bar(chart_data, x='Harga (Ribu USD)', y='Jumlah Rumah', color='Jumlah Rumah', color_continuous_scale='Viridis')
    fig_bar.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter", size=13), title=None,
        margin=dict(l=10, r=10, t=10, b=10), height=320
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_insight:
    st.markdown("""
    <div style="background: white; padding: 22px; border-radius: 20px; border: 1px solid #eef2ff; height: 320px; box-shadow: 0 10px 30px rgba(15,23,42,.02);">
        <h5 style="margin-top:0; color:#0f172a; font-size:14px; font-weight:700;">💡 AI Market Insights</h5>
        <ul style="margin-top:12px; padding-left:18px; color:#475569; font-size:13px; line-height:1.8;">
            <li>Wilayah dekat <b>Sungai Charles (CHAS)</b> memiliki nilai valuasi rata-rata rumah <b>24% lebih tinggi</b> dibandingkan area lainnya.</li>
            <li>Rumah dengan spesifikasi <b>RM > 6 Kamar</b> mendominasi sebaran nilai prediksi tertinggi di klaster harga.</li>
            <li>Tingkat kriminalitas rendah berkorelasi positif sangat kuat terhadap tingginya harga jual properti.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # TUTUP CONTAINER UTAMA

# 8. SIDEBAR FOOTER
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
with st.sidebar.container():
    st.markdown(f"""
    <div class="sidebar-premium-footer">
        <img src="data:image/png;base64,{logo_base64}" class="sidebar-image-fade-final">
        <div class="sidebar-text-style">
            <b style="color: #cbd5e1; font-size:12.5px;">Tentang Aplikasi:</b><br>
            Aplikasi ini dibangun untuk memprediksi harga rumah di wilayah Boston menggunakan model regresi linear.<br><br>
            <span style="font-size: 11px; opacity: 0.5;">Dibuat dengan ❤️ oleh Fikri</span>
        </div>
    </div>
    """, unsafe_allow_html=True)