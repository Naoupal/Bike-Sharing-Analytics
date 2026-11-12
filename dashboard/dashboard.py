from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

BASE_DIR = Path(__file__).parent

# ---------- KONFIGURASI HALAMAN ----------
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon=str(BASE_DIR / "favicon.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CUSTOM CSS (MIDNIGHT PANELS) ----------
st.markdown("""
    <style>
    .stApp {
        background-color: #060913;
        color: #F1F5F9;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1120 0%, #050811 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.75) 0%, rgba(2, 6, 23, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 3px solid #38BDF8;
        padding: 20px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: rgba(56, 189, 248, 0.4);
        border-top: 3px solid #FB923C;
        transform: translateY(-4px);
        box-shadow: 0 12px 32px -4px rgba(56, 189, 248, 0.15);
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 10px;
        font-weight: 600;
        color: #64748B;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0EA5E9 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }

    /* Logo & wordmark */
    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-title {
        font-weight: 800;
        letter-spacing: -0.4px;
        color: #F8FAFC;
        line-height: 1.15;
    }
    .brand-sub {
        color: #64748B;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 600;
    }
    .dashboard-header {
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #F8FAFC;
    }
    </style>
""", unsafe_allow_html=True)

# Logo vektor (SVG): lambang sepeda pada kotak gradasi biru
LOGO_SVG = """
<svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-label="Bike Sharing Analytics">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0EA5E9"/>
      <stop offset="1" stop-color="#0369A1"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#g)"/>
  <g fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="19" cy="41" r="10"/>
    <circle cx="45" cy="41" r="10"/>
    <path d="M19 41 L29 24 L45 41"/>
    <path d="M29 24 L41 24"/>
    <path d="M25 20 L33 20"/>
    <path d="M29 24 L36 41"/>
  </g>
</svg>
"""


def tampilkan_brand(size, judul, subjudul, ukuran_judul):
    # HTML dibuat satu baris tanpa indentasi agar tidak dibaca Markdown sebagai code block
    logo = " ".join(LOGO_SVG.format(size=size).split())
    html = (
        '<div class="brand">'
        f"{logo}"
        "<div>"
        f'<div class="brand-title" style="font-size: {ukuran_judul};">{judul}</div>'
        f'<div class="brand-sub">{subjudul}</div>'
        "</div>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


# Palet warna
BIRU, ORANYE, HIJAU, ABU = "#38BDF8", "#FB923C", "#34D399", "#64748B"

# Konfigurasi Matplotlib
plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.edgecolor": "#1E293B",
    "axes.labelcolor": "#94A3B8",
    "xtick.color": "#94A3B8",
    "ytick.color": "#94A3B8",
    "text.color": "#F1F5F9",
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "figure.dpi": 140,
})

URUTAN_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
URUTAN_MUSIM = ["Spring", "Summer", "Fall", "Winter"]
URUTAN_CUACA = ["Cerah", "Berkabut/Berawan", "Hujan/Salju Ringan"]
URUTAN_BULAN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


@st.cache_data
def muat_data():
    path = BASE_DIR / "main_data.csv"
    df = pd.read_csv(path, parse_dates=["dteday"])
    return df


def ke_harian(df):
    harian = df.groupby("dteday").agg(
        cnt=("cnt", "sum"),
        casual=("casual", "sum"),
        registered=("registered", "sum"),
        temp_c=("temp_c", "mean"),
        year=("year", "first"),
        month_label=("month_label", "first"),
        season_label=("season_label", "first"),
        day_type=("day_type", "first"),
        weather_day=("weather_day", "first"),
    ).reset_index()
    return harian


def sumber(fig, teks):
    fig.text(0.01, -0.06, teks, fontsize=8, color="#475569")


# ---------- DATA & FILTER SIDEBAR ----------
data = muat_data()

