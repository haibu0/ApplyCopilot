import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ApplyCopilot",
    page_icon="🤖",
    layout="wide"
)

# Title and subtitle
st.markdown("# 🤖 ApplyCopilot")
st.markdown("---")
st.markdown(
    "_Your AI-powered assistant for tailoring resumes, cover letters, and recruiter emails._"
)

# Sidebar inputs
with st.sidebar:
    st.header("Inputs")
    resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    job_description = st.text_area("Job Description", height=200)
    company_url = st.text_input("Company Website (optional)")
    linkedin = st.text_input("LinkedIn URL (optional)")
    github = st.text_input("GitHub URL (optional)")
    portfolio = st.text_input("Portfolio URL (optional)")
    cover_letter_option = st.radio(
        "Generate Cover Letter?", ("Yes", "No"), index=0
    )
    generate_button = st.button("Generate Outputs")

# Main content area
if generate_button:
    st.spinner(text="Running ApplyCopilot agents...")
    # Placeholder containers for results
    tab1, tab2, tab3 = st.tabs(["Tailored Resume", "Cover Letter", "Recruiter Email"])

    with tab1:
        st.subheader("✏️ Tailored Resume")
        st.info("Your tailored resume bullets will appear here.")

    if cover_letter_option == "Yes":
        with tab2:
            st.subheader("📝 Cover Letter")
            st.info("Your personalized cover letter will appear here.")
    else:
        tab2.empty()

    with tab3:
        st.subheader("📧 Recruiter Email")
        st.info("Your recruiter outreach email will appear here.")

else:
    st.info("Fill out the inputs in the sidebar and click Generate Outputs.")
