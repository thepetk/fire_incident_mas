from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .schemas import FireEventSchema
from mas_project.tools import MdxAnalyzerTool


@CrewBase
class EmergencyServicesCrew:
    """Emergency Services Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config["reader"],
            tools=[MdxAnalyzerTool()],
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
        )

    @task
    def injest_fire_event(self) -> Task:
        return Task(
            config=self.tasks_config["injest_fire_event"],
        )

    @task
    def summarize_fire_event(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_fire_event"],
            output_pydantic=FireEventSchema,
            human_input=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Emergency Services Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
