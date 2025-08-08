#!/usr/bin/env python3
"""
Generate JSON files for different dimensional configurations of the Community Action template.
This script creates multiple JSON files showing how the template adapts to different configurations.
"""

import json
import os
from typing import Dict, List, Any

from core.enums import (
    Duration,
    SocialStructure,
    CognitiveComplexity,
    AuthenticityLevel,
    ScaffoldingIntensity,
    ProductComplexity,
    DeliveryMode,
)
from registry.factory import get_template_by_intent
from configuration.dimensional_config import DimensionalConfiguration
from configuration.configured_project import ConfiguredProject

def generate_template_json_files():
    """Generate JSON files for different dimensional configurations."""
    
    # Output file will be in the root of the models/designing folder
    output_file = os.path.join(os.path.dirname(__file__), "community_action_configurations.json")
    
    # 2. Fetch the Community Action template
    templates = get_template_by_intent("COMMUNITY_ACTION")
    if not templates:
        print("Error: No Community Action template registered!")
        return
    template = templates[0]
    
    print(f"Generating JSON files for template: {template.template_id}")
    
    # 3. Define different configurations to test
    configurations = [
        # Configuration 1: Short, Collaborative, Simple (Sprint)
        {
            "name": "sprint_collaborative",
            "config": DimensionalConfiguration(
                duration=Duration.SPRINT,
                social_structure=SocialStructure.COLLABORATIVE,
                cognitive_complexity=CognitiveComplexity.APPLICATION,
                authenticity_level=AuthenticityLevel.SIMULATED,
                scaffolding_intensity=ScaffoldingIntensity.GUIDED,
                product_complexity=ProductComplexity.ARTIFACT,
                delivery_mode=DeliveryMode.FACE_TO_FACE,
                configuration_rationale="Short collaborative project for beginners"
            ),
            "title": "Quick Community Issue Exploration",
            "description": "A short collaborative project to introduce community action concepts"
        },
        
        # Configuration 2: Medium, Collaborative, Moderate (Unit)
        {
            "name": "unit_collaborative",
            "config": DimensionalConfiguration(
                duration=Duration.UNIT,
                social_structure=SocialStructure.COLLABORATIVE,
                cognitive_complexity=CognitiveComplexity.ANALYSIS,
                authenticity_level=AuthenticityLevel.ANCHORED,
                scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
                product_complexity=ProductComplexity.PORTFOLIO,
                delivery_mode=DeliveryMode.FACE_TO_FACE,
                configuration_rationale="Standard team-based unit project"
            ),
            "title": "Community Issue Investigation",
            "description": "A unit-length collaborative project for analyzing community issues"
        },
        
        # Configuration 3: Medium, Community-Connected, Moderate (Unit)
        {
            "name": "unit_community_connected",
            "config": DimensionalConfiguration(
                duration=Duration.UNIT,
                social_structure=SocialStructure.COMMUNITY_CONNECTED,
                cognitive_complexity=CognitiveComplexity.ANALYSIS,
                authenticity_level=AuthenticityLevel.APPLIED,
                scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
                product_complexity=ProductComplexity.PORTFOLIO,
                delivery_mode=DeliveryMode.FACE_TO_FACE,
                configuration_rationale="Community-connected unit project"
            ),
            "title": "Community Partnership Project",
            "description": "A unit-length project with direct community stakeholder engagement"
        },
        
        # Configuration 4: Long, Community-Connected, Complex (Journey)
        {
            "name": "journey_community_connected",
            "config": DimensionalConfiguration(
                duration=Duration.JOURNEY,
                social_structure=SocialStructure.COMMUNITY_CONNECTED,
                cognitive_complexity=CognitiveComplexity.SYNTHESIS,
                authenticity_level=AuthenticityLevel.APPLIED,
                scaffolding_intensity=ScaffoldingIntensity.INDEPENDENT,
                product_complexity=ProductComplexity.SYSTEM,
                delivery_mode=DeliveryMode.HYBRID,
                configuration_rationale="Extended community-connected project"
            ),
            "title": "Community Action Initiative",
            "description": "An extended project with implementation of community solutions"
        },
        
        # Configuration 5: Extended, Networked, Advanced (Campaign)
        {
            "name": "campaign_networked",
            "config": DimensionalConfiguration(
                duration=Duration.CAMPAIGN,
                social_structure=SocialStructure.NETWORKED,
                cognitive_complexity=CognitiveComplexity.EVALUATION,
                authenticity_level=AuthenticityLevel.IMPACT,
                scaffolding_intensity=ScaffoldingIntensity.MENTORED,
                product_complexity=ProductComplexity.EXPERIENCE,
                delivery_mode=DeliveryMode.HYBRID,
                configuration_rationale="Year-long networked community impact project"
            ),
            "title": "Community Impact Campaign",
            "description": "A year-long networked project with significant community impact"
        },
    ]
    
    # 4. Generate JSON files for each configuration
    for config_info in configurations:
        config = config_info["config"]
        name = config_info["name"]
        
        # Check compatibility
        is_compatible = template.is_compatible_with_config(config)
        
        if is_compatible:
            # Create configured project
            project = ConfiguredProject(
                template=template,
                config=config,
                title=config_info["title"],
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
            
            # Add the project data to our configurations list
            config_info["project_data"] = json.loads(project.model_dump_json())
            print(f"Generated configuration for: {name}")
        else:
            print(f"Configuration '{name}' is not compatible with the Community Action template")
    
    # Create the final output structure with all configurations
    output_data = {
        "template_id": template.template_id,
        "display_name": template.display_name,
        "template_data": json.loads(template.model_dump_json()),
        "configurations": []
    }
    
    for config_info in configurations:
        config = config_info["config"]
        is_compatible = template.is_compatible_with_config(config)
        
        config_data = {
            "name": config_info["name"],
            "title": config_info["title"],
            "description": config_info["description"],
            "compatible": is_compatible,
            "dimensions": {
                "duration": str(config.duration),
                "social_structure": str(config.social_structure),
                "cognitive_complexity": str(config.cognitive_complexity),
                "authenticity_level": str(config.authenticity_level),
                "scaffolding_intensity": str(config.scaffolding_intensity),
                "product_complexity": str(config.product_complexity),
                "delivery_mode": str(config.delivery_mode),
            }
        }
        
        # Add the configured project data if compatible
        if is_compatible and "project_data" in config_info:
            config_data["configured_project"] = config_info["project_data"]
            
        output_data["configurations"].append(config_data)
    
    # Save the complete file
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Generated complete configuration file: {output_file}")

if __name__ == "__main__":
    generate_template_json_files()
