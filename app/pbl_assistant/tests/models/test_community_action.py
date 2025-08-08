import pytest
import logging

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

def test_community_action_option():
    # 1. Fetch the Community Action template
    templates = get_template_by_intent("COMMUNITY_ACTION")
    assert templates, "No Community Action template registered!"
    template = templates[0]

    # Log and print out the template description and comprehensive overview
    logger.info("Loaded template: %s", template.template_id)
    logger.info("Template description: %s", template.description)
    print("\n=== TEMPLATE OVERVIEW ===")
    print(template.comprehensive_overview)
    print("\n=== COMPATIBLE CONFIGURATIONS ===")
    print(f"Duration: {', '.join([str(d) for d in template.compatibility_matrix.duration_compatible])}")
    print(f"Social Structure: {', '.join([str(s) for s in template.compatibility_matrix.social_structure_compatible])}")
    print(f"Cognitive Complexity: {', '.join([str(c) for c in template.compatibility_matrix.cognitive_complexity_range])}")
    print(f"Authenticity Level: {', '.join([str(a) for a in template.compatibility_matrix.authenticity_compatible])}")
    print(f"Scaffolding Intensity: {', '.join([str(s) for s in template.compatibility_matrix.scaffolding_compatible])}")
    print(f"Product Complexity: {', '.join([str(p) for p in template.compatibility_matrix.product_complexity_compatible])}")
    print(f"Delivery Mode: {', '.join([str(d) for d in template.compatibility_matrix.delivery_mode_compatible])}")
    print("==========================\n")

    # 2. Pick a compatible configuration
    config = DimensionalConfiguration(
        duration=Duration.UNIT,
        social_structure=SocialStructure.COLLABORATIVE,
        cognitive_complexity=CognitiveComplexity.ANALYSIS,
        authenticity_level=AuthenticityLevel.APPLIED,
        scaffolding_intensity=ScaffoldingIntensity.FACILITATED,
        product_complexity=ProductComplexity.PORTFOLIO,
        delivery_mode=DeliveryMode.FACE_TO_FACE,
    )

    # 3. Assert compatibility
    assert template.is_compatible_with_config(config), "Config should be compatible!"
    logger.info("Configuration is compatible with template.")

    # 4. Build a dummy project
    project = ConfiguredProject(
        template=template,
        config=config,
        title="Clean Water for All",
        driving_question="How can we improve access to clean water in our community?",
        key_activities=[
            "Identify local water sources",
            "Test water quality parameters",
            "Design and prototype simple filtration",
            "Partner with local stakeholders",
            "Present findings and action plan",
        ],
        assessment_highlights=[
            "Water quality test report",
            "Filtration prototype demonstration",
            "Community presentation feedback",
        ],
        differentiation_notes=(
            "Offer scaffolded data analysis tools for students who need support; "
            "provide extension activities on filtration design for advanced learners."
        ),
    )

    # 5. Confirm summarize() runs and contains the title
    summary = project.summarize()
    logger.info("Project summary generated.")
    print("\n=== PROJECT SUMMARY ===")
    print(summary)
    print("=======================\n")
    assert "Clean Water for All" in summary
