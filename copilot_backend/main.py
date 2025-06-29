
import os
from fastapi import FastAPI, Query, Request
import requests
import markdown

app = FastAPI()

ADO_ORG = "kiranmlops2025"
ADO_PROJECT = "GCP_CE_Project"
ADO_WIKI = "GCP_CE_Project.wiki"
ADO_PAT = os.environ.get("ADO_PAT")

def fetch_wiki_page(module_name):
    path = f"/{module_name}"
    url = (
        f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_apis/wiki/wikis/{ADO_WIKI}/pages"
        f"?path={path}&includeContent=true&api-version=7.1-preview.1"
    )
    res = requests.get(url, auth=("", ADO_PAT))

    if res.status_code == 200:
        markdown_content = res.json().get("content", "")
        html = markdown.markdown(
            markdown_content,
            extensions=["fenced_code", "tables", "codehilite"]
        )
        return html
    else:
        return f"<p><strong>Error:</strong> Wiki page not found for module <code>{module_name}</code></p>"

@app.get("wiki")
def get_module_doc(module: str = Query(...)):
    return {"wiki": fetch_wiki_page(module)}

@app.post("generate")
async def generate_module(request: Request):
    body = await request.json()
    # Dummy response for PR generation
    return {"pr_url": f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_git/infra/pullrequest/123"}
