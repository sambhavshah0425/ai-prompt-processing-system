from models.history_model import HistoryModel

class HistoryService:
    @staticmethod
    def log_single_request(user_input, final_prompt, response):
        """Logs a single generate request."""
        return HistoryModel.create_history_record(
            request_type="single",
            user_input=user_input,
            final_prompt=final_prompt,
            response=response
        )

    @staticmethod
    def log_batch_request(batch_id, user_input, final_prompt, response):
        """Logs a single request from a batch processing operation."""
        return HistoryModel.create_history_record(
            request_type="batch",
            user_input=user_input,
            final_prompt=final_prompt,
            response=response,
            batch_id=batch_id
        )
