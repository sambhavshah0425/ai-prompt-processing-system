from database.mongo import Database
from models.prompt_model import PromptModel

def seed_database():
    print("Initializing Database connection...")
    Database.initialize()
    
    prompt_id = "Education_Prompt"
    template = "You are an expert in education domain. Answer the following: {{userInput}}"
    
    print(f"Creating/Updating prompt with ID: {prompt_id}")
    PromptModel.create_prompt(prompt_id, template)
    
    print("Seed complete. You can now test the API.")

if __name__ == "__main__":
    seed_database()
