import os
from model import ModelHandler
from utils import Utils
from workFlow import WorkflowManager
from dotenv import load_dotenv
load_dotenv()
def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct paths relative to the script directory
    jd_path = os.path.join(script_dir, 'support', 'jd.pdf')
    resume_directory = os.path.join(script_dir, 'support', 'resumes')
    
    # Initialize your classes
    utils = Utils()
    model_handler = ModelHandler()
   
    
    jd = utils.load_job_description(jd_path)
    resume_texts = utils.load_resumes(resume_directory)

    # Initialize the workflow manager
    workflow_manager = WorkflowManager(model_handler.llm)
    app = workflow_manager.setup_workflow()

    # Process the resumes
    workflow_manager.process_resumes(app, resume_texts, jd)

if __name__ == "__main__":
    main()
