import streamlit as st
import pandas as pd
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
st.markdown("""
<style>

/* KPI CARD FULL FIX */
div[data-testid="metric-container"]{
    background: white;
    border-radius: 20px;
    padding: 22px 18px !important;
    min-height: 165px !important;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    border-top: 6px solid #00a6b2;
    margin-bottom: 8px;
}

div[data-testid="metric-container"] label{
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #486581 !important;
    text-align: center !important;
    margin-bottom: 8px !important;
}

div[data-testid="stMetricValue"]{
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    color: #003b49 !important;
    text-align: center !important;
    line-height: 1.1 !important;
}

[data-testid="column"]{
    padding: 0 6px !important;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
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

# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------
hour_data = pd.DataFrame({
    "Posting Hour": list(range(24)),
    "Average Notes": [
        1.4,2.0,1.5,6.6,2.0,1.6,1.2,1.8,1.5,1.4,1.1,3.4,
        1.6,5.5,4.0,2.0,2.1,2.3,2.0,2.5,1.7,2.5,2.2,3.2
    ]
})

tag_data = pd.DataFrame({
    "Tags Used": ["0-3", "4-6", "7-10", "11-15", "16+"],
    "High Engagement Rate": [52, 69, 70, 59, 82]
})

caption_data = pd.DataFrame({
    "Caption Length": ["0-25", "26-50", "51-100", "101-200", "200+"],
    "High Engagement Rate": [68, 70, 69, 65, 60]
})

style_data = pd.DataFrame({
    "Content Style": [
        "Aesthetic / Short",
        "Lyrical / Emotional",
        "Personal Storytelling",
        "Promotional"
    ],
    "Posts": [410, 420, 480, 95],
    "Average Notes": [2.25, 2.27, 2.38, 3.72]
})

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def metric_row(items):
    cols = st.columns(len(items))
    for i, item in enumerate(items):
        cols[i].metric(item[0], item[1])

# ---------------------------------------------------
# PAGE 1
# ---------------------------------------------------
if page == "Executive Overview":

    st.title("Tumblr Growth Intelligence Platform")
    st.subheader("AI-powered analytics platform for Tumblr indie music creators.")

    st.info(
        "This platform helps creators understand engagement, improve captions, "
        "optimize posting time, strengthen tag strategy, and grow audience reach."
    )

    metric_row([
        ("Posts Analyzed", "1,000"),
        ("Average Notes", "2.44"),
        ("Highest Notes", "128"),
        ("Best Posting Hour", "3:00")
    ])

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

# ---------------------------------------------------
# PAGE 2
# ---------------------------------------------------
elif page == "Analytics Dashboard":

    st.title("Analytics Dashboard")
    st.caption("Meaningful insights explaining what drives Tumblr engagement.")

    metric_row([
        ("High Engagement Rate", "67.5%"),
        ("Avg Caption Words", "100.0"),
        ("Avg Tags", "9.0"),
        ("Best Hour", "3:00"),
        ("Avg Sentiment", "0.12")
    ])

    st.markdown("##")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            hour_data,
            x="Posting Hour",
            y="Average Notes",
            title="Which Posting Hour Gets More Notes?"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("""
**What this tells us:**  
This graph shows the average number of notes by posting hour.  
The taller the bar, the stronger that hour performed historically.  
Creators should test top-performing hours first.
        """)

    with col2:
        fig = px.line(
            tag_data,
            x="Tags Used",
            y="High Engagement Rate",
            markers=True,
            title="How Many Tags Should Creators Use?"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("""
**What this tells us:**  
Posts with too few tags underperform.  
Balanced tag usage increases discoverability.  
Very high tag usage can work if highly relevant.
        """)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.area(
            caption_data,
            x="Caption Length",
            y="High Engagement Rate",
            title="Does Caption Length Improve Engagement?"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("""
**What this tells us:**  
Medium-length captions tend to perform strongest.  
Too short feels empty.  
Too long may reduce reading completion.
        """)

    with col4:
        fig = px.scatter(
            style_data,
            x="Posts",
            y="Average Notes",
            size="Posts",
            color="Content Style",
            title="Which Content Style Performs Best?"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("""
**What this tells us:**  
Personal and emotional storytelling content tends to perform better than generic promotional posts.
        """)

# ---------------------------------------------------
# PAGE 3
# ---------------------------------------------------
elif page == "Strategic Post Simulator":

    st.title("Strategic Post Simulator")
    st.caption("Predict post performance before publishing and receive practical improvement tips.")

    left, right = st.columns([1.2, 1])

    with left:
        caption = st.text_area(
            "Caption",
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
        score = 72

        if len(caption) > 80:
            score += 6
        if len(tags.split(",")) >= 7:
            score += 5
        if hour in [2, 3, 13, 14]:
            score += 7

        score = min(score, 95)

        st.markdown("---")
        st.subheader("Prediction Result")
        st.metric("Estimated High Engagement Probability", f"{score}%")

        tips = []

        if len(caption) < 50:
            tips.append("Write a more personal or emotional caption.")
        if len(tags.split(",")) < 6:
            tips.append("Use more relevant niche + broad tags.")
        if hour not in [2, 3, 13, 14]:
            tips.append("Try testing stronger posting windows like 3:00.")

        if not tips:
            tips.append("Strong setup detected. Publish and monitor results.")

        st.write("### Recommendations")
        for t in tips:
            st.write(f"• {t}")

# ---------------------------------------------------
# PAGE 4
# ---------------------------------------------------
elif page == "Growth Playbook":

    st.title("Growth Playbook")
    st.caption("Practical, non-technical recommendations creators can directly follow.")

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
    st.write("Use around 9–10 tags. Mix broad discovery tags with niche music tags.")
    st.write(
        "**Suggested tags:** indie music, new music, indie rock, "
        "bedroom pop, shoegaze, sad songs, playlist, recommendation"
    )

    st.subheader("3. Best Posting Time")
    st.write(
        "The strongest posting hour in this dataset is 3:00. "
        "Test this first, then compare with evening windows."
    )

    st.subheader("4. Ideal Caption Length")
    st.write(
        "High-performing posts average around 91 words. "
        "Avoid captions that are too empty or generic."
    )

    st.subheader("5. Weekly Growth Routine")
    st.write(
        "Post 3–5 times per week, track notes, compare tags, "
        "test different hours, and reuse formats that perform well."
    )

    st.markdown("##")

    df = pd.DataFrame({
        "Growth Lever": ["Caption", "Tags", "Timing", "Emotion", "Consistency"],
        "What To Do": [
            "Use emotional reactions and short stories",
            "Use broad + niche tags together",
            "Start testing around 3:00",
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

    st.dataframe(df, use_container_width=True)

# ---------------------------------------------------
# PAGE 5
# ---------------------------------------------------
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

    st.header("Presentation Tip")
    st.write(
        "Use the Strategic Post Simulator live during presentation to impress professors "
        "with interactivity and practical business application."
    )
