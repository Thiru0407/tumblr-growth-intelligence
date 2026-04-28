# ==========================================================
# FULL UPDATED app.py
# SAME OLD APP
# ONLY FIX = TEXT VISIBILITY ISSUE
# NOTHING ELSE CHANGED
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
# STYLE  (ONLY FIXED TEXT VISIBILITY)
# ==================================================
st.markdown("""
<style>

.stApp{
background:#eef2f5;
color:#17384A !important;
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
color:white !important;
box-shadow:0 12px 25px rgba(0,0,0,.15);
}

.hero *{
color:white !important;
}

/* WHITE CARD */
.card{
background:white;
padding:24px;
border-radius:18px;
box-shadow:0 10px 24px rgba(0,0,0,.08);
color:#17384A !important;
}

.card *{
color:#17384A !important;
opacity:1 !important;
}

/* KPI */
.kpi{
background:linear-gradient(135deg,#003b46,#008c9e);
padding:18px;
border-radius:16px;
text-align:center;
color:white !important;
}

.kpi *{
color:white !important;
}

/* TITLES */
.big{
font-size:42px;
font-weight:800;
color:#003b46 !important;
}

.sub{
color:#4d6773 !important;
font-size:16px;
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
label, textarea, input, p, li, span, div{
color:#17384A !important;
}

/* MAKE STREAMLIT TEXT ALWAYS DARK */
[data-testid="stMarkdownContainer"] *{
color:#17384A !important;
}

/* KEEP HERO WHITE */
.hero [data-testid="stMarkdownContainer"] *{
color:white !important;
}

/* TABLE */
table, th, td{
color:#17384A !important;
}

/* INFO BOX */
.stAlert{
color:#17384A !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HELPERS
# ==================================================
def split_tags(x):
    if pd.isna(x):
        return []
    return [i.strip() for i in str(x).replace(",", "|").split("|") if i.strip()]

def create_features(text, tags, hour):
    blob = TextBlob(text)
    wc = len(text.split())
    tc = len(split_tags(tags))

    return pd.DataFrame([{
        "text_length": len(text),
        "word_count": wc,
        "tag_count": tc,
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
        "hour": hour,
        "is_weekend": 0,
        "tags_text_ratio": tc/(wc+1)
    }])

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
# EXEC OVERVIEW
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
        (str(int(df.groupby("hour")["note_count"].mean().idxmax())) + ":00", "Best Posting Hour")
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
# DASHBOARD
# ==================================================
elif page == "Analytics Dashboard":

    st.markdown("<div class='big'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Meaningful creator insights built from Tumblr indie music data.</div>", unsafe_allow_html=True)

# ==================================================
# SIMULATOR
# ==================================================
elif page == "Strategic Post Simulator":

    st.markdown("<div class='big'>Strategic Post Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Predict post performance before publishing.</div>", unsafe_allow_html=True)

    text = st.text_area("Caption",height=220)
    tags = st.text_input("Tags")
    hour = st.slider("Posting Hour",0,23,19)

    if st.button("Analyze Post"):

        X = create_features(text,tags,hour)
        prob = model.predict_proba(X)[0][1]

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob*100,
            number={"suffix":"%"},
            title={"text":"Engagement Score"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"#003b46"},
                "steps":[
                    {"range":[0,50],"color":"#dceef0"},
                    {"range":[50,75],"color":"#8ed9df"},
                    {"range":[75,100],"color":"#00b8c8"}
                ]
            }
        ))

        fig.update_layout(height=420)
        st.plotly_chart(fig,use_container_width=True)

# ==================================================
# PLAYBOOK
# ==================================================
elif page == "Growth Playbook":

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())

    st.markdown("<div class='big'>Growth Playbook</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card'>
    <h2>Best Growth Tips</h2>

    • <b>Best Time to Post:</b> {best_hour}:00 based on dataset performance<br><br>

    • <b>Ideal Caption Style:</b> Personal, emotional, storytelling captions perform better.<br><br>

    • <b>Best Tag Count:</b> Use around {round(df['tag_count'].mean(),0)} tags.<br><br>

    • <b>Suggested Tags:</b> indie music, new music, indie rock, shoegaze, bedroom pop.<br><br>

    • <b>Growth Strategy:</b> Post consistently 3-5 times weekly.
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# SUMMARY
# ==================================================
elif page == "Consulting Summary":

    st.markdown("<div class='big'>Consulting Summary</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>

    <h2>Client</h2>
    Tumblr Indie Music Community

    <h2>Problem</h2>
    Creators do not know what drives notes / engagement.

    <h2>Solution</h2>
    AI dashboard + predictive analytics + strategy engine.

    <h2>Business Value</h2>
    Smarter posts, stronger reach, consistent growth.

    <h2>Final Recommendation</h2>
    Use the Strategic Post Simulator live in presentation.

    </div>
    """, unsafe_allow_html=True)
