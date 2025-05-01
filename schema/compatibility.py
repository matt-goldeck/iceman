class ScoreBreakdown(BaseModel):
    skills_match: int
    experience_alignment: int
    education_match: int
    keyword_overlap: int
    resume_quality: int
    adjustments: int


class CompatibilityScoreResponse(BaseModel):
    score_breakdown: ScoreBreakdown
    total_score: int
    explanation: str
