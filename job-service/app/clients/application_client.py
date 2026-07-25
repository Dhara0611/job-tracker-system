import requests
import logging

logger = logging.getLogger(__name__)

APPLICATION_SERVICE_URL = "http://localhost:5002"

def get_application_status(token):
    try:
        response = requests.get(
            f"{APPLICATION_SERVICE_URL}/api/v1/applications/user-status",
            headers={
                "Authorization" : token
            },
#Wait maximum 5 seconds for application-service to respond. If it does not respond within 5 seconds, raise an #exception.
            timeout=5
            )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.exception(
            "[APPLICATION_SERVICE_ERROR] error=%s",
            str(e)
        )
        return {
            "data": {}
        }

