import requests
import logging

logger = logging.getLogger(__name__)

JOB_SERVICE_URL = "http://localhost:5001"

def get_job_details(job_code,token):

    try:
        response = requests.get(
            f"{JOB_SERVICE_URL}/api/v1/jobs/{job_code}",
            headers={
                "Authorization" : token
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.exception(
            "[JOB_SERVICE_ERROR] job_code=%s error=%s",
            job_code,
            str(e)
        )
        return None