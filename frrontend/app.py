import streamlit as st
import requests

st.set_page_config(page_title="EdTech Assistant", layout="wide")

st.title("🎓 EdTech Assistant")
st.markdown("Ask questions or request practice materials")

query = st.text_area("Enter your question:", height=100,
                     placeholder="E.g., 'Explain photosynthesis' or 'Give me math practice questions'")

if st.button("Get Answer", type="primary"):
    if query.strip():
        with st.spinner("Processing your question..."):
            try:
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"query": query.strip()},
                    timeout=30
                )

                if response.status_code == 422:
                    st.error("Server couldn't process the request format. Please try again.")
                    st.stop()

                response.raise_for_status()
                data = response.json()

                st.subheader("Answer:")
                st.markdown(data["response"])

                with st.expander("Technical Details"):
                    st.markdown(f"**Agent used:** {data['agent']}")
                    st.markdown("**Debug Info:**")
                    st.code(response.text, language="json")

            except requests.exceptions.RequestException as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question")