import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
from pathlib import Path

# =========================================================
# HR GATE PASS MANAGEMENT SYSTEM - PHASE 2 UI/UX
# =========================================================
import streamlit as st
# --- CUSTOM CSS FOR BACKGROUND & GLASSMORPHISM LOGIN ---
def apply_login_styles():
    st.markdown("""
        <style>
        /* Modern Dark Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            color: #ffffff;
        }

        /* Hide Streamlit Header & Footer on Login */
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* Styled Input Fields */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.07) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #a855f7 !important;
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.4) !important;
        }

        /* Custom Login Button */
        div.stButton > button {
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 10px 24px !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM LOGIC ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        apply_login_styles()

        def password_entered():
            if (
                st.session_state.get("username") == "admin"
                and st.session_state.get("password") == "admin123"  # Yahan apna password set karein
            ):
                st.session_state["password_correct"] = True
                del st.session_state["password"]
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        # Center Layout
        col1, col2, col3 = st.columns([1, 1.2, 1])

        with col2:
            st.write("<br><br>", unsafe_allow_html=True)
            
            # Glass Container Card
            with st.container():
                st.markdown("<h2 style='text-align: center; color: #ffffff;'>🔒 HR Portal</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 14px;'>Authorized Access Only</p>", unsafe_allow_html=True)
                st.write("")

                st.text_input("Username", key="username", placeholder="Enter username")
                st.text_input("Password", type="password", key="password", placeholder="Enter password")

                st.write("")
                st.button("Login to Dashboard", on_click=password_entered, use_container_width=True)

                if "password_correct" in st.session_state and st.session_state["password_correct"] is False:
                    st.error("❌ Invalid Username or Password")

        return False

    return True

# Stop execution if not logged in
if not check_password():
    st.stop()

# --- SIDEBAR LOGOUT ---
with st.sidebar:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["password_correct"] = False
        st.rerun()

# Aapka baki normal Streamlit app code yahan se start hoga...
# Sidebar me Logout button
with st.sidebar:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["password_correct"] = False
        st.rerun()

# Aapka baki saara app code yahan se niche rahega....
st.set_page_config(
    page_title="HR Gate Pass Management System",
    page_icon="🪪",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "gatepass.db"

REQUIRED_COLUMNS = [
    "Date", "IVR Number", "PO No", "PO Validity", "Full Name",
    "Gender", "Designation", "DateOfBirth", "Marital Status",
    "Spouse Name", "Father or Husband Name", "Highest Education",
    "Medical Date", "Med Cert No", "PVC", "PVC Date", "Pass Validity",
    "WC Policy No", "WC Policy Validity", "Driving License No",
    "Driving License Expiry Date", "ESIC", "Vendor Code", "VendorName",
    "PASS Category", "Pass Status", "Medical Exp Date", "Status Print Card"
]

# ------------------------- UI STYLE ----------------------
st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.stApp{background:radial-gradient(circle at 5% 5%,rgba(59,130,246,.13),transparent 24%),radial-gradient(circle at 95% 10%,rgba(6,182,212,.10),transparent 22%),linear-gradient(135deg,#f7faff,#eef4ff 52%,#f8fbff)}
.block-container{padding:1.1rem 2rem 3rem;max-width:1800px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#071326,#0b1f3d 50%,#061021);border-right:1px solid rgba(255,255,255,.08)}
[data-testid="stSidebar"] .block-container{padding:1.1rem .75rem 1.4rem}
[data-testid="stSidebar"] *{color:#edf4ff}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:13px;padding:10px 11px;margin:3px 0;font-size:13px;transition:.18s;border:1px solid transparent}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:rgba(255,255,255,.075);border-color:rgba(255,255,255,.08);transform:translateX(3px)}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"]{gap:2px}
.brand{padding:5px 7px 18px;margin-bottom:13px;border-bottom:1px solid rgba(255,255,255,.1)}
.brand-row{display:flex;align-items:center;gap:11px}.brand-mark{width:48px;height:48px;display:flex;align-items:center;justify-content:center;border-radius:15px;background:linear-gradient(135deg,#2563eb,#06b6d4);box-shadow:0 12px 30px rgba(37,99,235,.38);font-size:24px}
.brand-title{font-size:18px;font-weight:900;line-height:1.12}.brand-sub{font-size:10px;color:#9eb0cb!important;margin-top:5px;line-height:1.4}
.side-section{font-size:9px;color:#7186a7;text-transform:uppercase;letter-spacing:1.3px;font-weight:900;margin:16px 8px 6px}.side-footer{margin-top:18px;padding:12px;border:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.04);border-radius:13px;font-size:10px;color:#93a7c5;line-height:1.55}.online-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 10px #22c55e;margin-right:5px}
.page-header{position:relative;overflow:hidden;margin:0 0 20px;padding:27px 30px;border:1px solid rgba(148,163,184,.18);border-radius:24px;background:linear-gradient(110deg,rgba(255,255,255,.97),rgba(242,248,255,.92));box-shadow:0 18px 50px rgba(15,23,42,.075);backdrop-filter:blur(15px)}
.page-header:after{content:"";position:absolute;right:-75px;top:-110px;width:280px;height:280px;border-radius:50%;background:linear-gradient(135deg,rgba(37,99,235,.16),rgba(6,182,212,.035))}
.page-title{position:relative;z-index:1;width:100%;font-size:clamp(30px,3.2vw,44px);line-height:1.13;font-weight:950;letter-spacing:-1.35px;color:#0a1730;margin:0;overflow-wrap:anywhere;white-space:normal}
.page-subtitle{position:relative;z-index:1;color:#64748b;font-size:13px;line-height:1.6;margin:9px 0 0;max-width:900px}.header-chip{position:relative;z-index:1;display:inline-flex;padding:6px 11px;border-radius:999px;background:#e8f1ff;color:#2563eb;font-size:9px;font-weight:900;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px}.header-meta{position:relative;z-index:1;margin-top:15px;display:flex;gap:8px;flex-wrap:wrap}.meta-pill{font-size:10px;color:#52627a;background:#f5f8fc;border:1px solid #e4eaf2;padding:6px 9px;border-radius:999px}
.kpi{position:relative;overflow:hidden;min-height:126px;padding:18px 19px;border:1px solid rgba(148,163,184,.17);border-radius:19px;background:rgba(255,255,255,.91);box-shadow:0 11px 30px rgba(15,23,42,.065);transition:.2s}.kpi:hover{transform:translateY(-3px);box-shadow:0 18px 38px rgba(15,23,42,.11)}.kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,#2563eb,#06b6d4)}.kpi-icon{position:absolute;right:16px;top:15px;width:35px;height:35px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:#eef5ff;font-size:17px}.kpi-label{font-size:10px;color:#718096;font-weight:850;text-transform:uppercase;letter-spacing:.55px}.kpi-value{font-size:30px;line-height:1.1;font-weight:950;color:#0f172a;margin-top:10px;letter-spacing:-.7px;overflow-wrap:anywhere}.kpi-note{font-size:10px;color:#98a5b8;margin-top:7px}
.section-title{font-size:16px;line-height:1.3;font-weight:900;color:#16213a;margin:19px 0 10px;display:flex;align-items:center;gap:8px}.section-title:before{content:"";width:4px;height:18px;border-radius:4px;background:linear-gradient(180deg,#2563eb,#06b6d4)}
.chart-card{padding:17px 18px;border:1px solid rgba(148,163,184,.17);border-radius:19px;background:rgba(255,255,255,.89);box-shadow:0 10px 27px rgba(15,23,42,.05)}
.profile{border:1px solid rgba(148,163,184,.18);border-radius:21px;padding:23px;background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(246,250,255,.89));box-shadow:0 13px 34px rgba(15,23,42,.065)}.profile-top{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.profile-avatar{width:58px;height:58px;border-radius:17px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#2563eb,#06b6d4);color:white;font-size:25px;font-weight:900;box-shadow:0 10px 24px rgba(37,99,235,.25)}.profile-name{font-size:27px;line-height:1.2;font-weight:950;color:#0b1730;overflow-wrap:anywhere}.profile-meta{color:#65748c;font-size:12px;line-height:1.55;margin-top:6px;overflow-wrap:anywhere}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;font-size:10px;font-weight:850;margin-right:5px;margin-bottom:4px}.badge-green{background:#dcfce7;color:#166534}.badge-red{background:#fee2e2;color:#991b1b}.badge-yellow{background:#fef3c7;color:#92400e}.badge-gray{background:#f1f5f9;color:#334155}
.mini-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #edf1f6;font-size:11px;color:#526176}.mini-row:last-child{border-bottom:0}.bar-wrap{height:7px;background:#edf2f7;border-radius:99px;margin-top:6px;overflow:hidden}.bar{height:100%;background:linear-gradient(90deg,#2563eb,#06b6d4);border-radius:99px}
.stButton>button,.stDownloadButton>button{border-radius:12px;min-height:43px;font-weight:800;border:1px solid rgba(37,99,235,.15);box-shadow:0 5px 14px rgba(15,23,42,.05);transition:.18s}.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-1px);box-shadow:0 9px 22px rgba(15,23,42,.10)}.stTextInput input,.stSelectbox [data-baseweb="select"],.stMultiSelect [data-baseweb="select"]{border-radius:12px}.stTextInput label,.stSelectbox label,.stMultiSelect label,.stFileUploader label{font-weight:750;color:#4b5a70}div[data-testid="stDataFrame"]{border:1px solid #e1e8f2;border-radius:14px;overflow:hidden;box-shadow:0 7px 22px rgba(15,23,42,.035)}.stAlert{border-radius:13px}.stFileUploader{border-radius:13px}hr{border:0;border-top:1px solid rgba(148,163,184,.2);margin:20px 0}[data-testid="stMetric"]{background:white;border:1px solid #e8edf4;border-radius:14px;padding:10px 13px}
@media(max-width:900px){.block-container{padding-left:1rem;padding-right:1rem}.page-header{padding:20px;border-radius:18px}.page-title{font-size:30px}.kpi-value{font-size:26px}.profile-top{display:block}.profile-avatar{margin-bottom:12px}}
</style>""", unsafe_allow_html=True)
def page_header(title, subtitle, chip="HR GATE PASS MANAGEMENT"):
    st.markdown(
        f'<div class="page-header"><div class="header-chip">{chip}</div>'
        f'<div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div>'
        f'<div class="header-meta"><span class="meta-pill">🛡️ Compliance Workspace</span>'
        f'<span class="meta-pill">⚡ Live Database View</span></div></div>',
        unsafe_allow_html=True)

