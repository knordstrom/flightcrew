import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import requests

from flightcrew.library.sdk import SDK
from flightcrew.tools.flight_finder import FlightFinderToolInput, FlightFinderTool, FlightFound, FlightsFound

@CrewBase
class FlightCrew():

    tasks_config = 'config/tasks.yaml'
    manager: Agent = None

    def __init__(self, goal: str, sdk=None):
        super().__init__()
        self.goal = goal
        self.sdk: SDK = sdk or SDK()
        self.sdk.authenticate()
        self.manager = Agent(
            role="Project Manager",
            goal= self.goal, #"Efficiently manage the crew and ensure high-quality task completion",
            backstory="""You're an experienced project manager, skilled in overseeing complex projects and 
            guiding teams to success.
            """,
            verbose = True,
            allow_delegation=True,
        )

    @agent
    def find_flights(self) -> Agent:
        return Agent(
            name="Flight Finder",
            role="Flight Researcher",
            goal= "Use the Amadeus API to find flights based on user input.",
            backstory="This agent is responsible for finding bespoke flights that conform to very specific criteria",
            description="Finds flights through the Amadeus API",
            tools=[FlightFinderTool(self.sdk)],
            output_pydantic=FlightsFound,
        )
    
    @agent
    def report_flights(self) -> Agent:
        return Agent(
            name="Flight Reporter",
            role="Flight Report Generator",
            goal= "Generate a report of the flights found.",
            backstory="""You're a meticulous analyst with a keen eye for detail. You're known for 
            your ability to turn complex data into clear and concise reports, making
            it easy for others to understand and act on the information you provide.""",
            description="Generates a report of the flights found.",
            input_pydantic=FlightsFound,
        )
    
    @task
    def find_flights_task(self) -> Task:
        return Task(
            name="Find Flights",
            description="Find flights using the Amadeus API.",
            agent=self.find_flights(),
            config=self.tasks_config['find_flights_task'],
            output_pydantic= FlightsFound
        )
    
    @task
    def reporting_task(self) -> Task:
        return Task(
            agent=self.report_flights(),
            name="Report Flights",
            description="Generate a report of the flights found.",
            expected_output="A markdown report with a table of the flights found.",
            input_json=FlightsFound,
            output_file='report.md'
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent = self.manager,
            verbose=True
        )
    