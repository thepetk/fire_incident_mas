from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .schemas import MedicalUnitSchema


@CrewBase
class MedicalServicesCrew:
    """Medical Services Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config["reader"],
        )

    @agent
    def balancer(self) -> Agent:
        return Agent(
            config=self.agents_config["balancer"],
        )

    @task
    def read_medical_units(self) -> Task:
        return Task(
            config=self.tasks_config["read_medical_units"],
            output_pydantic=MedicalUnitSchema,
        )

    @task
    def assign_medical_unit(self) -> Task:
        return Task(
            config=self.tasks_config["assign_medical_unit"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Medical Services Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
