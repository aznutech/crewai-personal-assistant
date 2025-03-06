import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from crewai.project import CrewBase, agent, crew, task
from personal_assistant.tools.buffet_tool import get_buffet_tool
from personal_assistant.tools.prayer_times_tool import get_prayer_times_tool

#for knowledge assistant must uv add that llm sdk otherwise it will not give any answer know knowledge
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
google_embedder = {
    "provider": "google",
    "config": {
        "model": "models/text-embedding-004",
        "api_key": GEMINI_API_KEY,
    }
}
content = "User name is Imran. He is 44 years old and lives in Faisalabad."
string_source = StringKnowledgeSource(
    content=content,
)


@CrewBase
class DevCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"    
    

    @agent
    def iftar_time_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["iftar_time_assistant"],
            tools=[self.get_prayer_times],
        )
    
    @agent 
    def buffet_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["buffet_assistant"],
            tools=[self.get_buffet],
        )
        
    @agent 
    def knowledge_assistant(self) -> Agent:
        
        return Agent(
            config=self.agents_config["knowledge_assistant"],
            verbose = True,
            allow_delegation=False,
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
            },
            
        )
        

    @task
    def get_iftar_time(self) -> Task:
        return Task(
            config=self.tasks_config["get_iftar_time"],
        )
    
    @task
    def get_buffet_info(self) -> Task:
        return Task(
            config=self.tasks_config["get_buffet_info"],
        )
   
    @task
    def get_knowledge(self) -> Task:
        return Task(
            config=self.tasks_config["get_knowledge"],
        )
   

    @tool("PrayerTimesTool")
    def get_prayer_times() -> str:
        """
        Retrieves today's iftar (Maghrib) time by calling the external prayer times tool.
        """
        return get_prayer_times_tool()
    
    @tool("BuffetTool")
    def get_buffet() -> str:
        """
        Retrieves buffet information from a designated website using BeautifulSoup.
        """   
        return get_buffet_tool()

    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = self.agents,  # Automatically created by the @agent decorator
            tasks = self.tasks,  # Automatically created by the @task decorator
            process = Process.sequential,
            verbose = True,
            knowledge_sources = [string_source],
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
            }
        )
