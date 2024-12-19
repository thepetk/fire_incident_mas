from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .schemas import FireEventSchema


@CrewBase
class EmergencyServicesCrew:
    """Emergency Services Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def reader(self) -> Agent:
        return Agent(
            config=self.agents_config["reader"],
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
            output_pydantic=FireEventSchema,
        )

    @task
    def summarize_fire_event(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_fire_event"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Emergency Services Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
