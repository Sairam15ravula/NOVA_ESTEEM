# Resume Analyzer - ML Module

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load Model (Once)
# Note: In a production app, we might want to lazy load this or load it on startup event
print("Loading ML Model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model Loaded.")

# Personality Trait Templates
TRAITS = {
    "leadership": [
        "I take initiative and lead teams",
        "I manage projects and guide others",
        "Target driven and result oriented",
        "Mentored junior developers"
    ],
    "teamwork": [
        "I collaborate and work well in teams",
        "I enjoy working with others",
        "Active team player",
        "Cross-functional collaboration"
    ],
    "learning": [
        "I constantly learn new skills",
        "I improve myself continuously",
        "Passionate about learning new technologies",
        "Self-taught developer"
    ],
    "communication": [
        "I communicate ideas clearly",
        "I explain concepts effectively",
        "Presented technical solutions to stakeholders",
        "Strong verbal and written communication"
    ],
    "problem_solving": [
        "I solve problems logically",
        "I analyze complex situations",
        "Debugged and fixed critical production issues",
        "Optimized algorithm performance"
    ]
}

# Expanded Skill Database
SKILLS_DB = {
    "Data / AI": [
        "python", "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "sql", "data visualization", "tableau",
        "power bi", "big data", "spark", "hadoop", "r", "statistics"
    ],
    "Web Development": [
        "html", "css", "javascript", "react", "angular", "vue", "node.js", 
        "typescript", "django", "flask", "fastapi", "graphql", "rest api",
        "mongodb", "postgresql", "mysql", "redis", "bootstrap", "tailwind"
    ],
    "Cloud / DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "cicd",
        "terraform", "ansible", "linux", "bash", "git", "github actions"
    ],
    "General": [
        "java", "c++", "c#", "go", "ruby", "swift", "kotlin", "agile", "scrum",
        "jira", "testing", "selenium", "unit testing"
    ]
}

# Flatten skills for general extraction
ALL_SKILLS = set(skill for category in SKILLS_DB.values() for skill in category)

def validate_resume(resume_text):
    """
    Validates if the input text looks like a resume using intelligent document classification.
    """
    # Preliminary check: minimum word count
    if len(resume_text.strip().split()) < 50:
        return False, "Document is too short. Please provide a complete resume with at least 50 words."
    
    # Use intelligent document classifier
    from backend.services.document_classifier import classify_document, get_error_message
    
    classification = classify_document(resume_text)
    
    # If it's a resume, validate
    if classification["is_resume"]:
        return True, "Valid"
    
    # If not a resume, provide specific error message
    error_msg = get_error_message(classification)
    
    # Add confidence info for debugging (optional)
    if classification["confidence"] > 70:
        # High confidence in classification
        return False, error_msg
    else:
        # Lower confidence, add a softer message
        return False, f"{error_msg} (Confidence: {classification['confidence']:.0f}%)"

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_similarity(text1, text2):
    v1 = model.encode(text1)
    v2 = model.encode(text2)
    score = cosine_similarity([v1], [v2])[0][0]
    return float(round(score * 100, 2))

def extract_skills(text):
    """
    Extracts skills from text using the predefined database.
    """
    found = []
    text = text.lower()
    
    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
            
    return list(set(found))

def detect_domain(jd):
    jd = jd.lower()
    scores = {category: 0 for category in SKILLS_DB}
    
    for category, skills in SKILLS_DB.items():
        for skill in skills:
            if skill in jd:
                scores[category] += 1
                
    # Return category with max matches
    best_match = max(scores, key=scores.get)
    if scores[best_match] == 0:
        return "General"
    return best_match

def adapt_traits_to_jd(jd):
    extra = []
    jd = jd.lower()
    if "research" in jd: extra.append("I conduct experiments and publish results")
    if "startup" in jd: extra.append("I work independently in fast environments")
    if "client" in jd: extra.append("I handle client communication effectively")
    return extra

def analyze_personality(resume_text, jd_text):
    summary = resume_text[:1000] 
    summary = clean_text(summary)
    
    trait_scores = {}
    
    for trait, refs in TRAITS.items():
        scores = []
        for ref in refs:
            sim = get_similarity(summary, ref)
            scores.append(sim)
        trait_scores[trait] = float(round(sum(scores)/len(scores), 2))
        
    personality_score = float(round(sum(trait_scores.values()) / len(trait_scores), 2))
    return personality_score, trait_scores

def calculate_technical_score(resume_skills, jd_skills, resume_text, jd_text):
    """
    Hybrid Score:
    1. Semantic Similarity (60%)
    2. Skill Match Ratio (40%)
    """
    # 1. Semantic
    semantic_score = get_similarity(resume_text, jd_text)
    
    # 2. Skill Match
    if not jd_skills:
        skill_score = 100 
    else:
        matching_skills = set(resume_skills).intersection(set(jd_skills))
        skill_score = (len(matching_skills) / len(jd_skills)) * 100
    
    # Weighted Average
    final_score = (0.6 * semantic_score) + (0.4 * skill_score)
    return round(final_score, 2), skill_score

