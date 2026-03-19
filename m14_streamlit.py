import streamlit as st

st.title("TrainerBot")
st.caption("Ask your course materials anything")

# File uploader
uploaded = st.file_uploader("Upload PDF", type="pdf")

if uploaded:
    st.success("PDF loaded!")
    question = st.text_input("Your question:")
    if question:
        st.write("Answer: coming soon...")