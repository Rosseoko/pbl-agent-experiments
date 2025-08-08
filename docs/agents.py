from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional
from dataclasses import dataclass
import logfire
import json

logfire.configure(send_to_logfire='if-token-present')
# model = get_model()  # Your model setup

# =============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUTS
# =============================================================================

class ProfileData(BaseModel):
    """Student and project profile information."""
    response: str = Field(description='Response to user if more information is needed')
    grade_level: str = Field(description='Student grade level (e.g., "5th grade", "High School")')
    subject_area: str = Field(description='Primary subject (e.g., "Science", "Math", "English")')
    class_size: int = Field(description='Number of students in class')
    student_demographics: str = Field(description='Brief description of student population')
    learning_objectives: List[str] = Field(description='Key learning goals for the unit')
    duration_weeks: int = Field(description='Desired unit length in weeks')
    available_resources: str = Field(description='Available technology, materials, budget constraints')
    special_considerations: str = Field(description='Any special needs, constraints, or preferences')
    all_details_given: bool = Field(description='True if profile is complete, false if more info needed')

class StandardsAlignment(BaseModel):
    """Educational standards and learning objectives."""
    response: str = Field(description='Summary of standards alignment')
    primary_standards: List[str] = Field(description='Main educational standards addressed')
    learning_goals: List[str] = Field(description='Specific measurable learning objectives')
    prerequisite_knowledge: List[str] = Field(description='Required prior knowledge/skills')
    key_concepts: List[str] = Field(description='Core concepts students will learn')
    cross_curricular_connections: List[str] = Field(description='Connections to other subjects')

class ProjectOptions(BaseModel):
    """Multiple project alternatives for teacher selection."""
    response: str = Field(description='Introduction to the project options')
    projects: List[Dict[str, Any]] = Field(description='List of 3-4 project alternatives')
    recommendation: str = Field(description='Which project is recommended and why')

class CurriculumPlan(BaseModel):
    """Detailed curriculum structure."""
    response: str = Field(description='Overview of the curriculum plan')
    unit_overview: str = Field(description='High-level description of the unit')
    weekly_breakdown: List[Dict[str, Any]] = Field(description='Week-by-week lesson plans')
    key_activities: List[Dict[str, Any]] = Field(description='Major learning activities and projects')
    timeline: Dict[str, str] = Field(description='Important milestones and deadlines')
    differentiation_strategies: List[str] = Field(description='How to support different learners')

class AssessmentPlan(BaseModel):
    """Comprehensive assessment strategy."""
    response: str = Field(description='Overview of assessment approach')
    formative_assessments: List[Dict[str, Any]] = Field(description='Ongoing assessment methods')
    summative_assessments: List[Dict[str, Any]] = Field(description='Final evaluation methods')
    rubrics: List[Dict[str, Any]] = Field(description='Detailed scoring rubrics')
    self_reflection_tools: List[str] = Field(description='Student self-assessment methods')
    peer_assessment_methods: List[str] = Field(description='Peer evaluation strategies')

class ResourceList(BaseModel):
    """Materials and resources needed."""
    response: str = Field(description='Overview of resource requirements')
    required_materials: List[Dict[str, Any]] = Field(description='Essential materials with costs/sources')
    optional_materials: List[Dict[str, Any]] = Field(description='Nice-to-have resources')
    digital_tools: List[Dict[str, Any]] = Field(description='Technology and software needed')
    reference_materials: List[Dict[str, Any]] = Field(description='Books, articles, websites for students/teacher')
    estimated_total_cost: str = Field(description='Approximate budget needed')

class FinalUnit(BaseModel):
    """Complete PBL unit package."""
    response: str = Field(description='Introduction to the complete unit')
    unit_title: str = Field(description='Engaging title for the PBL unit')
    executive_summary: str = Field(description='One-page overview for administrators')
    teacher_guide: Dict[str, Any] = Field(description='Complete implementation guide')
    student_materials: List[Dict[str, Any]] = Field(description='All student-facing materials')
    assessment_package: Dict[str, Any] = Field(description='Complete assessment materials')
    resource_list: Dict[str, Any] = Field(description='Final resource compilation')
    implementation_timeline: Dict[str, Any] = Field(description='Step-by-step implementation plan')

