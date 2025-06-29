
import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://copilot-backend")

st.title("Terraform Copilot Agent")

module_name = st.text_input("Enter Terraform Module Name (e.g., vpc, gke, cloudsql)")

# Step 1: Fetch wiki
if module_name:
    st.subheader("📘 Wiki Snippet: Inputs & Example")
    res = requests.get(f"{BACKEND_URL}/wiki", params={"module": module_name})
    if res.status_code == 200:
        st.markdown(res.json().get("wiki", ""))
    else:
        st.error("❌ Failed to fetch wiki")

# Step 2: Accept raw input for TF parameters
    st.subheader("✏️ Terraform Input Values")

    tf_input = st.text_area("Paste module block (or edit example):", height=250, placeholder="module \"gcs\" { ... }")

    if st.button("🚀 Generate Terraform & Create PR"):
        payload = {
            "module": module_name,
            "inputs": {
                "raw": tf_input
            }
        }
        response = requests.post(f"{BACKEND_URL}/generate", json=payload)

        if response.status_code == 200:
            data = response.json()
            if "terraform" in data:
                st.code(data["terraform"], language="hcl")
            if "pr_url" in data:
                st.success(f"✅ PR Created: [View PR]({data['pr_url']})")
        else:
            st.error("❌ Failed to generate")
