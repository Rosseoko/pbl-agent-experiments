#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8001"
OUTPUT_FILE="$(dirname "$0")/test_knowledgegraph_results.json"
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
            "api_endpoint": "'"$BASE_URL"'/knowledge_graph"
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
    local standard_code=$4  # Optional standard code to analyze
    
    print_header "${test_name}"
    
    echo -e "📝 TEST REQUEST:"
    echo "----------------"
    cat "$request_file"
    
    # Add standard code to query parameter if provided
    local url="$BASE_URL/knowledge_graph"
    if [ -n "$standard_code" ]; then
        url="${url}?standard_code=${standard_code}"
    fi
    
    echo -e "\n🚀 SENDING REQUEST..."
    
    # Make the API request
    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "@$request_file" 2>/dev/null)
    
    # Parse the response
    local status=$(echo "$response" | jq -r '.success // "false"' 2>/dev/null || echo "error")
    
    if [[ "$status" == "true" ]]; then
        echo -e "\n✅ Test passed!\n"
        
        # Extract standard analyzed
        STANDARD_ANALYZED=$(echo "$response" | jq -r '.standard_analyzed // ""')
        
        # Display standard analyzed
        if [ -n "$STANDARD_ANALYZED" ]; then
            echo -e "🔍 ANALYZING STANDARD:"
            echo "-------------------"
            echo "$STANDARD_ANALYZED" | fold -s -w 80
            echo -e "\n"
        fi
        
        # Create result object
        local result=$(echo "$response" | jq --arg test_id "$test_id" --arg test_name "$test_name" '
        {
            test_id: $test_id,
            test_name: $test_name,
            status: "success",
            standard_analyzed: .standard_analyzed,
            result: .kg_insights
        }' 2>/dev/null)
        
        # Add to results array
        TEST_RESULTS+=("$result")
        
        # Display knowledge graph insights
        echo -e "📊 KNOWLEDGE GRAPH INSIGHTS:"
        echo "-------------------"
        
        # Show topics
        echo -e "\nTopics:"
        echo "$response" | jq -r '.kg_insights.topics[0:3][] | "- " + .name + ": " + (.subtopics | join(", "))' 2>/dev/null || echo "  No topics found"
        
        # Show cross-curricular connections
        echo -e "\nCross-curricular Connections:"
        echo "$response" | jq -r '.kg_insights.cross_standards[0:2][] | "- " + .code + " (" + .subject + "): " + (.description | .[0:60] + "...")' 2>/dev/null || echo "  No cross-curricular connections found"
        
        # Show SDG connections
        echo -e "\nReal-world Applications:"
        echo "$response" | jq -r '.kg_insights.sdg_connections[0:2][] | "- Goal " + (.goal|tostring) + " (" + .name + "): " + (.applications[0] | .[0:60] + "...")' 2>/dev/null || echo "  No SDG connections found"
        
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
echo -e "🚀 Starting Knowledge Graph Agent Tests..."

# Test 1: Weather and Climate Standard (5-ESS2-1)
cat > test1_kg_request.json << 'EOL'
{
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
}
EOL
run_test "test1" "Weather and Climate Standard (5-ESS2-1)" "test1_kg_request.json"

# Test 2: Community Helpers Standard (CCSS.ELA-LITERACY.SL.1.4)
cat > test2_kg_request.json << 'EOL'
{
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
}
EOL
run_test "test2" "Community Helpers Standard (CCSS.ELA-LITERACY.SL.1.4)" "test2_kg_request.json"

# Test 3: Multiple Standards (Science and Math)
cat > test3_kg_request.json << 'EOL'
{
    "standards": [
        {
            "code": "5-ESS2-2",
            "type": "ngss",
            "description": "Describe and graph the amounts of salt water and fresh water in various reservoirs to provide evidence about the distribution of water on Earth.",
            "grade_level": "5",
            "is_valid": true,
            "primary_bloom_level": "analyze",
            "dok_level": "strategic_thinking",
            "project_specific_vocabulary": [
                "reservoirs",
                "salt water",
                "fresh water",
                "water distribution",
                "graphing"
            ],
            "learning_objectives": [
                {
                    "objective": "Create graphs that show the distribution of salt water and fresh water on Earth in the Weather and Climate project.",
                    "bloom_level": "create",
                    "dok_level": "skill_concept"
                },
                {
                    "objective": "Analyze data on water distribution to draw conclusions about Earth's water resources in the Weather and Climate project.",
                    "bloom_level": "analyze",
                    "dok_level": "strategic_thinking"
                }
            ]
        },
        {
            "code": "5.MD.2",
            "type": "ccss_math",
            "description": "Make a line plot to display a data set of measurements in fractions of a unit. Use operations on fractions to solve problems involving information presented in line plots.",
            "grade_level": "5",
            "is_valid": true,
            "primary_bloom_level": "apply",
            "dok_level": "strategic_thinking",
            "project_specific_vocabulary": [
                "line plot",
                "data set",
                "measurements",
                "fractions",
                "data analysis"
            ],
            "learning_objectives": [
                {
                    "objective": "Create line plots to display weather data measurements in the Weather and Climate project.",
                    "bloom_level": "apply",
                    "dok_level": "skill_concept"
                },
                {
                    "objective": "Solve problems using fractional measurements from weather data line plots in the Weather and Climate project.",
                    "bloom_level": "apply",
                    "dok_level": "strategic_thinking"
                }
            ]
        }
    ],
    "alignment_confidence": 0.9,
    "validation_issues": []
}
EOL
run_test "test3" "Multiple Standards (Science and Math)" "test3_kg_request.json" "5-ESS2-2"

# Save all results
save_results "${TEST_RESULTS[@]}"

# Clean up temporary files
rm -f test*_kg_request.json
