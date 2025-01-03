#!/usr/bin/env python
import json
import os

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start, router, or_

from mas_project.crews.emergency_services import EmergencyServicesCrew
from mas_project.crews.firefighter_services import FirefighterServicesCrew
from mas_project.crews.medical_services import MedicalServicesCrew

FIRE_REPORT_PATH: str = os.getenv("FIRE_REPORT_PATH", "emergency_01.mdx")


class FireEventState(BaseModel):
    """
    handles the state of the fire event on
    every step of the FireEventFlow object.
    """

    location_x: "float" = None
    location_y: "float" = None
    injured_people: "int" = None
    fire_type: "str" = None
    fire_severity: "str" = None
    assigned_medical_unit_id: "int" = None
    assigned_firefighter_unit_id: "int" = None
    status: str = "initialized"


class FireEventFlow(Flow[FireEventState]):
    """
    the main drive behind the functionality of the fire
    response mechanism. Combines the functionality of
    the 3 project crews (emergency, firefighter and med-
    ical services). Uses a router to decide which checks
    if the medical services are needed or not.

    """

    @start()
    def read_fire_event_report(self) -> "None":
        _r = (
            EmergencyServicesCrew()
            .crew()
            .kickoff(inputs={"mdx_file": FIRE_REPORT_PATH})
        )
        result = json.loads(_r.raw)
        self.state.location_x = result["location_x"]
        self.state.location_y = result["location_y"]
        self.state.injured_people = result["injured_people"]
        self.state.fire_type = result["fire_type"]
        self.state.fire_severity = result["fire_severity"]
        self.state.status = "reported"

    @router(read_fire_event_report)
    def check_for_injured_people(self) -> "str":
        if self.state.injured_people > 0:
            return "Has Injured People"
        else:
            return "No Injured People"

    def _assign_medical_units(self) -> "int":
        _r = (
            MedicalServicesCrew()
            .crew()
            .kickoff(
                inputs={
                    "json_file": FIRE_REPORT_PATH,
                    "location_x": self.state.location_x,
                    "location_y": self.state.location_y,
                    "injured_people": self.state.injured_people,
                }
            )
        )
        return _r.raw["uid"]

    def _dispatch_firefighter_units(self) -> "int":
        _r = (
            FirefighterServicesCrew()
            .crew()
            .kickoff(inputs={
                    "json_file": 'firetrucks.json',
                    "location_x": 28.461720670375886,
                    "location_y": -16.2835862728014,
                    "fire_type": "ordinary",
                    "fire_severity": "high",
                }
            )
        )
        return _r.raw["uid"]

    @listen("Has Injured People")
    def handle_event_with_injured_people(self) -> "None":
        self.state.assigned_firefighter_unit_id = self._dispatch_firefighter_units()
        self.state.assigned_medical_unit_id = self._assign_medical_units()
        self.state.status = "both_units_assigned"

    @listen("No Injured People")
    def handle_event_without_injured_people(self) -> "None":
        self.state.assigned_firefighter_unit_id = self._dispatch_firefighter_units()
        self.state.assigned_medical_unit_id = None

        self.state.status = "only_firefighter_units_assigned"

    @listen(or_(handle_event_with_injured_people, handle_event_without_injured_people))
    def print_response_scenario(self) -> "None":
        print(
            f"Assigned Firefighter Unit ID: {self.state.assigned_firefighter_unit_id}"
        )
        if self.state.status == "both_units_assigned":
            print(f"Assigned Medical Unit ID: {self.state.assigned_medical_unit_id}")
        else:
            print(f"Assigned Medical Unit ID: Not Needed")


def kickoff() -> "None":
    poem_flow = FireEventFlow()
    poem_flow.kickoff()


if __name__ == "__main__":
    kickoff()
