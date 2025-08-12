#importing required libraries

from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool

from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

import yaml
from pathlib import Path

#loading the environment variables
load_dotenv()

llm = LLM(
    provider = "gemini",
    model = "gemini-2.0-flash",
    temperature = 0.6
)

class Content(BaseModel):
    content_type: str = Field(...,description = "The type of content to be created(eg.Blog post, Social media post, video)")
    topic: str = Field(...,description = "The topic of the content")
    target_audience: str = Field(...,description = "The target audience of the content")
    tags: List[str] = Field(...,description = "Tags to be used for the content")
    content: str = Field(...,description = "The content itself")

@CrewBase
class TheMarketingCrew():
    """ this marketing crew is responsible for creating and executing marketing strategies,
     content creation,    and managing the market campaigns """

    def __init__(self):
        self.agents_config = self._load_yaml("config/agents.yaml")
        self.tasks_config = self._load_yaml("config/tasks.yaml")


    def _load_yaml(self,path):
        with open(Path(path),"r") as f:
            return yaml.safe_load(f)

    @agent
    def head_of_marketing(self) -> Agent:
        return Agent(
            config = self.agents_config['head_of_marketing'],
            tools = [
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("resources/drafts"),
                FileWriterTool(),
                FileReadTool("resources/drafts"),
            ],
            reasoning = True,
            inject_date = True,
            allow_delegation = True,
            max_rpm = 1,
            llm = llm,
        )

    @agent
    def content_creator_social_media(self) ->Agent:
        return Agent(
            config = self.agents_config['content_creator_social_media'],
            tools = [
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool('config/drafts'),
                FileWriterTool(),
                FileReadTool(),
            ],
            inject_date = True,
            allow_delegation = True,
            max_iter = 5,
            max_rpm =1,
            llm = llm,
        )

    @agent
    def content_writer_blogs(self) -> Agent:
        return Agent(
            config = self.agents_config['content_creator_blogs'],
            tools = [
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool('config/drafts'),
                FileWriterTool(),
                FileReadTool(),
            ],
            inject_date = True,
            allow_delegation = True,
            max_iter = 5,
            max_rpm = 1,
            llm = llm,
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config = self.agents_config['seo_specialist'],
            tools = [
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool(),
                FileWriterTool(),
                FileReadTool(),
            ],
            inject_date = True,
            allow_delegation = True,
            max_iter = 5,
            max_rpm = 1,
            llm = llm,
        )

    @task
    def market_research(self) ->Task:
        return Task(
            config = self.tasks_config['market_research'],
            agent = self.head_of_marketing(),
        )

    @task
    def prepare_marketing_research(self) -> Task:
        return Task(
            config = self.tasks_config['prepare_marketing_strategy'],
            agent = self.head_of_marketing(),
        )

    @task
    def create_content_calender(self) -> Task:
        return Task(
            config = self.tasks_config['create_content_calender'],
            agent = self.content_creator_social_media(),
        )

    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config = self.tasks_config['prepare_post_drafts'],
            agent = self.content_creator_social_media(),
            output_json = Content,
        )

    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config = self.tasks_config['prepare_scripts_for_reels'],
            agent = self.content_creator_social_media(),
            output_json = Content,
        )

    @task
    def content_research_for_blogs(self) -> Task:
        return Task(
            config = self.tasks_config['content_research_for_blogs'],
            agent = self.content_writer_blogs(),
        )

    @task
    def draft_blogs(self) -> Task:
        return Task(
            config = self.tasks_config['draft_blogs'],
            agent = self.content_writer_blogs(),
            output_json = Content,
        )

    @task
    def seo_optimization(self) -> Task:
        return Task(
            config = self.tasks_config['seo_optimization'],
            agent = self.seo_specialist(),
            output_json = Content,
        )

    @crew
    def marketing_crew(self) -> Crew:
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True,
            planning = True,
            planning_llm = True,
            max_rpm = 1,
        )

if __name__ == '__main__':
    from datetime import datetime

    inputs = {
        "product_name": "Personal AI Assistant for Education",
        "target_audience": "Small,Medium and large Universities,colleges,institutions",
        "product_description": "A tool that helps to students form 6 years old to adults using AI it can personalize the study experiance, like explanation, quizes, reminders, easy teaching and so on, hassel free demo's lessons like ELI5.",
        "budget": "Rs. 50,000",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }

    crew = TheMarketingCrew()
    crew.marketing_crew().kickoff(inputs = inputs)
    print("marketing has been successfully created and run check the resources folder")
