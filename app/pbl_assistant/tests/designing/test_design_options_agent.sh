#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8001"
OUTPUT_FILE="$(dirname "$0")/test_options_results.json"
TEST_RESULTS=()
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Function to format JSON output
format_json() {
    jq . 2>/dev/null || echo "$1"
}

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}================================================================${NC}"
    echo -e "🧪 ${1}"
    echo -e "${YELLOW}================================================================${NC}"
}

# Function to save results to JSON file
save_results() {
    local results=("$@")
    local json_output
    
    # Convert array of results to JSON array
    json_output=$(printf '%s\n' "${results[@]}" | jq -s '.' 2>/dev/null)
    
    # Create final JSON structure
    local final_json=$(jq -n --arg timestamp "$TIMESTAMP" --argjson tests "$json_output" '
    {
        "metadata": {
            "test_run_timestamp": $timestamp,
            "total_tests": ($tests | length),
            "api_endpoint": "'"$BASE_URL"'/design_options"
        },
        "tests": $tests
    }' 2>/dev/null)
    
    # Save to file with pretty print
    echo "$final_json" | jq '.' > "$OUTPUT_FILE"
    echo -e "\n💾 Results saved to: $OUTPUT_FILE"
}

# Function to run a test and collect results
run_test() {
    local test_id=$1
    local test_name=$2
    local request_file=$3
    
    print_header "${test_name}"
    
    echo -e "📝 TEST REQUEST:"
    echo "----------------"
    cat "$request_file"
    
    local url="$BASE_URL/design_options"
    
    echo -e "\n🚀 SENDING REQUEST..."
    
    # Make the API request
    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "@$request_file" 2>/dev/null)
    
    # Debug: Show raw response
    echo -e "\n📄 RAW RESPONSE:"
    echo "----------------"
    echo "$response" | jq '.' || echo "$response"
    echo -e "\n"
    
    # Parse the response
    local status=$(echo "$response" | jq -r '.success // "false"' 2>/dev/null || echo "error")
    
    if [[ "$status" == "true" ]]; then
        echo -e "\n✅ Test passed!\n"
        
        # Extract selected template
        SELECTED_TEMPLATE=$(echo "$response" | jq -r '.selected_template // ""')
        
        # Display selected template
        if [ -n "$SELECTED_TEMPLATE" ]; then
            echo -e "🔍 SELECTED TEMPLATE:"
            echo "-------------------"
            echo "$SELECTED_TEMPLATE" | fold -s -w 80
            echo -e "\n"
        fi
        
        # Create result object
        local result=$(echo "$response" | jq --arg test_id "$test_id" --arg test_name "$test_name" '
        {
            test_id: $test_id,
            test_name: $test_name,
            status: "success",
            selected_template: .selected_template,
            result: .options
        }' 2>/dev/null)
        
        # Add to results array
        TEST_RESULTS+=("$result")
        
        # Display project options
        echo -e "📊 PROJECT OPTIONS:"
        echo "-------------------"
        
        # Show project options
        echo -e "\nProject Options:"
        echo "$response" | jq -r '.options.project_options[0:3][] | "- " + .title + ": " + .focus_approach' 2>/dev/null || echo "  No project options found"
        
        # Show configuration details
        echo -e "\nConfiguration Details:"
        echo "$response" | jq -r '.options.configuration_details | to_entries[] | "- " + .key + ": " + .value' 2>/dev/null || echo "  No configuration details found"
        
    else
        echo -e "\n ${RED}Test failed!${NC}"
        local error_msg=$(echo "$response" | jq -r '.error // "Unknown error"' 2>/dev/null || echo 'Invalid response')
        echo -e "\nError: $error_msg"
        
        # Create error result
        local result=$(jq -n --arg test_id "$test_id" --arg test_name "$test_name" --arg error "$error_msg" '
        {
            test_id: $test_id,
            test_name: $test_name,
            status: "error",
            error: $error
        }' 2>/dev/null)
        
        # Add to results array
        TEST_RESULTS+=("$result")
    fi
}

# Initialize the results array if it doesn't exist
declare -a TEST_RESULTS

# Main execution
echo -e "🚀 Starting Design Options Agent Tests..."

# Test 1: Weather and Climate Project
cat > test1_options_request.json << 'EOL'
{
    "project_profile": {
        "topic": "Weather and Climate",
        "grade_level": "5",
        "duration_preference": "3 weeks",
        "primary_intent": "Scientific Inquiry",
        "content_area_focus": "STEM Heavy",
        "student_count": 25,
        "student_demographics": {
            "english_language_learners": "moderate",
            "special_education": "few",
            "socioeconomic_diversity": "high"
        },
        "resource_constraints": {
            "technology_access": "moderate",
            "classroom_space": "adequate",
            "funding": "limited"
        },
        "teacher_experience": {
            "pbl_experience": "beginner",
            "subject_expertise": "moderate",
            "collaboration_support": "minimal"
        },
        "learning_priorities": {
            "hands_on_learning": "high",
            "community_connection": "medium",
            "research_skills": "high",
            "design_challenge": "medium",
            "presentation_skills": "medium"
        }
    },
    "standards_alignment": {
        "standards": [
            {
                "code": "5-ESS2-1",
                "type": "ngss",
                "description": "Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or atmosphere interact.",
                "grade_level": "5",
                "is_valid": true,
                "primary_bloom_level": "create",
                "dok_level": "extended_thinking",
                "project_specific_vocabulary": [
                    "atmosphere",
                    "hydrosphere",
                    "geosphere",
                    "weather patterns",
                    "climate"
                ],
                "learning_objectives": [
                    {
                        "objective": "Explain how the atmosphere, hydrosphere, and geosphere interact to influence weather patterns and climate in the Weather and Climate project.",
                        "bloom_level": "understand",
                        "dok_level": "skill_concept"
                    },
                    {
                        "objective": "Create a model that demonstrates the interactions between the Earth's systems that drive weather and climate in the Weather and Climate project.",
                        "bloom_level": "create",
                        "dok_level": "extended_thinking"
                    }
                ]
            }
        ],
        "alignment_confidence": 0.95,
        "validation_issues": []
    },
    "kg_insights": {
        "standard_code": "5-ESS2-1",
        "standard_description": "Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or atmosphere interact.",
        "description": "Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or atmosphere interact.",
        "topics": [
            {
                "name": "Scientific Inquiry",
                "subtopics": [
                    "Observation",
                    "Hypothesis Testing",
                    "Data Analysis"
                ]
            },
            {
                "name": "Systems Thinking",
                "subtopics": [
                    "Interactions",
                    "Patterns",
                    "Cause and Effect"
                ]
            },
            {
                "name": "Evidence-Based Reasoning",
                "subtopics": [
                    "Data Collection",
                    "Analysis",
                    "Conclusions"
                ]
            }
        ],
        "cross_standards": [
            {
                "code": "CCSS.MATH.CONTENT.5.MD.B.2",
                "subject": "Mathematics",
                "description": "Represent and interpret data"
            },
            {
                "code": "NGSS.5-ESS3-1",
                "subject": "Science",
                "description": "Analyze environmental impacts"
            },
            {
                "code": "CCSS.ELA-LITERACY.SL.5.4",
                "subject": "ELA",
                "description": "Present findings clearly"
            }
        ],
        "sdg_connections": [
            {
                "goal": 4,
                "name": "Quality Education",
                "applications": [
                    "Educational equity projects",
                    "Learning technology integration",
                    "Inclusive classroom design"
                ]
            },
            {
                "goal": 11,
                "name": "Sustainable Communities",
                "applications": [
                    "Community improvement projects",
                    "Urban planning activities",
                    "Local problem-solving initiatives"
                ]
            },
            {
                "goal": 17,
                "name": "Partnerships for Goals",
                "applications": [
                    "Collaborative research projects",
                    "Community partnerships",
                    "Cross-cultural exchanges"
                ]
            }
        ],
        "curricula": [
            {
                "name": "Project Lead The Way",
                "grade_range": "K-12"
            },
            {
                "name": "Expeditionary Learning",
                "grade_range": "5-8"
            },
            {
                "name": "Buck Institute PBL",
                "grade_range": "K-12"
            }
        ]
    }
}
EOL
run_test "test1" "Weather and Climate Project (5-ESS2-1)" "test1_options_request.json"

# Test 2: Community Helpers Project
cat > test2_options_request.json << 'EOL'
{
    "project_profile": {
        "topic": "Community Helpers",
        "grade_level": "1",
        "duration_preference": "2 weeks",
        "primary_intent": "Community Action",
        "content_area_focus": "Humanities Focused",
        "student_count": 20,
        "student_demographics": {
            "english_language_learners": "high",
            "special_education": "moderate",
            "socioeconomic_diversity": "high"
        },
        "resource_constraints": {
            "technology_access": "limited",
            "classroom_space": "adequate",
            "funding": "minimal"
        },
        "teacher_experience": {
            "pbl_experience": "beginner",
            "subject_expertise": "high",
            "collaboration_support": "moderate"
        },
        "learning_priorities": {
            "hands_on_learning": "high",
            "community_connection": "high",
            "research_skills": "low",
            "design_challenge": "low",
            "presentation_skills": "medium"
        }
    },
    "standards_alignment": {
        "standards": [
            {
                "code": "CCSS.ELA-LITERACY.SL.1.4",
                "type": "ccss_ela",
                "description": "Describe people, places, things, and events with relevant details, expressing ideas and feelings clearly.",
                "grade_level": "1",
                "is_valid": true,
                "primary_bloom_level": "understand",
                "dok_level": "skill_concept",
                "project_specific_vocabulary": [
                    "community helpers",
                    "jobs",
                    "roles",
                    "presentation"
                ],
                "learning_objectives": [
                    {
                        "objective": "Describe different community helpers and their roles with relevant details in the Community Helpers project.",
                        "bloom_level": "understand",
                        "dok_level": "skill_concept"
                    },
                    {
                        "objective": "Present information about a community helper with clear expression of ideas in the Community Helpers project.",
                        "bloom_level": "apply",
                        "dok_level": "strategic_thinking"
                    }
                ]
            }
        ],
        "alignment_confidence": 0.92,
        "validation_issues": []
    },
    "kg_insights": {
        "standard_code": "CCSS.ELA-LITERACY.SL.1.4",
        "standard_description": "Describe people, places, things, and events with relevant details, expressing ideas and feelings clearly.",
        "description": "Describe people, places, things, and events with relevant details, expressing ideas and feelings clearly.",
        "topics": [
            {
                "name": "Communication Skills",
                "subtopics": [
                    "Oral Presentation",
                    "Descriptive Language",
                    "Active Listening"
                ]
            },
            {
                "name": "Community Awareness",
                "subtopics": [
                    "Local Helpers",
                    "Public Services",
                    "Career Exploration"
                ]
            },
            {
                "name": "Social Studies",
                "subtopics": [
                    "Citizenship",
                    "Community Roles",
                    "Social Responsibility"
                ]
            }
        ],
        "cross_standards": [
            {
                "code": "CCSS.ELA-LITERACY.W.1.8",
                "subject": "ELA",
                "description": "Gather information to answer a question"
            },
            {
                "code": "CCSS.ELA-LITERACY.SL.1.5",
                "subject": "ELA",
                "description": "Add drawings or visual displays"
            }
        ],
        "sdg_connections": [
            {
                "goal": 4,
                "name": "Quality Education",
                "applications": [
                    "Learning about careers",
                    "Community engagement",
                    "Communication skills"
                ]
            },
            {
                "goal": 11,
                "name": "Sustainable Communities",
                "applications": [
                    "Understanding community services",
                    "Appreciating public workers",
                    "Local community awareness"
                ]
            }
        ],
        "curricula": [
            {
                "name": "Social Studies Alive!",
                "grade_range": "K-5"
            },
            {
                "name": "Responsive Classroom",
                "grade_range": "K-8"
            }
        ]
    }
}
EOL
run_test "test2" "Community Helpers Project (CCSS.ELA-LITERACY.SL.1.4)" "test2_options_request.json"

# Save all results
save_results "${TEST_RESULTS[@]}"

# Clean up temporary files
rm -f test*_options_request.json
