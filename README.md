# ApplyCopilot

ApplyCopilot is your AI-powered assistant for tailoring job applications — built with **n8n**, **Streamlit**, and a bunch of helpful agents behind the scenes.

It scans your resume, analyzes job descriptions, pulls company intel, and spits out a tailored resume, cover letter, and recruiter email. You upload a PDF, fill in a few fields, and let the system do the thinking.

This started as a working prototype. It's not finished. It probably never will be. But it's getting smarter and faster with every version.


## 🧠 What It Does

* 📄 **Reads your resume**
  Uses OCR to extract clean text from PDFs.

* 🧾 **Breaks down job descriptions**
  Pulls required skills, values, and tone from raw JD text.

* 🛠 **Tailors your resume**
  Rewrites relevant bullet points using action verbs and job keywords.

* 🏢 **Scrapes company websites**
  Finds mission statements, tone, values, and recent updates to match your writing style.

* ✍️ **Writes your cover letter**
  Uses resume and company info to generate a 3-paragraph letter in the right tone.

* 📧 **Generates recruiter emails**
  Short, clean outreach message to go with your application.

* 📦 **Packages everything**
  Final output is formatted for copy-paste or Google Docs export.


## 🧰 Tech Stack

* `n8n` for orchestration
* `Streamlit` for the UI
* `Mistral API` for OCR
* `Google Gemini` for all language agents
* `Google Docs API` (optional) for final output delivery


## 🧪 Status

✅ First successful run
⚠️ Everything is subject to change
🚧 More structure, logic, and automation coming soon
🧩 Agents will become more modular and better connected over time

This is an MVP with high standards. It will keep evolving until it's something worth using every time you apply.


## 🛠 How to Use

1. Open the Streamlit frontend
2. Upload your resume and paste the job description
3. Optionally enter company website or LinkedIn
4. Submit and let ApplyCopilot do the rest

