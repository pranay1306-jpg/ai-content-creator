import os
import json
import time
from google import genai
from google.genai import types
from pydantic import ValidationError

from models import PlannerOutput, ContentDraft, OptimizedContent

class BaseAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it to use the agents.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def _generate_structured_response(self, prompt, schema_class, retries=3):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema_class,
                        temperature=0.7
                    ),
                )
                return schema_class.model_validate_json(response.text)
            except Exception as e:
                if attempt < retries - 1:
                    print(f"⚠️ API Error (Attempt {attempt+1}/{retries}). Retrying in 2 seconds... Error: {e}")
                    time.sleep(2)
                else:
                    print(f"❌ Final Error generating structured response: {e}")
                    raise

class PlannerAgent(BaseAgent):
    def generate_ideas(self, niche, target_audience, goals, platform, past_topics):
        print(f"🕵️ Planner Agent: Brainstorming ideas for {niche}...")
        
        past_topics_str = ", ".join(past_topics) if past_topics else "None"
        
        prompt = f"""
        You are an expert Content Strategy Planner.
        
        Niche: {niche}
        Target Audience: {target_audience}
        Goals: {goals}
        Platform: {platform}
        
        Past topics already covered (DO NOT REPEAT THESE): {past_topics_str}
        
        Your task is to generate 5 unique, highly relevant, and trend-aware content ideas.
        Rank them and identify the best idea overall based on trend potential.
        Ensure your ideas are fresh and practical.
        """
        return self._generate_structured_response(prompt, PlannerOutput)


class ContentAgent(BaseAgent):
    def create_content(self, idea_title, idea_description, platform, target_audience):
        print(f"✍️ Content Agent: Drafting content for '{idea_title}'...")
        
        prompt = f"""
        You are an expert Content Creator.
        
        Topic: {idea_title}
        Description: {idea_description}
        Platform: {platform}
        Target Audience: {target_audience}
        
        Write a draft script, a draft caption, and a strong call-to-action (CTA).
        Adjust your tone to perfectly match the target audience and platform expectations.
        Include platform-specific tips.
        """
        return self._generate_structured_response(prompt, ContentDraft)


class OptimizerAgent(BaseAgent):
    def optimize_content(self, draft_script, draft_caption, platform):
        print("🚀 Optimizer Agent: Polishing content and injecting SEO/hooks...")
        
        prompt = f"""
        You are a highly skilled Content Optimizer and Growth Hacker.
        
        Draft Script:
        {draft_script}
        
        Draft Caption:
        {draft_caption}
        
        Platform: {platform}
        
        Your job is to optimize this content to maximize engagement and virality.
        1. Improve the draft with strong, punchy phrasing.
        2. Provide 2-3 alternative strong hooks for the first 2 seconds of the video/post.
        3. Extract 5-10 SEO keywords.
        4. Generate relevant hashtags.
        Keep writing concise and highly engaging.
        """
        return self._generate_structured_response(prompt, OptimizedContent)
