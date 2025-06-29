
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
        styled = f"""
        <html>
        <head>
        <style>
        body {{
        font-family: Arial, sans-serif;
        color: #333;
        line-height: 1.6;
        }}
        code {{
        background-color: #f6f8fa;
        padding: 2px 4px;
        border-radius: 4px;
        font-size: 90%;
        }}
        pre {{
        background-color: #f6f8fa;
        padding: 10px;
        border-radius: 6px;
        overflow-x: auto;
        }}
        table {{
        border-collapse: collapse;
        width: 100%;
        }}
        th, td {{
        text-align: left;
        padding: 8px;
        border: 1px solid #ddd;
        }}
        </style>
        </head>
        <body>{html}</body>
        </html>
        """
        return styled
    else:
        return f"<p><strong>Error:</strong> Wiki page not found for module <code>{module_name}</code></p>"

@app.get("/wiki")
def get_module_doc(module: str = Query(...)):
    return {"wiki": fetch_wiki_page(module)}

@app.post("/generate")
async def generate_module(request: Request):
    body = await request.json()
    # Dummy response for PR generation
    return {"pr_url": f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_git/infra/pullrequest/123"}
