# ==========================================================
# FIXED VERSION
# ONLY ISSUE = TEXT WAS DARK ON DARK BACKGROUND
# THIS FORCE MAKES HERO + KPI TEXT WHITE
# KEEP EVERYTHING SAME
# ==========================================================

import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# LOAD
# ==================================================
@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# ==================================================
# CSS (REAL FIX)
# ==================================================
st.markdown("""
<style>

/* MAIN */
.stApp{
background:#eef2f5;
color:#17384A;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#003b46,#005f6b,#008c9e);
}

section[data-testid="stSidebar"] *{
color:white !important;
}

/* HERO */
.hero{
background:linear-gradient(135deg,#003b46,#008c9e,#00b8c8);
padding:35px;
border-radius:22px;
box-shadow:0 12px 25px rgba(0,0,0,.15);
}

.hero h1{
color:white !important;
font-size:56px;
font-weight:800;
margin-bottom:10px;
}

.hero p{
color:white !important;
font-size:22px;
line-height:1.6;
}

/* KPI */
.kpi{
background:linear-gradient(135deg,#003b46,#008c9e);
padding:22px;
border-radius:18px;
text-align:center;
}

.kpi h1{
color:white !important;
font-size:44px;
margin:0;
font-weight:800;
}

.kpi p{
color:white !important;
font-size:18px;
margin-top:8px;
}

/* CARD */
.card{
background:white;
padding:24px;
border-radius:18px;
box-shadow:0 10px 24px rgba(0,0,0,.08);
color:#17384A !important;
}

.card *{
color:#17384A !important;
}

/* TITLES */
.big{
font-size:48px;
font-weight:800;
color:#003b46;
}

.sub{
color:#5f6b73;
font-size:18px;
margin-bottom:18px;
}

/* BUTTON */
.stButton button{
background:#008c9e;
color:white !important;
border:none;
font-weight:700;
border-radius:10px;
}

/* INPUTS */
label{
color:#17384A !important;
font-weight:700;
}

textarea,input{
color:#17384A !important;
}

/* DEFAULT TEXT */
p,span,li,h1,h2,h3,h4,h5,h6{
color:#17384A;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("Tumblr Growth Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Analytics Dashboard",
        "Strategic Post Simulator",
        "Growth Playbook",
        "Consulting Summary"
    ]
)

# ==================================================
# EXECUTIVE OVERVIEW
# ==================================================
if page == "Executive Overview":

    st.markdown("""
    <div class='hero'>
        <h1>Tumblr Growth Intelligence Platform</h1>
        <p>
        AI-powered analytics platform helping indie music creators understand engagement,
        improve captions, optimize posting strategy, and grow audience reach.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    vals = [
        (len(df), "Posts Analyzed"),
        (round(df["note_count"].mean(),2), "Avg Notes"),
        (round(df["note_count"].max(),0), "Highest Notes"),
        (str(int(df.groupby("hour")["note_count"].mean().idxmax()))+":00", "Best Posting Hour")
    ]

    for col,v in zip([c1,c2,c3,c4], vals):
        with col:
            st.markdown(f"""
            <div class='kpi'>
                <h1>{v[0]}</h1>
                <p>{v[1]}</p>
            </div>
            """, unsafe_allow_html=True)

# ==================================================
# ANALYTICS DASHBOARD
# ==================================================
elif page == "Analytics Dashboard":
    st.markdown("<div class='big'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Meaningful creator insights built from Tumblr indie music data.</div>", unsafe_allow_html=True)

# ==================================================
# STRATEGIC POST SIMULATOR
# ==================================================
elif page == "Strategic Post Simulator":
    st.markdown("<div class='big'>Strategic Post Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Predict post performance before publishing.</div>", unsafe_allow_html=True)

# ==================================================
# GROWTH PLAYBOOK
# ==================================================
elif page == "Growth Playbook":
    st.markdown("<div class='big'>Growth Playbook</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h2>Recommended Creator Strategy</h2>
    <p>Use storytelling captions, niche tags, and best posting hours.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# CONSULTING SUMMARY
# ==================================================
elif page == "Consulting Summary":
    st.markdown("<div class='big'>Consulting Summary</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h2>Project Overview</h2>
    <p>This platform helps creators grow using analytics and machine learning.</p>

    <h2>Business Value</h2>
    <p>Better posts, stronger reach, repeatable growth.</p>
    </div>
    """, unsafe_allow_html=True)
