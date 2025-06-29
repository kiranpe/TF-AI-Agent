
import streamlit as st
import requests
import os
import streamlit.components.v1 as components

BACKEND_URL = os.getenv("BACKEND_URL", "http://copilot-backend/api")

st.title("Terraform Copilot Agent")

module_name = st.text_input("Enter Terraform Module Name (e.g., vpc, gke, cloudsql)")

if module_name:
    response = requests.get(f"{BACKEND_URL}/api/wiki", params={"module": module_name})

    if response.status_code == 200:
        html_content = response.json().get("wiki", "<p>No content found.</p>")
        components.html(html_content, height=600, scrolling=True)
    else:
        st.error(f"Failed to fetch wiki. Status: {response.status_code}")

if st.button("Show Module Wiki"):
    if not module_name:
        st.warning("Please enter a module name.")
    else:
        res = requests.get(f"{BACKEND_URL}/api/wiki", params={"module": module_name})
        wiki = res.json().get("wiki", "Module not found.")
        st.markdown(wiki)

st.markdown("---")
st.subheader("Enter Parameters for Module")

param_input = st.text_area("Enter input values as JSON", value='{}')

if st.button("Generate Terraform & Create PR"):
    if not module_name or not param_input:
        st.warning("Please provide both module name and parameter values.")
    else:
        try:
            params = eval(param_input)
            res = requests.post(f"{BACKEND_URL}/api/generate", json={
                "module_name": module_name,
                "parameters": params
            })
            pr_url = res.json().get("pr_url")
            st.success("Pull Request Created!")
            st.write(f"[View PR]({pr_url})")
        except Exception as e:
            st.error(f"Error in input: {e}")
