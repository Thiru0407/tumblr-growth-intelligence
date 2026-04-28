import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# ---------------------------------------------------
# PREMIUM UI CSS
# ---------------------------------------------------
st.markdown("""
<style>

.stApp{
background:
radial-gradient(circle at top left, rgba(0,183,181,0.28), transparent 35%),
radial-gradient(circle at bottom right, rgba(124,58,237,0.22), transparent 35%),
linear-gradient(135deg,#020617 0%,#0f172a 45%,#111827 100%);
color:white;
}

.block-container{
max-width:1450px;
padding-top:2rem;
padding-bottom:4rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
background:rgba(2,6,23,0.82);
border-right:1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] *{
color:white !important;
}

/* TITLES */
h1{
font-size:58px !important;
font-weight:900 !important;
margin-bottom:8px !important;
color:#ffffff !important;
}

h2{
font-size:36px !important;
font-weight:850 !important;
margin-top:8px !important;
color:#67e8f9 !important;
}

h3{
font-size:28px !important;
font-weight:800 !important;
color:#ffffff !important;
}

p,li,span,label{
font-size:18px !important;
line-height:1.8 !important;
color:#e6fbff !important;
}

/* KPI BOX */
div[data-testid="stMetric"]{
background:rgba(255,255,255,.06);
border:1px solid rgba(0,183,181,.25);
border-radius:22px;
padding:24px;
box-shadow:0 8px 25px rgba(0,0,0,.18);
}

div[data-testid="stMetricValue"]{
font-size:2.7rem !important;
font-weight:900 !important;
color:#67e8f9 !important;
}

div[data-testid="stMetricLabel"]{
font-size:16px !important;
}

/* PREMIUM CONTENT BOX */
.box{
background:rgba(255,255,255,.055);
border:1px solid rgba(103,232,249,.18);
border-radius:22px;
padding:28px;
margin-bottom:22px;
box-shadow:0 10px 28px rgba(0,0,0,.22);
backdrop-filter:blur(16px);
}

/* BUTTON */
.stButton button{
background:linear-gradient(90deg,#00b7b5,#7c3aed);
border:none;
color:white;
font-weight:800;
border-radius:14px;
padding:12px 24px;
font-size:17px;
}

.stButton button:hover{
transform:translateY(-1px);
}

/* Inputs */
textarea,input{
background:rgba(255,255,255,.08) !important;
color:white !important;
border-radius:14px !important;
}

/* Dataframe */
div[data-testid="stDataFrame"]{
background:rgba(255,255,255,.05);
border-radius:18px;
padding:8px;
}

/* Charts */
.js-plotly-plot{
background:rgba(255,255,255,.04);
border-radius:20px;
padding:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def premium_box(title, content):
    st.markdown(
        f"""
        <div class="box">
            <h3>{title}</h3>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

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

def dark_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5faff"),
        title_font=dict(size=26, color="#67e8f9"),
        height=460
    )
    return fig

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("Tumblr Growth Intelligence")
st.sidebar.caption("Glassmorphism Creator Analytics Platform")

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

# ---------------------------------------------------
# PAGE 1
# ---------------------------------------------------
if page == "Executive Overview":

    st.title("Tumblr Growth Intelligence Platform")
    st.subheader("AI-powered analytics platform for Tumblr indie music creators.")

    st.info(
        "This platform helps creators understand engagement, improve captions, optimize posting time, strengthen tag strategy, and grow audience reach."
    )

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Posts Analyzed", f"{len(df):,}")
    c2.metric("Average Notes", round(df["note_count"].mean(),2))
    c3.metric("Highest Notes", int(df["note_count"].max()))
    c4.metric("Best Posting Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")

    st.markdown("---")

    left,right = st.columns(2)

    with left:
        premium_box("Business Problem", """
        Creators often publish music content without knowing:
        <ul>
        <li>Best time to post</li>
        <li>Ideal caption length</li>
        <li>How many tags to use</li>
        <li>What emotional tone works best</li>
        <li>How to grow consistently</li>
        </ul>
        """)

    with right:
        premium_box("Delivered Solution", """
        This platform provides:
        <ul>
        <li>Historical analytics dashboard</li>
        <li>Engagement prediction engine</li>
        <li>Caption optimization simulator</li>
        <li>Growth playbook recommendations</li>
        <li>Business-focused consulting summary</li>
        </ul>
        """)

