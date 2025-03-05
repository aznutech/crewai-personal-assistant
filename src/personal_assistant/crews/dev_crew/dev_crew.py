from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from crewai.project import CrewBase, agent, crew, task
from personal_assistant.tools.buffet_tool import get_buffet_tool
from personal_assistant.tools.prayer_times_tool import get_prayer_times_tool

from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource

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
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
           
        )
