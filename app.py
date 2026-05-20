import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agents import PlannerAgent, ContentAgent, OptimizerAgent
from memory import get_past_topics_for_niche, add_to_memory

app = FastAPI(title="Content Forge AI API")

# Request Model
class GenerationRequest(BaseModel):
    niche: str
    audience: str
    platform: str
    goals: str = "Maximize engagement and virality"

# Response Model (matching the frontend needs)
class GenerationResponse(BaseModel):
    idea_title: str
    idea_description: str
    script: str
    caption: str
    hooks: list[str]
    seo_keywords: list[str]
    hashtags: list[str]

# API Endpoint
@app.post("/api/generate", response_model=GenerationResponse)
async def generate_content(req: GenerationRequest):
    try:
        planner = PlannerAgent()
        content = ContentAgent()
        optimizer = OptimizerAgent()
        
        # 1. Memory Check
        past_topics = get_past_topics_for_niche(req.niche)
        
        # 2. Planning
        planner_output = planner.generate_ideas(
            niche=req.niche,
            target_audience=req.audience,
            goals=req.goals,
            platform=req.platform,
            past_topics=past_topics
        )
        best_idx = planner_output.best_idea_index
        if best_idx < 0 or best_idx >= len(planner_output.ideas):
            best_idx = 0
        selected_idea = planner_output.ideas[best_idx]
        
        # 3. Content Draft
        draft = content.create_content(
            idea_title=selected_idea.title,
            idea_description=selected_idea.description,
            platform=req.platform,
            target_audience=req.audience
        )
        
        # 4. Optimization
        optimized = optimizer.optimize_content(
            draft_script=draft.script,
            draft_caption=draft.caption,
            platform=req.platform
        )
        
        # 5. Save to Memory
        add_to_memory(
            topic=selected_idea.title,
            platform=req.platform,
            niche=req.niche,
            script=optimized.final_script,
            hashtags=optimized.hashtags
        )
        
        return GenerationResponse(
            idea_title=selected_idea.title,
            idea_description=selected_idea.description,
            script=optimized.final_script,
            caption=optimized.final_caption,
            hooks=optimized.hooks,
            seo_keywords=optimized.seo_keywords,
            hashtags=optimized.hashtags
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")
