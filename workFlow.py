# workflow.py
# from langchain_core.messages import MessagesState, HumanMessage
from typing import List, Dict, Literal
from langchain_core.messages import HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

import random

from collections import Counter

import os
import PyPDF2

from tools import Tools

class WorkflowManager:
    def __init__(self, llm):
        self.tools = Tools()
        self.llm = llm

    def should_continue(self, state: MessagesState) -> str:
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def call_model(self, state: MessagesState) -> dict:
        messages = state['messages']
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def setup_workflow(self) -> StateGraph:
        tool_node = ToolNode([
            self.tools.summarize_resume, 
            self.tools.fitment_analysis, 
            self.tools.get_candidate_consent, 
            # self.tools.schedule_interview, 
            self.tools.craft_email
        ])

        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", tool_node)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", self.should_continue)
        workflow.add_edge("tools", 'agent')
        checkpointer = MemorySaver()
        return workflow.compile(checkpointer=checkpointer)

    def process_resumes(self, app, resume_texts: Dict[str, str], jd: str):
        for idx, (filename, text) in enumerate(resume_texts.items()):
            print(f"Filename: {filename}, Extracted Text: {text[:100]}...")

            config = {"configurable": {"thread_id": idx}}

            summary = app.invoke(
                {"messages": [HumanMessage(content=f"Summarize this resume: {text}")]},
                config=config
            )["messages"][-1].content

            fitment_results = app.invoke(
                {"messages": [HumanMessage(content=f"Perform fitment analysis for resume and breakdown these points strengths, weaknesses, risk_area, questions to ask in the interview {summary} with JD: {jd}")]},
                config=config
            )["messages"][-1].content

            consent_info = app.invoke(
                {"messages": [HumanMessage(content=f" give either 0 or 1 as a consent and a time slot betweeen 12pm to 6pm to schedule an interview. Everytime time should be different If it is 1 then the email tool will be called and the email will mention the time for the interview, otherwise regret email will be send {summary}")]},
                config=config
            )["messages"][-1].content

            email_content = app.invoke(
                {"messages": [HumanMessage(content=f"Craft email for candidate if the conscent is 1 then the mail should include the time for tomorrow and if it is 0 then the regret email will be send. after best regards mention the company name as OT Marketplace, dont mention any name of a person. In subject the role will be from the jd {consent_info}")]},
                config=config
            )["messages"][-1].content

            print(f"Results for {filename}:\n", fitment_results, "\n")
            print(f"Consent Info for {filename}:\n", consent_info, "\n")
            print(f"Email Content for {filename}:\n", email_content, "\n")
