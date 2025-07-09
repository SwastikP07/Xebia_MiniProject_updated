import streamlit as st
import pandas as pd
import os
import gdown

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Job Recommendation", layout="centered")
st.title("📄 Resume-Based Job Recommender")

# ---------------- GDrive Dataset Setup ----------------
csv_path = "data/jobs_dataset_with_features.csv"
drive_url = "https://drive.google.com/uc?id=1--bUAeQBYqc-rtZytUrjODVZVJ_6Ywnj"
os.makedirs("data", exist_ok=True)

@st.cache_data(show_spinner=False)
def download_and_load_data():
    if not os.path.exists(csv_path):
        gdown.download(drive_url, csv_path, quiet=False)
    return pd.read_csv(csv_path)

# ---------------- Upload Resume ----------------
uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded:
    with st.spinner("📦 Loading job dataset..."):
        try:
            job_df = download_and_load_data()
        except Exception as e:
            st.error("❌ Failed to load job dataset.")
            st.exception(e)
            st.stop()

    try:
        # Delayed import to avoid crashing before file upload
        from utils.extract import extract_text_from_pdf, extract_name, extract_skills_from_resume
        from utils.recommend import get_top_jobs

        with st.spinner("🧠 Analyzing resume..."):
            text = extract_text_from_pdf(uploaded)
            name = extract_name(text)
            skills = extract_skills_from_resume(text)
            top_jobs = get_top_jobs(skills, job_df, top_n=1)

        st.success("✅ Analysis complete!")

        st.markdown(f"### 👤 Name: **{name}**")

        st.markdown("### 🧠 Extracted Skills:")
        if skills:
            st.markdown("✅ " + ", ".join(skills))
        else:
            st.warning("No relevant skills found.")

        st.markdown("## 💼 Top Job Recommendation:")
        if not top_jobs.empty:
            row = top_jobs.iloc[0]
            st.markdown(f"#### {row['Role']}")
            st.markdown(f"[🔗 Apply on LinkedIn]({row['Link']})", unsafe_allow_html=True)
        else:
            st.warning("No suitable job found.")
    except Exception as e:
        st.error("❌ Error during resume analysis.")
        st.exception(e)

# ---------------- Original Code Reference ----------------
"""
# job_df = pd.read_csv("data/jobs_dataset_with_features.csv")
"""
