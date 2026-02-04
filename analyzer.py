# Resume Analyzer - ML Module

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


# Load Model (Once)
model = SentenceTransformer("all-MiniLM-L6-v2")


# Personality Trait Templates
TRAITS = {
    "leadership": [
        "I take initiative and lead teams",
        "I manage projects and guide others"
    ],

    "teamwork": [
        "I collaborate and work well in teams",
        "I enjoy working with others"
    ],

    "learning": [
        "I constantly learn new skills",
        "I improve myself continuously"
    ],

    "communication": [
        "I communicate ideas clearly",
        "I explain concepts effectively"
    ],

    "problem_solving": [
        "I solve problems logically",
        "I analyze complex situations"
    ]
}


# Skill Database
SKILLS = [
    "python", "machine learning", "sql", "deep learning",
    "tensorflow", "pandas", "numpy", "docker",
    "cloud", "aws", "git"
]


# Clean Text
def clean_text(text):

    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# Semantic Similarity
def get_similarity(text1, text2):

    v1 = model.encode(text1)
    v2 = model.encode(text2)

    score = cosine_similarity([v1], [v2])[0][0]

    return float(round(score * 100, 2))


# Extract Resume Summary
def extract_summary(resume):

    lines = resume.split("\n")

    return " ".join(lines[:5])


# Recommend Role
def recommend_role(data):

    if data["technical_score"] > 75:
        return "Technical Specialist"

    if data["personality_score"] > 75:
        return "Team-Oriented Role"

    if data["confidence"] == "High":
        return "Leadership Track"

    return "General Contributor"

# Personality Analysis
def analyze_personality(resume_text,jd_text):

    summary = extract_summary(resume_text)
    summary = clean_text(summary)

    trait_scores = {}

    extras = adapt_traits_to_jd(jd_text)

    for trait, refs in TRAITS.items():

        scores = []

        for ref in refs:

            sim = get_similarity(summary, ref)
            scores.append(sim)

        trait_scores[trait] = float(round(sum(scores)/len(scores), 2))



    personality_score = float(round(
        sum(trait_scores.values()) / len(trait_scores),
        2
    ))

    return personality_score, trait_scores


# Split Resume into Sections
def split_sections(resume):

    sections = {
        "summary": "",
        "skills": "",
        "projects": "",
        "experience": ""
    }

    current = "summary"

    for line in resume.split("\n"):

        l = line.lower()

        if "skill" in l:
            current = "skills"

        elif "project" in l:
            current = "projects"

        elif "experience" in l or "intern" in l:
            current = "experience"

        sections[current] += line + " "

    return sections


# Extract Dynamic Skills
def extract_dynamic_skills(jd_text):

    words = jd_text.lower().split()

    candidates = []

    for w in words:
        if len(w) > 3 and w.isalpha():
            candidates.append(w)

    return list(set(candidates))


# Get Trait Weights
def get_trait_weights(jd):

    weights = {
        "leadership":1,
        "teamwork":1,
        "learning":1,
        "communication":1,
        "problem_solving":1
    }

    jd = jd.lower()

    if "lead" in jd or "manager" in jd:
        weights["leadership"] = 1.5

    if "learn" in jd or "entry" in jd:
        weights["learning"] = 1.5

    if "research" in jd or "analyze" in jd:
        weights["problem_solving"] = 1.5

    return weights


# Get Score Weights
def get_score_weights(jd):

    jd = jd.lower()

    tech_words = [
        "python","sql","api","cloud","ml","model",
        "data","server","backend","frontend"
    ]

    soft_words = [
        "team","lead","communicate","collaborate",
        "culture","manage","mentor"
    ]

    tech_count = sum(jd.count(w) for w in tech_words)
    soft_count = sum(jd.count(w) for w in soft_words)

    if tech_count > soft_count:
        return {"tech":0.5, "personality":0.2, "quality":0.2, "skills":0.1}

    else:
        return {"tech":0.3, "personality":0.4, "quality":0.2, "skills":0.1}


# Calculate Section Scores
def section_scores(resume_text, jd_text):

    parts = split_sections(resume_text)

    scores = {}

    for k, v in parts.items():

        if len(v.strip()) > 20:
            scores[k] = float(round(get_similarity(v, jd_text), 2))

        else:
            scores[k] = 0.0

    return scores

ACTION_VERBS = [
    "built","developed","designed","implemented",
    "optimized","created","managed","led"
]


