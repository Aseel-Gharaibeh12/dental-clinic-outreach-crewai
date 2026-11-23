#!/usr/bin/env python
"""Run the lead-finder crew.

Usage:
    crewai run
    # or with custom inputs:
    CITY=Irbid SHEET_NAME="Irbid Dental Leads" crewai run
"""
import os

from amman_dental_clinic_outreach.crew import AmmanDentalClinicOutreachCrew


def _inputs() -> dict:
    return {
        "city": os.getenv("CITY", "Amman"),
        "country": os.getenv("COUNTRY", "Jordan"),
        "sheet_name": os.getenv("SHEET_NAME", "Amman Dental Leads"),
    }


def run():
    result = AmmanDentalClinicOutreachCrew().crew().kickoff(inputs=_inputs())
    print(result)


if __name__ == "__main__":
    run()
