import logging

logger = logging.getLogger(__name__)


def rank_jobs_by_preferences(jobs, preferences):
    """
    Rank jobs based on user preferences.

    jobs: list of Job model objects
    preferences: dictionary returned by user-service
    """
    if not preferences:
        logger.info("No preferences found. Returning jobs without ranking")
        return jobs

    
#ranked jobs will have list of dictionarys of scored jobs
    ranked_jobs = []


    for job in jobs:

        score = 0

        if preferences.get("role") and job.title:
            if preferences["role"].lower() in job.title.lower():
                score += 1

        if preferences.get("location") and job.location:
            if preferences["location"].lower() in job.location.lower():
                score+=1

        ranked_jobs.append(
            {
                "job":job,
                "score": score
            }
        )
        logger.info(
        "Job=%s score=%s",
        job.title,
        score
        )

#sort jobs based on score 
    ranked_jobs.sort(
        key=lambda x: x["score"],reverse=True
    )

#return list of jobs
    return [item["job"] for item in ranked_jobs]
