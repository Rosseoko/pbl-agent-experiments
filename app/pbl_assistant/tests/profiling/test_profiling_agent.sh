#!/bin/bash

# Test script for PBL Assistant API
# Make sure the API server is running before executing these tests

# Configuration
BASE_URL="http://localhost:8001"
OUTPUT_FILE="$(dirname "$0")/test_results_analysis.json"
TEST_RESULTS=()
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Function to format JSON output
format_json() {
    jq . 2>/dev/null || echo "$1"
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
            "api_endpoint": "'"$BASE_URL"'/profiling"
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
    local raw_message=$3
    
    echo -e "\n================================================================"
    echo -e "🧪 $test_name"
    echo -e "================================================================"
    echo -e "📝 TEACHER REQUEST:"
    echo -e "----------------"
    echo -e "$raw_message\n"
    
    # Create the JSON payload
    local payload=$(jq -n --arg msg "$raw_message" '{"raw_message": $msg}')
    
    echo -e "🔍 ANALYSIS RESULTS:"
    echo -e "-----------------"
    
    # Make the API request
    local response
    response=$(curl -s -X POST "${BASE_URL}/profiling" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>/dev/null)
    
    # Parse the response
    local status
    if echo "$response" | jq -e '.success == true' >/dev/null; then
        status="success"
        echo -e "✅ Test passed!"
    else
        status="failed"
        echo -e "❌ Test failed!"
    fi
    
    # Format the test result
    local test_result=$(jq -n \
        --arg id "$test_id" \
        --arg name "$test_name" \
        --arg status "$status" \
        --arg request "$raw_message" \
        --argjson response "$response" \
        '{
            "test_id": $id,
            "test_name": $name,
            "status": $status,
            "request": $request,
            "response": $response
        }' 2>/dev/null)
    
    # Add to results array
    TEST_RESULTS+=("$test_result")
    
    # Show response summary
    echo -e "\n📊 Response Summary:"
    echo "----------------"
    echo "Status: $status"
    if [ "$status" = "success" ]; then
        echo "Topic: $(echo "$response" | jq -r '.profile.topic')"
        echo "Grade Level: $(echo "$response" | jq -r '.profile.grade_level')"
        echo "Primary Intent: $(echo "$response" | jq -r '.profile.primary_intent')"
    else
        echo "Error: $(echo "$response" | jq -r '.error // "Unknown error"')"
    fi
    
    return 0
}

# Initialize the results array if it doesn't exist
declare -a TEST_RESULTS

# Test Cases
echo "🚀 Starting PBL Assistant API Tests..."

# Test 1: Basic project request in English with grade level
run_test "1" "Basic Project Request (English with Grade Level)" \
    "I want to create a 3-week project for my 5th grade class about renewable energy. The students will work in teams to design and build small wind turbines using recycled materials. We have access to basic craft supplies and a fan for testing. The project should incorporate science standards about energy and engineering design principles. We're particularly interested in NGSS standards 4-PS3-4 and 3-5-ETS1-1. The students enjoy hands-on activities related to renewable energy, engineering, and environmental science. I'd like them to develop skills in teamwork, problem-solving, and scientific inquiry."

# Test 2: Project with specific age (not grade level)
run_test "2" "Project with Specific Age" \
    "I need a 2-week project for my students who are 8 years old about marine life. We have access to a local aquarium for a field trip. The project should help students understand ocean ecosystems and conservation. Many of my students are visual learners and enjoy hands-on activities. I'd like them to develop observation skills and learn about marine biodiversity."

# Test 3: Project with age range
run_test "3" "Project with Age Range" \
    "I'm looking for a 4-week project for students aged 12-14 about ancient civilizations. The project should include research, creative presentations, and a hands-on component. We have access to the school library and computer lab twice a week. Students should develop research skills, critical thinking, and presentation abilities while learning about different ancient cultures."

# Test 4: Project in Spanish (Español)
run_test "4" "Project in Spanish (Español)" \
    "Necesito un proyecto de 2 semanas para mi clase de biología de secundaria (10mo grado) sobre ecosistemas. Tenemos acceso limitado a tecnología pero podemos usar el jardín de la escuela. El proyecto debería ayudar a los estudiantes a comprender las cadenas alimentarias y el impacto humano en el medio ambiente. Muchos de mis estudiantes están aprendiendo inglés, por lo que el proyecto debería incluir componentes visuales y actividades prácticas. Los estándares que nos interesan son HS-LS2-6 y HS-LS2-7. A los estudiantes les gusta la ecología, las ciencias ambientales y la jardinería. Quisiera que desarrollen habilidades en recolección de datos, observación científica y análisis de ecosistemas."

# Test 5: Project in French (Français)
run_test "5" "Project in French (Français)" \
    "Je recherche un projet de 4 semaines pour ma classe d'études sociales de 7e année sur le gouvernement local. Je veux que les élèves identifient un problème communautaire et proposent des solutions au conseil municipal. Nous pouvons faire une sortie scolaire à l'hôtel de ville. Le projet devrait inclure des recherches, des entretiens et une présentation. De nombreux élèves ont un accès limité à la technologie à la maison. Les compétences clés à développer sont la recherche, la prise de parole en public et la participation civique. Les élèves s'intéressent à l'engagement civique, au gouvernement local et au service communautaire."

# Test 6: Project in Mandarin (中文)
run_test "6" "Project in Mandarin (中文)" \
    "我正在为我的七年级社会科学课寻找一个关于地方政府的4周项目。我希望学生能够识别一个社区问题，并向市议会提出解决方案。我们可以去市政厅进行实地考察。这个项目应该包括研究、采访和展示部分。许多学生在家中使用科技设备的机会有限。学生们对公民参与、地方政府和社区服务感兴趣。我希望他们能发展研究、公开演讲和公民参与的能力。"

# Save all results
save_results "${TEST_RESULTS[@]}"

echo -e "\n✨ All tests completed!"

# Save all test results to JSON file
save_results "${TEST_RESULTS[@]}"

echo -e "\n✅ All tests completed! Results saved to: $OUTPUT_FILE"

# Display summary
pass_count=0
fail_count=0
for result in "${TEST_RESULTS[@]}"; do
  if echo "$result" | jq -e '.status == "success"' >/dev/null; then
    ((pass_count++))
  else
    ((fail_count++))
  fi
done

echo -e "\n📊 Test Summary:"
echo "----------------"
echo "Total Tests: ${#TEST_RESULTS[@]}"
echo "✅ Passed: $pass_count"
echo "❌ Failed: $fail_count"

if [ $fail_count -eq 0 ]; then
  echo "\n🎉 All tests passed successfully!"
  exit 0
else
  echo "\n⚠️  Some tests failed. Check the output above for details."
  exit 1
fi