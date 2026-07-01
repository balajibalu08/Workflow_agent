route_decision_fields = {
    "intent": "The intent identified from the user's query.",
    "input_source": "The type of input extracted from the user's query (url, file, text, or missing).",
    "source_value": "The extracted URL, local file path, or plain text depending on the input_source.",
    "requires_user_input": "Indicates whether additional user input is required before continuing.",
    "user_prompt": "The message displayed to the user when additional input is required."
}


spam_analysis_fields = {
    "is_spam": "Whether the email is classified as spam.",
    "confidence_score": "A confidence score between 0.0 and 1.0 indicating how confident the model is in its classification.",
    "category": "The category of the email such as phishing, marketing, scam, malware, or legitimate.",
    "reasoning": "A concise explanation supporting the spam classification.",
    "indicators": "A list of indicators or characteristics that influenced the classification.",
    "recommended_action": "The recommended action the user should take after the analysis."
}