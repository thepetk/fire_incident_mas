from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .schemas import FirefighterUnitSchema


@CrewBase
class FirefighterServicesCrew:
    """Firefighter Services Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config["reader"],
        )

    @agent
    def dispatcher(self) -> Agent:
        return Agent(
            config=self.agents_config["dispatcher"],
        )

    @task
    def read_firefighter_units(self) -> Task:
        return Task(
            config=self.tasks_config["read_firefighter_units"],
            output_pydantic=FirefighterUnitSchema,
        )

    @task
    def dispatch_firefighter_unit(self) -> Task:
        return Task(
            config=self.tasks_config["dispatch_firefighter_unit"],
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
