import requests
import random
import streamlit_nested_layout
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import sqlite3, os, json
from docx import Document
from io import BytesIO

st.set_page_config(page_title="ApplyCopilot", layout="centered", initial_sidebar_state="collapsed")

# --- SESSION STATE SETUP --- #
if "form_version" not in st.session_state:
    st.session_state.form_version = 0
if "n8n_response" not in st.session_state:
    st.session_state.n8n_response = None

# def reset_form():
#     """Reset just the application form + outputs, keep the app running."""
#     # Clear text/toggles
#     defaults = {
#         "job_description": "",
#         "company_website": "",
#         "company_linkedin": "",
#         "cover_letter_required": False,
#         "resume_analysis_requests": "",
#         "recruiter_message_requests": "",
#         "cover_letter_requests": "",
#         "linkedin": "",
#         "github": "",
#         "portfolio": "",
#     }
#     st.session_state.update(defaults)
#
#     # Clear files by bumping form_version so the uploaders get new keys
#     st.session_state.form_version += 1
#
#     # Clear outputs
#     st.session_state.n8n_response = None


# Using "with" notation
with st.sidebar:
    st.markdown("# Run History")
    st.button("*" + "Community Outreach Marketer2" + "*")
    st.button("*" + "Community Outreach Marketer" + "*")
    # Optional: full reset that truly nukes everything in session
    # if st.button("🧹 Full Reset (clear all state)"):
    #     st.session_state.clear(); st.rerun()

st.title("🛠️ ApplyCopilot")
st.caption("AI-powered resume tailoring, cover letters, and recruiter emails — in one place.")

# --- FORM INPUTS WITH COLUMNS --- #
with st.form("application_form"):
    st.markdown("### 📄 Job Information")

    job_col1, job_col2 = st.columns(2)
    with job_col1:
        job_description = st.text_area(
            "Job Description*",
            height=200,
            key="job_description",
        )

    with job_col2:
        company_website = st.text_input("Company Website", placeholder="https://example.com", key="company_website")
        company_linkedin = st.text_input("Company LinkedIn", placeholder="Optional", key="company_linkedin")
        cover_letter_required = st.toggle("Cover Letter Required?", key="cover_letter_required")
        with st.popover("Make Specific Requests"):
            resume_analysis_requests = st.text_area("Resume Analysis Specific Requests", height=70, key="resume_analysis_requests")
            recruiter_message_requests = st.text_area("Recruiter Message/Email Specific Requests", height=70, key="recruiter_message_requests")
            if cover_letter_required:
                cover_letter_requests = st.text_area("Cover Letter Requests", height=70, key="cover_letter_requests")

    st.markdown("---")

    st.markdown("### 🙋 Applicant Details")
    file_col, profile_col = st.columns([1.2, 1.8])
    with file_col:
        # Use versioned keys so uploader truly resets when we bump form_version
        resume_file = st.file_uploader(
            "Upload Your Resume (.pdf)*",
            type=["pdf"],
            key=f"resume_file_{st.session_state.form_version}"
        )
        master_resume_file = st.file_uploader(
            "Upload Your Master Resume (.pdf)*",
            type=["pdf"],
            key=f"master_resume_file_{st.session_state.form_version}"
        )
    with profile_col:
        linkedin = st.text_input("Your LinkedIn URL", placeholder="Optional", key="linkedin")
        github = st.text_input("Your GitHub URL", placeholder="Optional", key="github")
        portfolio = st.text_input("Portfolio or Personal Website", placeholder="Optional", key="portfolio")

    submitted = st.form_submit_button("🚀 Submit")

