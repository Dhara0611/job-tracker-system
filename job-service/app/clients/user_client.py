import requests
import logging

logger = logging.getLogger(__name__)

USER_SERVICE_URL = "http://127.0.0.1:5000"

def get_user_preferences(token):
    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/preferences",
            headers={
                "Authorization" : token
            },
#Wait maximum 5 seconds for application-service to respond. If it does not respond within 5 seconds, raise an #exception.
            timeout=5
            )
        response.raise_for_status()

        logger.info("User preferences response: %s", response)

        response_data =response.json()
        logger.info("User preferences response: %s", response_data)
        return response_data
    
    except requests.exceptions.RequestException as e:
        logger.exception(
            "[USER_SERVICE_ERROR] error=%s",
            str(e)
        )
        return None