from rag_pipeline import get_rationale
profile_original = {"income": 60000, "debt": 15000, "score": 650}
profile_drift = {"income": 60500, "debt": 15100, "score": 651}

print(get_rationale(profile_original))
print(get_rationale(profile_drift))
