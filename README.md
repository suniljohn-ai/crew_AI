# crew_AI
Imagine a couple of agents where, working for your social media, that's where this project demonstrates by using the industrial top framework for working with agentic AI sysytems, CrewAI

🚀 The Marketing Crew — Multi-Agent AI System with CrewAI
📌 Overview
The Marketing Crew is a fully functional multi-agent AI project built using the CrewAI framework.
It demonstrates how specialized AI agents can collaborate to perform complex workflows like content creation, SEO optimization, and marketing strategy — all autonomously.

This project also reflects hands-on expertise in:

Prompt Engineering

LLM Orchestration

Agent & Task Design

Multi-Agent Collaboration

Gemini LLM Integration

🛠 Features
4 Specialized Agents:

🧑‍💼 Head of Marketing — Oversees strategy & execution

✍ Content Creator (Social Media) — Crafts engaging posts & campaigns

📰 Content Creator (Blogs) — Writes SEO-friendly articles

🔍 SEO Specialist — Optimizes content for search engines

Dynamic Task Management

Gemini API Integration (Google Generative AI models)

Configurable via YAML for easy customization

Markdown Output for SEO-optimized blog storage

📂 Project Structure
📦 marketing_crew_project
 ┣ 📜 config                # Main CrewAI project script
       ┣ agents.yaml        # Agent roles, goals, and backstories
       ┣ tasks.yaml         # Task definitions & dependencies
       
 ┣ 📜 resources             
       ┣ drafts             # Generated content & results 

 ┣ 📜 crew.py               # Main CrewAI project script
 ┣ 📜 requirements.txt      # Dependencies
 ┣ 📜 README.md             # Project documentation     

 🚀 Installation & Usage
1️⃣ Clone the Repository
bash
git clone https://github.com/suniljohn-ai/crew_AI.git
cd marketing-crew

before runnig make sure to add your environment variables for gemini (llm) and serpAPI(for extra web results)
-> llm used "google/gemini-flash-2.0"
