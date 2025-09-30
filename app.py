from fastapi import FastAPI
from orchestrator import BlogOrchestrator  
from pydantic import BaseModel, Field 
from fastapi.responses import JSONResponse


app = FastAPI()
orchestrator = BlogOrchestrator()


class UserInput(BaseModel):
    topic: str = Field(..., description="The main topic of the blog.")
    target_length: int = Field(..., description="Desired length of the blog.")
    style: str = Field(..., description="Writing style for the blog.")

@app.post("/generate-blog")
def generate_blog(data: UserInput):

    try:
        result = orchestrator.write_blog(
            topic=data.topic, target_length=data.target_length, style=data.style
        )
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

