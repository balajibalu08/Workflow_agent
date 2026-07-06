from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from src.utils.field_prompts  import spam_analysis_fields

class SpamAnalysis(BaseModel):
    is_spam:bool = Field(..., description= spam_analysis_fields["is_spam"])
    confidence_score: float = Field(..., gt=0, lt=1, description=spam_analysis_fields["confidence_score"])
    category : Literal[
        "phishing",
        "marketing",
        "scam",
        "malware",
        "legitimate"
    ] = Field(..., description=spam_analysis_fields["category"])
    reasoning : str = Field(..., description=spam_analysis_fields["reasoning"])
    indicators:list[str] = Field(..., description=spam_analysis_fields["indicators"])
    recommended_action : str = Field(..., description=spam_analysis_fields["recommended_action"])

    @model_validator(mode="after")
    def check_conditional_fields(self):
        if not self.is_spam and self.category != "legitimate":
            raise ValueError("If mail is not spam category have to 'Legitimate'")
        if len(self.indicators) == 0:
            raise ValueError("If mail is spam then there should be indicators why the mail is spam")
        if self.reasoning.strip() =="" :
            raise ValueError("Resoning Cant be Empty")
        return self