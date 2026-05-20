from pydantic import BaseModel, Field
from typing import List

class ContentIdea(BaseModel):
    title: str = Field(description="The title or core concept of the content idea.")
    description: str = Field(description="A brief description of what the content will be about.")
    rationale: str = Field(description="Why this is a good idea based on current trends and the niche.")
    trend_potential: int = Field(description="Score out of 10 for how likely this is to perform well.")

class PlannerOutput(BaseModel):
    ideas: List[ContentIdea] = Field(description="List of 5 unique content ideas.")
    best_idea_index: int = Field(description="The 0-based index of the recommended best idea from the list.")

class ContentDraft(BaseModel):
    script: str = Field(description="The draft script for the video or post.")
    caption: str = Field(description="The draft caption for the post.")
    cta: str = Field(description="The call to action.")
    platform_specific_tips: str = Field(description="Any tips on how to format or present this on the specific platform.")

class OptimizedContent(BaseModel):
    final_script: str = Field(description="The optimized and viral-friendly script with strong hooks.")
    final_caption: str = Field(description="The optimized caption, keeping it concise and engaging.")
    hooks: List[str] = Field(description="A list of 2-3 strong alternative hooks for the first 2 seconds.")
    seo_keywords: List[str] = Field(description="List of 5-10 SEO keywords relevant to the topic.")
    hashtags: List[str] = Field(description="List of relevant hashtags.")
