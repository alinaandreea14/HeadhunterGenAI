# ==============================================================================
# DATA MODELS (PYDANTIC SCHEMAS)
# ==============================================================================

from typing import List, Literal, Self, Optional
from pydantic import BaseModel, Field, model_validator

class SalaryRange(BaseModel):
    min: Optional[int] = Field(default=0, description="Minimum salary value")
    max: Optional[int] = Field(default=0, description="Maximum salary value")
    currency: str = Field(..., description="Currency (eg: RON, EUR, USD, CHF)")
    frequency: Literal["yearly", "monthly", "per hour"] = Field(..., description="Salary frequency (e.g. annual, monthly, per hourly)")

class Location(BaseModel):
    city: str = Field(..., description="The city where the job is located")
    country: str = Field(..., description="Country where the job is located")
    is_remote: bool = Field(False, description="True if the job is remote")
    office_details: str = Field(..., description="Office details or physical presence requirements (e.g. 'Office in Bucharest, 2 days a week, hybrid, on-site')")

    @model_validator(mode="after")
    def check_remote_consistency(self) -> Self:
        office_keywords = ["office", "on-site", "physical presence", "in-person", "hybrid"]
        office_details_lower = self.office_details.lower()

        if self.is_remote and any(keyword in office_details_lower for keyword in office_keywords):
            raise ValueError("Inconsistency: 'is remote' is True, but 'office details' suggests physical presence.")
        
        return self

class RedFlag(BaseModel):
    severity: Literal["low", "medium", "high"] = Field(..., description="Red flag severity level")
    category: Literal["toxicity" "vague", "unrealistic", "unspecified salary", "unspecified salary", "too many years of experience required"] = Field(..., description="Category of the identified problem")

class JobAnalysis(BaseModel):
    role_title: str = Field(..., description="Standardized job title")
    company_name: str = Field(..., description="Company Name")
    seniority: Literal["Intern", "Junior", "Mid", "Senior", "Lead", "Architect", "Mid to Senior", "Junior to Mid"] = Field(..., description="Inferred experience level")
    match_score: int = Field(..., ge=0, le=100, description="Score 0-100: Quality of the job description")
    tech_stack: List[str] = Field(..., description="List of specific technologies (in: Python, AWS, React) You can also search by the word Tech")
    red_flags: List[RedFlag] = Field(..., description="List of alarm signals (toxicity, stress, vagueness, unspecified salary, unspecified salary, too many years of experience required)")
    summary: str = Field(..., description="A short summary of the role (max 2 sentences) in Romanian")
    salary_range: Optional[SalaryRange] = Field(..., description="Salary range if mentioned")
    job_location: Location = Field(..., description="Job location information")