# =============================================================================
# SIMPLIFIED AGENTS
# =============================================================================

# PROFILING AGENT
project_profiling_agent = Agent(
    model,
    result_type=ProfileData,
    system_prompt="""
You are a PBL (Project-Based Learning) planning assistant who helps teachers create comprehensive student profiles.

Your goal is to gather all necessary information about:
- Grade level and subject area
- Class size and student demographics  
- Learning objectives and goals
- Unit duration (in weeks)
- Available resources and technology
- Any special considerations or constraints

Ask follow-up questions naturally to get complete information. Be encouraging and help teachers think through what they want students to learn and achieve.

Output all the information you have in the required format, and ask for any missing details if necessary.
""",
    retries=2
)

# STANDARDS AGENT  
standards_agent = Agent(
    model,
    result_type=StandardsAlignment,
    system_prompt="""
You are an educational standards expert who aligns PBL projects with appropriate learning standards.

Based on the student profile provided, identify:
- Relevant educational standards (Common Core, NGSS, state standards, etc.)
- Specific measurable learning objectives
- Prerequisite knowledge students need
- Key concepts to be mastered
- Cross-curricular connections

Focus on standards that naturally fit with project-based learning approaches. Ensure objectives are measurable and age-appropriate.
""",
    retries=2
)

# PROJECT OPTIONS AGENT
project_options_agent = Agent(
    model,
    result_type=ProjectOptions,
    system_prompt="""
You are a creative PBL project designer who generates engaging project alternatives.

Based on the student profile and standards alignment, create 3-4 distinct project options that:
- Address the learning objectives authentically
- Are engaging and relevant to students
- Fit within the time and resource constraints
- Allow for student choice and voice
- Connect to real-world applications

Each project should have a clear title, description, final product/presentation, and key learning activities. Provide a recommendation with reasoning.
""",
    retries=2
)

# CURRICULUM PLANNING AGENT
curriculum_planning_agent = Agent(
    model,
    result_type=CurriculumPlan,
    system_prompt="""
You are a curriculum designer who creates detailed PBL implementation plans.

Based on the selected project, develop:
- Weekly breakdown of lessons and activities
- Key learning experiences and milestones
- Timeline with important deadlines
- Differentiation strategies for diverse learners
- Integration of formative assessments

Ensure the plan follows PBL best practices: student-centered, inquiry-driven, with authentic products and presentations.
""",
    retries=2
)

# ASSESSMENT DESIGN AGENT
assessment_design_agent = Agent(
    model,
    result_type=AssessmentPlan,
    system_prompt="""
You are an assessment specialist who designs comprehensive evaluation strategies for PBL units.

Create an assessment plan that includes:
- Formative assessments throughout the project
- Summative assessments of final products/presentations
- Detailed rubrics for major assignments
- Self-reflection and peer assessment opportunities
- Methods to assess both content knowledge and 21st-century skills

Focus on authentic assessment that evaluates real learning, not just compliance.
""",
    retries=2
)

# RESOURCE COMPILATION AGENT
resource_compilation_agent = Agent(
    model,
    result_type=ResourceList,
    system_prompt="""
You are a resource specialist who compiles materials needed for PBL implementation.

Based on the curriculum and assessment plans, identify:
- Required materials with specific sources and costs
- Optional enhancement materials
- Digital tools and technology needs
- Reference materials for students and teachers
- Estimated total budget

Prioritize cost-effective, accessible resources. Suggest alternatives for different budget levels.
""",
    retries=2
)

