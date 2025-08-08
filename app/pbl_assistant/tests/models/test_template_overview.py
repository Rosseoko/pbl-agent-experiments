#!/usr/bin/env python3
"""
Test script to output the template overview and configuration in JSON format.
This simplified test focuses on displaying just the template blurb and configuration options.
"""

import json
import pytest
import logging

from app.pbl_assistant.models.designing.core.enums import (
    Duration,
    SocialStructure,
    CognitiveComplexity,
    AuthenticityLevel,
    ScaffoldingIntensity,
    ProductComplexity,
    DeliveryMode,
)
from app.pbl_assistant.models.designing.configuration.dimensional_config import DimensionalConfiguration
from app.pbl_assistant.models.designing.configuration.configured_project import ConfiguredProject
from app.pbl_assistant.models.designing.templates.applied_creative.community_action import TEMPLATE as community_action_template

# Configure root logger to print to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_template_overview_and_config():
    """Test that the template overview and configuration can be generated"""
    # Use the directly imported Community Action template -> select right template
    template = community_action_template
    print(f"Testing template: {template.display_name}")
    
    # 2. Create a compatible configuration
    config = DimensionalConfiguration(
        duration=Duration.UNIT,
        social_structure=SocialStructure.COLLABORATIVE,
        cognitive_complexity=CognitiveComplexity.ANALYSIS,
        authenticity_level=AuthenticityLevel.APPLIED,
        scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
        product_complexity=ProductComplexity.PORTFOLIO,
        delivery_mode=DeliveryMode.FACE_TO_FACE,
        configuration_rationale="Standard team-based unit project"
    )
    
    # 3. Check compatibility
    is_compatible = template.is_compatible_with_config(config)
    assert is_compatible, "Configuration should be compatible with the template!"
    
    # 4. Create a configured project
    project = ConfiguredProject(
        template=template,
        config=config,
        title="Community Issue Investigation",
        driving_question="How can we address a critical need in our community?",
        key_activities=[
            "Identify community issues",
            "Research root causes",
            "Develop action plans",
            "Implement solutions",
            "Evaluate impact"
        ],
        assessment_highlights=[
            "Community needs assessment",
            "Action plan presentation",
            "Implementation documentation",
            "Impact evaluation report"
        ],
        differentiation_notes="Provide scaffolded research templates for students who need support; offer extension opportunities for advanced students to engage with community stakeholders."
    )
    
    # 5. Create a teacher-friendly JSON output with just the overview and configuration
    
    # Create a focused teacher-friendly JSON output with only the most essential elements
    output = {
        "template_name": template.display_name,
        "tagline": template.description,
        # Key elements for teachers at the top
        "key_elements": {
            "driving_question": project.driving_question,
            "final_product": template.final_product_description,
            "core_skills": [
                {
                    "skill": skill.skill_name,
                    "application": skill.application,
                    "assessment_connection": skill.assessment_connection
                } for skill in template.core_skills
            ]
        },
        "overview": template.comprehensive_overview,
        "configuration_details": {
            "time_commitment": config.duration.display_name,
            "collaboration_type": config.social_structure.display_name,
            "thinking_level": config.cognitive_complexity.display_name,
            "real_world_connection": config.authenticity_level.display_name,
            "teacher_guidance": config.scaffolding_intensity.display_name,
            "final_product": config.product_complexity.display_name,
            "instructional_mode": config.delivery_mode.display_name
        },
        "implementation": {
            "suggested_title": "Local Environmental Impact Initiative",
            "key_learning_activities": [
                "Wonder about community challenges that matter to students",
                "Interview community members to understand multiple perspectives", 
                "Prototype and test creative solutions with community feedback",
                "Facilitate community dialogue about proposed actions",
                "Reflect on growth as civic changemakers"
            ]
        },
        "assessment_highlights": template.assessment_highlights,
        "community_engagement_level": template.community_engagement_level,
        "student_readiness": template.student_readiness,
        "what_success_looks_like": template.what_success_looks_like
    }
    
    # 6. Output the JSON
    print("\n=== TEMPLATE OVERVIEW AND CONFIGURATION (JSON) ===")
    print(json.dumps(output, indent=2))
    print("==================================================\n")
    
    # 7. Save the JSON to a file in the same directory as this script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "template_overview.json")
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"JSON saved to: {output_file}")

if __name__ == "__main__":
    test_template_overview_and_config()
