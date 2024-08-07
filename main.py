# main.py
from model import ModelHandler
from utils import Utils
from workFlow import WorkflowManager

def main():
    utils = Utils()
    model_handler = ModelHandler()
    
    # Load job description and resumes
    jd_path = './support/jd.pdf'
    resume_directory = './support/resumes'
    
    jd = utils.load_job_description(jd_path)
    resume_texts = utils.load_resumes(resume_directory)

    # Initialize the workflow manager
    workflow_manager = WorkflowManager(model_handler.llm)
    app = workflow_manager.setup_workflow()

    # Process the resumes
    workflow_manager.process_resumes(app, resume_texts, jd)

if __name__ == "__main__":
    main()
