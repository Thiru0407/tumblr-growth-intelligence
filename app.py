# ==========================================================
# FULL UPDATED app.py
# Streamlit Cloud + VS Code SAME LOOK FIXED VERSION
# Keeps your original design, pages, logic
# Added deployment rendering fixes only
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
# GLOBAL CSS FIXED FOR STREAMLIT CLOUD
# ==================================================
st.markdown("""
<style>

/* ---------- APP ---------- */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.stApp{
    background:#eef2f5;
    color:#003b46;
}

/* ---------- MAIN WIDTH ---------- */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1400px;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#003b46,#005f6b,#008c9e);
}

section[data-testid="stSidebar"] *{
    color:white !important;
    font-weight:600;
}

/* ---------- HERO ---------- */
.hero{
    background:linear-gradient(135deg,#003b46,#008c9e,#00b8c8);
    padding:35px;
    border-radius:22px;
    color:white !important;
    box-shadow:0 12px 25px rgba(0,0,0,.15);
}

.hero h1{
    color:white !important;
    font-size:54px;
    font-weight:800;
}

.hero p{
    color:white !important;
    font-size:22px;
    line-height:1.6;
}

/* ---------- CARD ---------- */
.card{
    background:white;
    padding:28px;
    border-radius:18px;
    box-shadow:0 10px 24px rgba(0,0,0,.08);
    color:#003b46 !important;
}

.card h1,.card h2,.card h3,.card p,.card li{
    color:#003b46 !important;
}

/* ---------- KPI ---------- */
.kpi{
    background:linear-gradient(135deg,#003b46,#008c9e);
    padding:22px;
    border-radius:18px;
    text-align:center;
    color:white !important;
    min-height:140px;
}

.kpi h1{
    margin:0;
    font-size:42px;
    font-weight:800;
    color:white !important;
}

.kpi p{
    margin-top:8px;
    font-size:18px;
    color:white !important;
}

/* ---------- HEADINGS ---------- */
.big{
    font-size:54px;
    font-weight:900;
    color:#003b46 !important;
}

.sub{
    color:#4d6570 !important;
    font-size:24px;
    margin-bottom:18px;
}

/* ---------- INPUTS ---------- */
textarea, input{
    color:#003b46 !important;
    background:white !important;
}

label{
    color:#003b46 !important;
    font-weight:700 !important;
}

/* ---------- BUTTON ---------- */
.stButton button{
    background:#008c9e !important;
    color:white !important;
    border:none;
    font-weight:800;
    border-radius:10px;
    padding:12px 24px;
}

/* ---------- PLOTLY ---------- */
.js-plotly-plot{
    background:white !important;
    border-radius:14px;
    padding:8px;
}

/* ---------- METRIC GAP ---------- */
[data-testid="column"]{
    padding:4px;
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
        "Graph Insights Guide",
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
    st.markdown("<div class='sub'>Meaningful graphs showing what really drives Tumblr engagement.</div>", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)

    vals = [
        (f"{round(df['high_engagement'].mean()*100,1)}%","High Engagement Rate"),
        (round(df["word_count"].mean(),0),"Avg Words"),
        (round(df["tag_count"].mean(),0),"Avg Tags"),
        (str(int(df.groupby("hour")["note_count"].mean().idxmax()))+":00","Best Hour"),
        (round(df["polarity"].mean(),2),"Avg Sentiment")
    ]

    for col,v in zip([c1,c2,c3,c4,c5], vals):
        with col:
            st.markdown(f"""
            <div class='kpi'>
            <h1>{v[0]}</h1>
            <p>{v[1]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    a,b = st.columns(2)

    with a:
        temp = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(temp,x="hour",y="note_count",
                     title="Average Notes by Posting Hour",
                     color="note_count",
                     color_continuous_scale="Teal")
        fig.update_layout(template="plotly_white",height=500)
        st.plotly_chart(fig,use_container_width=True)

    with b:
        temp = df.groupby("high_engagement")["word_count"].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(temp,x="Class",y="word_count",
                     title="Average Caption Length: Low vs High Success",
                     color="Class",
                     color_discrete_sequence=["#003b46","#00b8c8"])
        fig.update_layout(template="plotly_white",height=500,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

# ==================================================
# GRAPH GUIDE
# ==================================================
elif page == "Graph Insights Guide":

    st.markdown("<div class='big'>Graph Insights Guide</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Simple explanation for non-technical audience.</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h2>What the charts mean</h2>
    <p>
    These graphs help creators understand:
    best posting hour, ideal caption size,
    tag strategy, and emotional writing style.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# SIMULATOR
# ==================================================
elif page == "Strategic Post Simulator":

    st.markdown("<div class='big'>Strategic Post Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Predict performance before publishing.</div>", unsafe_allow_html=True)

    text = st.text_area("Caption", height=220)
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

    st.markdown("<div class='big'>Growth Playbook</div>", unsafe_allow_html=True)

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())

    st.markdown(f"""
    <div class='card'>
    <h2>Best Growth Tips</h2>
    <p><b>Best Time to Post:</b> {best_hour}:00</p>
    <p><b>Ideal Caption Style:</b> emotional + storytelling</p>
    <p><b>Ideal Tag Count:</b> 8 to 10 tags</p>
    <p><b>Consistency:</b> 3 to 5 posts weekly</p>
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
    <p>Tumblr Indie Music Community</p>

    <h2>Problem</h2>
    <p>Creators lacked visibility into what drives engagement.</p>

    <h2>Solution</h2>
    <p>Analytics dashboard + prediction engine + strategy system.</p>

    <h2>Business Value</h2>
    <p>Better posts, stronger reach, repeatable audience growth.</p>
    </div>
    """, unsafe_allow_html=True)