# ------------------------- HELPERS -----------------------
def normalize_column_name(column):
    return " ".join(str(column).replace("\xa0", " ").split()).strip()

def clean_dataframe(df):
    df = df.copy()
    df.columns = [normalize_column_name(c) for c in df.columns]
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col].fillna("").astype(str)
                .str.replace("\xa0", " ", regex=False)
                .str.strip()
            )
    return df

def conn():
    return sqlite3.connect(DB_PATH)

def create_database():
    c = conn()
    cols = ", ".join(f'"{x}" TEXT' for x in REQUIRED_COLUMNS)
    c.execute(f'CREATE TABLE IF NOT EXISTS gate_pass (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})')
    c.commit()
    c.close()

def load_data():
    c = conn()
    try:
        d = pd.read_sql_query("SELECT * FROM gate_pass", c)
    except Exception:
        d = pd.DataFrame()
    c.close()
    return d.drop(columns=["id"], errors="ignore")

def valid_value(v):
    if pd.isna(v):
        return False
    return str(v).strip().lower() not in ["", "nan", "none", "null", "nat", "-", "na", "n/a"]

def covered_count(s):
    return int(s.apply(valid_value).sum())

def esic_status(v):
    if not valid_value(v):
        return "Not Covered"
    x = str(v).strip().lower()
    if x in ["not cover", "not covered", "no", "not available", "na", "n/a", "none", "nil", "0", "-"]:
        return "Not Covered"
    return "Covered"

