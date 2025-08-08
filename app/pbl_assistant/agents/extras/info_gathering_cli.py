#!/usr/bin/env python3

from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
from typing import List, Optional
import asyncio
import logfire
import sys
import os
import traceback

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
sys.path.append(project_root)

# Load environment variables
load_dotenv()

# Configure logfire to suppress warnings
logfire.configure(send_to_logfire='never')

# Import the info_gathering_agent
from app.pbl_assistant.agents.info_gathering_agent import info_gathering_agent
from app.pbl_assistant.models.profiling import ProjectDetails

class CLI:
    def __init__(self):
        self.messages: List[ModelMessage] = []
        self.console = Console()

    async def chat(self):
        print("Project Profiling Agent CLI (type 'quit' to exit)")
        print("Enter your message:")
        
        while True:
            try:
                # Get user input
                user_input = input("> ").strip()
                if user_input.lower() == 'quit':
                    break

                # Create a request message
                request = ModelRequest(parts=[UserPromptPart(content=user_input)])
                
                # Add to message history
                self.messages.append(request)
                
                # Run the agent with message history
                print("Processing...")
                try:
                    
                    # Run the agent with the full message history
                    async with info_gathering_agent.iter(user_input, message_history=self.messages[:-1]) as run:
                        result = None
                        async for node in run:
                            # Get the latest result from the node
                            if hasattr(node, 'result'):
                                result = node.result
                        
                        # Update message history with all messages from this run if available
                        if hasattr(run, 'result') and hasattr(run.result, 'all_messages'):
                            self.messages += run.result.all_messages()
                        
                        # If we didn't get a result from the iteration, try to get it from the run object
                        if result is None and hasattr(run, 'result'):
                            result = run.result
                        
                except Exception as e:
                    print(f"Error running agent: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    result = None
                
                # Get the actual ProjectDetails from the result's output field
                project_details = None
                if result and hasattr(result, 'output'):
                    project_details = result.output
                
                # Handle the project details
                if project_details:
                    # Extract and display the response
                    response_text = ""
                    if hasattr(project_details, 'response') and project_details.response:
                        response_text = project_details.response
                        print(f"\n{response_text}")
                    else:
                        # Create a fallback response based on the details we have
                        has_topic = hasattr(project_details, 'topic') and project_details.topic
                        has_grade = hasattr(project_details, 'grade_level') and project_details.grade_level
                        has_duration = hasattr(project_details, 'duration_preference') and project_details.duration_preference
                        
                        response_text = "I've updated your project details. "
                        if has_topic:
                            response_text += f"The topic is {project_details.topic}. "
                        if has_grade:
                            response_text += f"The grade level is {project_details.grade_level}. "
                        if has_duration:
                            response_text += f"The duration is {project_details.duration_preference}. "
                            
                        if not (has_topic and has_grade and has_duration):
                            response_text += "\n\nI still need "
                            missing = []
                            if not has_topic:
                                missing.append("the topic")
                            if not has_grade:
                                missing.append("the grade level")
                            if not has_duration:
                                missing.append("the project duration")
                            response_text += " and ".join(missing) + "." if len(missing) > 1 else missing[0] + "."
                        
                        print(f"\n{response_text}")
                    
                    # Note: We don't need to add to message history here anymore
                    # as we're already capturing all messages from the run
                    
                    # Check if we have all required fields
                    has_topic = hasattr(project_details, 'topic') and project_details.topic
                    has_grade = hasattr(project_details, 'grade_level') and project_details.grade_level
                    has_duration = hasattr(project_details, 'duration_preference') and project_details.duration_preference
                    
                    all_details_given = has_topic and has_grade and has_duration
                    
                    # Show current project details
                    print("\n--- Current Project Details ---")
                    if has_topic:
                        print(f"Topic: {project_details.topic}")
                    if has_grade:
                        print(f"Grade Level: {project_details.grade_level}")
                    if has_duration:
                        print(f"Duration: {project_details.duration_preference}")
                        
                    # Show what's missing
                    missing = []
                    if not has_topic:
                        missing.append("topic")
                    if not has_grade:
                        missing.append("grade level")
                    if not has_duration:
                        missing.append("duration")
                        
                    if missing:
                        print(f"\nMissing: {', '.join(missing)}")
                    else:
                        print("\nAll required details provided!")
                        
                        # Show complete project profile if all details are given
                        print("\n=== COMPLETE PROJECT PROFILE ===")
                        print(f"Topic: {project_details.topic}")
                        print(f"Grade Level: {project_details.grade_level}")
                        print(f"Duration: {project_details.duration_preference}")
                        print("===================================")
                elif project_details and not hasattr(project_details, 'response'):
                    print("\nAgent returned a result but no response text was found.")
                else:
                    print("\nNo valid project details received from the agent.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Traceback:")
                traceback.print_exc()

async def main():
    cli = CLI()
    await cli.chat()

if __name__ == "__main__":
    asyncio.run(main())