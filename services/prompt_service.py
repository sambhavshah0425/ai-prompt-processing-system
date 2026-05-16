from models.prompt_model import PromptModel

class PromptService:
    @staticmethod
    def process_prompt(prompt_id, user_input):
        """
        Fetches the prompt template and replaces the {{userInput}} placeholder.
        """
        prompt_data = PromptModel.get_prompt(prompt_id)
        if not prompt_data:
            raise ValueError(f"Prompt template with ID '{prompt_id}' not found.")
        
        template = prompt_data.get("template", "")
        # Assuming the placeholder format is {{userInput}}
        final_prompt = template.replace("{{userInput}}", user_input)
        return final_prompt
