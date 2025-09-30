from pydantic import BaseModel, Field 
from typing import Optional, List, Dict

#----------------------------------------------------------------------------------------------------------------------------------------------
# Data Models for Blog Writing Orchestration System
#----------------------------------------------------------------------------------------------------------------------------------------------
class SubTask(BaseModel):
    """Blog section task defined by orchestrator"""

    section_type: str = Field(..., description="Type of blog section to write. E.g., Introduction, Conclusion.")
    description: str = Field(..., description="Description of the section to be written.")
    style_guide: str = Field(description="Writing style for this section depending upon the topic.")
    word_count: int = Field(..., description="Word count for the section.")


class OrchestratorPlan(BaseModel):
    """Orchestrator's blog structure and tasks"""

    topic_analysis: str = Field(..., description="Analysis of the blog topic.")
    target_audience: str = Field(..., description="Description of the target audience.")
    sub_sections: List[SubTask] = Field(..., description="List of sub-tasks for writing the blog.")


class SectionContent(BaseModel):
    """Content written by a worker"""

    content: str = Field(..., description="Content of the blog section.")
    key_points: List[str] = Field(...,description="Main points covered.")


class SuggestedEdits(BaseModel):
    """Suggested edits for a section"""

    section_name: str = Field(description="Name of the section.")
    suggested_edit: str = Field(description="Suggested edit.")


class ReviewFeedback(BaseModel):
    """Final review and suggestions"""

    cohesion_score: float = Field(description="How well sections flow together (0-1).")
    suggested_edits: List[SuggestedEdits] = Field(
        description="Suggested edits by section."
    )
    final_version: str = Field(description="Complete, polished blog post.")