from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from composio_crewai import ComposioToolSet, Action, App
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from mem0.llms.gemini import GeminiLLM


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class RecipesApp():

	load_dotenv()

	composio_toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'))
	tools = composio_toolset.get_tools(actions=['GOOGLEDRIVE_CREATE_FOLDER'])

	"""RecipesApp crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def composio_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['composio_agent'],
			verbose=True,
			tools=self.tools,
		)



	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def composio_task(self) -> Task:
		return Task(
			config=self.tasks_config['composio_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the RecipesApp crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