def status_badge(value):
    x = str(value).strip().lower()
    if x in ["active", "valid", "approved", "covered", "yes"]:
        return '<span class="badge badge-green">● Valid</span>'
    if x in ["expired", "rejected", "inactive", "not covered", "not cover", "no"]:
        return '<span class="badge badge-red">● Expired / Not Covered</span>'
    return '<span class="badge badge-yellow">● Review</span>'

def kpi(label, value, note="", icon="📌"):
    st.markdown(
        f'<div class="kpi"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
        unsafe_allow_html=True)

def mini_chart(series, title, limit=8):
    s = series.value_counts().head(limit)
    if s.empty:
        st.info("No data available")
        return
    max_v = max(int(s.max()), 1)
    rows = []
    for name, value in s.items():
        pct = int(float(value) / max_v * 100)
        safe_name = str(name)[:32] if str(name) else "Unknown"
        rows.append(f'<div class="mini-row"><div style="width:72%"><b>{safe_name}</b><div class="bar-wrap"><div class="bar" style="width:{pct}%"></div></div></div><strong>{int(value):,}</strong></div>')
    st.markdown(f'<div class="chart-card"><div class="section-title">{title}</div>{"".join(rows)}</div>', unsafe_allow_html=True)

create_database()
df = load_data()

# ------------------------- SIDEBAR -----------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-row">
        <div class="brand-mark">🪪</div>
        <div><div class="brand-title">HR Gate Pass</div>
        <div class="brand-sub">Management & Compliance System</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "MAIN MENU",
        [
            "📊 Dashboard",
            "📤 Upload Excel",
            "🔎 Employee Search",
            "👥 Employee Master",
            "🛡️ WC Policy",
            "🏥 ESIC",
            "🏢 Vendor Analysis",
            "⏰ Expiry & Alerts",
            "📋 Master Data"
        ],
        label_visibility="visible"
    )

    st.markdown('<div class="side-section">System</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-footer"><span class="online-dot"></span><b>System Online</b><br>Phase 2 • Dynamic database foundation<br>Secure HR compliance workspace</div>', unsafe_allow_html=True)

