# ==============================
# FINAL CLEAN PREMIUM app.py
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# CSS (NO BROKEN HTML CONTENT)
# --------------------------------
st.markdown("""
<style>
.stApp{
background:
radial-gradient(circle at top left, rgba(0,183,181,.20), transparent 25%),
radial-gradient(circle at bottom right, rgba(124,58,237,.22), transparent 35%),
linear-gradient(135deg,#020617 0%,#071426 50%,#171036 100%);
color:white;
}

.block-container{
padding-top:2rem;
padding-left:2rem;
padding-right:2rem;
max-width:1450px;
}

section[data-testid="stSidebar"]{
background:rgba(0,0,0,.45);
border-right:1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] *{
color:white !important;
}

.page-title{
font-size:42px;
font-weight:900;
line-height:1.1;
margin-bottom:8px;
}

.page-sub{
font-size:18px;
color:#d7f8ff;
margin-bottom:25px;
}

.card{
background:rgba(255,255,255,.06);
border:1px solid rgba(0,183,181,.25);
border-radius:18px;
padding:22px;
box-shadow:0 12px 28px rgba(0,0,0,.20);
margin-bottom:18px;
}

.card h3{
margin-top:0;
color:#67e8f9;
font-size:24px;
}

.tip{
background:rgba(103,232,249,.12);
border-left:5px solid #67e8f9;
border-radius:14px;
padding:16px;
margin-top:10px;
margin-bottom:18px;
}

div[data-testid="stMetric"]{
background:rgba(255,255,255,.07);
border-radius:18px;
padding:16px;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 10px 24px rgba(0,0,0,.18);
}

div[data-testid="stMetricValue"]{
font-size:2rem !important;
font-weight:900 !important;
}

.stButton button{
background:linear-gradient(90deg,#00b7b5,#7c3aed);
color:white;
border:none;
border-radius:12px;
padding:10px 24px;
font-weight:800;
}

.stButton button:hover{
transform:translateY(-2px);
}

.js-plotly-plot{
background:rgba(255,255,255,.05);
border-radius:18px;
padding:8px;
border:1px solid rgba(255,255,255,.06);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOAD FILES
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# --------------------------------
# HELPERS
# --------------------------------
def header(title, subtitle):
    st.markdown(f"<div class='page-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-sub'>{subtitle}</div>", unsafe_allow_html=True)

def card(title):
    st.markdown(f"<div class='card'><h3>{title}</h3>", unsafe_allow_html=True)

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)

def tip(text):
    st.markdown(f"<div class='tip'>{text}</div>", unsafe_allow_html=True)

def tags_count(x):
    return len([i.strip() for i in str(x).split(",") if i.strip()])

def create_features(text, tags, hour):
    blob = TextBlob(text)
    wc = len(text.split())
    tc = tags_count(tags)

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

def style_fig(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=35,r=25,t=60,b=35),
        height=430
    )
    return fig

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.title("Tumblr Growth Intelligence")
st.sidebar.caption("Creator Analytics Platform")

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

# =====================================================
# PAGE 1
# =====================================================
if page == "Executive Overview":

    header(
        "Tumblr Growth Intelligence Platform",
        "AI-powered analytics platform for Tumblr indie music creators."
    )

    st.info("This platform helps creators understand engagement, improve captions, optimize posting time, strengthen tag strategy, and grow audience reach.")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Posts Analyzed", f"{len(df):,}")
    c2.metric("Average Notes", round(df["note_count"].mean(),2))
    c3.metric("Highest Notes", int(df["note_count"].max()))
    c4.metric("Best Posting Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")

    st.write("")
    left,right = st.columns(2)

    with left:
        card("Business Problem")
        st.markdown("""
Creators often publish music content without knowing:

- Best time to post  
- Ideal caption length  
- How many tags to use  
- What emotional tone works best  
- How to grow consistently
""")
        end_card()

    with right:
        card("Delivered Solution")
        st.markdown("""
This platform provides:

- Historical analytics dashboard  
- Engagement prediction engine  
- Caption optimization simulator  
- Growth playbook recommendations  
- Business-focused consulting summary
""")
        end_card()

# =====================================================
# PAGE 2
# =====================================================
elif page == "Analytics Dashboard":

    header("Analytics Dashboard","Meaningful insights explaining what drives Tumblr engagement.")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("High Engagement Rate", f"{round(df['high_engagement'].mean()*100,1)}%")
    c2.metric("Avg Words", round(df["word_count"].mean(),0))
    c3.metric("Avg Tags", round(df["tag_count"].mean(),0))
    c4.metric("Best Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")
    c5.metric("Avg Sentiment", round(df["polarity"].mean(),2))

    a,b = st.columns(2)

    with a:
        temp=df.groupby("hour")["note_count"].mean().reset_index()
        fig=px.bar(temp,x="hour",y="note_count",title="Average Notes by Posting Hour",
        color="note_count",color_continuous_scale=["#003b46","#00b7b5","#67e8f9"])
        st.plotly_chart(style_fig(fig),use_container_width=True)
        tip("This graph shows the average notes by posting hour. Taller bars = stronger time slots.")

    with b:
        tg=df.groupby("tag_count")["high_engagement"].mean().reset_index()
        tg["high_engagement"]=tg["high_engagement"]*100
        fig=px.line(tg,x="tag_count",y="high_engagement",markers=True,
        title="Tags Used vs Engagement")
        st.plotly_chart(style_fig(fig),use_container_width=True)
        tip("Using more relevant tags usually improves visibility.")

# =====================================================
# PAGE 3
# =====================================================
elif page == "Strategic Post Simulator":

    header(
        "Strategic Post Simulator",
        "Predict post performance before publishing and receive practical improvement tips."
    )

    l,r = st.columns([1.2,1])

    with l:
        caption=st.text_area("Caption",height=220,placeholder="Example: this song changed my week...")
        tags=st.text_input("Tags","indie music, shoegaze, bedroom pop, new music")
        hour=st.slider("Posting Hour",0,23,19)
        run=st.button("Analyze Post")

    with r:
        card("How the Simulator Works")
        st.markdown("""
The simulator evaluates:

- Caption length  
- Word count  
- Number of tags  
- Emotional tone  
- Posting hour  
- Historical patterns
""")
        end_card()

    if run:
        X=create_features(caption,tags,hour)
        prob=model.predict_proba(X)[0][1]

        a,b,c=st.columns(3)
        a.metric("Success Probability",f"{prob:.0%}")
        b.metric("Words",len(caption.split()))
        c.metric("Tags",tags_count(tags))

        fig=go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob*100,
            number={'suffix':'%'},
            title={'text':'Engagement Score'},
            gauge={'axis':{'range':[0,100]}}
        ))
        st.plotly_chart(style_fig(fig),use_container_width=True)

# =====================================================
# PAGE 4
# =====================================================
elif page == "Growth Playbook":

    header("Growth Playbook","Practical, non-technical recommendations creators can directly follow.")

    best_hour=int(df.groupby("hour")["note_count"].mean().idxmax())
    ideal_words=round(df[df["high_engagement"]==1]["word_count"].mean(),0)
    ideal_tags=round(df[df["high_engagement"]==1]["tag_count"].mean(),0)

    card("Recommended Creator Strategy")

    st.markdown(f"""
### 1. Caption Strategy
Do not only post a link. Add emotional reactions or short stories.

### 2. Tag Strategy
Use around **{ideal_tags}** tags.

Suggested tags: indie music, new music, playlist, shoegaze, bedroom pop

### 3. Best Posting Time
Strongest posting hour is **{best_hour}:00**

### 4. Ideal Caption Length
High-performing posts average **{ideal_words} words**

### 5. Weekly Growth Routine
Post 3–5 times weekly and track results.
""")
    end_card()

# =====================================================
# PAGE 5
# =====================================================
elif page == "Consulting Summary":

    header("Consulting Summary","Business-facing summary of platform value and impact.")

    card("Project Overview")
    st.markdown("""
This project follows Track 2: User / Influencer / Brand-Facing Analytics.

Client focus: Tumblr indie music creator community.

Final solution helps creators improve traffic, engagement, and audience growth.
""")
    end_card()

    card("Business Problem")
    st.markdown("""
Creators lacked visibility into why some posts receive more notes than others.
""")
    end_card()

    card("Solution Delivered")
    st.markdown("""
- Analytics Dashboard  
- Strategic Post Simulator  
- Growth Playbook  
- Consulting Summary
""")
    end_card()

    card("Business Value")
    st.markdown("""
- Better posting decisions  
- Stronger reach  
- Repeatable audience growth  
- Faster learning cycle
""")
    end_card()
