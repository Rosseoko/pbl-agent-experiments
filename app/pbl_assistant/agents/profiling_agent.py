from pydantic_ai import Agent, RunContext
from pydantic_ai.models.bedrock import BedrockConverseModel
from app.pbl_assistant.models.profiling import ProjectDetails, TeacherRequest

# Simple profiling agent - NO TOOLS
profiling_agent = Agent(
    model=BedrockConverseModel("anthropic.claude-3-haiku-20240307-v1:0"),
    deps_type=TeacherRequest,
    result_type=ProjectDetails,
    result_retries=3,
    system_prompt="""
    You are an expert at analyzing educational project requests and creating detailed project profiles.
    
    CRITICAL INSTRUCTIONS FOR NON-ENGLISH REQUESTS:
    1. First, detect if the request is in a language other than English
    2. If it's not English, you MUST:
       - Set original_language to the language code (e.g., 'es', 'fr', 'de', 'zh')
       - Set original_utterance to the exact original text
       - Translate the text to English mentally
       - Set translated_utterance to your English translation
       - Base ALL your analysis on the English translation
    3. If it's already English:
       - Set original_language to 'en'
       - Leave original_utterance empty or null
       - Leave translated_utterance empty or null
    
    ALWAYS create your project profile analysis in English, regardless of input language.
    Be thorough and detailed in your analysis.
    """
)

@profiling_agent.system_prompt
async def add_user_request(ctx: RunContext[TeacherRequest]) -> str:
    """Add the user's request to the prompt."""
    return f"""
    ## Teacher's Project Request
    {ctx.deps.raw_message}
    
    Analyze this request carefully and create a detailed project profile.
    Remember to handle language translation as specified in your instructions.
    """

async def create_project_profile(request: TeacherRequest) -> dict:
    """Create a project profile from a teacher's request."""
    try:
        # Run the agent
        result = await profiling_agent.run(
            "Create a comprehensive project profile based on the teacher's request.", 
            deps=request
        )
        
        if not result or not result.data:
            return {"success": False, "error": "Failed to create profile"}
        
        # Add age data if available
        profile = result.data
        if hasattr(request, 'raw_message'):
            from app.pbl_assistant.utils.profiling import process_age_input
            age_data = process_age_input(request.raw_message)
            
            if age_data and age_data.get('ages'):
                if age_data.get('age_range', {}).get('min') is not None:
                    profile.age_range = age_data['age_range']
                
                if not profile.grade_level and age_data.get('grade_info', {}).get('all_grades'):
                    grades = age_data['grade_info']['all_grades']
                    profile.grade_level = grades[0] if len(grades) == 1 else f"{grades[0]}-{grades[-1]}"
        
        return {"success": True, "profile": profile.dict()}
        
    except Exception as e:
        return {"success": False, "error": str(e)}