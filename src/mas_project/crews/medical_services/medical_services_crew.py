from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from mas_project.tools.json import JSONReaderTool
from mas_project.tools.map import RouteDistanceTool
from .schemas import MedicalUnitSchema, MedicalUnitListSchema


@CrewBase
class MedicalServicesCrew:
    """Medical Services Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config["reader"],
            tools=[JSONReaderTool(json_file_type="hospitals")],
            max_iter=3,
        )

    @agent
    def balancer(self) -> Agent:
        return Agent(
            config=self.agents_config["balancer"],
            tools=[RouteDistanceTool()],
        )

    @task
    def read_medical_units(self) -> Task:
        return Task(
            config=self.tasks_config["read_medical_units"],
            output_pydantic=MedicalUnitListSchema,
        )

    @task
    def assign_medical_unit(self) -> Task:
        return Task(
            config=self.tasks_config["assign_medical_unit"],
            output_pydantic=MedicalUnitSchema,
            human_input=True,
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
