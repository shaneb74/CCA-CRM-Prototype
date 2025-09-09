
import streamlit as st

def section(title):
    st.subheader(title)
    st.write("")

def kpi(label, value, help_text=""):
    st.metric(label, value, help_text)

def table(rows):
    st.dataframe(rows, hide_index=True, use_container_width=True)

def pills(items):
    if not items:
        st.write("—")
    else:
        st.write(", ".join(items))