# FINAL ASSEMBLY AGENT
final_assembly_agent = Agent(
    model,
    result_type=FinalUnit,
    system_prompt="""
You are a PBL unit packager who creates comprehensive, ready-to-implement units.

Integrate all components into a complete package including:
- Engaging unit title and executive summary
- Complete teacher implementation guide
- All student-facing materials and handouts
- Assessment package with rubrics
- Final resource compilation
- Step-by-step implementation timeline

Ensure everything is organized, professional, and ready for immediate classroom use.
""",
    retries=2
)

# =============================================================================
# REFINEMENT AGENTS (Simplified)
# =============================================================================

class RefinementResult(BaseModel):
    """Result of refinement process."""
    response: str = Field(description='Explanation of changes made')
    updated_component: Dict[str, Any] = Field(description='The refined component')
    changes_summary: List[str] = Field(description='List of specific changes made')

curriculum_refinement_agent = Agent(
    model,
    result_type=RefinementResult,
    system_prompt="""
You are a curriculum refinement specialist who improves PBL plans based on teacher feedback.

Analyze the feedback provided and make targeted improvements to:
- Address specific concerns or requests
- Enhance clarity and implementation guidance
- Improve alignment with teacher needs
- Maintain PBL best practices

Explain what changes you made and why.
""",
    retries=2
)

assessment_refinement_agent = Agent(
    model,
    result_type=RefinementResult,
    system_prompt="""
You are an assessment refinement specialist who improves evaluation strategies based on teacher feedback.

Refine the assessment plan to:
- Address teacher concerns or preferences
- Improve clarity of rubrics and expectations
- Better align with curriculum activities
- Maintain authentic assessment principles

Explain your refinements clearly.
""",
    retries=2
)

resource_refinement_agent = Agent(
    model,
    result_type=RefinementResult,
    system_prompt="""
You are a resource refinement specialist who optimizes material lists based on teacher feedback.

Adjust the resource list to:
- Work within budget constraints
- Replace unavailable or difficult-to-source materials
- Add requested resources or alternatives
- Maintain quality learning experiences

Document all changes and alternatives provided.
""",
    retries=2
)

global_refinement_agent = Agent(
    model,
    result_type=RefinementResult,
    system_prompt="""
You are a holistic PBL refinement specialist who makes final improvements to complete units.

Based on teacher feedback, make cohesive improvements across:
- Curriculum flow and pacing
- Assessment integration
- Resource optimization
- Implementation guidance

Ensure all components work together seamlessly while addressing the specific feedback provided.
""",
    retries=2
)

# =============================================================================
# EXAMPLE USAGE IN GRAPH NODES
# =============================================================================

async def create_project_profile(state: PBLState, writer) -> Dict[str, Any]:
    """Gather student and project profile information from teacher."""
    writer("👥 Gathering project profile information...")
    
    # Get conversation history from state
    conversation_history = state.get("messages", [])
    user_input = state.get("user_input", "")
    
    # Run the profiling agent
    result = await project_profiling_agent.run(user_input)
    
    return {
        "profile_data": result.data.model_dump(),
        "profile_complete": result.data.all_details_given,
        "messages": conversation_history + [result.data.response],
        "current_phase": "profiling"
    }

async def get_standards(state: PBLState, writer) -> Dict[str, Any]:
    """Fetch and process educational standards based on profile."""
    writer("🎯 Aligning with educational standards...")
    
    profile_data = state["profile_data"]
    
    # Create context for the agent
    context = f"""
    Student Profile:
    - Grade Level: {profile_data.get('grade_level')}
    - Subject Area: {profile_data.get('subject_area')}
    - Learning Objectives: {profile_data.get('learning_objectives')}
    - Duration: {profile_data.get('duration_weeks')} weeks
    - Special Considerations: {profile_data.get('special_considerations')}
    """
    
    result = await standards_agent.run(context)
    
    return {
        "standards_data": result.data.model_dump(),
        "current_phase": "design"
    }

# Similar pattern for other nodes...