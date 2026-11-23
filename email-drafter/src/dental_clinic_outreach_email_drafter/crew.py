from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

MODEL = "openai/gpt-5.6-luna"


@CrewBase
class DentalClinicOutreachEmailDrafterCrew:
    """Reads clinics from an existing Google Sheet and writes an email subject,
    email body, status and WhatsApp message for every row. Uses no web search."""

    @agent
    def outreach_email_writer_for_zero_company(self) -> Agent:
        return Agent(
            config=self.agents_config["outreach_email_writer_for_zero_company"],
            tools=[],
            apps=[
                "google_sheets/get_values@private",
                "google_sheets/update_values@private",
                "google_sheets/get_sheet_names@private",
            ],
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=LLM(model=MODEL),
        )

    @task
    def draft_outreach_emails_and_whatsapp_messages_in_sheet(self) -> Task:
        return Task(
            config=self.tasks_config["draft_outreach_emails_and_whatsapp_messages_in_sheet"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
