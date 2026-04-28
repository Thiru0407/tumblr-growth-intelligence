# ==========================================================
# PREMIUM NATIVE STREAMLIT VERSION
# Tumblr Growth Intelligence Platform
# Works SAME on Local + Streamlit Cloud
# ==========================================================

import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# ==========================================================
# STYLE
# ==========================================================
st.markdown("""
<style>
.stApp{
    background:#eef2f5;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#003b46,#005f6b,#008c9e);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

.block-container{
    padding-top:2rem;
    max-width:1400px;
}

div[data-testid="stMetric"]{
    background:white;
    padding:18px;
    border-radius:18px;
    box-shadow:0 8px 20px rgba(0,0,0,.08);
}

h1,h2,h3{
    color:#003b46;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HELPERS
# ==========================================================
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

# ==========================================================
# SIDEBAR
# ==========================================================
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

# ==========================================================
# EXECUTIVE OVERVIEW
# ==========================================================
if page == "Executive Overview":

    st.title("Tumblr Growth Intelligence Platform")
    st.caption("AI-powered analytics platform for Tumblr indie music creators.")

    st.info("""
This platform helps creators understand engagement, improve captions,
optimize posting time, strengthen tag strategy, and grow audience reach.
""")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Posts Analyzed", f"{len(df):,}")
    c2.metric("Average Notes", round(df["note_count"].mean(),2))
    c3.metric("Highest Notes", int(df["note_count"].max()))
    c4.metric("Best Posting Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")

    st.write("")

    a,b = st.columns(2)

    with a:
        st.subheader("Business Problem")
        st.write("""
Creators often publish music content without knowing:

- Best time to post  
- Ideal caption length  
- How many tags to use  
- What emotional tone works best  
- How to grow consistently
""")

    with b:
        st.subheader("Delivered Solution")
        st.write("""
This platform provides:

- Historical analytics dashboard  
- Engagement prediction engine  
- Caption optimization simulator  
- Growth playbook recommendations  
- Business-focused consulting summary
""")

# ==========================================================
# ANALYTICS DASHBOARD
# ==========================================================
elif page == "Analytics Dashboard":

    st.title("Analytics Dashboard")
    st.caption("Meaningful insights explaining what drives Tumblr engagement.")

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("High Engagement Rate", f"{round(df['high_engagement'].mean()*100,1)}%")
    c2.metric("Avg Words", round(df["word_count"].mean(),0))
    c3.metric("Avg Tags", round(df["tag_count"].mean(),0))
    c4.metric("Best Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")
    c5.metric("Avg Sentiment", round(df["polarity"].mean(),2))

    st.write("")

    a,b = st.columns(2)

    with a:
        temp = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(
            temp,x="hour",y="note_count",
            title="Average Notes by Posting Hour",
            color="note_count",
            color_continuous_scale="Teal"
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig,use_container_width=True)

    with b:
        temp = df.groupby("high_engagement")["word_count"].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(
            temp,x="Class",y="word_count",
            title="Caption Length vs Success",
            color="Class",
            color_discrete_sequence=["#003b46","#00b8c8"]
        )
        fig.update_layout(showlegend=False,height=450)
        st.plotly_chart(fig,use_container_width=True)

    c,d = st.columns(2)

    with c:
        temp = df.groupby("high_engagement")["tag_count"].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.line(
            temp,x="Class",y="tag_count",
            markers=True,
            title="Tags Used vs Success",
            color_discrete_sequence=["#008c9e"]
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig,use_container_width=True)

    with d:
        temp = df.groupby("high_engagement")[["polarity","subjectivity"]].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(
            temp,x="Class",y=["polarity","subjectivity"],
            barmode="group",
            title="Emotion Level in Successful Posts"
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig,use_container_width=True)

# ==========================================================
# SIMULATOR
# ==========================================================
elif page == "Strategic Post Simulator":

    st.title("Strategic Post Simulator")
    st.caption("Predict post performance before publishing.")

    a,b = st.columns([1.2,1])

    with a:
        text = st.text_area("Caption", height=220)
        tags = st.text_input("Tags")
        hour = st.slider("Posting Hour",0,23,19)

        run = st.button("Analyze Post")

    with b:
        st.subheader("How This Helps")
        st.write("""
This tool analyzes:

- Caption length  
- Number of tags  
- Emotional tone  
- Posting time  
- Historical engagement patterns

Then predicts engagement probability.
""")

    if run:

        X = create_features(text,tags,hour)
        prob = model.predict_proba(X)[0][1]

        c1,c2,c3 = st.columns(3)
        c1.metric("Success Probability", f"{prob:.0%}")
        c2.metric("Words", len(text.split()))
        c3.metric("Tags", len(split_tags(tags)))

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

# ==========================================================
# PLAYBOOK
# ==========================================================
elif page == "Growth Playbook":

    st.title("Growth Playbook")
    st.caption("Practical actions creators should follow.")

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())

    st.subheader("Best Growth Tips")

    st.write(f"""
**Best Time to Post:** {best_hour}:00 based on dataset performance  

**Ideal Caption Style:** Personal, emotional, storytelling captions perform better.  

**Ideal Caption Length:** Around {round(df[df['high_engagement']==1]['word_count'].mean(),0)} words.  

**Best Tag Count:** Use around {round(df[df['high_engagement']==1]['tag_count'].mean(),0)} tags.  

**Suggested Tags:** indie music, new music, indie rock, shoegaze, bedroom pop.  

**Growth Strategy:** Post consistently 3-5 times weekly and track results.
""")

# ==========================================================
# SUMMARY
# ==========================================================
elif page == "Consulting Summary":

    st.title("Consulting Summary")

    st.subheader("Client")
    st.write("Tumblr Indie Music Community")

    st.subheader("Problem")
    st.write("Creators lacked visibility into what drives engagement.")

    st.subheader("Solution")
    st.write("Analytics dashboard + prediction engine + strategy system.")

    st.subheader("Business Value")
    st.write("Better posts, stronger reach, repeatable audience growth.")

    st.subheader("Presentation Tip")
    st.write("Use simulator live during presentation to impress professor.")
