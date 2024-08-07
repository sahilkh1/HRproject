# tools.py
from typing import Dict
# import spacy
from langchain_core.tools import tool
from typing import Dict
# from langchain_core.messages import HumanMessage
# from langchain.chat_models import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import END, StateGraph, MessagesState
# from langgraph.prebuilt import ToolNode

import random
# import spacy
from collections import Counter
# from spacy.lang.en.stop_words import STOP_WORDS
import os
import PyPDF2

class Tools:
    # def __init__(self):
    #     # Load the spaCy model for English
    #     self.nlp = spacy.load("en_core_web_sm")

    #     # Define constants for technical and business keywords
    #     self.TECHNICAL_KEYWORDS = {
    #         "python", "java", "c++", "machine learning",
    #         "data analysis", "artificial intelligence",
    #         "cloud computing", "devops"
    #     }
    #     self.BUSINESS_KEYWORDS = {
    #         "project management", "stakeholder", "business development",
    #         "sales", "marketing", "finance", "strategy", "leadership"
    #     }

    # def summarize_res(self, resume: str) -> str:
    #     """Summarize the resume by highlighting technical and business keywords."""
    #     doc = self.nlp(resume.lower())
    #     words = [token.text for token in doc if token.is_alpha and token.text not in spacy.lang.en.stop_words.STOP_WORDS]
    #     word_freq = spacy.util.Counter(words)
    #     keywords = [word for word in word_freq if word in self.TECHNICAL_KEYWORDS | self.BUSINESS_KEYWORDS]
    #     keywords = sorted(keywords, key=lambda x: word_freq[x], reverse=True)
    #     sentences = [sent.text for sent in doc.sents]
    #     sentence_scores = {sentence: sum(1 for word in self.nlp(sentence.lower()) if word.text in keywords) for sentence in sentences if sum(1 for word in self.nlp(sentence.lower()) if word.text in keywords) > 0}
    #     sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    #     summary = sorted_sentences[:10]
    #     return " ".join(summary)

    @tool
    def summarize_resume(self, resume: str) -> str:
        """You are an AI assistant designed to process resumes. Your task is to summarize the resume by extracting key technical and business terms. Focus on identifying skills, experiences, and relevant industry-specific terminology. Use the following resume text to generate the summary:
        {resume_text}
        Provide a concise summary highlighting the most relevant technical and business keywords.
        """

        return self.summarize_res(resume)

    @tool
    def fitment_analysis(self, resume_summary: str, jd: str) -> Dict[str, str]:
        """You are analyzing the fitment of a candidate based on their resume summary compared to a job description. Evaluate the candidate’s suitability for the position by identifying strengths, weaknesses, potential risk areas, and questions to ask during an interview. 
        Resume Summary:
        {resume_summary}
        Job Description:
        {job_description}
        Provide a detailed analysis highlighting the candidate's strengths, weaknesses, risk areas, and any pertinent questions to ask.
        """
        # return {
        #     "strengths": "Identified strengths",
        #     "weaknesses": "Identified weaknesses",
        #     "risk_areas": "Potential risk areas",
        #     "questions": "Questions to ask"
        # }

    @tool
    def get_candidate_consent(self, summary: str) -> Dict[str, str]:
        """Based on the following resume summary and fitment analysis, determine if the candidate should be invited for a screening interview. If consent is given, propose a random time for the interview.
        Summary and Analysis:
        {summary_analysis}
        Output:
        - Consent: 0 or 1 (0 if not proceeding, 1 if proceeding)
        - Proposed Time: Randomly generated within business hours (9:00-17:00)
        """
        # doc = self.nlp(summary)
        # candidate_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        # candidate_name = candidate_names[0] if candidate_names else "Unknown Candidate"
        # consent = random.randint(0, 1)
        # hours = random.randint(9, 17)
        # minutes = random.choice([0, 15, 30, 45])
        # proposed_time = f"{hours}:{minutes:02d}"
        # return {
        #     "candidate_name": candidate_name,
        #     "proposed_time": proposed_time,
        #     "consent": bool(consent),
        #     "summary": summary
        # }

    @tool
    def craft_email(self, candidate_name: str, proposed_time: str, consent: bool) -> str:
        """You are tasked with crafting a personalized email to a candidate regarding their interview status. If consent is given, include the proposed time for the interview. Otherwise, politely inform them that the process will not continue.
        Candidate Name: {candidate_name}
        Proposed Time: {proposed_time}
        Consent: {consent}
        Draft the email as follows:
        - If consent is 1, invite the candidate for an interview.
        - If consent is 0, notify the candidate that the process will not proceed.
        Email:
        """
        if consent:
            return (f"Dear {candidate_name},\n\nWe are pleased to invite you for an interview at {proposed_time}. "
                    "Please confirm your availability.\n\nBest regards,\nHR Team")
        else:
            return (f"Dear {candidate_name},\n\nThank you for your application. Unfortunately, we cannot proceed further at this time."
                    "\n\nBest regards,\nHR Team")
