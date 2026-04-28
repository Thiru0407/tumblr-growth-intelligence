# ===============================
# TUMBLR GROWTH INTELLIGENCE PLATFORM
# FULL FIXED STREAMLIT CODE
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from textblob import TextBlob

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# LOAD FILES
# -----------------------------------
df = pd.read_csv("tumblr_features.csv")
model = joblib.load("tumblr_model.pkl")

# -----------------------------------
# CSS FIXED UI
# -----------------------------------
st.markdown("""
<style>

/* App */
.stApp{
    background:#E8EEF1;
}

/* Main spacing */
.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

/* Headings */
h1,h2,h3{
    color:#004D61 !important;
    font-weight:800 !important;
}

/* Normal text */
p,li,label,span,div{
    color:#163847;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#005461,#00B7B5);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Cards */
.custom-card{
    background:white;
    padding:28px;
    border-radius:18px;
    box-shadow:0 8px 18px rgba(0,0,0,.08);
    margin-bottom:20px;
}

.custom-card *{
    color:#17394A !important;
}

/* Hero */
.hero{
    background:linear-gradient(90deg,#005461,#00B7B5);
    padding:35px;
    border-radius:22px;
    color:white !important;
    margin-bottom:18px;
}

.hero h1,.hero p{
    color:white !important;
}

/* KPI */
.metric{
    background:linear-gradient(135deg,#005461,#00B7B5);
    padding:25px;
    border-radius:18px;
    text-align:center;
    color:white !important;
    font-weight:700;
}

.metric h1,.metric h3,.metric p{
    color:white !important;
}

/* Buttons */
.stButton>button{
    background:linear-gradient(90deg,#005461,#00B7B5);
    color:white;
    border:none;
    padding:0.7rem 1.2rem;
    border-radius:10px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
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

# -----------------------------------
# COMMON METRICS
# -----------------------------------
posts = len(df)
avg_notes = round(df["note_count"].mean(), 2)
max_notes = int(df["note_count"].max())
best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())

# -----------------------------------
# PAGE 1
# -----------------------------------
if page == "Executive Overview":

    st.markdown(f"""
    <div class='hero'>
        <h1>Tumblr Growth Intelligence Platform</h1>
        <p>An AI-powered creator analytics platform for Tumblr indie music creators. 
        Understand what drives engagement, improve captions, optimize tags, identify stronger posting windows, 
        and make smarter publishing decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"<div class='metric'><h1>{posts:,}</h1><p>Posts Analyzed</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric'><h1>{avg_notes}</h1><p>Average Notes</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric'><h1>{max_notes}</h1><p>Highest Notes</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric'><h1>{best_hour}:00</h1><p>Best Posting Hour</p></div>", unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("## Business Problem")
        st.write("""
Tumblr creators often publish music recommendations, playlists, lyrics, and reactions without knowing:

- Best time to post  
- Ideal caption style  
- Best number of tags  
- What emotional tone works  
- How to improve growth consistently
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("## Delivered Solution")
        st.write("""
This platform converts historical Tumblr data into creator intelligence through:

- Visual analytics dashboard  
- Predictive machine learning model  
- Strategic post simulator  
- Growth recommendations engine  
- Consulting-style summary
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# PAGE 2 DASHBOARD
# -----------------------------------
elif page == "Analytics Dashboard":

    st.title("Analytics Dashboard")
    st.write("Meaningful creator insights built from Tumblr indie music data.")

    c1,c2,c3,c4,c5 = st.columns(5)

    high_rate = round((df["high_engagement"].mean()*100),1)
    avg_words = round(df["word_count"].mean(),1)
    avg_tags = round(df["tag_count"].mean(),1)
    avg_sent = round(df["polarity"].mean(),2)

    cards = [
        (high_rate,"% High Engagement"),
        (avg_words,"Avg Words"),
        (avg_tags,"Avg Tags"),
        (f"{best_hour}:00","Best Hour"),
        (avg_sent,"Avg Sentiment")
    ]

    for col,val in zip([c1,c2,c3,c4,c5],cards):
        with col:
            st.markdown(f"<div class='metric'><h1>{val[0]}</h1><p>{val[1]}</p></div>", unsafe_allow_html=True)

    # chart 1
    a,b = st.columns(2)

    with a:
        x = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(x, x="hour", y="note_count",
                     title="Which Posting Hour Gets More Notes?",
                     color="note_count",
                     color_continuous_scale="Teal")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Higher bars = stronger historical posting hours.")

    with b:
        bins = pd.cut(df["tag_count"], bins=[0,3,6,10,15,100],
                      labels=["0-3","4-6","7-10","11-15","16+"])
        temp = df.groupby(bins)["high_engagement"].mean().reset_index()
        temp["high_engagement"]*=100
        fig = px.line(temp, x="tag_count", y="high_engagement",
                      markers=True,
                      title="How Many Tags Should Creators Use?")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Shows which tag range has highest engagement chance.")

    c,d = st.columns(2)

    with c:
        temp = df.groupby("high_engagement")["word_count"].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(temp, x="Class", y="word_count",
                     title="Caption Length vs Success",
                     color="Class")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Compares average caption length.")

    with d:
        temp = df.groupby("high_engagement")[["polarity","subjectivity"]].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        melted = temp.melt(id_vars="Class")
        fig = px.bar(melted, x="Class", y="value", color="variable",
                     barmode="group",
                     title="Emotion vs Engagement")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Measures positivity + emotional opinion level.")

# -----------------------------------
# PAGE 3 SIMULATOR
# -----------------------------------
elif page == "Strategic Post Simulator":

    st.title("Strategic Post Simulator")
    st.write("Predict post performance before publishing.")

    col1,col2 = st.columns([1.2,1])

    with col1:
        caption = st.text_area("Caption", height=220,
        placeholder="Example: this song completely changed my week...")
        tags = st.text_input("Tags", "indie music, shoegaze, bedroom pop")
        hour = st.slider("Posting Hour",0,23,19)

        if st.button("Analyze Post"):

            words = len(caption.split())
            tag_count = len(tags.split(","))
            sentiment = TextBlob(caption).sentiment

            sample = pd.DataFrame([{
                "text_length":len(caption),
                "word_count":words,
                "tag_count":tag_count,
                "polarity":sentiment.polarity,
                "subjectivity":sentiment.subjectivity,
                "hour":hour
            }])

            proba = model.predict_proba(sample)[0][1]*100

            st.success(f"Predicted Engagement Score: {round(proba,1)}%")

            if tag_count < 5:
                st.warning("Use more tags (5-15 recommended).")
            if words < 20:
                st.warning("Add storytelling or context.")
            if hour == best_hour:
                st.info("Great timing choice based on data.")

    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("## How the Simulator Works")
        st.write("""
The trained machine learning model evaluates:

- Caption length  
- Word count  
- Number of tags  
- Sentiment positivity  
- Emotional tone  
- Posting hour  

It compares your input to historical Tumblr patterns and estimates likely engagement.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# PAGE 4 PLAYBOOK
# -----------------------------------
elif page == "Growth Playbook":

    st.title("Growth Playbook")
    st.write("Practical recommendations creators can directly follow.")

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("## Recommended Creator Strategy")

    st.markdown(f"""
### 1. Caption Strategy
Use reactions, stories, opinions, nostalgia, or personal meaning.

**Example:**  
“This track feels like walking home at midnight after a long week.”

### 2. Tag Strategy
Use around **{round(df['tag_count'].mean())} to 15 tags**

Mix broad + niche:

indie music, shoegaze, dream pop, playlist, new music

### 3. Best Posting Time
Strongest historical hour in dataset: **{best_hour}:00**

### 4. Ideal Caption Length
Use **40–120 words** with emotion and context.

### 5. Weekly Growth Routine
- Test 2 posting hours  
- Rotate tags  
- Track best captions  
- Repeat winners
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# PAGE 5 SUMMARY
# -----------------------------------
elif page == "Consulting Summary":

    st.title("Consulting Summary")

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    st.markdown("""
## Project Overview
This project follows a creator-facing analytics strategy model for Tumblr indie music creators.

## Business Problem
Creators often lack clear insight into why some posts succeed while others underperform.

## Solution Delivered
The Tumblr Growth Intelligence Platform combines:

- Historical analytics dashboards  
- Predictive machine learning  
- Pre-post publishing simulator  
- Growth strategy playbook

## Technical Methods Used

- Feature engineering  
- Sentiment analysis  
- Random Forest model  
- Dashboard storytelling  
- Behavioral content analytics

## Key Findings

- Best posting hour identified  
- Better tag counts improve visibility  
- Emotional captions slightly outperform neutral posts  
- Structured testing can improve creator growth

## Business Value

This transforms guessing into data-driven content planning.

## Final Recommendation

Use the simulator before posting, test top time windows, and build repeatable creator strategy.
    """)

    st.markdown("</div>", unsafe_allow_html=True)
