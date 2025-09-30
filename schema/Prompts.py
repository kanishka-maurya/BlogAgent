import json

#----------------------------------------------------------------------------------------------------------------------------------------------
# System Prompts
#----------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------------------
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ORCHESTRATOR PROMPT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#----------------------------------------------------------------------------------------------------------------------------------------------

SCHEMA_ORCHESTRATOR = {
  "type": "object",
  "properties": {
    "topic_analysis": { "type": "string" },
    "target_audience": { "type": "string" },
    "sub_sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "section_type": { "type": "string" },
          "description": { "type": "string" },
          "style_guide": { "type": "string" },
          "word_count": { "type": "integer" }
        },
        "required": ["section_type", "description", "style_guide", "word_count"],
        "additionalProperties": False
      }
    }
  },
  "required": ["topic_analysis", "target_audience", "sub_sections"],
  "additionalProperties": False
}

ORCHESTRATOR_PROMPT = """
You are the Blog Orchestrator. Your role is to analyze the given topic and design a clear, logical blog structure.

Topic: {topic}
Target Length: {target_length} words
Style: {style}

### Instructions:
1. Break the blog into logical sections that flow naturally from one to another.
2. For each section, specify:
   - Type (e.g., Introduction, How-to, Case Study, Analysis, FAQ, Conclusion)
   - Style Guide (tone, voice, perspective, formatting considerations)
3. Ensure the sections build narrative flow (hook → depth → resolution).
"""


#----------------------------------------------------------------------------------------------------------------------------------------------
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WORKER PROMPT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#----------------------------------------------------------------------------------------------------------------------------------------------

SCHEMA_WORKER = {
  "type": "object",
  "properties": {
    "content": { "type": "string" },
    "key_points": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    }
  },
  "required": ["content", "key_points"],
  "additionalProperties": False
}

WORKER_PROMPT = """
You are the Blog Writer. Write one section of a blog post based on the provided outline.

Topic: {topic}
Section Type: {section_type}
Section Goal: {description}
Style Guide: {style_guide}
Word Count: {word_count}
Previous Sections of the Blog: {previous_sections}

### Instructions:
- Stick to the section’s goal.
- Follow the style guide (tone, voice, formatting).
- Use examples, lists, or storytelling where helpful.
- Keep length appropriate (balanced depth, avoid fluff).
- Make sure the section can connect smoothly with others.
"""


#----------------------------------------------------------------------------------------------------------------------------------------------
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> REVIEWER PROMPT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#----------------------------------------------------------------------------------------------------------------------------------------------

SCHEMA_REVIEWER = {
  "type": "object",
  "properties": {
    "cohesion_score": { "type": "number" },
    "suggested_edits": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "section_name": { "type": "string" },
          "suggested_edit": { "type": "string" }
        },
        "required": ["section_name", "suggested_edit"],
        "additionalProperties": False
      }
    },
    "final_version": { "type": "string" }
  },
  "required": ["cohesion_score", "suggested_edits", "final_version"],
  "additionalProperties": False
}

REVIEWER_PROMPT = """
You are the Blog Reviewer. Review the full draft for flow, cohesion, and polish.

Topic: {topic}
Target Audience: {audience}
Sections: {sections}

### Instructions:
1. Assign a Cohesion Score (0.0–1.0):
   - 1.0 = seamless flow, perfect cohesion
   - 0.7–0.9 = mostly cohesive, minor transitions/tone issues
   - <0.7 = weak cohesion, major improvements needed
2. Suggest edits for each section if necessary (tone, clarity, transitions).
3. Identify if tone/style is consistent across sections.
4. For suggested edits, focus on improving transitions and maintaining consistent tone across sections.
5. The final version should incorporate your suggested improvements into a polished, cohesive blog post.
"""

