from pydantic import BaseModel,Field, model_validator
from typing import Optional, Literal
from src.utils.field_prompts import route_decision_fields
class RouteDecision(BaseModel):
    intent: Literal[
        "resume_analysis",
        "spam_detection",
        "unknown"
    ] = Field(..., description=route_decision_fields["intent"])
    input_source:Literal[
        "url",
        "text",
        "file",
        "missing"
    ] = Field(...,description=route_decision_fields["input_source"])
    source_value : Optional[str] =  Field(default=None, description=route_decision_fields["source_value"])
    requires_user_input : bool = Field(default= False, description=route_decision_fields["requires_user_input"])
    user_prompt : Optional[str] = Field(default=None, description=route_decision_fields["user_prompt"])
    @model_validator(mode = 'after')
    def check_conditional_fields(self):
        if self.intent == "unknown" and self.requires_user_input is False:
            raise ValueError("if Intent is unkown then requires_user_input must be True")
        if self.input_source == "missing" and self.source_value:
            raise ValueError("source_value must be None when input_source is 'missing'.")
        if self.input_source !="missing" and self.source_value is None:
            raise ValueError("source_value must be provided when input_source is 'url', 'file', or 'text'.")
        if self.requires_user_input and self.user_prompt is None:
            raise ValueError("if requires_user_input is True then user_prompt must not be None")
        if self.requires_user_input is False and self.user_prompt:
            raise ValueError("if requires_user_input is False then user_prompt must  be None")
        return self