from typing import Dict, List, Optional, Union, Tuple
import re


#add conversion fo grades across different countries -> mx, us, fr

# -------------------------------------------------------------------
# 1️⃣ Age → grade helper (already in your file)
# -------------------------------------------------------------------

# Age to grade mapping (approximate)
AGE_GRADE_MAPPING = {
    5: ["K"],
    6: ["1"],
    7: ["2"],
    8: ["3"],
    9: ["4"],
    10: ["5"],
    11: ["6"],
    12: ["7"],
    13: ["8"],
    14: ["9"],
    15: ["10"],
    16: ["11"],
    17: ["12"],
    18: ["12", "College"]  # 18 could be senior or college freshman
}

def extract_age_from_text(text: str) -> Optional[int]:
    """
    Extract age information from text.
    Example: "for my 13 years old" -> 13
    """
    # Look for patterns like "X years old", "X-year-old", "X year olds"
    patterns = [
        r'(\d+)\s*(?:years?|yrs?)\s*old',
        r'(\d+)[- ]year[- ]old',
        r'(\d+)\s*years?',
        r'age\s*(?:of|is|:)?\s*(\d+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return the first age found
            return int(matches[0])
    
    return None

def extract_age_range_from_text(text: str) -> Optional[Dict[str, int]]:
    """
    Extract age range information from text.
    Example: "ages 10-12" -> {"min": 10, "max": 12}
    """
    # Look for patterns like "ages 10-12", "10 to 12 years old"
    patterns = [
        r'ages?\s*(\d+)\s*[-–—]\s*(\d+)',
        r'ages?\s*(\d+)\s*to\s*(\d+)',
        r'(\d+)\s*[-–—]\s*(\d+)\s*(?:years?|yrs?)\s*old',
        r'(\d+)\s*to\s*(\d+)\s*(?:years?|yrs?)\s*old',
        r'between\s*(\d+)\s*and\s*(\d+)\s*(?:years?|yrs?)',
        r'for\s*(?:ages?)?\s*(\d+)\s*to\s*(\d+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            min_age, max_age = int(matches[0][0]), int(matches[0][1])
            return {"min": min_age, "max": max_age}
    
    return None

def get_grade_from_age(age: int) -> List[str]:
    """Get possible grade levels for a given age"""
    return AGE_GRADE_MAPPING.get(age, [])

def get_grade_range(ages: List[int]) -> Dict[str, Union[str, List[str]]]:
    """
    Convert a list of ages to a grade range representation
    
    Args:
        ages: List of student ages
        
    Returns:
        Dict with min_grade, max_grade, and all_grades
    """
    if not ages:
        return {}
        
    all_grades = []
    for age in ages:
        all_grades.extend(get_grade_from_age(age))
    
    if not all_grades:
        return {}
        
    # Get unique grades and sort them
    unique_grades = sorted(list(set(all_grades)))
    
    return {
        "min_grade": min(unique_grades, key=lambda x: int(x) if x != "K" else 0),
        "max_grade": max(unique_grades, key=lambda x: int(x) if x != "K" else 0),
        "all_grades": unique_grades
    }

def process_age_input(age_input: Union[int, List[int], Dict[str, int], str]) -> Dict:
    """
    Process age input which could be:
    - Single age (int)
    - List of ages
    - Dict with min/max ages
    - String containing age information
    
    Returns a standardized format with age range and grade information
    """
    ages = []
    
    if isinstance(age_input, int):
        ages = [age_input]
    elif isinstance(age_input, list):
        ages = age_input
    elif isinstance(age_input, dict):
        min_age = age_input.get('min')
        max_age = age_input.get('max')
        if min_age is not None and max_age is not None:
            ages = list(range(min_age, max_age + 1))
        else:
            ages = []
    elif isinstance(age_input, str):
        # First try to extract age range
        age_range = extract_age_range_from_text(age_input)
        if age_range:
            min_age = age_range.get('min')
            max_age = age_range.get('max')
            if min_age is not None and max_age is not None:
                ages = list(range(min_age, max_age + 1))
        else:
            # Try to extract single age
            single_age = extract_age_from_text(age_input)
            if single_age:
                ages = [single_age]
    else:
        ages = []
    
    grade_info = get_grade_range(ages)
    
    return {
        "ages": ages,
        "age_range": {
            "min": min(ages) if ages else None,
            "max": max(ages) if ages else None
        },
        "grade_info": grade_info
    }


##International grade -> US
# ─── US grade ↔ local‐label aliases ──────────────────────────────────────────
US_GRADE_ALIASES: Dict[int, List[str]] = {
    0:  ["K", "Kindergarten", "CP"],
    1:  ["1", "Grade 1", "Year 1", "1re année", "Primaria 1", "1° Primaria", "Primero de Primaria", "1ro de Primaria", "1° Primaria"],
    2:  ["2", "Grade 2", "Year 2", "2e année", "Primaria 2", "2° Primaria", "Segundo de Primaria", "2do de Primaria", "2° Primaria"],
    3:  ["3", "Grade 3", "Year 3", "3e année", "Primaria 3", "3° Primaria", "Tercero de Primaria", "3ro de Primaria", "3° Primaria"],
    4:  ["4", "Grade 4", "Year 4", "4e année", "Primaria 4", "4° Primaria", "Cuarto de Primaria", "4to de Primaria", "4° Primaria"],
    5:  ["5", "Grade 5", "Year 5", "5e année", "Primaria 5", "5° Primaria", "Quinto de Primaria", "5to de Primaria", "5° Primaria"],
    6:  ["6", "Grade 6", "Year 6", "6e année", "Primaria 6", "6° Primaria", "Sexto de Primaria", "6to de Primaria", "6° Primaria"],
    7:  [
        "7", "Grade 7", "Year 7",
        "7e année", "Secondaire I",
        "Primero de Secundaria", "1ro de Secundaria", "1° Secundaria", "primero de secundaria", "primer año de secundaria"
    ],
    8:  [
        "8", "Grade 8", "Year 8",
        "8e année", "Secondaire II",
        "Segundo de Secundaria", "2do de Secundaria", "2° Secundaria", "segundo de secundaria", "segundo año de secundaria"
    ],
    9:  [
        "9", "Grade 9", "Year 9",
        "9e année", "Secondaire III",
        "Tercero de Secundaria", "3ro de Secundaria", "3° Secundaria", "tercero de secundaria", "tercer año de secundaria"
    ],
    10: [
        "10","Grade 10","Year 10",
        "10e année", "Preparatoria 1", "1ro de Preparatoria", "1° Preparatoria", "preparatoria 1", "primero de preparatoria", "primer año de preparatoria"
    ],
    11: [
        "11","Grade 11","Year 11",
        "11e année", "Preparatoria 2", "2ro de Preparatoria", "2° Preparatoria", "preparatoria 2", "segundo de preparatoria", "segundo año de preparatoria"
    ],
    12: [
        "12","Grade 12","Year 12",
        "12e année", "Preparatoria 3", "3ro de Preparatoria", "3° Preparatoria", "preparatoria 3", "tercero de preparatoria", "tercer año de preparatoria"
    ],
}

def get_grade_aliases(us_grade: int) -> List[str]:
    """
    Given a US grade (0=K…12), return its common labels
    in MX, AR and CA (English & French).
    """
    return US_GRADE_ALIASES.get(us_grade, [])