# ---------------------------------------------------
# PAGE 2
# ---------------------------------------------------
elif page == "Analytics Dashboard":

    st.title("Analytics Dashboard")
    st.caption("Meaningful insights explaining what drives Tumblr engagement.")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("High Engagement Rate", f"{round(df['high_engagement'].mean()*100,1)}%")
    c2.metric("Avg Words", round(df["word_count"].mean(),0))
    c3.metric("Avg Tags", round(df["tag_count"].mean(),0))
    c4.metric("Best Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")
    c5.metric("Avg Sentiment", round(df["polarity"].mean(),2))

    a,b = st.columns(2)

    with a:
        temp = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(temp, x="hour", y="note_count", title="Average Notes by Posting Hour",
                     color="note_count",
                     color_continuous_scale=["#003b46","#00b7b5","#67e8f9"])
        st.plotly_chart(dark_chart(fig), use_container_width=True)

        premium_box("What this tells us",
        "Top-performing posting hours historically generate more notes. Test strong time windows first.")

    with b:
        bucket = pd.cut(df["tag_count"],
                        bins=[0,3,6,10,15,100],
                        labels=["0-3","4-6","7-10","11-15","16+"],
                        include_lowest=True)

        temp = df.groupby(bucket)["high_engagement"].mean().reset_index()
        temp.columns=["Tags","High Engagement"]
        temp["High Engagement"]*=100

        fig = px.line(temp, x="Tags", y="High Engagement",
                      title="How Many Tags Should Creators Use?",
                      markers=True)
        fig.update_traces(line=dict(width=5))
        st.plotly_chart(dark_chart(fig), use_container_width=True)

        premium_box("What this tells us",
        "Balanced tag strategy improves discoverability. Too few tags usually underperform.")

# ---------------------------------------------------
# PAGE 3
# ---------------------------------------------------
elif page == "Strategic Post Simulator":

    st.title("Strategic Post Simulator")
    st.caption("Predict post performance before publishing and receive practical improvement tips.")

    left,right = st.columns([1.2,1])

    with left:
        caption = st.text_area("Caption", height=220,
        placeholder="Example: this song completely changed my week...")

        tags = st.text_input("Tags",
        value="indie music, shoegaze, bedroom pop, new music")

        hour = st.slider("Posting Hour",0,23,19)

        run = st.button("Analyze Post")

    with right:
        premium_box("How the Simulator Works", """
        The simulator estimates whether a Tumblr post has high engagement potential.

        <ul>
        <li>Caption length</li>
        <li>Word count</li>
        <li>Number of tags</li>
        <li>Sentiment polarity</li>
        <li>Subjectivity / personal tone</li>
        <li>Posting hour</li>
        <li>Tag-to-text balance</li>
        </ul>

        The output is a decision-support score based on historical posting patterns.
        """)

    if run:
        if caption.strip()=="":
            st.warning("Please enter a caption first.")
        else:
            X = create_features(caption,tags,hour)
            prob = model.predict_proba(X)[0][1]

            c1,c2,c3 = st.columns(3)
            c1.metric("Success Probability", f"{prob:.0%}")
            c2.metric("Words", len(caption.split()))
            c3.metric("Tags", len(split_tags(tags)))

# ---------------------------------------------------
# PAGE 4
# ---------------------------------------------------
elif page == "Growth Playbook":

    st.title("Growth Playbook")
    st.caption("Practical recommendations creators can directly follow.")

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())
    ideal_words = round(df[df["high_engagement"]==1]["word_count"].mean(),0)
    ideal_tags = round(df[df["high_engagement"]==1]["tag_count"].mean(),0)

    premium_box("Recommended Creator Strategy", f"""
    <b>1. Caption Strategy</b><br>
    Add emotion, story, or reaction instead of only posting a link.<br><br>

    <b>2. Tag Strategy</b><br>
    Use around {ideal_tags} focused tags.<br><br>

    <b>3. Best Posting Time</b><br>
    Test around {best_hour}:00 first.<br><br>

    <b>4. Ideal Caption Length</b><br>
    Strong posts average around {ideal_words} words.<br><br>

    <b>5. Weekly Growth Routine</b><br>
    Post 3–5 times weekly and track performance.
    """)

# ---------------------------------------------------
# PAGE 5
# ---------------------------------------------------
elif page == "Consulting Summary":

    st.title("Consulting Summary")

    premium_box("Project Overview",
    "Track 2 User / Influencer / Brand-Facing Analytics focused on Tumblr indie music creators.")

    premium_box("Business Problem",
    "Creators often lack visibility into why some posts outperform others.")

    premium_box("Solution Delivered", """
    <ul>
    <li>Analytics Dashboard</li>
    <li>Strategic Post Simulator</li>
    <li>Growth Playbook</li>
    <li>Consulting Summary</li>
    </ul>
    """)

    premium_box("Technical Methods Used", """
    <ul>
    <li>Feature engineering</li>
    <li>EDA</li>
    <li>Classification logic</li>
    <li>Plotly dashboards</li>
    <li>Recommendation framework</li>
    </ul>
    """)

    premium_box("Business Value Created", """
    <ul>
    <li>Better content decisions</li>
    <li>Faster learning cycles</li>
    <li>Improved discoverability</li>
    <li>More consistent growth</li>
    <li>Stronger creator confidence</li>
    </ul>
    """)
