from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from retriever import retrieve_from_query
from generator import MedicalGenerator

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize generator
generator = MedicalGenerator()

# Index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "answer": "", "query": ""})

# Ask endpoint
@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, query: str = Form(...)):
    # Retrieve top docs
    top_docs = retrieve_from_query(query, top_k=2)
    # Generate answer
    answer = generator.generate(query, top_docs)
    return templates.TemplateResponse("index.html", {"request": request, "answer": answer, "query": query})

# Run with: python app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
