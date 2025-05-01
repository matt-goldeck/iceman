import json
import openai
from pydantic import ValidationError
from sqlmodel import Session

from llms.base import BaseLLMAgent, LLMInput, LLMRole
from llms.exceptions import FailedToParseAgentResponse
from models.job_listing import CompatibilityScore, JobListing
from models.resume import Resume
from repositories.job_listing import CompatibilityScoreRepository
from schema.compatibility import CompatibilityScoreResponse


class CompatibilityScoringService:
    def __init__(self, llm: BaseLLMAgent, session: Session):
        self.session = session
        self.llm = llm

    def score(self, job_listing: JobListing, resume: Resume) -> CompatibilityScore:
        """
        Calculate a compatibility score between a job listing and a resume.
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(job_listing, resume)

        raw_response = self._call_llm(user_prompt, system_prompt)

        try:
            json_response = json.loads(raw_response)
            score_data = CompatibilityScoreResponse.model_validate(json_response)
        except json.JSONDecodeError as e:
            raise FailedToParseAgentResponse("LLM output is not valid JSON") from e
        except ValidationError as e:
            raise FailedToParseAgentResponse(
                "LLM output did not match expected schema"
            ) from e

        return self._create_score(score_data)

    def _create_score(
        self,
        score_data: CompatibilityScoreResponse,
        job_listing: JobListing,
        resume: Resume,
    ):
        repo = CompatibilityScoreRepository(self.session)
        return repo.create(
            CompatibilityScore(
                job_listing_id=job_listing.id,
                resume_id=resume.id,
                total_score=score_data.total_score,
                explanation=score_data.explanation,
                score_breakdown=score_data.score_breakdown.model_dump(),
            )
        )

    def _call_llm(self, user_prompt: str, system_prompt: str) -> dict:
        self.llm.get_response(input=[system_prompt, user_prompt])

    def _build_system_prompt(self) -> LLMInput:
        # TODO: Should this have knowledge of the company/industry/job?
        raw_system_prompt = (
            "You are an expert technical recruiter and career coach. "
            "You have deep knowledge of the job market and the skills required for various roles."
            "Given a job listing and a resume, assess compatibility on a scale of 0 to 100."
        )
        return LLMInput(role=LLMRole.system, content=raw_system_prompt)

    def _build_user_prompt(self, job_listing: JobListing, resume: Resume) -> LLMInput:
        prompt = f"""
Given a **job listing** and a **candidate's resume**, assess the candidate's **compatibility score** on a scale of 0 to 100 using the following criteria and weights:

{self._get_scoring_criteria()}

{self._get_output_instructions()}

---

### Job Title:
{job_listing.title}

### Job Description:
{job_listing.description}

---

### Resume:
{resume.content}
"""
        return prompt

    def _get_output_instructions(self) -> str:
        # TODO: make this be dynamic to match the pydantic model
        return """Return your response in the following JSON format:
{
    "score_breakdown": {
        "skills_match": 0,
        "experience_alignment": 0,
        "education_match": 0,
        "keyword_overlap": 0,
        "resume_quality": 0,
        "adjustments": 0
    },
    "total_score": 0,
    "explanation": "Your explanation here",
}
"""

    def _get_scoring_criteria(self) -> str:
        return """
### Scoring Categories

1. Skills Match (35 pts max)  
Evaluate how well the candidate's hard and soft skills match the required and preferred skills in the job listing.

2. Experience Alignment (25 pts max)  
Consider role titles, years of experience, seniority, relevant industries, domain familiarity, and career progression.

3. Education Match (10 pts max)  
Evaluate degree level, field of study, and relevance to the job requirements. Consider certifications if applicable.

4. Keyword Overlap (15 pts max)  
Assess overlap of significant terms and phrases from the job description and the resume. Focus on technologies, responsibilities, and key business terms.

5. Resume Quality & Clarity (15 pts max)  
Assess formatting, grammar, use of measurable outcomes, clarity of bullet points, and logical structure.

### Optional Adjustments (±5 pts each, up to ±10 total)
- +5 for strong location match  
- +5 for clear motivation or cultural fit  
- -5 for missing hard requirements  
- -5 for frequent job hopping or unexplained gaps
"""