with st.sidebar:
    tampilkan_brand(40, "Bike Sharing", "Analytics", "1.15rem")
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.markdown("### Panel Kontrol")
    st.markdown("<p style='font-size: 13px; color: #64748B;'>Sesuaikan parameter data untuk memperbarui visualisasi.</p>", unsafe_allow_html=True)

    tgl_min, tgl_maks = data["dteday"].min().date(), data["dteday"].max().date()
    rentang = st.date_input("Rentang Tanggal", (tgl_min, tgl_maks), min_value=tgl_min, max_value=tgl_maks)

    st.markdown("")
    musim = st.multiselect("Musim", URUTAN_MUSIM, default=URUTAN_MUSIM)

    st.markdown("")
    jenis_hari = st.multiselect("Kategori Hari", ["Hari Kerja", "Akhir Pekan/Libur"],
                                default=["Hari Kerja", "Akhir Pekan/Libur"])

    st.markdown("---")
    st.markdown("<div style='font-size: 11px; color: #475569;'><b>Sumber Data:</b> Capital Bikeshare, Washington D.C. (2011-2012)</div>", unsafe_allow_html=True)

if isinstance(rentang, tuple) and len(rentang) == 2:
    awal, akhir = rentang
else:
    awal, akhir = tgl_min, tgl_maks

hour_df = data[
    (data["dteday"].dt.date >= awal) & (data["dteday"].dt.date <= akhir)
    & (data["season_label"].isin(musim)) & (data["day_type"].isin(jenis_hari))
]

# ---------- HEADER UTAMA ----------
tampilkan_brand(52, "Bike Sharing Analytics Dashboard",
                "Capital Bikeshare &middot; Washington D.C. &middot; 2011-2012", "2rem")
st.markdown("<p style='color: #94A3B8; font-size: 1.05rem; margin: 16px 0 24px 0;'>Ringkasan performa penyewaan, pola perilaku pengguna, dan pengaruh faktor lingkungan.</p>", unsafe_allow_html=True)

if hour_df.empty:
    st.warning("Tidak ada data yang tersedia untuk kombinasi filter ini. Silakan perbarui filter pada sidebar.")
    st.stop()

day_df = ke_harian(hour_df)

# ---------- RINGKASAN (KPI CARDS) ----------
total = int(day_df["cnt"].sum())
rata_harian = day_df["cnt"].mean()
porsi_registered = day_df["registered"].sum() / day_df["cnt"].sum()
jam_puncak = hour_df.groupby("hr")["cnt"].mean().idxmax()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Penyewaan", f"{total:,}", help="Jumlah seluruh penyewaan pada filter yang dipilih.")
k2.metric("Rata-rata per Hari", f"{rata_harian:,.0f}", help="Rata-rata total penyewaan per hari.")
k3.metric("Pengguna Registered", f"{porsi_registered:.1%}", help="Porsi pengguna terdaftar terhadap total penyewaan.")
k4.metric("Jam Puncak", f"{jam_puncak:02d}.00", help="Jam dengan rata-rata penyewaan tertinggi (waktu setempat Washington D.C.).")

st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)

# ---------- TABS NAVIGASI UTAMA ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "Pola Jam Sibuk", "Pengaruh Cuaca & Musim", "Analisis Pertumbuhan", "Eksplorasi Lanjutan"
])

# ---------- TAB 1: POLA JAM ----------
with tab1:
    st.markdown("### Analisis Pola Waktu Permintaan")
    st.markdown("<p style='color: #64748B; font-size: 0.95rem;'>Perbandingan kurva penyewaan per jam antara hari kerja dan akhir pekan/libur.</p>", unsafe_allow_html=True)

    pola = hour_df.groupby(["hr", "day_type"])["cnt"].mean().unstack()

    fig, ax = plt.subplots(figsize=(11, 4.8))
    for kolom, warna in [("Hari Kerja", BIRU), ("Akhir Pekan/Libur", ORANYE)]:
        if kolom in pola.columns:
            ax.plot(pola.index, pola[kolom], color=warna, lw=3, marker="o", ms=5, label=kolom, alpha=0.95)
            jam, nilai = pola[kolom].idxmax(), pola[kolom].max()
            ax.annotate(f"Puncak {jam:02d}.00\n{nilai:.0f} unit", (jam, nilai),
                        textcoords="offset points", xytext=(0, 14), ha="center",
                        color=warna, fontsize=8.5, fontweight="bold")

    ax.set_xticks(range(24))
    ax.set_xlabel("Jam dalam Sehari", labelpad=10, fontweight="semibold")
    ax.set_ylabel("Rata-rata Penyewaan / Jam", labelpad=10, fontweight="semibold")
    ax.set_ylim(0, pola.max().max() * 1.25)
    ax.grid(axis="y", linestyle=":", alpha=0.15, color="#F8FAFC")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    sumber(fig, "Sumber: Capital Bikeshare (hour.csv)")
    st.pyplot(fig)
    plt.close(fig)

    st.info("**Key Takeaway:** Hari kerja didominasi aktivitas komuter dengan dua puncak tajam (pagi dan sore), sementara akhir pekan menunjukkan pola rekreasi dengan satu puncak di siang hari.")

