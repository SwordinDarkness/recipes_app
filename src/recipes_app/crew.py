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
	file_tools = composio_toolset.get_tools(actions=[Action.FILETOOL_CREATE_FILE,Action.FILETOOL_WRITE])
	google_drive_tools = composio_toolset.get_tools(actions=[Action.GOOGLEDRIVE_CREATE_FOLDER, Action.GOOGLEDRIVE_FIND_FOLDER, Action.GOOGLEDRIVE_UPLOAD_FILE])

	"""RecipesApp crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def chef_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['chef_agent'],
			verbose=True,
		)
	@agent
	def file_writer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['file_writer_agent'],
			verbose=True,
			tools=self.file_tools,
		)

	@agent
	def google_drive_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['google_drive_agent'],
			verbose=True,
			tools=self.google_drive_tools,
		)



	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def chef_task(self) -> Task:
		return Task(
			config=self.tasks_config['chef_task'],
		)

	@task
	def file_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['file_writer_task'],
		)
	@task
	def google_drive_task(self) -> Task:
		return Task(
			config=self.tasks_config['google_drive_task'],
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
