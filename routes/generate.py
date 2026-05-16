import asyncio
from flask import Blueprint, request, jsonify
from bson import ObjectId

from services.prompt_service import PromptService
from services.ai_service import AIService
from services.history_service import HistoryService
from utils.helpers import parse_json

generate_bp = Blueprint('generate', __name__)

PROMPT_ID = "Education_Prompt" # Default prompt ID for this project

@generate_bp.route('/generate', methods=['POST'])
def generate():
    """
    Single response generation API.
    """
    try:
        data = request.get_json()
        if not data or 'userInput' not in data:
            return jsonify({"error": "Missing 'userInput' in request body"}), 400
            
        user_input = data['userInput']
        
        try:
            final_prompt = PromptService.process_prompt(PROMPT_ID, user_input)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

        # Call AI service synchronously
        response = AIService.call_ai_sync(final_prompt)
        
        # Log history
        HistoryService.log_single_request(user_input, final_prompt, response)
        
        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@generate_bp.route('/generate-batch', methods=['POST'])
def generate_batch():
    """
    Async batch processing API.
    """
    try:
        data = request.get_json()
        if not data or 'inputs' not in data or not isinstance(data['inputs'], list):
            return jsonify({"error": "Missing or invalid 'inputs' list in request body"}), 400
            
        inputs = data['inputs']
        batch_id = str(ObjectId())

        # Prepare tasks
        async def process_single_input(user_input):
            try:
                final_prompt = PromptService.process_prompt(PROMPT_ID, user_input)
            except ValueError as e:
                # If prompt not found, return error string
                return f"Error: {str(e)}"
                
            response = await AIService.call_ai_async(final_prompt)
            HistoryService.log_batch_request(batch_id, user_input, final_prompt, response)
            return response

        # Run concurrently
        async def run_batch(inputs_list):
            tasks = [process_single_input(inp) for inp in inputs_list]
            return await asyncio.gather(*tasks)

        responses = asyncio.run(run_batch(inputs))
        
        return jsonify({"responses": responses}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@generate_bp.route('/history', methods=['GET'])
def get_history():
    """
    Retrieves all prompt processing history.
    """
    try:
        from models.history_model import HistoryModel
        history_records = HistoryModel.get_all_history()
        return jsonify({"history": parse_json(history_records)}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
