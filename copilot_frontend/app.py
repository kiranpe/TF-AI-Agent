
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
        wiki_content = res.json().get("wiki", "").strip()

        if wiki_content.lower().startswith("wiki page not found") or "not found" in wiki_content.lower():
            st.warning("⚠️ Module wiki not found. Please check the module name.")
        else:
            # Show Wiki content
            st.subheader("📘 Wiki Snippet: Inputs & Example")
            st.markdown(wiki_content)

            # Step 2: Accept user-provided input block
            st.subheader("✏️ Terraform Input Values")
            tf_input = st.text_area(
                "Paste or edit the module block:",
                height=250,
                placeholder="module \"gcs\" {\n  name = \"...\"\n  location = \"...\"\n versioning = \"...\"\n}"
            )

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
    else:
        st.error(f"❌ Wiki fetch failed: {res.status_code}")
