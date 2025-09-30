from typing import Dict
import os
import logging
import json
from groq import Groq
from dotenv import load_dotenv
from schema.Prompts import SCHEMA_ORCHESTRATOR, SCHEMA_WORKER, SCHEMA_REVIEWER
from schema.DataModels import OrchestratorPlan, SubTask, SectionContent, ReviewFeedback
from schema.Prompts import ORCHESTRATOR_PROMPT, WORKER_PROMPT, REVIEWER_PROMPT

load_dotenv()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

class BlogOrchestrator:
    def __init__(self):
        self.sections_content = {}
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])

    def get_plan(self, topic: str, style: str, target_length: int) -> OrchestratorPlan:
        """Get orchestrator's blog structure plan"""
        
        # Prompt the orchestrator to create a blog structure
        orchestrator_prompt = ORCHESTRATOR_PROMPT.format(
            topic=topic,
            style=style,
            target_length=target_length)
        
        # Model call to get the blog plan
        response = self.client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct", 
        messages=[
            {"role": "system", "content": "You are a helpful Orchestrator."},
            {"role": "user", "content": orchestrator_prompt}
        ],
        response_format={"type": "json_schema", 
                         "json_schema": {
                                        "name": "orchestrator_schema",
                                        "schema": SCHEMA_ORCHESTRATOR
                                        }
                        }
        )
        raw_output = response.choices[0].message.content

        # Response validation
        try:
            result = OrchestratorPlan.model_validate_json(raw_output)
            return result
        except Exception as e:
            print("❌ JSON validation failed:", e)
            return None
        

    def write_section(self, topic: str, sub_task: SubTask) -> SectionContent:
        """Write a blog section-based on the sub-task"""
        
        # Previous sections context
        previous_sections = "\n\n".join(
            [
                f"=== {section_type} ===\n{content.content}"
                for section_type, content in self.sections_content.items()
            ])
        
        # Prompt the worker to write the section
        worker_prompt = WORKER_PROMPT.format(topic=topic,
                                        section_type=sub_task.section_type,
                                        description=sub_task.description,
                                        style_guide=sub_task.style_guide,
                                        word_count=sub_task.word_count,
                                        previous_sections=previous_sections if previous_sections else "This is the first Section.")
        
        # Model call to write the section
        response = self.client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct", 
        messages=[
            {"role": "system", "content": "You are a helpful Blog Section Writer."},
            {"role": "user", "content": worker_prompt}
        ],
        response_format = {
                            "type": "json_schema",
                            "json_schema": {
                                "name": "worker_schema",
                                "schema": SCHEMA_WORKER
                                  }
                          }
        )
        raw_output = response.choices[0].message.content

        # Response validation
        try:
            result = SectionContent.model_validate_json(raw_output)
            return result
        except Exception as e:
            print("❌ JSON validation failed:", e)
            return None
        

    def review_post(self, topic: str, plan: OrchestratorPlan) -> ReviewFeedback:
        """Reviewer: Analyze and improve overall cohesion"""

        # Combine all sections for review
        sections_text = "\n\n".join(
            [
                f"=== {section_type} ===\n{content.content}"
                for section_type, content in self.sections_content.items()
            ])

        # Prompt the reviewer to analyze and improve the blog post
        reviewer_prompt = REVIEWER_PROMPT.format(
            topic=topic,
            audience=plan.target_audience,
            sections=sections_text
        )
        
        # Model call to review the blog post
        response = self.client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct", 
        messages=[
            {"role": "system", "content": "You are a helpful Blog Post Reviewer."},
            {"role": "user", "content": reviewer_prompt}
        ],
        response_format = {
                            "type": "json_schema",
                            "json_schema": {
                                "name": "reviewer_schema",
                                "schema": SCHEMA_REVIEWER
                            }
                        }
        )
        raw_output = response.choices[0].message.content

        # Response validation
        try:
            result = ReviewFeedback.model_validate_json(raw_output)
            return result
        except Exception as e:
            print("❌ JSON validation failed:", e)
            return None
        

    def write_blog(self, topic: str, target_length: int = 1000, style: str = "informative") -> Dict:
        """Process the entire blog writing task"""

        # Get blog structure plan
        plan = self.get_plan(topic, target_length, style)
        
        # Write each section
        for section in plan.sub_sections:
            content = self.write_section(topic, section)
            self.sections_content[section.section_type] = content

        # Review and polish
        review = self.review_post(topic, plan)

        return {"Blog": review.final_version}