# ---------- TAB 2: CUACA & MUSIM ----------
with tab2:
    st.markdown("### Dampak Lingkungan terhadap Volume Sewa")
    st.markdown("<p style='color: #64748B; font-size: 0.95rem;'>Evaluasi fluktuasi penyewaan berdasarkan variasi cuaca harian dan musim dalam setahun.</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    cuaca = day_df.groupby("weather_day")["cnt"].agg(["mean", "count"]).reindex(URUTAN_CUACA).dropna()
    with c1:
        fig, ax = plt.subplots(figsize=(5.5, 4.2))
        warna = [HIJAU if n == "Cerah" else (ORANYE if n.startswith("Hujan") else ABU) for n in cuaca.index]
        bars = ax.bar(range(len(cuaca)), cuaca["mean"], color=warna, width=0.55, alpha=0.9)

        for bar, (_, b) in zip(bars, cuaca.iterrows()):
            ax.text(bar.get_x() + bar.get_width() / 2., b["mean"] + 120, f"{b['mean']:,.0f}",
                    ha="center", fontsize=9, fontweight="bold", color="#F1F5F9")

        ax.set_xticks(range(len(cuaca)))
        ax.set_xticklabels([f"{n}\n(n={int(c)})" for n, c in zip(cuaca.index, cuaca["count"])], fontsize=8.5)
        ax.set_ylim(0, 6500)
        ax.set_ylabel("Rata-rata Penyewaan Harian", fontweight="semibold")
        ax.set_title("Berdasarkan Kondisi Cuaca", pad=12)
        ax.grid(axis="y", linestyle=":", alpha=0.15, color="#F8FAFC")
        st.pyplot(fig)
        plt.close(fig)

    musim_df = day_df.groupby("season_label")["cnt"].mean().reindex(URUTAN_MUSIM).dropna()
    with c2:
        fig, ax = plt.subplots(figsize=(5.5, 4.2))
        warna = [ORANYE if m == musim_df.idxmin() else BIRU for m in musim_df.index]
        bars = ax.bar(musim_df.index, musim_df.values, color=warna, width=0.55, alpha=0.9)

        for bar, v in zip(bars, musim_df.values):
            ax.text(bar.get_x() + bar.get_width() / 2., v + 120, f"{v:,.0f}",
                    ha="center", fontsize=9, fontweight="bold", color="#F1F5F9")

        ax.set_ylim(0, 6500)
        ax.set_title("Berdasarkan Musim", pad=12)
        ax.grid(axis="y", linestyle=":", alpha=0.15, color="#F8FAFC")
        st.pyplot(fig)
        plt.close(fig)

    if "Cerah" in cuaca.index and "Hujan/Salju Ringan" in cuaca.index:
        turun = cuaca.loc["Hujan/Salju Ringan", "mean"] / cuaca.loc["Cerah", "mean"] - 1
        st.info(f"**Key Takeaway:** Hari hujan atau salju ringan mengalami penurunan rata-rata sebesar {abs(turun):.0%} dibandingkan hari cerah. "
                "Perhatikan jumlah hari (n) pada tiap kategori; kelompok dengan sedikit hari kurang kuat dijadikan dasar kesimpulan.")

# ---------- TAB 3: PERTUMBUHAN ----------
with tab3:
    st.markdown("### Perbandingan Pertumbuhan 2012 terhadap 2011")
    st.markdown("<p style='color: #64748B; font-size: 0.95rem;'>Tren bulanan dan kenaikan volume berdasarkan tipe pengguna.</p>", unsafe_allow_html=True)

    bulanan = day_df.groupby(["year", "month_label"])["cnt"].sum().unstack(0).reindex(URUTAN_BULAN)
    per_tahun = day_df.groupby("year")[["casual", "registered", "cnt"]].sum()

    c1, c2 = st.columns([3, 2])
    with c1:
        fig, ax = plt.subplots(figsize=(7, 4.2))
        if 2011 in bulanan.columns:
            ax.plot(bulanan.index, bulanan[2011], color=ABU, lw=2, marker="o", ms=4, label="2011", alpha=0.7)
        if 2012 in bulanan.columns:
            ax.plot(bulanan.index, bulanan[2012], color=BIRU, lw=2.8, marker="o", ms=5, label="2012")

        ax.set_ylim(0, max(bulanan.max().max() * 1.15, 1))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1000:.0f}rb"))
        ax.set_ylabel("Total Penyewaan Bulanan", fontweight="semibold")
        ax.grid(axis="y", linestyle=":", alpha=0.15, color="#F8FAFC")
        ax.legend(frameon=False, loc="upper left")
        ax.set_title("Tren Pertumbuhan Bulanan", pad=12)
        st.pyplot(fig)
        plt.close(fig)

    with c2:
        if {2011, 2012}.issubset(per_tahun.index):
            tumbuh = (per_tahun.loc[2012] / per_tahun.loc[2011] - 1) * 100
            fig, ax = plt.subplots(figsize=(4.5, 4.2))
            bars = ax.bar(["Casual", "Registered"], [tumbuh["casual"], tumbuh["registered"]], color=[ABU, BIRU], width=0.5)

            for bar, t in zip(bars, ["casual", "registered"]):
                val = tumbuh[t]
                ax.text(bar.get_x() + bar.get_width() / 2., val + 1.5, f"+{val:.1f}%",
                        ha="center", fontsize=10, fontweight="bold", color="#F1F5F9")

            ax.set_ylim(0, max(tumbuh[["casual", "registered"]].max() * 1.25, 1))
            ax.set_ylabel("Pertumbuhan (%)", fontweight="semibold")
            ax.grid(axis="y", linestyle=":", alpha=0.15, color="#F8FAFC")
            ax.set_title("Pertumbuhan Tipe Pengguna", pad=12)
            st.pyplot(fig)
            plt.close(fig)

            st.info(f"**Key Takeaway:** Total penyewaan tumbuh sebesar **{tumbuh['cnt']:.1f}%** pada tahun 2012.")
        else:
            st.warning("Perbandingan pertumbuhan memerlukan cakupan data tahun 2011 dan 2012.")

