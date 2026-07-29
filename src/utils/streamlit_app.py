import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Resume & Spam Analyzer",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

div[data-testid="stMetricValue"]{
    font-size:28px;
}

.skill{
    display:inline-block;
    padding:6px 12px;
    margin:4px;
    border-radius:15px;
    background:#1f77b4;
    color:white;
    font-size:14px;
}

.good{
    padding:12px;
    border-radius:10px;
    background:#d4edda;
    color:#155724;
    margin-bottom:8px;
}

.warn{
    padding:12px;
    border-radius:10px;
    background:#fff3cd;
    color:#856404;
    margin-bottom:8px;
}

.bad{
    padding:12px;
    border-radius:10px;
    background:#f8d7da;
    color:#721c24;
    margin-bottom:8px;
}

</style>
""",unsafe_allow_html=True)

st.title("🤖 AI Resume & Spam Analyzer")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose Task",
    [
        "Resume Analysis",
        "Spam Analysis"
    ]
)

##################################################################################
# Resume Analysis
##################################################################################

if page=="Resume Analysis":

    st.header("📄 Resume Analysis")

    uploaded_file=st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Analyze Resume"):

            with st.spinner("Analyzing Resume..."):

                files={
                    "file":(
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf"
                    )
                }

                response=requests.post(
                    API_URL+"/analyze/resume",
                    files=files
                )

            if response.status_code!=200:

                st.error(response.text)

                st.stop()

            data=response.json()

            routing=data["routing"]

            result=data["result"]["data"]

            st.success("Analysis Completed")

            st.divider()

            st.subheader("Routing Decision")

            c1,c2,c3=st.columns(3)

            c1.metric(
                "Intent",
                routing["intent"]
            )

            c2.metric(
                "Input",
                routing["input_source"]
            )

            c3.metric(
                "Need User",
                str(routing["requires_user_input"])
            )

            st.divider()

            candidate=result["candidate"]

            st.header("👤 Candidate")

            col1,col2=st.columns(2)

            with col1:

                st.write("### Personal Details")

                st.write("**Name:**",candidate["name"])
                st.write("**Email:**",candidate["email"])
                st.write("**Phone:**",candidate["phone"])
                st.write("**Location:**",candidate["location"])

            with col2:

                st.write("### Profiles")

                st.write("**LinkedIn:**",candidate["linkedin"])
                st.write("**GitHub:**",candidate["GitHub"])
                st.write("**Portfolio:**",candidate["portfolio"])

            st.divider()

            analysis=result["ai_analysis"]

            st.header("🤖 AI Resume Score")

            st.metric(
                "Resume Score",
                f"{analysis['resume_score']}/100"
            )

            st.progress(
                float(analysis["resume_score"])/100
            )

            st.info(
                analysis["resume_summary"]
            )

            st.divider()

            st.header("💻 Skills")

            skills=result["skills"]

            def draw_skill_list(title,items):

                if not items:
                    return

                st.subheader(title)

                html=""

                for skill in items:

                    html+=f"<span class='skill'>{skill}</span>"

                st.markdown(
                    html,
                    unsafe_allow_html=True
                )

            draw_skill_list(
                "Programming Languages",
                skills["programming_languages"]
            )

            draw_skill_list(
                "Frameworks",
                skills["frameworks"]
            )

            draw_skill_list(
                "Databases",
                skills["Databases"]
            )

            draw_skill_list(
                "Cloud Platforms",
                skills["cloud_platforms"]
            )

            draw_skill_list(
                "AI / ML",
                skills["ai_ml_tools"]
            )

            draw_skill_list(
                "Soft Skills",
                skills["soft_skills"]
            )

            st.divider()
            ####################################################################
            # Education
            ####################################################################

            st.header("🎓 Education")

            education = result.get("education", [])

            for edu in education:

                with st.expander(f"🎓 {edu['degree']}"):

                    st.write(f"**Institution:** {edu['institution']}")

                    if edu.get("graduation_year"):
                        st.write(f"**Graduation Year:** {edu['graduation_year']}")

            st.divider()

            ####################################################################
            # Experience
            ####################################################################

            st.header("💼 Experience")

            experience = result.get("experience")

            if experience:

                for exp in experience:

                    with st.container(border=True):

                        st.subheader(exp["role"])

                        st.write(f"**Company:** {exp['company']}")

                        if exp.get("start_date") or exp.get("end_date"):
                            st.write(
                                f"**Duration:** {exp.get('start_date','')} - {exp.get('end_date','Present')}"
                            )

                        responsibilities = exp.get("responsibilities")

                        if responsibilities:

                            st.write("### Responsibilities")

                            for r in responsibilities:
                                st.write(f"• {r}")

            else:

                st.info("No work experience found.")

            st.divider()

            ####################################################################
            # Projects
            ####################################################################

            st.header("🚀 Projects")

            projects = result.get("projects")

            if projects:

                for project in projects:

                    with st.container(border=True):

                        st.subheader(project["title"])

                        st.write(project["description"])

                        tech = project.get("technologies_used")

                        if tech:

                            html = ""

                            for t in tech:
                                html += f"<span class='skill'>{t}</span>"

                            st.markdown(
                                html,
                                unsafe_allow_html=True
                            )

                        if project.get("link"):
                            st.link_button(
                                "Open Project",
                                project["link"]
                            )

            else:

                st.info("No projects available.")

            st.divider()

            ####################################################################
            # Certifications
            ####################################################################

            st.header("📜 Certifications")

            certifications = result.get("certifications")

            if certifications:

                for cert in certifications:

                    with st.expander(cert["name"]):

                        st.write(
                            f"**Organization:** {cert['issuing_organization']}"
                        )

                        if cert.get("issue_date"):
                            st.write(
                                f"**Issued:** {cert['issue_date']}"
                            )

                        if cert.get("credential_id"):
                            st.write(
                                f"**Credential ID:** {cert['credential_id']}"
                            )

                        if cert.get("credential_url"):
                            st.link_button(
                                "Verify",
                                cert["credential_url"]
                            )

            else:

                st.info("No certifications found.")

            st.divider()

            ####################################################################
            # Achievements
            ####################################################################

            achievements = result.get("achievements")

            if achievements:

                st.header("🏆 Achievements")

                for achievement in achievements:

                    with st.container(border=True):

                        st.subheader(achievement["title"])

                        st.write(achievement["description"])

                        if achievement.get("date"):
                            st.caption(achievement["date"])

            st.divider()

            ####################################################################
            # Languages
            ####################################################################

            languages = result.get("languages")

            if languages:

                st.header("🌍 Languages")

                df = pd.DataFrame(languages)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

            st.divider()

            ####################################################################
            # AI Analysis
            ####################################################################

            st.header("🤖 AI Insights")

            st.subheader("✅ Strengths")

            for item in analysis.get("strengths", []):

                st.markdown(
                    f"<div class='good'>✔ {item}</div>",
                    unsafe_allow_html=True
                )

            st.subheader("⚠ Areas for Improvement")

            for item in analysis.get("areas_for_improvement", []):

                st.markdown(
                    f"<div class='warn'>⚠ {item}</div>",
                    unsafe_allow_html=True
                )

            st.subheader("📚 Missing Skills")

            missing = analysis.get("missing_skills")

            if missing:

                html = ""

                for skill in missing:

                    html += f"<span class='skill'>{skill}</span>"

                st.markdown(
                    html,
                    unsafe_allow_html=True
                )

            st.subheader("💼 Suggested Job Roles")

            roles = analysis.get("suggested_job_roles")

            if roles:

                cols = st.columns(2)

                for i, role in enumerate(roles):

                    cols[i % 2].success(role)

            st.info(
                f"Experience Level : {analysis['experience_level']}"
            )
####################################################################################
# Spam Analysis
####################################################################################

elif page == "Spam Analysis":

    st.header("📧 Spam Email Analysis")

    email_text = st.text_area(
        "Paste Email Content",
        height=300,
        placeholder="Paste the complete email here..."
    )

    if st.button("Analyze Email"):

        if not email_text.strip():

            st.warning("Please enter an email.")

            st.stop()

        with st.spinner("Analyzing Email..."):

            response = requests.post(
                API_URL + "/analyze/spam",
                data={
                    "email_text": email_text
                }
            )

        if response.status_code != 200:

            st.error(response.text)

            st.stop()

        data = response.json()

        routing = data["routing"]

        result = data["result"]["data"]

        st.success("Analysis Completed")

        st.divider()

        ####################################################################
        # Routing
        ####################################################################

        st.subheader("Routing Decision")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Intent",
            routing["intent"]
        )

        c2.metric(
            "Input Source",
            routing["input_source"]
        )

        c3.metric(
            "Requires User",
            str(routing["requires_user_input"])
        )

        st.divider()

        ####################################################################
        # Spam Verdict
        ####################################################################

        st.header("🛡 Email Verdict")

        if result["is_spam"]:

            st.markdown(
                """
                <div class='bad'>
                <h2>🚨 SPAM DETECTED</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class='good'>
                <h2>✅ LEGITIMATE EMAIL</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        ####################################################################
        # Confidence
        ####################################################################

        confidence = float(result["confidence_score"])

        st.metric(
            "Confidence",
            f"{confidence*100:.1f}%"
        )

        st.progress(confidence)

        st.divider()

        ####################################################################
        # Category
        ####################################################################

        st.subheader("📂 Category")

        st.info(result["category"].upper())

        st.divider()

        ####################################################################
        # Reasoning
        ####################################################################

        st.subheader("🧠 AI Reasoning")

        st.write(result["reasoning"])

        st.divider()

        ####################################################################
        # Indicators
        ####################################################################

        st.subheader("🔍 Spam Indicators")

        indicators = result.get("indicators", [])

        if indicators:

            for item in indicators:

                st.markdown(
                    f"""
                    <div class='warn'>
                    ✔ {item}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success("No suspicious indicators found.")

        st.divider()

        ####################################################################
        # Recommended Action
        ####################################################################

        st.subheader("✅ Recommended Action")

        st.success(result["recommended_action"])

        st.divider()

        ####################################################################
        # Raw Email
        ####################################################################

        with st.expander("View Submitted Email"):

            st.text(email_text)

####################################################################################
# Footer
####################################################################################

st.sidebar.markdown("---")

st.sidebar.info(
    """
    ### 🤖 AI Resume & Spam Analyzer

    **Features**

    - 📄 Resume Analysis
    - 📧 Spam Detection
    - 🤖 AI Insights
    - 🎯 Job Recommendations
    - ⚠ Resume Improvements

    Built using:

    - Microsoft Agent Framework
    - Azure AI Foundry
    - Azure Document Intelligence
    - FastAPI
    - Streamlit
    """
)