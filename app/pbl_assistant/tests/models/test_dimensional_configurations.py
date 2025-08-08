import pytest
import logging
import json
from tabulate import tabulate

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

# Configure root logger to print to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_community_action_dimensions():
    """Test how different dimensional configurations affect the Community Action template."""
    
    # 1. Fetch the Community Action template
    templates = get_template_by_intent("COMMUNITY_ACTION")
    assert templates, "No Community Action template registered!"
    template = templates[0]
    
    # Display the template overview
    print("\n=== TEMPLATE OVERVIEW ===")
    print(template.comprehensive_overview)
    print("==========================\n")
    
    logger.info("Loaded template: %s", template.template_id)
    logger.info("Template description: %s", template.description)
    
    # 2. Define different configurations to test
    configurations = [
        # Configuration 1: Short, Individual, Simple (Sprint)
        DimensionalConfiguration(
            duration=Duration.SPRINT,
            social_structure=SocialStructure.INDIVIDUAL,
            cognitive_complexity=CognitiveComplexity.APPLICATION,
            authenticity_level=AuthenticityLevel.SIMULATED,
            scaffolding_intensity=ScaffoldingIntensity.GUIDED,
            product_complexity=ProductComplexity.ARTIFACT,
            delivery_mode=DeliveryMode.FACE_TO_FACE,
            configuration_rationale="Short individual project for beginners"
        ),
        
        # Configuration 2: Medium, Collaborative, Moderate (Unit)
        DimensionalConfiguration(
            duration=Duration.UNIT,
            social_structure=SocialStructure.COLLABORATIVE,
            cognitive_complexity=CognitiveComplexity.ANALYSIS,
            authenticity_level=AuthenticityLevel.ANCHORED,
            scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
            product_complexity=ProductComplexity.PORTFOLIO,
            delivery_mode=DeliveryMode.FACE_TO_FACE,
            configuration_rationale="Standard team-based unit project"
        ),
        
        # Configuration 3: Long, Community-Connected, Complex (Journey)
        DimensionalConfiguration(
            duration=Duration.JOURNEY,
            social_structure=SocialStructure.COMMUNITY_CONNECTED,
            cognitive_complexity=CognitiveComplexity.SYNTHESIS,
            authenticity_level=AuthenticityLevel.APPLIED,
            scaffolding_intensity=ScaffoldingIntensity.INDEPENDENT,
            product_complexity=ProductComplexity.SYSTEM,
            delivery_mode=DeliveryMode.HYBRID,
            configuration_rationale="Extended community-connected project"
        ),
        
        # Configuration 4: Extended, Networked, Advanced (Campaign)
        DimensionalConfiguration(
            duration=Duration.CAMPAIGN,
            social_structure=SocialStructure.NETWORKED,
            cognitive_complexity=CognitiveComplexity.EVALUATION,
            authenticity_level=AuthenticityLevel.IMPACT,
            scaffolding_intensity=ScaffoldingIntensity.MENTORED,
            product_complexity=ProductComplexity.EXPERIENCE,
            delivery_mode=DeliveryMode.HYBRID,
            configuration_rationale="Year-long networked community impact project"
        ),
    ]
    
    # 3. Test each configuration and collect results
    results = []
    
    for i, config in enumerate(configurations):
        config_name = f"Configuration {i+1}"
        
        # Check compatibility
        is_compatible = template.is_compatible_with_config(config)
        
        if is_compatible:
            # Create configured project
            project = ConfiguredProject(
                template=template,
                config=config,
                title=f"Community Action Project {i+1}",
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
            
            # Extract key differences for comparison
            results.append({
                "Configuration": config_name,
                "Duration": config.duration,
                "Social Structure": config.social_structure,
                "Cognitive Complexity": config.cognitive_complexity,
                "Authenticity Level": config.authenticity_level,
                "Scaffolding": config.scaffolding_intensity,
                "Product Complexity": config.product_complexity,
                "Delivery Mode": config.delivery_mode,
                "Est. Duration": project.estimated_total_duration if hasattr(project, "estimated_total_duration") else "N/A",
                "Group Organization": project.group_organization if hasattr(project, "group_organization") else "N/A",
                "Teacher Role": project.teacher_role_description if hasattr(project, "teacher_role_description") else "N/A",
                "Student Autonomy": project.student_autonomy_level if hasattr(project, "student_autonomy_level") else "N/A",
                "Compatible": "Yes",
            })
        else:
            results.append({
                "Configuration": config_name,
                "Duration": config.duration,
                "Social Structure": config.social_structure,
                "Cognitive Complexity": config.cognitive_complexity,
                "Authenticity Level": config.authenticity_level,
                "Scaffolding": config.scaffolding_intensity,
                "Product Complexity": config.product_complexity,
                "Delivery Mode": config.delivery_mode,
                "Est. Duration": "N/A",
                "Group Organization": "N/A",
                "Teacher Role": "N/A",
                "Student Autonomy": "N/A",
                "Compatible": "No",
            })
    
    # 4. Display results in a table format
    print("\n=== DIMENSIONAL CONFIGURATION COMPARISON ===")
    headers = ["Configuration", "Duration", "Social Structure", "Cognitive Complexity", 
               "Authenticity", "Scaffolding", "Product", "Delivery", "Compatible"]
    table_data = [[
        r["Configuration"],
        r["Duration"],
        r["Social Structure"],
        r["Cognitive Complexity"],
        r["Authenticity Level"],
        r["Scaffolding"],
        r["Product Complexity"],
        r["Delivery Mode"],
        r["Compatible"]
    ] for r in results]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # 5. For compatible configurations, show more detailed differences and JSON
    print("\n=== DETAILED PROJECT DIFFERENCES ===")
    for r in results:
        if r["Compatible"] == "Yes":
            print(f"\n{r['Configuration']} ({r['Duration']}, {r['Social Structure']}, {r['Authenticity Level']}):\n  - Estimated Duration: {r['Est. Duration']}\n  - Group Organization: {r['Group Organization']}\n  - Teacher Role: {r['Teacher Role']}\n  - Student Autonomy: {r['Student Autonomy']}")
            
            # Display the full configured template in JSON format
            config_index = int(r["Configuration"].split()[-1]) - 1
            config = configurations[config_index]
            
            # Create configured project
            project = ConfiguredProject(
                template=template,
                config=config,
                title=f"Community Action Project {config_index+1}",
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
            
            # Display simplified configuration information
            print(f"\n=== CONFIGURATION SUMMARY: {r['Configuration']} ===")
            print(f"Title: {project.title}")
            print(f"Driving Question: {project.driving_question}")
            print(f"Duration: {config.duration}")
            print(f"Social Structure: {config.social_structure}")
            print(f"Cognitive Complexity: {config.cognitive_complexity}")
            print(f"Authenticity Level: {config.authenticity_level}")
            print(f"Scaffolding Intensity: {config.scaffolding_intensity}")
            print(f"Product Complexity: {config.product_complexity}")
            print(f"Delivery Mode: {config.delivery_mode}")
    
    # 6. Assert that at least some configurations are compatible
    assert any(r["Compatible"] == "Yes" for r in results), "No compatible configurations found!"


def test_mixed_dimensional_configurations():
    """Test mixing and matching different dimensional configurations."""
    
    # 1. Fetch the Community Action template
    templates = get_template_by_intent("COMMUNITY_ACTION")
    assert templates, "No Community Action template registered!"
    template = templates[0]
    
    # Display the template overview
    print("\n=== TEMPLATE OVERVIEW ===")
    print(template.comprehensive_overview)
    print("==========================\n")
    
    # 2. Define dimensions to test
    durations = [Duration.SPRINT, Duration.UNIT, Duration.JOURNEY, Duration.CAMPAIGN]
    social_structures = [SocialStructure.INDIVIDUAL, SocialStructure.COLLABORATIVE, 
                        SocialStructure.COMMUNITY_CONNECTED, SocialStructure.NETWORKED]
    
    # 3. Test combinations of duration and social structure
    compatibility_matrix = []
    
    for duration in durations:
        row = []
        for social in social_structures:
            # Create a basic configuration with these two dimensions
            config = DimensionalConfiguration(
                duration=duration,
                social_structure=social,
                cognitive_complexity=CognitiveComplexity.ANALYSIS,  # Default
                authenticity_level=AuthenticityLevel.ANCHORED,      # Default
                scaffolding_intensity=ScaffoldingIntensity.FACILITATED,  # Default
                product_complexity=ProductComplexity.PORTFOLIO,     # Default
                delivery_mode=DeliveryMode.FACE_TO_FACE,           # Default
            )
            
            # Check compatibility
            is_compatible = template.is_compatible_with_config(config)
            row.append("✓" if is_compatible else "✗")
        
        compatibility_matrix.append(row)
    
    # 4. Display compatibility matrix
    print("\n=== COMPATIBILITY MATRIX: DURATION × SOCIAL STRUCTURE ===")
    headers = [""] + [str(s).split(".")[1] for s in social_structures]
    table_data = [[str(d).split(".")[1]] + row for d, row in zip(durations, compatibility_matrix)]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # 5. Test a few specific combinations in detail
    interesting_configs = [
        # Short individual project
        (Duration.SPRINT, SocialStructure.INDIVIDUAL, "Short individual project"),
        # Extended collaborative project
        (Duration.JOURNEY, SocialStructure.COLLABORATIVE, "Extended collaborative project"),
        # Campaign with community connection
        (Duration.CAMPAIGN, SocialStructure.COMMUNITY_CONNECTED, "Year-long community project"),
    ]
    
    print("\n=== SPECIFIC CONFIGURATION DETAILS ===")
    for duration, social, name in interesting_configs:
        config = DimensionalConfiguration(
            duration=duration,
            social_structure=social,
            cognitive_complexity=CognitiveComplexity.ANALYSIS,
            authenticity_level=AuthenticityLevel.APPLIED,
            scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
            product_complexity=ProductComplexity.PORTFOLIO,
            delivery_mode=DeliveryMode.FACE_TO_FACE,
        )
        
        is_compatible = template.is_compatible_with_config(config)
        print(f"\n{name} ({duration}, {social}):")
        print(f"  - Compatible: {'Yes' if is_compatible else 'No'}")
        
        if is_compatible:
            # Create configured project
            project = ConfiguredProject(
                template=template,
                config=config,
                title=f"Community Action: {name}",
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
            
            # Show key project attributes
            if hasattr(project, "estimated_total_duration"):
                print(f"  - Est. Duration: {project.estimated_total_duration}")
            if hasattr(project, "group_organization"):
                print(f"  - Group Organization: {project.group_organization}")
            if hasattr(project, "teacher_role_description"):
                print(f"  - Teacher Role: {project.teacher_role_description}")
            if hasattr(project, "student_autonomy_level"):
                print(f"  - Student Autonomy: {project.student_autonomy_level}")
                
            # Display simplified configuration information
            print(f"\n=== CONFIGURATION SUMMARY: {name} ({duration}, {social}) ===")
            print(f"Title: {project.title}")
            print(f"Driving Question: {project.driving_question}")
            print(f"Duration: {config.duration}")
            print(f"Social Structure: {config.social_structure}")
            print(f"Cognitive Complexity: {config.cognitive_complexity}")
            print(f"Authenticity Level: {config.authenticity_level}")
            print(f"Scaffolding Intensity: {config.scaffolding_intensity}")
            print(f"Product Complexity: {config.product_complexity}")
            print(f"Delivery Mode: {config.delivery_mode}")


if __name__ == "__main__":
    test_community_action_dimensions()
    test_mixed_dimensional_configurations()
