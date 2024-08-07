# # utils.py
import os
import PyPDF2
from typing import Dict

class Utils:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from a PDF file."""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
        return text

    def load_job_description(self, jd_path: str) -> str:
        """Load job description from a PDF file."""
        return self.extract_text_from_pdf(jd_path)

    def load_resumes(self, resume_directory: str) -> Dict[str, str]:
        """Load resumes from a directory of PDF files."""
        resume_files = [f for f in os.listdir(resume_directory) if f.endswith('.pdf')]
        resume_texts = {resume_file: self.extract_text_from_pdf(os.path.join(resume_directory, resume_file)) for resume_file in resume_files}
        return resume_texts
