import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="Tumblr Growth Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv("tumblr_features.csv")

@st.cache_resource
def load_model():
    return joblib.load("tumblr_model.pkl")

df = load_data()
model = load_model()

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp{
    background:#eef2f5;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#003b46,#005461,#018790);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

.hero{
    background:linear-gradient(135deg,#003b46,#018790,#00B7B5);
    padding:36px;
    border-radius:24px;
    color:white;
    box-shadow:0 14px 30px rgba(0,0,0,.18);
}

.hero h1{
    font-size:44px;
    font-weight:850;
    margin-bottom:12px;
}

.hero p{
    font-size:17px;
    line-height:1.65;
}

.kpi{
    background:linear-gradient(135deg,#005461,#018790);
    color:white;
    padding:22px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 10px 24px rgba(0,0,0,.12);
}

.kpi h1{
    margin:0;
    font-size:34px;
    font-weight:850;
}

.kpi p{
    margin:0;
    font-size:14px;
    opacity:.9;
}

.big{
    font-size:40px;
    font-weight:850;
    color:#003b46;
}

.sub{
    color:#53666E;
    font-size:16px;
    margin-bottom:20px;
}

.card{
    background:white;
    padding:26px;
    border-radius:20px;
    box-shadow:0 10px 24px rgba(0,0,0,.08);
    border:1px solid #dfe7ea;
}

.card h2, .card h3{
    color:#003b46;
}

.insight{
    background:#dbeaf0;
    padding:18px;
    border-left:6px solid #018790;
    border-radius:14px;
    margin-top:10px;
    color:#003b46;
}

.stButton button{
    background:linear-gradient(90deg,#018790,#00B7B5);
    color:white;
    border:none;
    border-radius:12px;
    font-weight:750;
    padding:10px 20px;
}

.stButton button:hover{
    background:#003b46;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
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

def chart_layout(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        title_font=dict(size=18, color="#003b46"),
        font=dict(color="#334155"),
        margin=dict(l=40, r=30, t=60, b=50)
    )
    return fig

# ---------------- SIDEBAR ----------------
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

# ---------------- EXECUTIVE OVERVIEW ----------------
if page == "Executive Overview":

    st.markdown("""
    <div class='hero'>
        <h1>Tumblr Growth Intelligence Platform</h1>
        <p>
        An AI-powered creator analytics platform for Tumblr indie music creators.
        The system helps creators understand what drives engagement, improve captions,
        optimize tags, identify stronger posting windows, and make smarter publishing decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    kpis = [
        (f"{len(df):,}", "Posts Analyzed"),
        (round(df["note_count"].mean(), 2), "Average Notes"),
        (int(df["note_count"].max()), "Highest Notes"),
        (f"{int(df.groupby('hour')['note_count'].mean().idxmax())}:00", "Best Posting Hour")
    ]

    for col, (num, label) in zip([c1, c2, c3, c4], kpis):
        with col:
            st.markdown(f"""
            <div class='kpi'>
                <h1>{num}</h1>
                <p>{label}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class='card'>
            <h2>Business Problem</h2>
            <p>
            Indie music creators on Tumblr often publish songs, lyrics, playlists, reactions,
            and promotional updates without knowing what actually improves engagement.
            </p>
            <p><b>Main creator pain points:</b></p>
            <ul>
                <li>Unclear best posting time</li>
                <li>Uncertainty about caption length</li>
                <li>Confusion about tag quantity and tag strategy</li>
                <li>No prediction tool before publishing</li>
                <li>No simple growth playbook for non-technical creators</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class='card'>
            <h2>Delivered Solution</h2>
            <p>
            This project converts Tumblr post data into a practical creator-facing intelligence system.
            </p>
            <p><b>The platform provides:</b></p>
            <ul>
                <li>Dashboard insights for historical content performance</li>
                <li>Machine learning engagement prediction</li>
                <li>Strategic Post Simulator for new captions</li>
                <li>Growth Playbook with actionable posting guidance</li>
                <li>Consulting-style summary for business value</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
elif page == "Analytics Dashboard":

    st.markdown("<div class='big'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Meaningful graphs that explain what drives Tumblr indie music engagement.</div>", unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)

    high_rate = round(df["high_engagement"].mean() * 100, 1)
    avg_words = round(df["word_count"].mean(), 0)
    avg_tags = round(df["tag_count"].mean(), 0)
    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())
    avg_sentiment = round(df["polarity"].mean(), 2)

    kpis = [
        (f"{high_rate}%", "High Engagement Rate"),
        (avg_words, "Avg Caption Words"),
        (avg_tags, "Avg Tags Used"),
        (f"{best_hour}:00", "Best Posting Hour"),
        (avg_sentiment, "Avg Sentiment")
    ]

    for col, (num, label) in zip([c1, c2, c3, c4, c5], kpis):
        with col:
            st.markdown(f"""
            <div class='kpi'>
                <h1>{num}</h1>
                <p>{label}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # GRAPH 1: Posting Hour Bar
    col1, col2 = st.columns(2)

    with col1:
        hour_data = df.groupby("hour")["note_count"].mean().reset_index()
        fig = px.bar(
            hour_data,
            x="hour",
            y="note_count",
            title="Which Posting Hour Gets More Notes?",
            color="note_count",
            color_continuous_scale=["#005461", "#018790", "#00B7B5"],
            labels={"hour": "Posting Hour", "note_count": "Average Notes"}
        )
        fig = chart_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class='insight'>
        <b>What this tells:</b><br>
        This graph shows the average number of notes by posting hour.
        The taller the bar, the better that hour performed historically.
        Creators can use this to choose stronger posting windows.
        </div>
        """, unsafe_allow_html=True)

    # GRAPH 2: Tag count buckets
    with col2:
        df["tag_bucket"] = pd.cut(
            df["tag_count"],
            bins=[0, 3, 6, 10, 15, 100],
            labels=["0-3", "4-6", "7-10", "11-15", "16+"],
            include_lowest=True
        )

        tag_bucket = df.groupby("tag_bucket")["high_engagement"].mean().reset_index()
        tag_bucket["High Engagement Rate"] = tag_bucket["high_engagement"] * 100

        fig = px.line(
            tag_bucket,
            x="tag_bucket",
            y="High Engagement Rate",
            markers=True,
            title="How Many Tags Should Creators Use?",
            labels={"tag_bucket": "Number of Tags Used", "High Engagement Rate": "High Engagement Rate (%)"},
            color_discrete_sequence=["#00B7B5"]
        )
        fig.update_traces(line=dict(width=5), marker=dict(size=12))
        fig = chart_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class='insight'>
        <b>What this tells:</b><br>
        This graph shows which tag-count range has the highest chance of high engagement.
        It helps creators avoid using too few tags or overloading the post with too many tags.
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # GRAPH 3: Caption length buckets
    col3, col4 = st.columns(2)

    with col3:
        df["caption_bucket"] = pd.cut(
            df["word_count"],
            bins=[0, 25, 50, 100, 200, 2000],
            labels=["0-25", "26-50", "51-100", "101-200", "200+"],
            include_lowest=True
        )

        cap_bucket = df.groupby("caption_bucket")["high_engagement"].mean().reset_index()
        cap_bucket["High Engagement Rate"] = cap_bucket["high_engagement"] * 100

        fig = px.area(
            cap_bucket,
            x="caption_bucket",
            y="High Engagement Rate",
            title="Does Caption Length Improve Engagement?",
            labels={"caption_bucket": "Caption Word Range", "High Engagement Rate": "High Engagement Rate (%)"},
            color_discrete_sequence=["#018790"]
        )
        fig.update_traces(line=dict(width=4))
        fig = chart_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        <div class='insight'>
        <b>What this tells:</b><br>
        This graph compares short, medium, and long captions.
        It helps creators understand whether storytelling captions perform better than very short captions.
        </div>
        """, unsafe_allow_html=True)

    # GRAPH 4: Content cluster performance
    with col4:
        if "cluster_label" in df.columns:
            cluster_perf = df.groupby("cluster_label").agg(
                avg_notes=("note_count", "mean"),
                posts=("note_count", "count")
            ).reset_index()

            fig = px.scatter(
                cluster_perf,
                x="posts",
                y="avg_notes",
                size="posts",
                color="cluster_label",
                title="Which Content Style Performs Best?",
                labels={"posts": "Number of Posts", "avg_notes": "Average Notes", "cluster_label": "Content Style"},
                color_discrete_sequence=["#003b46", "#005461", "#018790", "#00B7B5"]
            )
            fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="white")))
            fig = chart_layout(fig)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            <div class='insight'>
            <b>What this tells:</b><br>
            Each bubble is a content style group.
            Bigger bubbles mean more posts in that style.
            Higher bubbles mean stronger average engagement.
            This helps creators choose what type of content to focus on.
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # GRAPH 5: Top tags treemap
    tags = []
    for t in df["tags"]:
        tags.extend(split_tags(t))

    top_tags = pd.DataFrame(Counter(tags).most_common(15), columns=["Tag", "Count"])

    fig = px.treemap(
        top_tags,
        path=["Tag"],
        values="Count",
        title="Top Discovery Tags in the Indie Music Community",
        color="Count",
        color_continuous_scale=["#005461", "#018790", "#00B7B5"]
    )
    fig = chart_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight'>
    <b>What this tells:</b><br>
    This treemap shows the most common discovery tags.
    Larger boxes mean the tag appears more often.
    Creators should combine broad tags like “indie music” with niche tags like “shoegaze” or “bedroom pop”
    to improve discoverability.
    </div>
    """, unsafe_allow_html=True)

# ---------------- SIMULATOR ----------------
elif page == "Strategic Post Simulator":

    st.markdown("<div class='big'>Strategic Post Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Predict post performance before publishing and receive practical improvement tips.</div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:
        text = st.text_area("Caption", height=220, placeholder="Example: this song completely changed my week...")
        tags = st.text_input("Tags", placeholder="indie music, shoegaze, bedroom pop, new music")
        hour = st.slider("Posting Hour", 0, 23, 19)

        run = st.button("Analyze Post")

    with right:
        st.markdown("""
        <div class='card'>
        <h2>How the Simulator Works</h2>
        <p>
        The simulator uses the trained Random Forest model to estimate whether a new Tumblr post
        has high engagement potential.
        </p>
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
        <p>
        The output is not a guarantee of virality. It is a decision-support score based on historical Tumblr patterns.
        </p>
        </div>
        """, unsafe_allow_html=True)

    if run:
        if text.strip() == "":
            st.warning("Please enter a caption first.")
        else:
            X = create_features(text, tags, hour)
            prob = model.predict_proba(X)[0][1]

            c1, c2, c3 = st.columns(3)
            c1.metric("Success Probability", f"{prob:.0%}")
            c2.metric("Words", len(text.split()))
            c3.metric("Tags", len(split_tags(tags)))

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                number={"suffix": "%"},
                title={"text": "Engagement Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#003b46"},
                    "steps": [
                        {"range": [0, 50], "color": "#dceef0"},
                        {"range": [50, 75], "color": "#8ed9df"},
                        {"range": [75, 100], "color": "#00B7B5"}
                    ]
                }
            ))
            gauge.update_layout(height=400)
            st.plotly_chart(gauge, use_container_width=True)

            st.markdown("<div class='card'><h2>Improvement Tips</h2>", unsafe_allow_html=True)

            word_count = len(text.split())
            tag_count = len(split_tags(tags))
            sentiment = TextBlob(text).sentiment.polarity

            if word_count < 50:
                st.write("- Add more storytelling. Explain why the song matters, what mood it creates, or how it made you feel.")
            else:
                st.write("- Caption length is strong. Keep it clear and emotionally focused.")

            if tag_count < 5:
                st.write("- Add more tags. Try 5–15 tags for better discovery.")
            elif tag_count > 15:
                st.write("- Reduce tags slightly. Too many tags may make the post unfocused.")
            else:
                st.write("- Tag count is in a healthy range.")

            if sentiment < 0.1:
                st.write("- Add more emotional or expressive wording.")
            else:
                st.write("- Emotional tone is clear.")

            if hour not in [3, 11, 13, 14, 23]:
                st.write("- Consider testing stronger hours such as 3 AM, 11 AM, 1 PM, 2 PM, or 11 PM based on this dataset.")
            else:
                st.write("- Posting hour aligns with stronger historical windows.")

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PLAYBOOK ----------------
elif page == "Growth Playbook":

    st.markdown("<div class='big'>Growth Playbook</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Practical, non-technical recommendations creators can directly follow.</div>", unsafe_allow_html=True)

    best_hour = int(df.groupby("hour")["note_count"].mean().idxmax())
    ideal_words = round(df[df["high_engagement"] == 1]["word_count"].mean(), 0)
    ideal_tags = round(df[df["high_engagement"] == 1]["tag_count"].mean(), 0)

    st.markdown(f"""
    <div class='card'>
    <h2>Recommended Creator Strategy</h2>

    <h3>1. Caption Strategy</h3>
    <p>
    Do not only post a link. Add a short emotional reaction, story, or reason why the song matters.
    A strong caption should feel personal and specific.
    </p>
    <p><b>Example caption:</b><br>
    “This track feels like walking home at midnight after a long week. The vocals are soft, the guitar is dreamy,
    and it has that perfect indie sadness I keep replaying.”</p>

    <h3>2. Tag Strategy</h3>
    <p>
    Use around <b>{ideal_tags} tags</b>. Mix broad discovery tags with niche music tags.
    </p>
    <p><b>Suggested tag mix:</b><br>
    indie music, new music, indie rock, bedroom pop, shoegaze, sad songs, playlist, music recommendation</p>

    <h3>3. Best Posting Time</h3>
    <p>
    The strongest posting hour in this dataset is <b>{best_hour}:00</b>.
    Creators should test this hour first, then compare results with evening windows.
    </p>

    <h3>4. Ideal Caption Length</h3>
    <p>
    High-performing posts average around <b>{ideal_words} words</b>.
    This does not mean every caption must be long, but creators should avoid captions that are too empty or generic.
    </p>

    <h3>5. Weekly Growth Routine</h3>
    <p>
    Post 3–5 times per week, track notes, compare tags, test different hours, and reuse formats that perform well.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    table = pd.DataFrame({
        "Growth Lever": [
            "Caption",
            "Tags",
            "Timing",
            "Emotion",
            "Consistency"
        ],
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
            "Increases visibility during stronger windows",
            "Encourages replies and reblogs",
            "Creates repeatable growth learning"
        ]
    })

    st.dataframe(table, use_container_width=True)

# ---------------- SUMMARY ----------------
elif page == "Consulting Summary":

    st.markdown("<div class='big'>Consulting Summary</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h2>Project Overview</h2>
    <p>
    This project follows <b>Track 2: User / Influencer / Brand-Facing Analytics</b>.
    The selected client context is the Tumblr indie music creator community.
    The final solution is a creator-facing analytics platform that helps users improve traffic,
    engagement, and audience development.
    </p>

    <h2>Business Problem</h2>
    <p>
    Tumblr creators produce highly creative text-heavy content, but they often lack simple analytics tools
    to understand why some posts receive more notes than others. This makes content planning difficult.
    Creators may not know which captions, tags, emotional tones, or posting hours are helping them grow.
    </p>

    <h2>Solution Delivered</h2>
    <p>
    The Tumblr Growth Intelligence Platform provides four major capabilities:
    </p>
    <ul>
        <li><b>Analytics Dashboard:</b> explains historical engagement patterns using meaningful charts.</li>
        <li><b>Strategic Post Simulator:</b> predicts engagement potential before publishing.</li>
        <li><b>Growth Playbook:</b> converts model insights into practical creator actions.</li>
        <li><b>Consulting Summary:</b> connects technical results to Tumblr’s business value.</li>
    </ul>

    <h2>Technical Methods Used</h2>
    <ul>
        <li>Feature engineering from captions, tags, and posting time</li>
        <li>Sentiment analysis using polarity and subjectivity</li>
        <li>Content clustering to identify post styles</li>
        <li>Logistic Regression baseline model</li>
        <li>Random Forest predictive model</li>
        <li>Validation using accuracy, precision, recall, F1-score, and ROC-AUC</li>
    </ul>

    <h2>Business Value</h2>
    <p>
    The platform helps creators make smarter posting decisions. Instead of guessing, creators can use data
    to decide when to post, how many tags to use, how detailed captions should be, and how emotional or personal
    their writing should be. This supports better discoverability, stronger engagement, and more consistent audience growth.
    </p>

    <h2>Limitations</h2>
    <p>
    Tumblr engagement is influenced by hidden factors such as follower count, image quality, reblog networks,
    creator popularity, and algorithmic timing. Therefore, the model should be positioned as a decision-support tool,
    not a perfect virality predictor.
    </p>

    <h2>Final Recommendation</h2>
    <p>
    During the lightning talk, demonstrate the Strategic Post Simulator live. Enter one sample caption,
    add indie music tags, choose a posting hour, and show how the system gives an engagement score and practical improvement tips.
    This will clearly communicate both technical work and business usefulness.
    </p>
    </div>
    """, unsafe_allow_html=True)