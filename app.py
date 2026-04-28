import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    page_icon="📈",
    layout="wide"
)

# ---------- LOAD ----------
@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# ---------- GLASSMORPHISM UI ----------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(0,183,181,0.35), transparent 35%),
        radial-gradient(circle at bottom right, rgba(124,58,237,0.30), transparent 35%),
        linear-gradient(135deg, #020617 0%, #0f172a 50%, #111827 100%);
    color: #e5faff;
}

section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.75);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(0, 183, 181, 0.25);
}

section[data-testid="stSidebar"] * {
    color: #e5faff !important;
}

.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

h1, h2, h3 {
    color: #e5faff !important;
    font-weight: 800 !important;
}

p, li, label, span {
    color: #d9faff !important;
    font-size: 17px;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(0, 183, 181, 0.35);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 0 25px rgba(0, 183, 181, 0.15);
    backdrop-filter: blur(18px);
}

div[data-testid="stMetricValue"] {
    color: #67e8f9 !important;
    font-size: 2.4rem !important;
    font-weight: 900 !important;
}

div[data-testid="stMetricLabel"] {
    color: #c7f9ff !important;
}

.stAlert {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(0,183,181,0.35);
    border-radius: 18px;
    backdrop-filter: blur(18px);
}

.stButton > button {
    background: linear-gradient(90deg, #00b7b5, #7c3aed);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 12px 26px;
    font-size: 17px;
    font-weight: 800;
    box-shadow: 0 0 20px rgba(0,183,181,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(124,58,237,0.45);
}

textarea, input {
    background: rgba(255,255,255,0.10) !important;
    color: #e5faff !important;
    border-radius: 14px !important;
}

div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 12px;
    border: 1px solid rgba(0,183,181,0.25);
}

.js-plotly-plot {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 20px;
    padding: 10px;
    border: 1px solid rgba(0,183,181,0.25);
    box-shadow: 0 0 24px rgba(0,183,181,0.10);
}
</style>
""", unsafe_allow_html=True)

# ---------- HELPERS ----------
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
        title_font=dict(color="#67e8f9", size=20),
        height=450
    )
    return fig

# ---------- SIDEBAR ----------
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

# ---------- EXECUTIVE OVERVIEW ----------
if page == "Executive Overview":

    st.title("Tumblr Growth Intelligence Platform")
    st.subheader("AI-powered analytics platform for Tumblr indie music creators.")

    st.info(
        "This platform helps creators understand engagement, improve captions, "
        "optimize posting time, strengthen tag strategy, and grow audience reach."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Posts Analyzed", f"{len(df):,}")
    c2.metric("Average Notes", round(df["note_count"].mean(), 2))
    c3.metric("Highest Notes", int(df["note_count"].max()))
    c4.metric("Best Posting Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Business Problem")
        st.write("Creators often publish music content without knowing:")
        st.markdown("""
- Best time to post  
- Ideal caption length  
- How many tags to use  
- What emotional tone works best  
- How to grow consistently
""")

    with col2:
        st.header("Delivered Solution")
        st.write("This platform provides:")
        st.markdown("""
- Historical analytics dashboard  
- Engagement prediction engine  
- Caption optimization simulator  
- Growth playbook recommendations  
- Business-focused consulting summary
""")

# ---------- DASHBOARD ----------
elif page == "Analytics Dashboard":

    st.title("Analytics Dashboard")
    st.caption("Meaningful insights explaining what drives Tumblr engagement.")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("High Engagement Rate", f"{round(df['high_engagement'].mean()*100,1)}%")
    c2.metric("Avg Words", round(df["word_count"].mean(), 0))
    c3.metric("Avg Tags", round(df["tag_count"].mean(), 0))
    c4.metric("Best Hour", f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00")
    c5.metric("Avg Sentiment", round(df["polarity"].mean(), 2))

    st.write("")

    a, b = st.columns(2)

    with a:
        temp = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(
            temp,
            x="hour",
            y="note_count",
            title="Average Notes by Posting Hour",
            color="note_count",
            color_continuous_scale=["#003b46", "#00b7b5", "#67e8f9"]
        )
        st.plotly_chart(dark_chart(fig), use_container_width=True)

        st.success("""
**What this tells us:**  
This graph shows the average number of notes by posting hour.  
The taller the bar, the stronger that hour performed historically.  
Creators should test top-performing hours first.
""")

    with b:
        tag_bucket = pd.cut(
            df["tag_count"],
            bins=[0, 3, 6, 10, 15, 100],
            labels=["0-3", "4-6", "7-10", "11-15", "16+"],
            include_lowest=True
        )
        temp = df.groupby(tag_bucket)["high_engagement"].mean().reset_index()
        temp.columns = ["Tags Used", "High Engagement Rate"]
        temp["High Engagement Rate"] *= 100

        fig = px.line(
            temp,
            x="Tags Used",
            y="High Engagement Rate",
            markers=True,
            title="How Many Tags Should Creators Use?",
            color_discrete_sequence=["#67e8f9"]
        )
        fig.update_traces(line=dict(width=5), marker=dict(size=12))
        st.plotly_chart(dark_chart(fig), use_container_width=True)

        st.success("""
**What this tells us:**  
Posts with too few tags underperform.  
Balanced tag usage increases discoverability.  
Very high tag usage can work if highly relevant.
""")

    c, d = st.columns(2)

    with c:
        caption_bucket = pd.cut(
            df["word_count"],
            bins=[0, 25, 50, 100, 200, 2000],
            labels=["0-25", "26-50", "51-100", "101-200", "200+"],
            include_lowest=True
        )
        temp = df.groupby(caption_bucket)["high_engagement"].mean().reset_index()
        temp.columns = ["Caption Length", "High Engagement Rate"]
        temp["High Engagement Rate"] *= 100

        fig = px.area(
            temp,
            x="Caption Length",
            y="High Engagement Rate",
            title="Does Caption Length Improve Engagement?",
            color_discrete_sequence=["#00b7b5"]
        )
        st.plotly_chart(dark_chart(fig), use_container_width=True)

        st.success("""
**What this tells us:**  
Medium-length captions tend to perform strongest.  
Too short feels empty.  
Too long may reduce reading completion.
""")

    with d:
        if "cluster_label" in df.columns:
            temp = df.groupby("cluster_label").agg(
                Posts=("note_count", "count"),
                Average_Notes=("note_count", "mean")
            ).reset_index()

            fig = px.scatter(
                temp,
                x="Posts",
                y="Average_Notes",
                size="Posts",
                color="cluster_label",
                title="Which Content Style Performs Best?",
                color_discrete_sequence=["#67e8f9", "#00b7b5", "#7c3aed", "#f472b6"]
            )
            st.plotly_chart(dark_chart(fig), use_container_width=True)

            st.success("""
**What this tells us:**  
Each bubble is a content style group.  
Bigger bubbles mean more posts.  
Higher bubbles mean stronger average engagement.
""")

# ---------- SIMULATOR ----------
elif page == "Strategic Post Simulator":

    st.title("Strategic Post Simulator")
    st.caption("Predict post performance before publishing and receive practical improvement tips.")

    left, right = st.columns([1.2, 1])

    with left:
        caption = st.text_area(
            "Caption",
            height=220,
            placeholder="Example: this song completely changed my week..."
        )

        tags = st.text_input(
            "Tags",
            value="indie music, shoegaze, bedroom pop, new music"
        )

        hour = st.slider("Posting Hour", 0, 23, 19)

        run = st.button("Analyze Post")

    with right:
        st.subheader("How the Simulator Works")
        st.write("The simulator estimates whether a Tumblr post has high engagement potential.")
        st.markdown("""
It evaluates:

- Caption length  
- Word count  
- Number of tags  
- Sentiment polarity  
- Subjectivity / personal tone  
- Posting hour  
- Tag-to-text balance
""")
        st.write(
            "The output is not a guarantee of virality. "
            "It is a decision-support score based on historical posting patterns."
        )

    if run:
        if caption.strip() == "":
            st.warning("Please enter a caption first.")
        else:
            X = create_features(caption, tags, hour)
            prob = model.predict_proba(X)[0][1]

            c1, c2, c3 = st.columns(3)
            c1.metric("Success Probability", f"{prob:.0%}")
            c2.metric("Words", len(caption.split()))
            c3.metric("Tags", len(split_tags(tags)))

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                number={"suffix": "%"},
                title={"text": "Engagement Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#67e8f9"},
                    "steps": [
                        {"range": [0, 50], "color": "rgba(255,255,255,0.12)"},
                        {"range": [50, 75], "color": "rgba(0,183,181,0.35)"},
                        {"range": [75, 100], "color": "rgba(103,232,249,0.55)"}
                    ]
                }
            ))
            st.plotly_chart(dark_chart(fig), use_container_width=True)

            st.subheader("Recommendations")
            if len(caption.split()) < 50:
                st.write("- Add more storytelling or emotional context.")
            else:
                st.write("- Caption depth is strong.")

            if len(split_tags(tags)) < 5:
                st.write("- Add more relevant tags. Try 5–15 focused tags.")
            else:
                st.write("- Tag count is healthy.")

            if hour not in [3, 11, 13, 14, 23]:
                st.write("- Test stronger posting windows such as 3:00, 11:00, 13:00, 14:00, or 23:00.")
            else:
                st.write("- Posting hour aligns with stronger historical windows.")

# ---------- PLAYBOOK ----------
elif page == "Growth Playbook":

    st.title("Growth Playbook")
    st.caption("Practical, non-technical recommendations creators can directly follow.")

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())
    ideal_words = round(df[df["high_engagement"] == 1]["word_count"].mean(), 0)
    ideal_tags = round(df[df["high_engagement"] == 1]["tag_count"].mean(), 0)

    st.header("Recommended Creator Strategy")

    st.subheader("1. Caption Strategy")
    st.write(
        "Do not only post a link. Add a short emotional reaction, story, "
        "or reason why the song matters."
    )

    st.write("**Example caption:**")
    st.write(
        "This track feels like walking home at midnight after a long week. "
        "The vocals are soft, the guitar is dreamy, and I keep replaying it."
    )

    st.subheader("2. Tag Strategy")
    st.write(f"Use around {ideal_tags} tags. Mix broad discovery tags with niche music tags.")
    st.write(
        "**Suggested tags:** indie music, new music, indie rock, "
        "bedroom pop, shoegaze, sad songs, playlist, recommendation"
    )

    st.subheader("3. Best Posting Time")
    st.write(
        f"The strongest posting hour in this dataset is {best_hour}:00. "
        "Test this first, then compare with evening windows."
    )

    st.subheader("4. Ideal Caption Length")
    st.write(
        f"High-performing posts average around {ideal_words} words. "
        "Avoid captions that are too empty or generic."
    )

    st.subheader("5. Weekly Growth Routine")
    st.write(
        "Post 3–5 times per week, track notes, compare tags, "
        "test different hours, and reuse formats that perform well."
    )

    st.markdown("##")

    playbook = pd.DataFrame({
        "Growth Lever": ["Caption", "Tags", "Timing", "Emotion", "Consistency"],
        "What To Do": [
            "Use emotional reactions and short stories",
            "Use broad + niche tags together",
            f"Start testing around {best_hour}:00",
            "Write with personal opinion and feeling",
            "Post 3–5 times weekly and track results"
        ],
        "Why It Helps": [
            "Builds stronger audience connection",
            "Improves discoverability",
            "Increases visibility during strong hours",
            "Encourages replies and reblogs",
            "Creates repeatable growth learning"
        ]
    })

    st.dataframe(playbook, use_container_width=True)

# ---------- SUMMARY ----------
elif page == "Consulting Summary":

    st.title("Consulting Summary")

    st.header("Project Overview")
    st.write(
        "This project follows Track 2: User / Influencer / Brand-Facing Analytics. "
        "The selected client context is the Tumblr indie music creator community."
    )

    st.write(
        "The final solution is a creator-facing intelligence platform helping users improve traffic, "
        "engagement, and audience development."
    )

    st.header("Business Problem")
    st.write(
        "Tumblr creators produce highly creative content, but often lack analytics tools "
        "to understand why some posts receive more notes than others."
    )

    st.write(
        "This makes content planning difficult. Creators may not know whether captions, "
        "tags, emotional tone, or posting hours are helping growth."
    )

    st.header("Solution Delivered")
    st.markdown("""
- Analytics Dashboard: explains historical engagement patterns  
- Strategic Post Simulator: predicts engagement potential  
- Growth Playbook: converts insights into practical actions  
- Consulting Summary: links technical work to business value
""")

    st.header("Technical Methods Used")
    st.markdown("""
- Feature engineering from captions, tags, and posting time  
- Exploratory data analysis  
- Classification logic for engagement scoring  
- Visual dashboards with Plotly  
- Recommendation framework for creator decisions
""")

    st.header("Business Value Created")
    st.markdown("""
- Better content decisions  
- Faster learning cycles  
- Improved discoverability  
- More consistent audience growth  
- Stronger creator confidence
""")
