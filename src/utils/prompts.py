ResumeAnalysisPrompt = """
                You are an expert HR Resume Analyzer.

                Analyze the provided resume and extract:
                - Candidate information
                - Skills
                - Education
                - Work experience
                - Projects
                - Certifications

                Return the response strictly according to the ResumeAnalysis schema.
                
                Do not invent information.

                If a field is missing from the resume,
                return null or an empty list.

                Do not include explanations or markdown.
                Only return the structured ResumeAnalysis object.
            """

route_decision_prompts={
    "intent":"The type of input extracted from the user's query (URL, local file path, plain text, or missing).",
    "input_source" : "The type of input extracted from the user's query (URL, local file path, plain text, or missing).",
    "source_value" : "The actual input extracted from the user's query. If input_type is 'url', this contains the URL. If 'file', it contains the local file path. If 'text', it contains the user-provided text. It is None when input_type is 'missing'.",
    "requires_user_input" : "Whether additional information is required from the user before continuing.",
    "user_prompt" : "Message to display to the user when additional input is required."
}