#!/usr/bin/env python
from operator import or_
import os

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start, router

from .crews.emergency_services import EmergencyServicesCrew
from .crews.firefighter_services import FirefighterServicesCrew
from .crews.medical_services import MedicalServicesCrew

FIRE_REPORT_PATH: str = os.getenv("FIRE_REPORT_PATH", "fire_report.mdx")


class FireEventState(BaseModel):
    location_x: int
    location_y: int
    injured_people: int
    fire_type: str
    fire_severity: str
    assigned_medical_unit_id: int
    assigned_firefighter_unit_id: int
    status: str


class FireEventFlow(Flow[FireEventState]):
    @start()
    def read_fire_event_report(self):
        result = (
            EmergencyServicesCrew()
            .crew()
            .kickoff(inputs={"mdx_file": FIRE_REPORT_PATH})
        )
        self.state.location_x = result.pydantic.location_x
        self.state.location_y = result.pydantic.location_y
        self.state.injured_people = result.pydantic.injured_people
        self.state.fire_type = result.pydantic.fire_type
        self.state.fire_severity = result.pydantic.fire_severity
        self.state.status = "reported"

    @router(read_fire_event_report)
    def check_for_injured_people(self):
        if self.state.injured_people > 0:
            return "Has Injured People"
        else:
            return "No Injured People"

    def _assign_medical_units(self) -> int:
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
        return _r.pydantic.uid

    def _dispatch_firefighter_units(self) -> int:
        _r = (
            FirefighterServicesCrew()
            .crew()
            .kickoff(
                inputs={
                    "json_file": FIRE_REPORT_PATH,
                    "location_x": self.state.location_x,
                    "location_y": self.state.location_y,
                    "fire_type": self.state.fire_type,
                    "fire_severity": self.state.fire_severity,
                }
            )
        )
        return _r.pydantic.uid

    @listen("Has Injured People")
    def handle_event_with_injured_people(self):
        self.state.assigned_firefighter_unit_id = self._dispatch_firefighter_units()
        self.state.assigned_medical_unit_id = self._assign_medical_units()
        self.state.status = "both_units_assigned"

    @listen("No Injured People")
    def handle_event_without_injured_people(self):
        self.state.assigned_firefighter_unit_id = self._dispatch_firefighter_units()
        self.state.assigned_medical_unit_id = None

        self.state.status = "only_firefighter_units_assigned"

    @listen(or_(handle_event_with_injured_people, handle_event_without_injured_people))
    def print_response_scenario(self):
        print(
            f"Assigned Firefighter Unit ID: {self.state.assigned_firefighter_unit_id}"
        )
        if self.state.status == "both_units_assigned":
            print(f"Assigned Medical Unit ID: {self.state.assigned_medical_unit_id}")
        else:
            print(f"Assigned Medical Unit ID: Not Needed")


def kickoff():
    poem_flow = FireEventFlow()
    poem_flow.kickoff()


if __name__ == "__main__":
    kickoff()
