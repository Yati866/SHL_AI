import streamlit as st
from query import query_recommendations  # your backend file
import pandas as pd

# Page config
st.set_page_config(page_title="SHL RAG Assistant", page_icon="📘", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>📘 SHL RAG Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ask anything related to SHL assessments and get the best matched solutions</p>", unsafe_allow_html=True)

# Query input
query = st.text_input("🔍 Type your query here:", placeholder="e.g. I want a short remote cognitive test with adaptive scoring")

def format_results(results):
    formatted = []
    for res in results:
        formatted.append({
            "Assessment Name": res.get("name", "N/A"),
            "URL": f"[🔗 Link]({res.get('url', '#')})",
            "Remote": "✅" if res.get("remote_testing") else "❌",
            "Adaptive/IRT": "✅" if res.get("adaptive_irt") else "❌",
            "Test Type": res.get("test_types", "N/A"),
            "Duration": res.get("duration", "N/A"),
            "Similarity": f"{res.get('similarity', 0):.2f}"
        })
    return pd.DataFrame(formatted)

if query:
    with st.spinner("🔎 Matching assessments..."):
        try:
            results = query_recommendations(query, threshold=0.4)
            if results:
                st.success("✅ Top Matching Assessments")

                df = format_results(results)
                # Render as Markdown Table with clickable links
                st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

            else:
                st.warning("⚠️ No results found. Try changing your query.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
