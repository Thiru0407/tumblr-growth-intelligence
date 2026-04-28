import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# FINAL CLEAN PREMIUM UI
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(0,183,181,0.22), transparent 28%),
        radial-gradient(circle at bottom right, rgba(124,58,237,0.25), transparent 34%),
        linear-gradient(135deg, #020817 0%, #071426 50%, #171036 100%);
    color: #eafcff;
}

.block-container {
    padding-top: 2rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.92);
    border-right: 1px solid rgba(0, 183, 181, 0.22);
}

section[data-testid="stSidebar"] * {
    color: #e5faff !important;
}

section[data-testid="stSidebar"] h1 {
    font-size: 25px !important;
    line-height: 1.2 !important;
    font-weight: 850 !important;
}

.page-title {
    font-size: 42px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    line-height: 1.1 !important;
    margin-bottom: 8px !important;
    letter-spacing: -0.6px;
}

.page-subtitle {
    font-size: 18px !important;
    color: #bfefff !important;
    margin-bottom: 26px !important;
    line-height: 1.5;
    font-weight: 500;
}

h1, h2, h3 {
    color: #eafcff !important;
}

h2 {
    font-size: 25px !important;
    color: #67e8f9 !important;
}

h3 {
    font-size: 20px !important;
}

p, li, label, span, div {
    font-size: 15.8px;
    line-height: 1.55;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(0,183,181,0.32);
    border-radius: 18px;
    padding: 18px 20px;
    min-height: 120px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 2.15rem !important;
    font-weight: 900 !important;
}

div[data-testid="stMetricLabel"] {
    color: #c7f9ff !important;
    font-weight: 700 !important;
}

.info-card {
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(0,183,181,0.25);
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
}

.info-card h2 {
    margin-top: 0;
    color: #67e8f9 !important;
    font-size: 24px !important;
}

.info-card h3 {
    color: #ffffff !important;
    font-size: 19px !important;
}

.info-card p, .info-card li {
    color: #e3fbff !important;
    font-size: 15.8px !important;
}

.insight-card {
    background: rgba(103,232,249,0.12);
    border-left: 5px solid #67e8f9;
    border-radius: 16px;
    padding: 16px 20px;
    margin-top: 10px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.20);
    color: #eafcff !important;
}

.insight-card b {
    color: #ffffff !important;
}

.stAlert {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(0,183,181,0.28);
    border-radius: 16px;
}

.stAlert * {
    color: #eafcff !important;
}

.stButton > button {
    background: linear-gradient(90deg, #00b7b5, #7c3aed);
    color: white !important;
    border: none;
    border-radius: 13px;
    padding: 10px 24px;
    font-size: 15.5px;
    font-weight: 800;
    box-shadow: 0 0 18px rgba(0,183,181,0.28);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 26px rgba(124,58,237,0.38);
}

textarea, input {
    background: rgba(255,255,255,0.10) !important;
    color: #e5faff !important;
    border-radius: 13px !important;
}

div[data-baseweb="input"], div[data-baseweb="textarea"] {
    background: rgba(255,255,255,0.10) !important;
    border-radius: 13px !important;
}

.js-plotly-plot {
    background: rgba(255,255,255,0.07) !important;
    border-radius: 18px;
    padding: 8px;
    border: 1px solid rgba(0,183,181,0.22);
    box-shadow: 0 8px 24px rgba(0,0,0,0.20);
}

div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 10px;
    border: 1px solid rgba(0,183,181,0.25);
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.14);
    margin: 1.8rem 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA + MODEL
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# =========================
# HELPERS
# =========================
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
        "tags_text_ratio": tc / (wc + 1)
    }])

def dark_chart(fig, height=430):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5faff", size=13),
        title_font=dict(color="#67e8f9", size=19),
        height=height,
        margin=dict(l=48, r=35, t=65, b=50)
    )
    return fig

def page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def info_card(title, html_body):
    st.markdown(
        f"""
        <div class="info-card">
            <h2>{title}</h2>
            {html_body}
        </div>
        """,
        unsafe_allow_html=True
    )

