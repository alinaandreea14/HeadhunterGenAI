# ==============================================================================
# DATA MODELS (PYDANTIC SCHEMAS)
# ==============================================================================

from typing import List, Literal, Self
from pydantic import BaseModel, Field, model_validator

class SalaryRange(BaseModel):
    min: int = Field(..., description="Suma minima a salariului")
    max: int = Field(..., description="Suma maxima a salariului")
    currency: str = Field(..., description="Moneda (ex: RON, EUR, USD, CHF)")
    frequency: Literal["anual", "lunar", "pe ora"] = Field(..., description="Frecvența salariului (ex: anual, lunar, pe ora)")

class Location(BaseModel):
    city: str = Field(..., description="Orasul in care se afla jobul")
    country: str = Field(..., description="Tara in care se afla jobul")
    is_remote: bool = Field(False, description="True daca jobul este remote")
    office_details: str = Field(..., description="Detalii despre birou sau cerințe de prezență fizică (ex: 'Birou în București, 2 zile pe săptămână')")

    @model_validator(mode="after")
    def check_remote_consistency(self) -> Self:
        office_keywords = ["birou", "office", "on-site", "prezență fizică", "in-person", "hibrid"]
        office_details_lower = self.office_details.lower()

        if self.is_remote and any(keyword in office_details_lower for keyword in office_keywords):
            raise ValueError("Inconsistență: 'is_remote' este True, dar 'office_details' sugerează prezență fizică.")
        
        return self

class RedFlag(BaseModel):
    severity: Literal["low", "medium", "high"] = Field(..., description="Nivelul de gravitate al red flag-ului")
    category: Literal["toxicity" "vague", "unrealistic"] = Field(..., description="Categoria problemei identificate")

class JobAnalysis(BaseModel):
    role_title: str = Field(..., description="Titlul jobului standardizat")
    company_name: str = Field(..., description="Numele companiei")
    seniority: Literal["Intern", "Junior", "Mid", "Senior", "Lead", "Architect"] = Field(..., description="Nivelul de experiență dedus")
    match_score: int = Field(..., ge=0, le=100, description="Scor 0-100: Calitatea descrierii jobului")
    tech_stack: List[str] = Field(..., description="Listă cu tehnologii specifice (ex: Python, AWS, React) Poti sa cauti si dupa cuvantul Tech")
    red_flags: List[RedFlag] = Field(..., description="Lista de semnale de alarmă (toxicitate, stres, vaguitate)")
    summary: str = Field(..., description="Un rezumat scurt al rolului (max 2 fraze) în limba română")
    salary_range: SalaryRange = Field(..., description="Intervalul salarial dacă este menționat")
    job_location: Location = Field(..., description="Informații despre locația jobului")