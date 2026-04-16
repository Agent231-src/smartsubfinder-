from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re

class MLAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        self._train_model()
    
    def _train_model(self):
        # Dummy training data: high-value vs noise patterns
        high_value = ['admin', 'api', 'dev', 'staging', 'beta', 'internal']
        noise = ['www', 'mail', 'ftp', 'static']
        X = high_value + noise
        y = [1] * len(high_value) + [0] * len(noise)
        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)
    
    def score_subdomains(self, subs):
        scores = []
        for sub in subs:
            # Extract keywords
            keywords = re.findall(r'([a-z]+)', sub.lower())
            vec = self.vectorizer.transform(keywords)
            score = self.model.predict_proba(vec.mean(axis=0))[0][1]
            
            # HTTP check bonus
            try:
                r = requests.get(f'http://{sub}', timeout=3)
                score += 0.2 if r.status_code == 200 else 0
            except:
                pass
            
            scores.append({'subdomain': sub, 'score': min(1.0, score)})
        return sorted(scores, key=lambda x: x['score'], reverse=True)
