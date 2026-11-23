#!/usr/bin/env python
"""Run the email-drafter crew on an existing Google Sheet.

Usage:
    SPREADSHEET_ID=<your sheet id> TAB_NAME=Sheet1 crewai run
"""
import os
import sys

from dental_clinic_outreach_email_drafter.crew import DentalClinicOutreachEmailDrafterCrew


def run():
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    if not spreadsheet_id:
        sys.exit("Set SPREADSHEET_ID (the long id in the Google Sheet URL).")
    inputs = {
        "spreadsheet_id": spreadsheet_id,
        "tab_name": os.getenv("TAB_NAME", "Sheet1"),
    }
    result = DentalClinicOutreachEmailDrafterCrew().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()
