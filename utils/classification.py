# utils/classification.py
from difflib import SequenceMatcher

def compute_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def classify_accident(text: str) -> dict:
    """
    Compares the input text with a predefined list of possible accident causes
    and returns the cause with the highest similarity score along with the score.
    """
    causes = [
        "Driver distraction",
        "Speeding",
        "Driving under the influence of alcohol or drugs",
        "Disregard for traffic rules",
        "Fatigue and drowsiness",
        "Lack of vehicle maintenance",
        "Adverse weather conditions",
        "Inadequate infrastructure",
        "Aggressive behavior",
        "Lack of experience",
        "Inadequate use of safety equipment",
        "Animals on the road",
        "Visibility issues",
        "Disregard for right of way",
        "Improper lane usage",
        "Lack of attention to pedestrians and cyclists",
        "Driver health issues",
        "Pedestrian inattention",
        "Others"
    ]
    
    best_score = 0.0
    best_cause = "Others"
    for cause in causes:
        score = compute_similarity(text.lower(), cause.lower())
        if score > best_score:
            best_score = score
            best_cause = cause
    return {"root_cause": best_cause, "score": best_score}
