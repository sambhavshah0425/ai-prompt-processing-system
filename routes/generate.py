import asyncio
from flask import Blueprint, request, jsonify
from bson import ObjectId

from services.prompt_service import PromptService
from services.ai_service import AIService

generate_bp = Blueprint('generate', __name__)

PROMPT_ID = "Education_Prompt"


@generate_bp.route('/generate', methods=['POST'])
def generate():
    """
    Single response generation API.
    """
    try:
        data = request.get_json()

        if not data or 'userInput' not in data:
            return jsonify({
                "error": "Missing 'userInput' in request body"
            }), 400

        user_input = data['userInput']

        try:
            final_prompt = PromptService.process_prompt(
                PROMPT_ID,
                user_input
            )

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 404

        # Generate AI response
        response = AIService.call_ai_sync(final_prompt)

        return jsonify({
            "response": response
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@generate_bp.route('/generate-batch', methods=['POST'])
def generate_batch():
    """
    Async batch processing API.
    """
    try:
        data = request.get_json()

        if not data or 'inputs' not in data:
            return jsonify({
                "error": "Missing 'inputs' list"
            }), 400

        if not isinstance(data['inputs'], list):
            return jsonify({
                "error": "'inputs' must be a list"
            }), 400

        inputs = data['inputs']

        batch_id = str(ObjectId())

        async def process_single_input(user_input):

            try:
                final_prompt = PromptService.process_prompt(
                    PROMPT_ID,
                    user_input
                )

            except ValueError as e:
                return f"Error: {str(e)}"

            response = await AIService.call_ai_async(
                final_prompt
            )

            return {
                "batchId": batch_id,
                "input": user_input,
                "response": response
            }

        async def run_batch(inputs_list):

            tasks = [
                process_single_input(inp)
                for inp in inputs_list
            ]

            return await asyncio.gather(*tasks)

        responses = asyncio.run(
            run_batch(inputs)
        )

        return jsonify({
            "responses": responses
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@generate_bp.route('/history', methods=['GET'])
def get_history():
    """
    Mock history endpoint
    """

    return jsonify({
        "history": []
    }), 200