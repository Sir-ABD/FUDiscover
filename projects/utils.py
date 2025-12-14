import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Project

def check_title_similarity(new_title):
    """
    Checks if title is >80% similar to existing titles using Levenshtein distance.
    Returns (bool, matching_title)
    """
    existing_titles = Project.objects.filter(is_approved=True).values_list('title', flat=True)
    if not existing_titles:
        return False, None

    for title in existing_titles:
        ratio = difflib.SequenceMatcher(None, new_title.lower(), title.lower()).ratio()
        if ratio > 0.8:
            return True, title
    return False, None

def check_abstract_similarity(new_abstract):
    """
    Checks if abstract is >70% similar to existing abstracts using Cosine Similarity.
    Returns (bool, matching_title)
    """
    existing_projects = Project.objects.filter(is_approved=True).values_list('abstract', 'title')
    if not existing_projects:
        return False, None
    
    # Prepare documents
    existing_abstracts = [p[0] for p in existing_projects]
    documents = [new_abstract] + existing_abstracts
    
    try:
        tfidf = TfidfVectorizer().fit_transform(documents)
        # Compare new_abstract (index 0) with others
        cosine_similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
        
        for i, score in enumerate(cosine_similarities):
            if score > 0.7:  # 70% similarity threshold
                return True, existing_projects[i][1]
    except Exception as e:
        print(f"Error in similarity check: {e}")
        # Fallback or pass if error (e.g. empty vocab)
        pass
        
    return False, None
