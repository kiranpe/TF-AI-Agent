
import os
from fastapi import FastAPI, Query, Request
import requests

app = FastAPI()

ADO_ORG = "kiranmlops2025"
ADO_PROJECT = "GCP_CE_Project"
ADO_WIKI = "GCP_CE_Project.wiki"
ADO_PAT = os.environ.get("ADO_PAT")


def extract_sections(md, sections=["## Inputs", "## Example"]):
    output = []
    for section in sections:
        pattern = re.escape(section) + r"(.*?)(?=\n## |\Z)"  # up to next ## or end 
        match = re.search(pattern, md, flags=re.DOTALL | re.IGNORECASE)
        if match:
            output.append(section + match.group(1).rstrip())
    return "\n\n".join(output)

def fetch_wiki_page(module_name):
    path = f"/{module_name}"
    url = (
        f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_apis/wiki/wikis/{ADO_WIKI}/pages"
        f"?path={path}&includeContent=true&api-version=7.1-preview.1"
    )
    res = requests.get(url, auth=("", ADO_PAT))

    if res.status_code == 200:
        markdown_content = res.json().get("content", "")
        filtered_md = extract_sections(markdown_content)
        return filtered_md or "Requested sections not found in the wiki page."
    else:
        return f"Error: Wiki page not found for module {module_name}"

@app.get("/wiki")
def get_module_doc(module: str = Query(...)):
    return {"wiki": fetch_wiki_page(module)}

@app.post("/generate")
async def generate_module(request: Request):
    body = await request.json()
    # Dummy response for PR generation
    return {"pr_url": f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_git/infra/pullrequest/123"}