# Resume Quality
def resume_quality(resume):

    text = resume.lower()

    words = text.split()
    length = len(words)

    length_score = 100 if 400 <= length <= 700 else max(40, 100 - abs(length-550)//5)

    action_count = sum(1 for v in ACTION_VERBS if v in text)

    number_count = len(re.findall(r'\d+%?', text))

    verb_score = min(100, action_count * 15)
    number_score = min(100, number_count * 10)

    quality = round(
        0.4*length_score +
        0.3*verb_score +
        0.3*number_score,
        2
    )

    return quality

STRONG_WORDS = [
    "led","achieved","improved","optimized",
    "built","designed","delivered"
]

WEAK_WORDS = [
    "helped","assisted","tried","supported","basic"
]


# Confidence Level
def confidence_level(resume):

    text = resume.lower()

    strong = sum(text.count(w) for w in STRONG_WORDS)
    weak = sum(text.count(w) for w in WEAK_WORDS)

    if strong > weak+2:
        return "High"
    elif weak > strong+2:
        return "Low"
    else:
        return "Medium"


# Extract Skills
def extract_skills(text):

    found = []

    text = text.lower()

    for skill in SKILLS:

        if skill in text:
            found.append(skill.upper())

    return list(set(found))


# Find Missing Skills
def find_missing_skills(resume, jd):

    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(jd)

    missing = list(set(jd_skills) - set(resume_skills))

    return missing


# Detect Domain
def detect_domain(jd):

    jd = jd.lower()

    if any(w in jd for w in ["ml","model","ai","data"]):
        return "Data / AI"

    if any(w in jd for w in ["react","javascript","frontend","css"]):
        return "Web Development"

    if any(w in jd for w in ["aws","cloud","devops","docker"]):
        return "Cloud / DevOps"

    if any(w in jd for w in ["marketing","seo","content"]):
        return "Marketing"

    return "General"


# Generate Suggestions
def generate_suggestions(data):

    suggestions = []

    if data["technical_score"] < 60:
        suggestions.append("Improve alignment with job requirements")

    if data["personality_score"] < 50:
        suggestions.append("Add examples of leadership and teamwork")

    if data["resume_quality"] < 65:
        suggestions.append("Improve resume structure and impact")

    if len(data["missing_skills"]) > 0:
        suggestions.append("Learn missing skills: " + ", ".join(data["missing_skills"]))

    if data["confidence"] == "Low":
        suggestions.append("Use stronger action-oriented language")

    return suggestions

def adapt_traits_to_jd(jd):

    extra = []

    jd = jd.lower()

    if "research" in jd:
        extra.append("I conduct experiments and publish results")

    if "startup" in jd:
        extra.append("I work independently in fast environments")

    if "client" in jd:
        extra.append("I handle client communication effectively")

    return extra


# Main Analyzer Function
def analyze_resume(resume_text, jd_text):

    resume = clean_text(resume_text)
    jd = clean_text(jd_text)
    weights = get_score_weights(jd_text)

    technical_score = get_similarity(resume, jd)

    personality_score, traits = analyze_personality(resume_text,jd_text)

    missing = find_missing_skills(resume, jd)

    sections = section_scores(resume_text, jd_text)

    domain = detect_domain(jd_text)

    quality = resume_quality(resume_text)

    confidence = confidence_level(resume_text)

    overall = round(
    weights["tech"] * technical_score +
    weights["personality"] * personality_score +
    weights["quality"] * quality +
    weights["skills"] * (100 - len(missing)*5),
    2
)

    domain = detect_domain(jd_text)
    weights = get_score_weights(jd_text)


    data = {
        "overall_score": overall,
        "technical_score": technical_score,
        "personality_score": personality_score,
        "section_scores": sections,
        "traits": traits,
        "resume_quality": quality,
        "confidence": confidence,
        "missing_skills": missing,
        "detected_domain": domain,
        "score_weights": weights,

    }

    data["suggestions"] = generate_suggestions(data)

    return data



# Test Run
if __name__ == "__main__":

    resume = """
    Passionate machine learning engineer.
    Loves learning and teamwork.
    Built AI projects in Python and TensorFlow.
    Strong problem solving skills.
    """

    jd = """
    Hiring ML engineer with Python, SQL, and AWS.
    Needs strong analytical thinking.
    Experience in deep learning preferred.
    """

    print(analyze_resume(resume, jd))


