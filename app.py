# ==========================================================
# FULL UPDATED app.py
# Better Storytelling Graphs + Graph Explanation Page
# Better Growth Playbook (real tips)
# Keep everything else same
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
# STYLE
# ==================================================
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

.hero{
background:linear-gradient(135deg,#003b46,#008c9e,#00b8c8);
padding:35px;
border-radius:22px;
color:white;
box-shadow:0 12px 25px rgba(0,0,0,.15);
}

.card{
background:white;
padding:24px;
border-radius:18px;
box-shadow:0 10px 24px rgba(0,0,0,.08);
}

.kpi{
background:linear-gradient(135deg,#003b46,#008c9e);
padding:18px;
border-radius:16px;
text-align:center;
color:white;
}

.kpi h1{
margin:0;
font-size:34px;
}

.kpi p{
margin:0;
font-size:14px;
}

.big{
font-size:42px;
font-weight:800;
color:#003b46;
}

.sub{
color:#5f6b73;
font-size:16px;
margin-bottom:18px;
}

.stButton button{
background:#008c9e;
color:white;
border:none;
font-weight:700;
border-radius:10px;
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
    st.markdown("<div class='sub'>Meaningful graphs showing what really drives Tumblr engagement.</div>", unsafe_allow_html=True)

    # KPIs
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

    # Graph 1 Real Story = Top performing hours
    a,b = st.columns(2)

    with a:
        temp = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(
            temp,
            x="hour",
            y="note_count",
            title="Average Notes by Posting Hour",
            color="note_count",
            color_continuous_scale="Teal"
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig,use_container_width=True)

    with b:
        temp = df.groupby("high_engagement")["word_count"].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(
            temp,
            x="Class",
            y="word_count",
            title="Average Caption Length: Low vs High Success",
            color="Class",
            color_discrete_sequence=["#003b46","#00b8c8"]
        )
        fig.update_layout(template="plotly_white",showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

    c,d = st.columns(2)

    with c:
        temp = df.groupby("high_engagement")["tag_count"].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(
            temp,
            x="Class",
            y="tag_count",
            title="Average Tags Used: Low vs High Success",
            color="Class",
            color_discrete_sequence=["#005f6b","#00b8c8"]
        )
        fig.update_layout(template="plotly_white",showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

    with d:
        temp = df.groupby("high_engagement")[["polarity","subjectivity"]].mean().reset_index()
        temp["Class"] = temp["high_engagement"].map({0:"Low",1:"High"})
        fig = px.bar(
            temp,
            x="Class",
            y=["polarity","subjectivity"],
            barmode="group",
            title="Emotion Level in Successful Posts",
            color_discrete_sequence=["#003b46","#00b8c8"]
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig,use_container_width=True)

# ==================================================
# GRAPH EXPLANATION PAGE
# ==================================================
elif page == "Graph Insights Guide":

    st.markdown("<div class='big'>Graph Insights Guide</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Simple explanation for non-technical audience.</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h3>1. Average Notes by Posting Hour</h3>
    <b>X-axis:</b> Hour of day (0 to 23)<br>
    <b>Y-axis:</b> Average notes received<br><br>

    <b>Meaning:</b> Shows best time to publish posts.  
    Higher bar = better engagement.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class='card'>
    <h3>2. Caption Length vs Success</h3>
    <b>X-axis:</b> Low vs High performing posts<br>
    <b>Y-axis:</b> Average words used<br><br>

    <b>Meaning:</b> Helps understand ideal caption length.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class='card'>
    <h3>3. Tags Used vs Success</h3>
    <b>X-axis:</b> Low vs High posts<br>
    <b>Y-axis:</b> Number of tags used<br><br>

    <b>Meaning:</b> Shows whether using more tags helps visibility.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class='card'>
    <h3>4. Emotion Level in Successful Posts</h3>
    <b>Polarity:</b> Positive / Negative tone<br>
    <b>Subjectivity:</b> Personal feeling / opinion level<br><br>

    <b>Meaning:</b> Shows emotional writing impact on engagement.
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# SIMULATOR
# ==================================================
elif page == "Strategic Post Simulator":

    st.markdown("<div class='big'>Strategic Post Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Predict performance before publishing.</div>", unsafe_allow_html=True)

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

        st.info("""
How it works:

• Reads your caption length  
• Counts tags  
• Measures sentiment  
• Checks posting hour  
• Uses trained ML model  
• Predicts probability of high engagement
""")

# ==================================================
# PLAYBOOK
# ==================================================
elif page == "Growth Playbook":

    st.markdown("<div class='big'>Growth Playbook</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Practical actions creators should follow.</div>", unsafe_allow_html=True)

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())

    st.markdown(f"""
    <div class='card'>
    <h2>Best Growth Tips</h2>

    • <b>Best Time to Post:</b> {best_hour}:00 based on dataset performance<br><br>

    • <b>Ideal Caption Style:</b> Personal, emotional, storytelling captions perform better.<br><br>

    • <b>Ideal Caption Length:</b> Around {round(df[df['high_engagement']==1]['word_count'].mean(),0)} words.<br><br>

    • <b>Best Tag Count:</b> Use around {round(df[df['high_engagement']==1]['tag_count'].mean(),0)} tags.<br><br>

    • <b>Suggested Tags:</b> indie music, new music, indie rock, shoegaze, bedroom pop.<br><br>

    • <b>Growth Strategy:</b> Post consistently 3-5 times weekly and track results.
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
    Creators lacked visibility into what drives engagement.

    <h2>Solution</h2>
    Analytics dashboard + prediction engine + strategy system.

    <h2>Business Value</h2>
    Better posts, stronger reach, repeatable audience growth.

    <h2>Presentation Tip</h2>
    Use simulator live to impress professor.
    </div>
    """, unsafe_allow_html=True)
