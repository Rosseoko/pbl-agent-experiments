#!/usr/bin/env python3
"""
Enhanced PBL Agent CLI Chat Interface with Real-time Streaming
Save this file as: app/pbl_assistant/cli_chat.py
Run with: python -m app.pbl_assistant.cli_chat

This integrates with your existing graph and provides real-time streaming responses.
"""

import asyncio
import uuid
from datetime import datetime
import sys
import os
from typing import List, Dict, Any

# Import from your existing graph module
from .agent_graph import pbl_agent_graph

class EnhancedPBLCLI:
    def __init__(self):
        self.thread_id = str(uuid.uuid4())
        self.chat_history: List[Dict[str, Any]] = []
        self.first_message = True
        
    def print_banner(self):
        print("=" * 60)
        print("🎓 PBL AGENT - PROJECT-BASED LEARNING ASSISTANT")
        print("=" * 60)
        print("I'll help you create a project-based learning experience.")
        print("Tell me about your project topic, grade level, and duration.")
        print()
        print("Example: 'I want a 2-week project about solar system for grade 5'")
        print("Type 'quit' to exit.")
        print("=" * 60)
        print()

    def is_exit_command(self, user_input: str) -> bool:
        return user_input.lower().strip() in ['quit', 'exit', 'bye', 'stop']

    async def invoke_agent_graph(self, user_input: str):
        """Stream agent responses with real-time output"""
        config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

        if self.first_message:
            initial_state = {
                "user_input": user_input,
                "project_details": {},
                "standards_result": {},
                "knowledge_graph_result": {},
                "project_options": {},
                "class_profile": (
                    "Our class of 25 has 1:1 tablets, no lab, "
                    "access to an outdoor courtyard, reliable Wi-Fi, "
                    "and a maker corner with basic craft supplies."
                ),
                "messages": []
            }
            
            # Try custom streaming first, fall back to values if needed
            try:
                async for msg in pbl_agent_graph.astream(
                        initial_state, config, stream_mode="custom"
                    ):
                    yield msg
            except Exception:
                # Fallback to values mode
                async for event in pbl_agent_graph.astream(initial_state, config):
                    for node_name, node_output in event.items():
                        if node_name != "__end__":
                            yield f"📍 {node_name.replace('_', ' ').title()}\n"
                        if "project_details" in node_output and node_output["project_details"].get("response"):
                            yield node_output["project_details"]["response"]
        else:
            from langgraph.types import Command
            try:
                async for msg in pbl_agent_graph.astream(
                    Command(resume=user_input), config, stream_mode="custom"
                ):
                    yield msg
            except Exception:
                async for event in pbl_agent_graph.astream(
                    Command(resume=user_input), config
                ):
                    for node_name, node_output in event.items():
                        if node_name != "__end__":
                            yield f"📍 {node_name.replace('_', ' ').title()}\n"
                        if "project_details" in node_output and node_output["project_details"].get("response"):
                            yield node_output["project_details"]["response"]

    def display_node_progress(self, node_name: str):
        """Display node execution progress"""
        formatted_name = node_name.replace('_', ' ').title()
        print(f"\n📍 {formatted_name}")

    def display_project_options(self, project_options: Dict[str, Any]):
        """Display project options nicely formatted"""
        if not project_options:
            return
            
        print("\n" + "=" * 50)
        print("🎯 PROJECT OPTIONS")
        print("=" * 50)
        
        options = project_options.get("project_options", [])
        response = project_options.get("response", "")
        
        if response:
            print(f"\n{response}")
        
        if options and isinstance(options, list):
            print("\n📋 Available Options:")
            for i, option in enumerate(options, 1):
                print(f"\n{i}. {option}")
                
            print("\n💡 Reply with your choice (e.g., 'I choose option 1')")
        
        print("=" * 50)

    async def run_conversation(self):
        """Main conversation loop with real-time streaming"""
        self.print_banner()

        print("✏️  Please share a short description of your classroom (tech, space, materials, students, etc.):")
        class_profile = input("> ").strip()
        self.class_profile = class_profile
        
        while True:
            try:
                user_input = input("💬 Your message: ").strip()
                if not user_input:
                    print("   Please enter a message.\n")
                    continue
                if self.is_exit_command(user_input):
                    print("\n👋 Thank you for using PBL Agent!")
                    break

                self.chat_history.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                
                print(f"\n👤 You: {user_input}")
                print("🤖 Erandi: ", end="", flush=True)
                
                response_content = ""
                exit_after_selection = False
                
                try:
                    async for chunk in self.invoke_agent_graph(user_input):
                        if isinstance(chunk, str):
                            print(chunk, end="", flush=True)
                            response_content += chunk
                        elif isinstance(chunk, dict):
                            if "node_name" in chunk:
                                self.display_node_progress(chunk["node_name"])
                        # we ignore other chunk types here
                    print()  # finish line
                except Exception as e:
                    print(f"\n❌ Error during processing: {e}")
                    print("Please try again.\n")
                    continue

                # mark that we've now done the first message
                if self.first_message:
                    self.first_message = False

                # record assistant reply
                if response_content:
                    self.chat_history.append({
                        "role": "assistant",
                        "content": response_content,
                        "timestamp": datetime.now().strftime("%I:%M %p")
                    })

                # display the final structured project options (values mode fallback)
                # so user sees them if we're in values mode
                # then exit if they already selected
                # detect the Spanish congratulations line
                if "🎉 Tu proyecto está listo" in response_content or "Tu proyecto está listo" in response_content:
                    print("\n🎉 Project setup complete. Goodbye!")
                    break

                print()  # blank line before next prompt

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try again.\n")

    def show_chat_history(self):
        ...

    def clear_history(self):
        ...

async def main():
    try:
        cli = EnhancedPBLCLI()
        await cli.run_conversation()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Failed to start CLI: {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ("--help","-h"):
            print("Usage: python -m app.pbl_assistant.cli_chat")
            sys.exit(0)
        if cmd == "--version":
            print("PBL Agent CLI v1.0.0")
            sys.exit(0)
    asyncio.run(main())