def generate_dynamic_suggestions(data, jd_skills, missing_skills, domain):
    suggestions = []
    
    # 1. Skill Gap Suggestions
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append(f"Critical Skills Missing: You are missing {', '.join(top_missing)} which are required for this {domain} role.")
    
    # 2. Score Based Suggestions
    if data["technical_score"] < 60:
        suggestions.append("Low Technical Match: Your resume content does not semantically align well with the JD. Tailor your summary and experience to use similar terminology.")
    elif data["skill_match_score"] < 50: 
        suggestions.append("Keyword Optimization: You have good experience but are missing specific keywords. explicitly list the missing skills in your 'Skills' section.")

    # 3. Domain Specific
    if domain == "Data / AI" and "projects" not in data.get("sections_present", []):
         suggestions.append("Portfolio: For Data/AI roles, adding a 'Projects' section with links to GitHub/Kaggle is highly recommended.")
    
    # 4. Soft Skills
    if data["personality_score"] < 50:
        suggestions.append("Soft Skills: Highlight leadership and teamwork. Use phrases like 'Led a team', 'Collaborated with', OR 'Mentored'.")
        
    return suggestions

def split_sections(resume):
    sections = { "summary": "", "skills": "", "projects": "", "experience": "" }
    present = []
    current = "summary"
    
    for line in resume.split("\n"):
        l = line.lower().strip()
        if "skill" in l: current = "skills"; present.append("skills")
        elif "project" in l: current = "projects"; present.append("projects")
        elif "experience" in l or "intern" in l or "work history" in l: current = "experience"; present.append("experience")
        elif "education" in l: present.append("education") 
        
        sections[current] += line + " "
        
    return sections, list(set(present))


def analyze_resume(resume_text, jd_text):
    
    # 1. Validation
    is_valid, msg = validate_resume(resume_text)
    if not is_valid:
        return {"error": msg}
    
    # 2. Preprocessing
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    
    # 3. Domain & Skills
    domain = detect_domain(jd_text)
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    missing_skills = list(set(jd_skills) - set(resume_skills))
    
    # 4. Scoring
    tech_score, skill_match_score = calculate_technical_score(resume_skills, jd_skills, resume_clean, jd_clean)
    personality_score, traits = analyze_personality(resume_text, jd_text)
    
    # Simple overall score logic
    overall_score = round(0.7 * tech_score + 0.3 * personality_score, 2)
    
    sections_content, sections_present = split_sections(resume_text)
    
    # IMPROVED: Score sections based on content quality, not just length
    section_scores = {}
    for name, content in sections_content.items():
        word_count = len(content.split())
        
        # Base score from length (30-100 words = good)
        if word_count < 20:
            length_score = 30
        elif word_count < 50:
            length_score = 50 + (word_count - 20)
        elif word_count < 150:
            length_score = 80 + min(20, (word_count - 50) / 5)
        else:
            length_score = 100
        
        # Bonus for quantification (numbers, percentages)
        has_metrics = bool(re.search(r'\d+%|\d+\+|\d+ years?|\$\d+|[0-9]+', content))
        metric_bonus = 10 if has_metrics else 0
        
        # Bonus for action verbs
        action_verbs = ['led', 'managed', 'developed', 'created', 'improved', 'increased', 'reduced', 'built', 'designed', 'implemented']
        verb_count = sum(1 for verb in action_verbs if verb in content.lower())
        verb_bonus = min(10, verb_count * 2)
        
        # Bonus for JD keyword presence
        jd_keywords_in_section = sum(1 for skill in jd_skills if skill in content.lower())
        keyword_bonus = min(15, jd_keywords_in_section * 3)
        
        # Calculate final score
        final_score = min(100, length_score + metric_bonus + verb_bonus + keyword_bonus)
        section_scores[name] = round(final_score, 1)


    data = {
        "overall_score": overall_score,
        "technical_score": tech_score,
        "skill_match_score": skill_match_score, 
        "personality_score": personality_score,
        "traits": traits,
        "missing_skills": missing_skills,
        "detected_domain": domain,
        "sections_present": sections_present,
        "section_scores": section_scores,
        "design_style": detect_design_style(resume_text)
    }
    
    # 5. Suggestions
    data["suggestions"] = generate_dynamic_suggestions(data, jd_skills, missing_skills, domain)
    
    # 6. DYNAMIC ANALYSIS - New enhanced features
    from backend.services.analyzer_dynamic import (
        extract_jd_priorities,
        identify_contextual_gaps,
        calculate_rejection_risk,
        generate_personalized_recommendations
    )
    
    # Extract what JD values most
    jd_priorities = extract_jd_priorities(jd_text)
    data["jd_priorities"] = jd_priorities
    
    # Identify contextual gaps
    gaps = identify_contextual_gaps(resume_text, jd_text, resume_skills, jd_skills, jd_priorities)
    data["gaps"] = gaps
    
    # Calculate rejection risk
    rejection_risk = calculate_rejection_risk(resume_text, jd_text, gaps, section_scores)
    data["rejection_risk"] = rejection_risk
    
    # Generate personalized recommendations
    recommendations = generate_personalized_recommendations(gaps, rejection_risk["factors"], jd_priorities)
    data["recommendations"] = recommendations
    
    return data

def detect_design_style(text):
    """
    Heuristic to determine if the resume needs a Modern or Classic template.
    """
    # 1. Density Check
    word_count = len(text.split())
    
    # 2. Header Style Check (Uppercased headers suggest Modern/Clean)
    uppercase_lines = [line for line in text.split('\n') if line.strip().isupper() and len(line.strip()) > 3]
    
    # Logic:
    # High word count + few uppercase headers -> Classic/Academic (Dense)
    # Moderate word count + many uppercase headers -> Modern (Clean sections)
    
    if word_count > 600 and len(uppercase_lines) < 3:
        return "classic"
    else:
        return "modern"