# --- SUBMISSION HANDLER --- #
if submitted:
    # Check for required fields first
    if not st.session_state.job_description or not st.session_state.get(f"resume_file_{st.session_state.form_version}"):
        st.error("Please fill out all required fields marked with *.")
    # New check for the cover letter confirmation
    elif not st.session_state.cover_letter_required:
        if "confirm_no_cover_letter" not in st.session_state:
            st.session_state.confirm_no_cover_letter = False

        if not st.session_state.confirm_no_cover_letter:
            st.warning(
                "⚠️ **Cover Letter Required?** is unchecked. Are you sure you don't want a cover letter generated?")
            if st.button("Yes, Proceed Without Cover Letter"):
                st.session_state.confirm_no_cover_letter = True
                st.rerun()
            elif st.button("No, Include Cover Letter in Response"):
                # 🔧 FIX: update session state, not a local variable
                st.session_state.cover_letter_required = True
                st.rerun()
            else:
                st.stop()

        # If confirmed, proceed to the final 'else' block below

    # If all required fields are filled AND cover letter is checked or confirmed to be skipped
    else:
        # Reset confirmation state if it was set (important if they change their mind later)
        if "confirm_no_cover_letter" in st.session_state:
            del st.session_state.confirm_no_cover_letter

        st.success("✅ Form submitted! Processing now...")

        payload = {
            "Job Description": st.session_state.job_description,
            "Company Website": st.session_state.company_website,
            "User LinkedIn": st.session_state.linkedin,
            "User GitHub": st.session_state.github,
            "Recruiter Message Requests": st.session_state.recruiter_message_requests,
            # 🔧 FIX: include these so backend knows to generate a cover letter
            "Cover Letter Required": st.session_state.cover_letter_required,
            "Cover Letter Requests": st.session_state.get("cover_letter_requests", ""),
        }

        files = {}
        up = st.session_state.get(f"resume_file_{st.session_state.form_version}")
        if up is not None:
            files["User_Resume___pdf_"] = (up.name, up.getvalue(), "application/pdf")

        loading_text = [
            "Firing up the jet engines...",
            # ... (rest of your loading text)
            "Taking off towards your dream job...",
        ]

        with st.spinner(random.choice(loading_text), show_time=True):
            webhook_url = "http://localhost:5678/webhook/be1e32a4-6cc4-4917-bbd6-0f43609ce653"
            response = requests.post(webhook_url, data=payload, files=files)

        st.success("✅ Success!")

        # Store output in session so it survives reruns and can be cleared on reset
        st.session_state.n8n_response = response.json().get("output")

# --- OUTPUT SECTION --- #
if st.session_state.n8n_response:

    # -- Start by saving output to DB -- #
    n8n_response = st.session_state.n8n_response

    # -- Now Display Outputs -- #
    with st.expander("📊 Resume Score Chart"):
        ratings, theta = [], []
        for k, v in n8n_response["resume_stats"].items():
            ratings.append(v);
            theta.append(k)
        ratings = ratings + [ratings[0]]
        theta = theta + [theta[0]]

        avg_score = np.mean(ratings[:-1])


        def score_to_rgba(score, vmin=0, vmax=100, alpha=0.4):
            norm = np.clip((score - vmin) / (vmax - vmin), 0, 1)
            r = int(255 * (1 - norm));
            g = int(255 * norm);
            b = 80
            return f"rgba({r},{g},{b},{alpha})"


        fill_color = score_to_rgba(avg_score)
        line_color = fill_color.replace(f",{fill_color.split(',')[-1]}", ",1.0)")

        fig = go.Figure(go.Scatterpolar(
            r=ratings, theta=theta, mode="lines+markers", line_shape="spline",
            fill="toself", fillcolor=fill_color,
            line=dict(color=line_color, width=2),
            marker=dict(size=8, color=line_color, line=dict(width=1, color="white")),
            hovertemplate="%{theta}: %{r}<extra></extra>"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=20, b=0),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=False, range=[0, 100], gridcolor="rgba(200,200,200,0.5)", gridwidth=1),
                angularaxis=dict(tickfont=dict(size=12, family="Arial"),
                                 gridcolor="rgba(200,200,200,0.5)", gridwidth=1),
            ),
            annotations=[dict(text=f"{avg_score:.0f}", x=0.5, y=0.5, xref="paper", yref="paper",
                              showarrow=False, font=dict(size=28, family="Arial", color=line_color))]
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown(n8n_response["coverageSummary"])

    with st.expander("📄 Resume Analysis"):
        st.markdown(n8n_response["tailored_resume"])

    with st.expander("✉️ Cover Letter"):
        if st.session_state.cover_letter_required:
            if n8n_response.get("cover_letter"):
                cover_letter_text = n8n_response["cover_letter"]
                st.markdown(cover_letter_text)

                # --- Convert to .docx for download ---
                docx_buffer = BytesIO()
                doc = Document()
                for line in cover_letter_text.split("\n"):
                    doc.add_paragraph(line)
                doc.save(docx_buffer)
                docx_buffer.seek(0)

                st.download_button(
                    label="⬇️ Download Cover Letter (.docx)",
                    data=docx_buffer,
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            else:
                st.write("Cover letter was requested, but the backend didn't return one.")

    with st.expander("📧 Recruiter Email / Simple Chat Message"):
        st.markdown(f"**Subject:** {n8n_response['recruiter_email']['subject']}")
        st.markdown(n8n_response["recruiter_email"]["body"])
        st.markdown("---")
        st.markdown("**📧 Recruiter Message**")
        st.markdown(n8n_response["recruiter_message"])
        with st.expander("📝 Strategy Notes"):
            st.markdown(f"**Notes:** {n8n_response['metadata']['strategy_notes']}")
            st.markdown(f"**Tone**\n{n8n_response['metadata']['tone']}")

    # 🔄 Reset button appears with results
    # st.button("🔄 Reset for New Application", type="secondary", on_click=reset_form)
    # Rerun to refresh the UI instantly
    # st.rerun()