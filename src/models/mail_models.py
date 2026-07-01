from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from utils.field_prompts  import spam_analysis

class SpamAnalysis(BaseModel):
    is_spam:bool = Field(..., description= spam_analysis["is_spam"])
    confidence_score: float = Field(..., gt=0, lt=1, description=spam_analysis["confidence_score"])
    category : Literal[
        "phishing",
        "marketing",
        "scam",
        "malware",
        "legitimate"
    ] = Field(..., description=spam_analysis["category"])
    reasoning : str = Field(..., description=spam_analysis["reasoning"])
    indicators:list[str] = Field(..., description=spam_analysis["indicators"])
    recommended_action : str = Field(..., description=spam_analysis["recommended_action"])
    
    @model_validator(mode="after")
    def check_conditional_fields(self):
        if not self.is_spam and self.category != "Legitimate":
            raise ValueError("If mail is not spam category have to 'Legitimate'")
        if len(self.indicators) == 0:
            raise ValueError("If mail is spam then there should be indicators why the mail is spam")
        if self.reasoning.strip() =="" :
            raise ValueError("Resoning Cant be Empty")
        return self