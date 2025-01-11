from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from mas_project.tools.json import JSONReaderTool
from .schemas import FirefighterUnitSchema, FirefighterUnitListSchema
from mas_project.tools import RouteDistanceTool


@CrewBase
class FirefighterServicesCrew:
    """Firefighter Services Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config["reader"],
            tools=[JSONReaderTool()],
            max_iter=3,
        )

    @agent
    def dispatcher(self) -> Agent:
        return Agent(
            config=self.agents_config["dispatcher"],
            tools=[RouteDistanceTool()],
        )

    @task
    def read_firefighter_units(self) -> Task:
        return Task(
            config=self.tasks_config["read_firefighter_units"],
            output_pydantic=FirefighterUnitListSchema,
        )

    @task
    def dispatch_firefighter_unit(self) -> Task:
        return Task(
            config=self.tasks_config["dispatch_firefighter_unit"],
            output_pydantic=FirefighterUnitSchema,
            human_input=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Firefighter Services Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
