# Blog Agent

<aside>
💡

**Description**
</aside>

**Blog Agent** is an AI-powered tool that generates well-structured blog posts from a topic provided by the user. The agent takes inputs like **Topic**, **Style**, and **Length**, then runs a multi-step workflow to create a polished blog. The workflow includes topic analysis, content generation, and quality review to ensure the final output is cohesive and engaging.  

<aside>
💡

**Core Workflow**
</aside>

1. **Orchestrator**: Analyzes the topic, defines the target audience, and creates a plan with sub-topics for the blog.  
2. **Writer**: Generates content and key points for each sub-topic, taking context from previously written sections.  
3. **Reviewer**: Reviews all sections, gives a cohesion score, suggests edits, and produces the final polished blog.  
4. **Output**: Provides the complete blog post along with cohesion score and suggested improvements.  

---

## Features

- Topic-based AI blog generation  
- Customizable style and length  
- Multi-section blog planning  
- Cohesion scoring and review feedback  
- Polished, ready-to-publish output  

---


---

## Setup Instructions

1️⃣ **Clone the repository**

```bash
git clone https://github.com/kanishka-maurya/BlogAgent.git
cd BlogAgent
```

2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

3️⃣ **Configure API Key**
```bash
AI_API_KEY=your_api_key_here
```

4️⃣ **Start Services**
```bash
Start FastAPI Backend: uvicorn main:app --reload --port 8000
Start Streamlit Frontend: streamlit run frontend.py
```

