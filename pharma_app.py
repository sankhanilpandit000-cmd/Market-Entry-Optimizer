import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Market Entry Intelligence AI", page_icon="🧬", layout="wide")
st.title("🧬 Market Entry Intelligence AI")
st.markdown("### Predictive analytics for pharmaceutical pipeline strategy.")
st.divider()

with st.sidebar:
    st.header("⚙️ System Configuration")
    api_key = st.text_input("Enter Google AI Studio API Key:", type="password")

query = st.text_input("Enter a Drug Category or Molecule (e.g., Immunosuppressants):", placeholder="Type here...")

if st.button("Analyze Market Viability", type="primary"):
    if not api_key:
        st.error("Please enter your Google AI Studio API Key in the sidebar.")
    elif not query:
        st.warning("Please enter a drug category to analyze.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.1-pro-preview')
        prompt = f"Act as an elite Pharmaceutical Market Strategist. Analyze the drug category: '{query}'. Provide a highly professional business intelligence report containing: 1. Current Market Landscape 2. Clinical Risk Profile (ADRs) 3. Market Entry Prediction (Chance of Success) 4. Strategic Advice."
        with st.spinner(f"Scanning global databases for '{query}'..."):
            try:
                response = model.generate_content(prompt)
                st.success("Market Intelligence Compiled Successfully.")
                with st.container(border=True):
                    st.markdown(response.text)
            except Exception as e:

                st.error(f"An error occurred: {e}")


