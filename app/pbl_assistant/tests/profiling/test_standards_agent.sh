#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8001"
OUTPUT_FILE="$(dirname "$0")/test_standards_results.json"
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
            "api_endpoint": "'"$BASE_URL"'/standards"
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
    
    echo -e "\n🚀 SENDING REQUEST..."
    
    # Make the API request
    response=$(curl -s -X POST "$BASE_URL/standards" \
        -H "Content-Type: application/json" \
        -d "@$request_file" 2>/dev/null)
    
    # Parse the response
    local status=$(echo "$response" | jq -r '.success // "false"' 2>/dev/null || echo "error")
    
    if [[ "$status" == "true" ]]; then
        echo -e "\n✅ Test passed!\n"
        
        # Extract teacher's request and original utterance
        TEACHER_REQUEST=$(echo "$response" | jq -r '.teacher_request // ""')
        ORIGINAL_UTTERANCE=$(echo "$response" | jq -r '.original_utterance // ""')
        
        # Display teacher's request if available
        if [ -n "$TEACHER_REQUEST" ] || [ -n "$ORIGINAL_UTTERANCE" ]; then
            echo -e "📝 TEACHER'S REQUEST:"
            echo "-------------------"
            if [ -n "$TEACHER_REQUEST" ]; then
                echo "$TEACHER_REQUEST" | fold -s -w 80
            else
                echo "$ORIGINAL_UTTERANCE" | fold -s -w 80
            fi
            echo -e "\n"
        fi
        
        # Create result object with teacher info at the top
        local result=$(echo "$response" | jq --arg test_id "$test_id" --arg test_name "$test_name" '
        {
            test_id: $test_id,
            test_name: $test_name,
            status: "success",
            teacher_request: .teacher_request,
            original_utterance: .original_utterance,
            result: del(.teacher_request, .original_utterance)
        }' 2>/dev/null)
        
        # Add to results array
        TEST_RESULTS+=("$result")
        
        # Display standards alignment
        echo -e "📊 STANDARDS ALIGNMENT:"
        echo "-------------------"
        echo "Standards Count: $(echo "$response" | jq '.alignment.standards | length' 2>/dev/null || echo 'N/A')"
        
        # Show first 3 standards
        echo -e "\nTop Standards:"
        echo "$response" | jq -r '.alignment.standards[0:3][] | "- " + .code + " (" + .type + "): " + (.description | .[0:60] + "...")' 2>/dev/null || echo "  No standards found"
        
    else
        echo -e "\n ${RED}Test failed!${NC}"
        local error_msg=$(echo "$response" | jq -r '.error // "Unknown error"' 2>/dev/null || echo 'Invalid response')
        echo -e "\nError: $error_msg"
        
        # Create error result
        local result=$(jq -n --arg test_id "$test_id" --arg test_name "$test_name" --arg error "$error_msg" '
        {
            test_id: $test_id,
            test_name: $test_name,
            status: "failed",
            error: $error
        }' 2>/dev/null)
        
        # Add to results array
        TEST_RESULTS+=("$result")
    fi
}

# Initialize the results array if it doesn't exist
declare -a TEST_RESULTS

# Main execution
echo -e "🚀 Starting Standards Agent Tests..."

# Test 1: Basic Project Request (English with Grade Level)
# cat > test1_request.json << 'EOL'
# {
#     "topic": "Renewable Energy",
#     "grade_level": "5",
#     "content_area_focus": "STEM Heavy",
#     "primary_intent": "Engineering Design",
#     "duration_preference": "3 weeks",
#     "standard_codes": ["4-PS3-4", "3-5-ETS1-1"],
#     "end_product": "Working wind turbine model",
#     "class_interests": ["renewable energy", "engineering", "environmental science"],
#     "includes_design_challenge": true,
#     "hands_on_emphasis": true,
#     "original_utterance": "I'm looking for a 3-week project for my 5th grade science class on renewable energy. I want students to design and build a working wind turbine model. The project should cover energy principles and the engineering design process. Students will work in teams and present their designs. We have access to basic materials like cardboard, popsicle sticks, and small motors. The project should be hands-on and include a design challenge component.",
#     "learning_outcomes": [
#         "Understand energy principles",
#         "Apply engineering design process",
#         "Develop teamwork and problem-solving skills"
#     ]
# }
# EOL
# run_test "test1" "Basic Project Request (English with Grade Level)" "test1_request.json"

# Test 2: Project with Specific Age
# cat > test2_request.json << 'EOL'
# {
#     "topic": "Marine Life",
#     "grade_level": "3",
#     "content_area_focus": "STEM Heavy",
#     "primary_intent": "Scientific Inquiry",
#     "duration_preference": "2 weeks",
#     "standard_codes": ["3-LS4-3", "3-LS4-4"],
#     "end_product": "Marine ecosystem diorama",
#     "class_interests": ["ocean life", "animals", "conservation"],
#     "hands_on_emphasis": true,
#     "original_utterance": "I need a 2-week science project for my 3rd grade class about marine life. The students are fascinated by ocean animals and conservation. We'll be creating dioramas of marine ecosystems, and I want to make sure we're covering the right standards about habitats and animal adaptations. The project should be very hands-on and include opportunities for students to observe and document different marine species.",
#     "learning_outcomes": [
#         "Understand ocean ecosystems",
#         "Develop observation skills",
#         "Learn about marine biodiversity"
#     ]
# }
# EOL
# run_test "test2" "Project with Specific Age" "test2_request.json"

# Test 3: Project with Age Range
# cat > test3_request.json << 'EOL'
# {
#     "topic": "Ancient Civilizations",
#     "grade_level": "7",
#     "content_area_focus": "Humanities Focused",
#     "primary_intent": "Research Investigation",
#     "duration_preference": "4 weeks",
#     "standard_codes": ["RH.6-8.1", "RH.6-8.7"],
#     "end_product": "Multimedia presentation on an ancient civilization",
#     "class_interests": ["history", "culture", "archaeology"],
#     "research_intensive": true,
#     "presentation_focused": true,
#     "original_utterance": "I'm planning a 4-week unit on ancient civilizations for my 7th grade social studies class. Students will research and create multimedia presentations about different civilizations. We'll focus on comparing aspects like government, religion, and cultural achievements. The project should help students develop strong research and presentation skills while meeting the Common Core standards for history. Many of my students are visual learners, so I'd like to incorporate maps and images into the project.",
#     "learning_outcomes": [
#         "Develop research skills",
#         "Enhance critical thinking",
#         "Improve presentation abilities"
#     ]
# }
# EOL
# run_test "test3" "Project with Age Range" "test3_request.json"

# Test 4: Project in Spanish (Español)
# cat > test4_request.json << 'EOL'
# {
#     "topic": "Ecosystems",
#     "grade_level": "10",
#     "content_area_focus": "STEM Heavy",
#     "primary_intent": "Scientific Inquiry",
#     "duration_preference": "2 weeks",
#     "standard_codes": ["HS-LS2-6", "HS-LS2-7"],
#     "end_product": "Ecosystem analysis report",
#     "class_interests": ["ecology", "environmental science", "gardening"],
#     "original_language": "es",
#     "original_utterance": "Necesito un proyecto de 2 semanas para mi clase de biología de secundaria (10mo grado) sobre ecosistemas. Tenemos acceso limitado a tecnología pero podemos usar el jardín de la escuela. El proyecto debería ayudar a los estudiantes a comprender las cadenas alimentarias y el impacto humano en el medio ambiente.",
#     "learning_outcomes": [
#         "Understand food chains",
#         "Analyze human impact on environment",
#         "Develop data collection and analysis skills"
#     ]
# }
# EOL
# run_test "test4" "Project in Spanish (Español)" "test4_request.json"

# Test 5: Multiple Standards
cat > test5_request.json << 'EOL'
{
    "topic": "Weather and Climate",
    "grade_level": "5",
    "content_area_focus": "STEM Heavy",
    "primary_intent": "Scientific Inquiry",
    "duration_preference": "3 weeks",
    "standard_codes": ["5-ESS2-1", "5-ESS3-1", "5-ESS2-2", "5-PS1-4"],
    "end_product": "Weather station and data analysis report",
    "class_interests": ["weather patterns", "data collection", "environmental science"],
    "hands_on_emphasis": true,
    "requires_experimentation": true,
    "original_utterance": "I need a 3-week project for my 5th grade class where students will track weather patterns and analyze climate data. They should use instruments to collect data and create a report. The project should cover multiple standards related to Earth's systems and engineering.",
    "learning_outcomes": [
        "Understand weather and climate patterns",
        "Learn to collect and analyze scientific data",
        "Develop skills in data interpretation and presentation"
    ]
}
EOL
run_test "test5" "Multiple Standards (4+ standards)" "test5_request.json"

# Test 6: No Standards Provided
cat > test6_request.json << 'EOL'
{
    "topic": "Community Helpers",
    "grade_level": "1",
    "content_area_focus": "Humanities Focused",
    "primary_intent": "Community Action",
    "duration_preference": "1 week",
    "standard_codes": [],
    "end_product": "Community helper presentation",
    "class_interests": ["community", "jobs", "helpers"],
    "original_utterance": "Looking for a 1-week project for my 1st graders about community helpers. No specific standards needed, just want something age-appropriate and engaging that helps them learn about different jobs in our community.",
    "learning_outcomes": [
        "Identify different community helpers",
        "Understand roles in the community",
        "Develop presentation skills"
    ]
}
EOL
run_test "test6" "No Standards Provided" "test6_request.json"

# Test 7: Invalid Standard Code - Commented out
# cat > test7_request.json << 'EOL'
# {
#     "topic": "Space Exploration",
#     "grade_level": "8",
#     "content_area_focus": "STEM Heavy",
#     "primary_intent": "Scientific Inquiry",
#     "duration_preference": "2 weeks",
#     "standard_codes": ["MS-ESS1-88", "MS-ESSSS3-123", "MS-ESS1-3"],
#     "end_product": "Space mission proposal",
#     "class_interests": ["space", "technology", "exploration"],
#     "original_utterance": "Planning a 2-week unit on space exploration for 8th grade. I want to include some standards about Earth's place in the universe, but I'm not sure about all the exact codes. One of them might be incorrect.",
#     "learning_outcomes": [
#         "Understand Earth's place in the universe",
#         "Develop research skills",
#         "Create a scientific proposal"
#     ]
# }
# EOL
# run_test "test7" "Invalid Standard Code" "test7_request.json"

# Test 8: Mixed Valid and Invalid Standards - Commented out
# cat > test8_request.json << 'EOL'
# {
#     "topic": "Genetics and Heredity",
#     "grade_level": "10",
#     "content_area_focus": "STEM Heavy",
#     "primary_intent": "Research Investigation",
#     "duration_preference": "3 weeks",
#     "standard_codes": ["HS-LS3-1", "BIO-123-INVALID", "HS-LS3-2", "GENETICS-456"],
#     "end_product": "Genetic disorder research project",
#     "class_interests": ["genetics", "biology", "health"],
#     "research_intensive": true,
#     "original_utterance": "I need a 3-week project on genetics and heredity for my 10th grade biology class. I have a couple of standard codes but I'm not sure if they're all correct. The project should involve researching genetic disorders and presenting findings.",
#     "learning_outcomes": [
#         "Understand principles of genetics and heredity",
#         "Research and analyze genetic disorders",
#         "Develop scientific communication skills"
#     ]
# }
# EOL
# run_test "test8" "Mixed Valid and Invalid Standards" "test8_request.json"

# Test 9: Standards from Different Grade Levels - Commented out
# cat > test9_request.json << 'EOL'
# {
#     "topic": "Water Cycle",
#     "grade_level": "6",
#     "content_area_focus": "STEM Heavy",
#     "primary_intent": "Scientific Inquiry",
#     "duration_preference": "2 weeks",
#     "standard_codes": ["5-ESS2-2", "MS-ESS2-4", "4-ESS2-1"],
#     "end_product": "Water cycle model with explanation",
#     "class_interests": ["water cycle", "weather", "environment"],
#     "hands_on_emphasis": true,
#     "original_utterance": "I'm teaching a 6th grade unit on the water cycle. I'd like to include standards from different grade levels to review and extend student understanding. The project should be hands-on and help students visualize the water cycle process.",
#     "learning_outcomes": [
#         "Understand the water cycle process",
#         "Create and explain a water cycle model",
#         "Connect water cycle to weather patterns"
#     ]
# }
# EOL
# run_test "test9" "Standards from Different Grade Levels" "test9_request.json"

# Test 10: Standards from Different Content Areas - Commented out
# cat > test10_request.json << 'EOL'
# {
#     "topic": "Sustainable Cities",
#     "grade_level": "9",
#     "content_area_focus": "Balanced Integration",
#     "primary_intent": "Community Action",
#     "duration_preference": "4 weeks",
#     "standard_codes": ["HS-ESS3-4", "HS-ETS1-3", "WHST.9-10.7", "HSS-IC.B.6"],
#     "end_product": "Sustainable city design proposal",
#     "class_interests": ["sustainability", "urban planning", "environment"],
#     "community_connection_desired": true,
#     "original_utterance": "I'm planning a 4-week interdisciplinary project on sustainable cities for my 9th grade class. I want to include standards from science, engineering, and social studies. The project should involve researching sustainable practices and designing a model city that addresses environmental challenges.",
#     "learning_outcomes": [
#         "Understand principles of sustainable urban development",
#         "Apply engineering design process",
#         "Develop research and presentation skills",
#         "Analyze data to support claims"
#     ]
# }
# EOL
# run_test "test10" "Standards from Different Content Areas" "test10_request.json"

# Save all results
save_results "${TEST_RESULTS[@]}"

# Clean up temporary files
rm -f test*_request.json
