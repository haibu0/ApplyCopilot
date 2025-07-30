import requests
import random
import streamlit_nested_layout
from test_values import job_desc_ph, company_website_ph
import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="ApplyCopilot", layout="centered")
st.title("🛠️ ApplyCopilot")
st.caption("AI-powered resume tailoring, cover letters, and recruiter emails — in one place.")

# --- FORM INPUTS WITH COLUMNS --- #
with st.form("application_form"):
    st.markdown("### 📄 Job Information")

    job_col1, job_col2 = st.columns(2)
    with job_col1:
        job_description = st.text_area("Job Description*", height=200, value=job_desc_ph)

    with job_col2:
        company_website = st.text_input("Company Website*", placeholder="https://example.com", value=company_website_ph)
        company_linkedin = st.text_input("Company LinkedIn", placeholder="Optional")
        cover_letter_required = st.toggle("Cover Letter Required?")
        simple_message = st.toggle("Additional Simple Message?")

    st.markdown("---")

    st.markdown("### 🙋 Applicant Details")

    file_col, profile_col = st.columns([1.2, 1.8])
    with file_col:
        resume_file = st.file_uploader("Upload Your Resume (.pdf)*", type=["pdf"])
        master_resume_file = st.file_uploader("Upload Your Master Resume (.pdf)*", type=["pdf"])
    with profile_col:
        linkedin = st.text_input("Your LinkedIn URL", placeholder="Optional")
        github = st.text_input("Your GitHub URL", placeholder="Optional")
        portfolio = st.text_input("Portfolio or Personal Website", placeholder="Optional")

    submitted = st.form_submit_button("🚀 Submit")

# --- DISPLAY SUBMISSION CONFIRMATION --- #
if submitted:
    if not job_description or not company_website or not resume_file:
        st.error("Please fill out all required fields marked with *.")
    else:
        st.success("✅ Form submitted! Processing now...")

        # -- SEND TO N8N -- #
        payload = {
            "Job Description": job_description,
            "Company Website": company_website,
            "Company LinkedIn": company_linkedin,
            "Cover Letter Required": cover_letter_required,
            "User LinkedIn": linkedin,
            "User GitHub": github,
        }
        files = {}
        if resume_file is not None:
            # This is the correct way to send files to n8n
            files["User_Resume___pdf_"] = (
                resume_file.name,  # filename
                resume_file.getvalue(),  # file content as bytes
                "application/pdf"  # MIME type
            )

        loading_text = [
            "Firing up the jet engines...",
            "Checking autopilot settings...",
            "Plotting your career trajectory...",
            "Rewriting your story at 30,000 feet...",
            "Scanning the job skies for opportunities...",
            "Running final checks on your resume runway...",
            "Assembling your application flight plan...",
            "Powering up AI copilots and coffee...",
            "Adjusting your experience for maximum altitude...",
            "Taking off towards your dream job...",
        ]
        with st.spinner(random.choice(loading_text), show_time=True):
            webhook_url = "http://localhost:5678/webhook-test/be1e32a4-6cc4-4917-bbd6-0f43609ce653"
            response = requests.post(
                webhook_url,
                data=payload,
                files=files
        )
        st.success("✅ Success!")

        n8n_response = response.json()["output"]

        # --- OUTPUT --- #
        with st.expander("📄 Resume Analysis"):
            st.markdown(n8n_response["tailored_resume"])
            with st.expander("📊 Resume Score Chart"):
                chart_data = pd.DataFrame(np.random.randn(20, 3),columns=["a", "b", "c"])
                st.area_chart(chart_data)  # Placeholder Chart

        with st.expander("✉️ Cover Letter"):
            st.markdown(n8n_response["cover_letter"])

        with st.expander("📧 Recruiter Email"):
            st.markdown(f"**Subject:** {n8n_response['recruiter_email']['subject']}")
            st.markdown(n8n_response["recruiter_email"]["body"])
            st.markdown("---")
            st.markdown(f"** 📧 Recruiter Message **")
            st.markdown(n8n_response["recruiter_message"])

            with st.expander("📝 Strategy Notes"):
                st.markdown(f"**Notes:** {n8n_response['metadata']['strategy_notes']}")
                st.markdown(f"**Tone**\n{n8n_response['metadata']['tone']}")




