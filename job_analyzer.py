# ==============================================================================
# UI - STREAMLIT APP
# ==============================================================================

import streamlit as st
import pandas as pd
from src.services.scraper import scrape_clean_job_text
from src.services.llm_service import analyze_job_with_ai

st.markdown("""
    <style>
    /* Main Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Card Style */
    .job-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Score Circle */
    .score-container {
        text-align: center;
        border-left: 2px solid #ff4b4b;
        padding-left: 20px;
    }

    /* Tech Badge Styling */
    .tech-badge {
        display: inline-block;
        background: #1e293b;
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
        border: 1px solid #38bdf8;
    }
    
    /* Hover effects for buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8080 100%);
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Informative Sidebar (No sensitive data input)
with st.sidebar:
    st.header("🕵️ GenAI Headhunter")
    st.success("✅ API Key uploaded securely")
    st.markdown("---")
    st.write("This tool demonstrates:")
    st.write("• Web Scraping (BS4)")
    st.write("• Secure Env Variables")
    st.write("• Structured Data (Pydantic)")

st.title("🕵️ GenAI Headhunter Assistant")
st.markdown("Transform any Job Description into a structured analysis using AI.")

# Tabs
tab1, tab2 = st.tabs(["🚀 Job Analysis", "📊 Market Scan (Batch)"])

# --- TAB 1: SINGLE LINK ANALYSIS ---
with tab1:
    st.subheader("Analyze a Job URL")
    url_input = st.text_input("Enter the URL:", placeholder="https://...")
    
    if st.button("Analyze Job", key="btn_single"):
        if not url_input:
            st.warning("Please enter a URL.")
        else:
            with st.spinner("🕷️ Scraping & 🤖 AI Analysis..."):
                raw_text = scrape_clean_job_text(url_input)
            
            if "Error" in raw_text:
                st.error(raw_text)
            else:
                try:
                    data = analyze_job_with_ai(raw_text)
                    
                    # -- DISPLAY --
                    col_main, col_right = st.columns([3, 1])
                    with col_main:
                        st.divider()
                        col_h1, col_h2= st.columns([3, 1])
                        with col_h1:
                            st.markdown(f"### {data.role_title}")
                            st.caption(f"Company: **{data.company_name}** | Level: **{data.seniority}**")
                            if data.salary_range != None:
                                st.caption(f"Salary: 💰 **{data.salary_range.min} - {data.salary_range.max} {data.salary_range.currency} {data.salary_range.frequency}**")
                            st.caption(f"📍 Location: **{data.job_location.city}, {data.job_location.country}**")
                            st.markdown('<div class="job_card">', unsafe_allow_html=True)
                        with col_h2:
                            st.markdown(f"""
                                <div class="score-container">
                                <p style="margin-bottom:0;">Quality Score</p>
                                <h1 style="color:#ff4b4b; font-size: 3rem;">{data.match_score}<span style="font-size:1.2rem; color:grey;">/100</span></h1>
                                </div>
                            """, unsafe_allow_html=True)

                        # Details
                        c1, c2, c3 = st.columns(3)
                        c1.info(f"**Remote:** {'Yes' if data.job_location.is_remote else 'No'}")
                        c2.success(f"**Tehnology:** {len(data.tech_stack)}")
                        c3.error(f"**Red Flags:** {len(data.red_flags)}")

                        st.markdown(f"**📝 Summary:** {data.summary}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.subheader("🛠️ Tech Stack")
                        tech_html = "".join([f'<span class="tech-badge">{tech}</span>' for tech in data.tech_stack])
                        st.markdown(tech_html, unsafe_allow_html=True)

                    with col_right:
                        st.markdown("#### 🚩 Warnings")
                        if data.red_flags:    
                            for flag in data.red_flags:
                                st.warning(f"⚠️ {flag.category.capitalize()} ({flag.severity})")

                except Exception as e:
                    st.error(f"AI Error: {str(e)}")

# --- TAB 2: BATCH PROCESSING ---
with tab2:
    st.subheader("📊 Compare multiple jobs")
    urls_text = st.text_area("Paste URLs (one per line):", height=150)
    
    if st.button("Scan the Market", key="btn_batch"):
        urls = [u.strip() for u in urls_text.split('\n') if u.strip()]
        
        if not urls:
            st.warning("You have not entered any links.")
        else:
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, link in enumerate(urls):
                status_text.text(f"Analyze {i+1}/{len(urls)}...")
                text = scrape_clean_job_text(link)
                
                if "Error" not in text:
                    try:
                        res = analyze_job_with_ai(text)
                        results.append({
                            "Role": res.role_title,
                            "Company": res.company_name,
                            "Seniority": res.seniority,
                            "Tech": res.tech_stack,
                            "Score": res.match_score
                        })
                    except:
                        pass
                
                progress_bar.progress((i + 1) / len(urls))
            
            status_text.text("Done!")
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
                
                # Grafic simplu
                st.bar_chart(df['Seniority'].value_counts())