def insight_card(html_body):
    st.markdown(
        f"""
        <div class="insight-card">
            {html_body}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# SIDEBAR
# =========================
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

# =========================
# EXECUTIVE OVERVIEW
# =========================
if page == "Executive Overview":
    page_header(
        "Tumblr Growth Intelligence Platform",
        "AI-powered analytics platform for Tumblr indie music creators."
    )

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
        info_card(
            "Business Problem",
            """
            <p>Creators often publish music content without knowing:</p>
            <ul>
                <li>Best time to post</li>
                <li>Ideal caption length</li>
                <li>How many tags to use</li>
                <li>What emotional tone works best</li>
                <li>How to grow consistently</li>
            </ul>
            """
        )

    with col2:
        info_card(
            "Delivered Solution",
            """
            <p>This platform provides:</p>
            <ul>
                <li>Historical analytics dashboard</li>
                <li>Engagement prediction engine</li>
                <li>Caption optimization simulator</li>
                <li>Growth playbook recommendations</li>
                <li>Business-focused consulting summary</li>
            </ul>
            """
        )

# =========================
# ANALYTICS DASHBOARD
# =========================
elif page == "Analytics Dashboard":
    page_header(
        "Analytics Dashboard",
        "Meaningful insights explaining what drives Tumblr engagement."
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("High Engagement Rate", f"{round(df['high_engagement'].mean() * 100, 1)}%")
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

        insight_card("""
        <b>What this tells us:</b><br>
        This graph shows the average number of notes by posting hour.<br>
        The taller the bar, the stronger that hour performed historically.<br>
        Creators should test top-performing hours first.
        """)

    with b:
        tag_bucket = pd.cut(
            df["tag_count"],
            bins=[0, 3, 6, 10, 15, 100],
            labels=["0-3", "4-6", "7-10", "11-15", "16+"],
            include_lowest=True
        )
        temp = df.groupby(tag_bucket, observed=False)["high_engagement"].mean().reset_index()
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
        fig.update_traces(line=dict(width=5), marker=dict(size=11))
        st.plotly_chart(dark_chart(fig), use_container_width=True)

        insight_card("""
        <b>What this tells us:</b><br>
        Posts with too few tags underperform.<br>
        Balanced tag usage increases discoverability.<br>
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
        temp = df.groupby(caption_bucket, observed=False)["high_engagement"].mean().reset_index()
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

        insight_card("""
        <b>What this tells us:</b><br>
        Medium-length captions tend to perform strongest.<br>
        Too short feels empty.<br>
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

            insight_card("""
            <b>What this tells us:</b><br>
            Each bubble is a content style group.<br>
            Bigger bubbles mean more posts.<br>
            Higher bubbles mean stronger average engagement.
            """)
        else:
            st.info("Content style clustering is unavailable because `cluster_label` is not present in the dataset.")

# =========================
# STRATEGIC POST SIMULATOR
# =========================
elif page == "Strategic Post Simulator":
    page_header(
        "Strategic Post Simulator",
        "Predict post performance before publishing and receive practical improvement tips."
    )

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
        info_card(
            "How the Simulator Works",
            """
            <p>The simulator estimates whether a Tumblr post has high engagement potential.</p>
            <p><b>It evaluates:</b></p>
            <ul>
                <li>Caption length</li>
                <li>Word count</li>
                <li>Number of tags</li>
                <li>Sentiment polarity</li>
                <li>Subjectivity / personal tone</li>
                <li>Posting hour</li>
                <li>Tag-to-text balance</li>
            </ul>
            <p>The output is not a guarantee of virality. It is a decision-support score based on historical posting patterns.</p>
            """
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
            st.plotly_chart(dark_chart(fig, height=420), use_container_width=True)

            tips = []
            if len(caption.split()) < 50:
                tips.append("Add more storytelling or emotional context.")
            else:
                tips.append("Caption depth is strong.")

            if len(split_tags(tags)) < 5:
                tips.append("Add more relevant tags. Try 5–15 focused tags.")
            else:
                tips.append("Tag count is healthy.")

            if hour not in [3, 11, 13, 14, 23]:
                tips.append("Test stronger posting windows such as 3:00, 11:00, 13:00, 14:00, or 23:00.")
            else:
                tips.append("Posting hour aligns with stronger historical windows.")

            info_card(
                "Recommendations",
                "<ul>" + "".join([f"<li>{tip}</li>" for tip in tips]) + "</ul>"
            )

# =========================
# GROWTH PLAYBOOK
# =========================
elif page == "Growth Playbook":
    page_header(
        "Growth Playbook",
        "Practical, non-technical recommendations creators can directly follow."
    )

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())
    ideal_words = round(df[df["high_engagement"] == 1]["word_count"].mean(), 0)
    ideal_tags = round(df[df["high_engagement"] == 1]["tag_count"].mean(), 0)

    info_card(
        "Recommended Creator Strategy",
        f"""
        <h3>1. Caption Strategy</h3>
        <p>Do not only post a link. Add a short emotional reaction, story, or reason why the song matters.</p>
        <p><b>Example caption:</b></p>
        <p>This track feels like walking home at midnight after a long week. The vocals are soft, the guitar is dreamy, and I keep replaying it.</p>

        <h3>2. Tag Strategy</h3>
        <p>Use around {ideal_tags} tags. Mix broad discovery tags with niche music tags.</p>
        <p><b>Suggested tags:</b> indie music, new music, indie rock, bedroom pop, shoegaze, sad songs, playlist, recommendation</p>

        <h3>3. Best Posting Time</h3>
        <p>The strongest posting hour in this dataset is {best_hour}:00. Test this first, then compare with evening windows.</p>

        <h3>4. Ideal Caption Length</h3>
        <p>High-performing posts average around {ideal_words} words. Avoid captions that are too empty or generic.</p>

        <h3>5. Weekly Growth Routine</h3>
        <p>Post 3–5 times per week, track notes, compare tags, test different hours, and reuse formats that perform well.</p>
        """
    )

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

# =========================
# CONSULTING SUMMARY
# =========================
elif page == "Consulting Summary":
    page_header(
        "Consulting Summary",
        "Business-facing summary of platform value and impact."
    )

    info_card(
        "Project Overview",
        """
        <p>This project follows Track 2: User / Influencer / Brand-Facing Analytics. The selected client context is the Tumblr indie music creator community.</p>
        <p>The final solution is a creator-facing intelligence platform helping users improve traffic, engagement, and audience development.</p>
        """
    )

    info_card(
        "Business Problem",
        """
        <p>Tumblr creators produce highly creative content, but often lack analytics tools to understand why some posts receive more notes than others.</p>
        <p>This makes content planning difficult. Creators may not know whether captions, tags, emotional tone, or posting hours are helping growth.</p>
        """
    )

    info_card(
        "Solution Delivered",
        """
        <ul>
            <li>Analytics Dashboard: explains historical engagement patterns</li>
            <li>Strategic Post Simulator: predicts engagement potential</li>
            <li>Growth Playbook: converts insights into practical actions</li>
            <li>Consulting Summary: links technical work to business value</li>
        </ul>
        """
    )

    info_card(
        "Technical Methods Used",
        """
        <ul>
            <li>Feature engineering from captions, tags, and posting time</li>
            <li>Exploratory data analysis</li>
            <li>Classification logic for engagement scoring</li>
            <li>Visual dashboards with Plotly</li>
            <li>Recommendation framework for creator decisions</li>
        </ul>
        """
    )

    info_card(
        "Business Value Created",
        """
        <ul>
            <li>Better content decisions</li>
            <li>Faster learning cycles</li>
            <li>Improved discoverability</li>
            <li>More consistent audience growth</li>
            <li>Stronger creator confidence</li>
        </ul>
        """
    )
