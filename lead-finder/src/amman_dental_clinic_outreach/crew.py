from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, SerperScrapeWebsiteTool

MODEL = "openai/gpt-5.6-luna"


@CrewBase
class AmmanDentalClinicOutreachCrew:
    """Finds dental clinics, their public contacts, saves them to Google Sheets
    and drafts a personalized outreach email + WhatsApp message for each one."""

    @agent
    def dental_clinic_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["dental_clinic_researcher"],
            tools=[SerperDevTool()],
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=LLM(model=MODEL),
        )

    @agent
    def contact_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["contact_finder"],
            tools=[SerperDevTool(), SerperScrapeWebsiteTool()],
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=LLM(model=MODEL),
        )

    @agent
    def google_sheets_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["google_sheets_manager"],
            tools=[],
            apps=[
                "google_sheets/create_spreadsheet@private",
                "google_sheets/append_values@private",
                "google_sheets/get_values@private",
                "google_sheets/lookup_spreadsheet_row@private",
            ],
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=LLM(model=MODEL),
        )

    @agent
    def outreach_email_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["outreach_email_writer"],
            tools=[],
            apps=[
                "google_sheets/get_values@private",
                "google_sheets/get_sheet_names@private",
                "google_sheets/update_values@private",
            ],
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=LLM(model=MODEL),
        )

    @task
    def find_dental_clinics_in_city(self) -> Task:
        return Task(config=self.tasks_config["find_dental_clinics_in_city"])

    @task
    def find_clinic_contact_details(self) -> Task:
        return Task(config=self.tasks_config["find_clinic_contact_details"])

    @task
    def write_clinics_to_google_sheet(self) -> Task:
        return Task(config=self.tasks_config["write_clinics_to_google_sheet"])

    @task
    def write_outreach_emails_and_final_summary(self) -> Task:
        return Task(config=self.tasks_config["write_outreach_emails_and_final_summary"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