# ---------- TAB 4: ANALISIS LANJUTAN ----------
with tab4:
    st.markdown("### Segmentasi Lanjutan dan Pola Perilaku")
    st.markdown("<p style='color: #64748B; font-size: 0.95rem;'>Manual grouping dan binning: heatmap waktu, kelompok suhu, tingkat permintaan, dan profil pengguna. RFM dan geospatial tidak digunakan karena data tidak memuat ID pelanggan maupun koordinat.</p>", unsafe_allow_html=True)

    st.markdown("**a. Peta Panas Aktivitas (Hari vs Jam)**")
    heat = hour_df.pivot_table(index="weekday_label", columns="hr", values="cnt", aggfunc="mean")
    heat = heat.reindex([h for h in URUTAN_HARI if h in heat.index])

    fig, ax = plt.subplots(figsize=(11, 3.8))
    sns.heatmap(heat, cmap="Blues", linewidths=0.4, linecolor="#0B1120",
                cbar_kws={"label": "Rata-rata/jam"}, ax=ax, cbar=True)
    ax.set_xlabel("Jam dalam Sehari", labelpad=8, fontweight="semibold")
    ax.set_ylabel("")
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**b. Kelompok Suhu Harian**")
        label_suhu = ["Dingin (<10°C)", "Sejuk (10-20°C)", "Hangat (20-30°C)", "Panas (>30°C)"]
        tmp = day_df.copy()
        tmp["temp_group"] = pd.cut(tmp["temp_c"], bins=[0, 10, 20, 30, 41], labels=label_suhu, include_lowest=True)
        suhu = tmp.groupby("temp_group", observed=True)["cnt"].agg(["mean", "count"])

        fig, ax = plt.subplots(figsize=(5.5, 4))
        warna = [BIRU if v == suhu["mean"].max() else ABU for v in suhu["mean"]]
        ax.bar(range(len(suhu)), suhu["mean"], color=warna, width=0.55)

        for i, (v, n) in enumerate(zip(suhu["mean"], suhu["count"])):
            ax.text(i, v + 120, f"{v:,.0f}", ha="center", fontsize=9, fontweight="bold", color="#F1F5F9")

        ax.set_xticks(range(len(suhu)))
        ax.set_xticklabels([f"{l}\n(n={int(n)})" for l, n in zip(suhu.index, suhu["count"])], fontsize=7.5)
        ax.set_ylim(0, max(suhu["mean"].max() * 1.2, 1))
        ax.set_ylabel("Rata-rata Penyewaan", fontweight="semibold")
        ax.grid(axis="y", linestyle=":", alpha=0.15, color="#F8FAFC")
        st.pyplot(fig)
        plt.close(fig)

    with c2:
        st.markdown("**c. Komposisi Tingkat Permintaan Musiman**")
        tmp["demand_level"] = pd.cut(tmp["cnt"], bins=[0, 3000, 6000, max(tmp["cnt"].max(), 6001)],
                                     labels=["Rendah", "Sedang", "Tinggi"])
        komposisi = pd.crosstab(tmp["season_label"], tmp["demand_level"], normalize="index") * 100
        komposisi = komposisi.reindex([m for m in URUTAN_MUSIM if m in komposisi.index])
        komposisi = komposisi.reindex(columns=["Rendah", "Sedang", "Tinggi"], fill_value=0)

        fig, ax = plt.subplots(figsize=(5.5, 4))
        komposisi.plot(kind="barh", stacked=True, ax=ax, color=[ORANYE, ABU, BIRU], width=0.6)
        ax.invert_yaxis()

        for container in ax.containers:
            ax.bar_label(container, labels=[f"{v:.0f}%" if v >= 8 else "" for v in container.datavalues],
                         label_type="center", color="#FFFFFF", fontsize=8, fontweight="bold")

        ax.set_xlim(0, 100)
        ax.set_xlabel("Persentase Hari (%)", fontweight="semibold")
        ax.set_ylabel("")
        ax.legend(title="Permintaan", frameon=False, bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Rendah < 3.000, Sedang 3.000-6.000, Tinggi > 6.000 sepeda per hari.")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown("**d. Karakter Profil Pengguna Berdasarkan Tipe Hari**")
    tmp["casual_share"] = tmp["casual"] / tmp["cnt"]
    tmp["user_profile"] = pd.cut(tmp["casual_share"], bins=[0, 0.15, 0.30, 1.0],
                                 labels=["Komuter (<15% casual)", "Campuran (15-30%)", "Rekreasi (>30% casual)"])
    profil = pd.crosstab(tmp["day_type"], tmp["user_profile"], normalize="index") * 100
    profil = profil.reindex(columns=["Komuter (<15% casual)", "Campuran (15-30%)", "Rekreasi (>30% casual)"], fill_value=0)

    fig, ax = plt.subplots(figsize=(11, 2.8))
    profil.plot(kind="barh", stacked=True, ax=ax, color=[BIRU, ABU, ORANYE], width=0.5)

    for container in ax.containers:
        ax.bar_label(container, labels=[f"{v:.0f}%" if v >= 8 else "" for v in container.datavalues],
                     label_type="center", color="#FFFFFF", fontsize=8, fontweight="bold")

    ax.set_xlim(0, 100)
    ax.set_xlabel("Persentase Hari (%)", fontweight="semibold")
    ax.set_ylabel("")
    ax.legend(title="Profil Pengguna", frameon=False, bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)
    st.pyplot(fig)
    plt.close(fig)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #475569; font-size: 13px; padding-bottom: 20px;'>"
    "Bike Sharing Analytics Dashboard &middot; Proyek Analisis Data &middot; Streamlit &amp; Python"
    "</div>",
    unsafe_allow_html=True,
)