# =========================================================
# DASHBOARD
# =========================================================
if menu == "📊 Dashboard":
    page_header("Dashboard", "HR manpower, gate pass and compliance overview")
    st.markdown('<div class="chart-card" style="margin-bottom:18px"><b style="font-size:13px;color:#16213a">✨ Good to see you</b><span style="color:#64748b;font-size:12px"> — Monitor workforce, gate-pass validity and statutory compliance from one place.</span></div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No records found. Upload your Excel file to start.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi("Total People", f"{len(df):,}", "Employees in master", "👥")
        with c2:
            active = df["Pass Status"].astype(str).str.lower().str.strip().isin(["active","valid"]).sum()
            kpi("Active Pass", f"{active:,}", "Currently active", "🎫")
        with c3:
            wc = covered_count(df["WC Policy No"])
            kpi("WC Covered", f"{wc:,}", f"{wc/len(df)*100:.1f}% coverage", "🛡️")
        with c4:
            esic = df["ESIC"].apply(esic_status).eq("Covered").sum()
            kpi("ESIC Covered", f"{esic:,}", f"{esic/len(df)*100:.1f}% coverage", "🏥")

        st.write("")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            expired = df["Pass Status"].astype(str).str.lower().str.strip().isin(["expired","inactive"]).sum()
            kpi("Expired Pass", f"{expired:,}", "Needs attention", "⚠️")
        with c2:
            kpi("Vendors", f"{df['VendorName'].nunique():,}", "Contractors / vendors", "🏢")
        with c3:
            both = ((df["WC Policy No"].apply(valid_value)) & (df["ESIC"].apply(esic_status).eq("Covered"))).sum()
            kpi("WC + ESIC Both", f"{both:,}", "Both available", "✅")
        with c4:
            neither = ((~df["WC Policy No"].apply(valid_value)) & (df["ESIC"].apply(esic_status).eq("Covered") == False)).sum()
            kpi("Neither Covered", f"{neither:,}", "Priority review", "🚨")

        st.divider()
        left, right = st.columns([1.25, 1])
        with left:
            mini_chart(df["VendorName"], "Top Vendors by Manpower", 10)
        with right:
            mini_chart(df["Pass Status"], "Pass Status Overview", 6)

        st.write("")
        wc_pct = covered_count(df["WC Policy No"]) / len(df) * 100
        esic_pct = df["ESIC"].apply(esic_status).eq("Covered").sum() / len(df) * 100
        active_pct = df["Pass Status"].astype(str).str.lower().str.strip().isin(["active","valid"]).sum() / len(df) * 100
        health = f"""<div class=\"chart-card\">
        <div class=\"section-title\">Compliance Health</div>
        <div style=\"display:grid;grid-template-columns:repeat(3,1fr);gap:16px\">
          <div><div style=\"font-size:11px;color:#718096\">ACTIVE PASS</div><div style=\"font-size:23px;font-weight:900\">{active_pct:.1f}%</div><div class=\"bar-wrap\"><div class=\"bar\" style=\"width:{min(active_pct,100):.1f}%\"></div></div></div>
          <div><div style=\"font-size:11px;color:#718096\">WC COVERAGE</div><div style=\"font-size:23px;font-weight:900\">{wc_pct:.1f}%</div><div class=\"bar-wrap\"><div class=\"bar\" style=\"width:{min(wc_pct,100):.1f}%\"></div></div></div>
          <div><div style=\"font-size:11px;color:#718096\">ESIC COVERAGE</div><div style=\"font-size:23px;font-weight:900\">{esic_pct:.1f}%</div><div class=\"bar-wrap\"><div class=\"bar\" style=\"width:{min(esic_pct,100):.1f}%\"></div></div></div>
        </div></div>"""
        st.markdown(health, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Vendor Compliance Snapshot</div>', unsafe_allow_html=True)
        summary = df.groupby("VendorName").agg(
            Total=("IVR Number","count"),
            WC_Covered=("WC Policy No", lambda x: covered_count(x)),
            ESIC_Covered=("ESIC", lambda x: x.apply(esic_status).eq("Covered").sum())
        ).reset_index()
        summary["WC %"] = (summary["WC_Covered"]/summary["Total"]*100).round(1)
        summary["ESIC %"] = (summary["ESIC_Covered"]/summary["Total"]*100).round(1)
        st.dataframe(summary, use_container_width=True, hide_index=True)

# =========================================================
# UPLOAD
# =========================================================
elif menu == "📤 Upload Excel":
    page_header("Upload Excel", "Import and validate HR gate pass master data")

    uploaded = st.file_uploader("Choose Excel file", type=["xlsx","xls"])

    if uploaded:
        try:
            x = clean_dataframe(pd.read_excel(uploaded))
            missing = [c for c in REQUIRED_COLUMNS if c not in x.columns]
            extra = [c for c in x.columns if c not in REQUIRED_COLUMNS]

            a,b,c = st.columns(3)
            with a: kpi("Rows", f"{len(x):,}", "Detected records")
            with b: kpi("Columns", f"{len(x.columns):,}", "Detected columns")
            with c: kpi("Required", "28", "Expected columns")

            if missing:
                st.error("Missing required columns")
                st.write(missing)
            else:
                st.success("✓ All required columns matched after automatic header cleaning.")
                if extra:
                    st.warning("Extra columns ignored")
                    st.write(extra)

                st.dataframe(x[REQUIRED_COLUMNS].head(10), use_container_width=True, hide_index=True)

                if st.button("💾 Import / Replace Database", type="primary", use_container_width=True):
                    imp = x[REQUIRED_COLUMNS].fillna("").copy()
                    for col in REQUIRED_COLUMNS:
                        imp[col] = imp[col].astype(str).str.strip()
                    c = conn()
                    imp.to_sql("gate_pass", c, if_exists="replace", index=False)
                    c.close()
                    uploaded.seek(0)
                    (UPLOAD_DIR / uploaded.name).write_bytes(uploaded.getbuffer())
                    st.success(f"Successfully imported {len(imp):,} records.")
                    st.rerun()
        except Exception as e:
            st.error(f"Excel error: {e}")

# =========================================================
# EMPLOYEE SEARCH
# =========================================================
elif menu == "🔎 Employee Search":
    page_header("Employee Search", "Search employee, IVR, vendor, PO, WC or ESIC details")

    if df.empty:
        st.info("Upload data first.")
    else:
        q = st.text_input("🔎 Search", placeholder="Enter name, IVR number, vendor, PO, WC policy, ESIC...")
        col1,col2,col3 = st.columns(3)
        with col1:
            vendor = st.selectbox("Vendor", ["All"] + sorted(df["VendorName"].dropna().astype(str).unique().tolist()))
        with col2:
            pass_status = st.selectbox("Pass Status", ["All"] + sorted(df["Pass Status"].dropna().astype(str).unique().tolist()))
        with col3:
            category = st.selectbox("Pass Category", ["All"] + sorted(df["PASS Category"].dropna().astype(str).unique().tolist()))

        result = df.copy()
        if q:
            mask = result.astype(str).apply(lambda col: col.str.contains(q.strip(), case=False, na=False, regex=False)).any(axis=1)
            result = result[mask]
        if vendor != "All": result = result[result["VendorName"] == vendor]
        if pass_status != "All": result = result[result["Pass Status"] == pass_status]
        if category != "All": result = result[result["PASS Category"] == category]

        st.success(f"{len(result):,} record(s) found")
        st.dataframe(result, use_container_width=True, hide_index=True)

# =========================================================
# EMPLOYEE MASTER
# =========================================================
elif menu == "👥 Employee Master":
    page_header("Employee Master", "Detailed employee profile and compliance view")

    if df.empty:
        st.info("Upload data first.")
    else:
        ivrs = df["IVR Number"].astype(str).tolist()
        selected = st.selectbox("Select IVR Number", ["Select"] + ivrs)
        if selected != "Select":
            row = df[df["IVR Number"].astype(str) == selected].iloc[0]

            st.markdown(
                f'<div class="profile"><div class="profile-name">{row["Full Name"]}</div>'
                f'<div class="profile-meta">IVR: {row["IVR Number"]} &nbsp; | &nbsp; Vendor: {row["VendorName"]} &nbsp; | &nbsp; Designation: {row["Designation"]}</div><br>'
                f'{status_badge(row["Pass Status"])} '
                f'{status_badge("Covered" if valid_value(row["WC Policy No"]) else "Not Covered")} '
                f'{status_badge(esic_status(row["ESIC"]))}</div>',
                unsafe_allow_html=True
            )

            st.write("")
            a,b,c,d = st.columns(4)
            with a: kpi("Pass Status", row["Pass Status"], str(row["Pass Validity"]))
            with b: kpi("WC Policy", "Covered" if valid_value(row["WC Policy No"]) else "Not Covered", str(row["WC Policy Validity"]))
            with c: kpi("ESIC", esic_status(row["ESIC"]), "ESIC record")
            with d: kpi("Medical", str(row["Medical Exp Date"]), "Medical expiry")

            st.markdown('<div class="section-title">Employee Information</div>', unsafe_allow_html=True)
            info_cols = ["IVR Number","Full Name","Gender","Designation","DateOfBirth","Marital Status",
                         "Spouse Name","Father or Husband Name","Highest Education"]
            st.dataframe(row[info_cols].to_frame("Value"), use_container_width=True)

            st.markdown('<div class="section-title">Documents & Compliance</div>', unsafe_allow_html=True)
            doc_cols = ["PO No","PO Validity","Medical Date","Med Cert No","PVC","PVC Date",
                        "Pass Validity","WC Policy No","WC Policy Validity","Driving License No",
                        "Driving License Expiry Date","ESIC","PASS Category","Pass Status","Status Print Card"]
            st.dataframe(row[doc_cols].to_frame("Value"), use_container_width=True)

# =========================================================
# WC
# =========================================================
elif menu == "🛡️ WC Policy":
    page_header("WC Policy Compliance", "Vendor-wise Workers Compensation policy coverage")

    if df.empty:
        st.info("Upload data first.")
    else:
        total = len(df); covered = covered_count(df["WC Policy No"]); notcov = total-covered
        a,b,c,d = st.columns(4)
        with a: kpi("Total People", f"{total:,}")
        with b: kpi("WC Covered", f"{covered:,}")
        with c: kpi("Not Covered", f"{notcov:,}")
        with d: kpi("Coverage", f"{covered/total*100:.1f}%")

        s = df.groupby("VendorName").agg(Total=("IVR Number","count"), WC_Covered=("WC Policy No", lambda x: covered_count(x))).reset_index()
        s["Not_Covered"] = s["Total"] - s["WC_Covered"]
        s["Coverage %"] = (s["WC_Covered"]/s["Total"]*100).round(1)
        st.dataframe(s, use_container_width=True, hide_index=True)

# =========================================================
# ESIC
# =========================================================
elif menu == "🏥 ESIC":
    page_header("ESIC Compliance", "ESIC coverage and vendor-wise compliance")

    if df.empty:
        st.info("Upload data first.")
    else:
        total = len(df); covered = df["ESIC"].apply(esic_status).eq("Covered").sum(); notcov = total-covered
        a,b,c,d = st.columns(4)
        with a: kpi("Total People", f"{total:,}")
        with b: kpi("ESIC Covered", f"{covered:,}")
        with c: kpi("Not Covered", f"{notcov:,}")
        with d: kpi("Coverage", f"{covered/total*100:.1f}%")

        s = df.groupby("VendorName").agg(Total=("IVR Number","count"), ESIC_Covered=("ESIC", lambda x: x.apply(esic_status).eq("Covered").sum())).reset_index()
        s["Not_Covered"] = s["Total"] - s["ESIC_Covered"]
        s["Coverage %"] = (s["ESIC_Covered"]/s["Total"]*100).round(1)
        st.dataframe(s, use_container_width=True, hide_index=True)

# =========================================================
# VENDOR
# =========================================================
elif menu == "🏢 Vendor Analysis":
    page_header("Vendor Analysis", "Manpower and compliance performance by contractor")

    if df.empty:
        st.info("Upload data first.")
    else:
        s = df.groupby("VendorName").agg(
            Total=("IVR Number","count"),
            WC_Covered=("WC Policy No", lambda x: covered_count(x)),
            ESIC_Covered=("ESIC", lambda x: x.apply(esic_status).eq("Covered").sum()),
            Active_Pass=("Pass Status", lambda x: x.astype(str).str.lower().str.strip().isin(["active","valid"]).sum())
        ).reset_index()
        s["WC %"] = (s["WC_Covered"]/s["Total"]*100).round(1)
        s["ESIC %"] = (s["ESIC_Covered"]/s["Total"]*100).round(1)
        st.dataframe(s, use_container_width=True, hide_index=True)
        st.bar_chart(s.set_index("VendorName")["Total"])

# =========================================================
# EXPIRY
# =========================================================
elif menu == "⏰ Expiry & Alerts":
    page_header("Expiry & Alerts", "Find expired and soon-to-expire documents")

    if df.empty:
        st.info("Upload data first.")
    else:
        document = st.selectbox("Document", ["PO Validity","Pass Validity","WC Policy Validity",
                                               "Driving License Expiry Date","Medical Exp Date","PVC Date"])
        window = st.selectbox("Alert window (days)", [7,15,30,60,90], index=2)

        x = df.copy()
        x["Expiry_Date"] = pd.to_datetime(x[document], errors="coerce", dayfirst=True)
        today = pd.Timestamp.today().normalize()
        x["Days_Remaining"] = (x["Expiry_Date"] - today).dt.days

        expired = (x["Days_Remaining"] < 0).sum()
        soon = ((x["Days_Remaining"] >= 0) & (x["Days_Remaining"] <= window)).sum()
        valid = (x["Days_Remaining"] > window).sum()

        a,b,c = st.columns(3)
        with a: kpi("Expired", f"{expired:,}")
        with b: kpi(f"Expiring ≤ {window} days", f"{soon:,}")
        with c: kpi("Valid", f"{valid:,}")

        result = x[x["Days_Remaining"] <= window].sort_values("Days_Remaining")
        st.dataframe(result[["IVR Number","Full Name","VendorName",document,"Days_Remaining"]],
                     use_container_width=True, hide_index=True)

# =========================================================
# MASTER DATA
# =========================================================
elif menu == "📋 Master Data":
    page_header("Master Data", "Complete HR gate pass master database")

    if df.empty:
        st.info("Upload data first.")
    else:
        st.metric("Total Records", f"{len(df):,}")
        st.dataframe(df, use_container_width=True, height=600, hide_index=True)

        out = BytesIO()
        with pd.ExcelWriter(out, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Gate Pass Data")
        st.download_button(
            "📥 Download Excel Report",
            data=out.getvalue(),
            file_name="GatePass_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
