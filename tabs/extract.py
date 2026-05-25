import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

'''
main function: extract_pairs_from_notes
input: long string of text
output: list of tuples with (word, definition)



'''

def rank_pairs_with_tfidf(pairs):
    """
    Takes pairs in the form:
    (term, definition)

    Returns:
    (term, definition, importance_score)
    sorted from most important to least important.
    """

    if len(pairs) == 0:
        return []

    if len(pairs) == 1:
        term, definition = pairs[0]
        return [(term, definition, 1.0)]

    # Use term + definition as the text TF-IDF looks at
    chunks = []

    for term, definition in pairs:
        chunks.append(term + " " + definition)


    #unsupervised learning part!!
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(chunks)

    scores = np.asarray(tfidf_matrix.sum(axis=1)).flatten()

    max_score = scores.max()

    ranked_pairs = []

    for i, score in enumerate(scores):
        term, definition = pairs[i]

        if max_score > 0:
            importance = score / max_score
        else:
            importance = 0

        ranked_pairs.append((term, definition, importance))

    ranked_pairs.sort(key=lambda x: x[2], reverse=True)

    result_pairs = []
    for pair in ranked_pairs:
        result_pairs.append((ranked_pairs[0], ranked_pairs[1]))

    return result_pairs


def extract_pairs_from_notes(text):
        """
        Looks for patterns like:
        - term is definition.
        - term: definition
        - term = definition

        Stops sections at periods or new lines.
        Returns list of tuples: (word, definition)
        """
        pairs = []

        # Stop sections at period or newline
        chunks = re.split(r"[.\n]+", text)

        patterns = [
            r"^(.+?)\s+is\s+(.+)$",
            r"^(.+?)\s+are\s+(.+)$",
            r"^(.+?)\s*:\s*(.+)$",
            r"^(.+?)\s*=\s*(.+)$",
            r"^(.+?)\s+means\s+(.+)$",
            r"^(.+?)\s+refers to\s+(.+)$",
            r"^(.+?)\s+is defined as\s+(.+)$",
        ]

        # print(chunks)

        for chunk in chunks:
            chunk = chunk.strip()
            chunk = re.sub(r"\s+", " ", chunk)

            if len(chunk) < 5:
                continue

            for pattern in patterns:
                match = re.match(pattern, chunk, re.IGNORECASE)

                if match:
                    term = match.group(1).strip()
                    definition = match.group(2).strip()

                    # Avoid terrible flashcards like giant paragraphs as terms
                    if len(term) > 1 and len(definition) > 1 and len(term.split()) <= 12:
                        pairs.append((term, definition))

                    break
            
        # print(pairs)
        
        new_pairs = rank_pairs_with_tfidf(pairs)
        # print(new_pairs)
        return pairs
    
    
    
clean_test = '''
Crop: temporary food storage, in front of gizzard
Gizzard: grinds up food, muscular
Intestine: long tube from gizzard -> anus, digestion/absorption
Clitellum: swollen part ⅓ way from anterior (front) to posterior (end)
Also aids in reproduction
Mouth : below prostomium, anterior, not considered a segment
Anus: solid waste exit, posterior
Metanephridia: connect with Nephridiopores
'''

test = '''
The worm has many amazing features, such as the gizzard, crop, and intestine. 
The gizzard is a muscle that grinds up food.
The intestine is a long tube from the gizzard to the anus.
Worms are really cool.
I really like worms.
Clitellum is the swollen part 1/3 from anterior to posterior.
I wonder what's in the worm's anus.
The anus is a solid waste exist, posterior of the worm.
Solid waste is basically poop.
Quite wonderful.
'''


extract_pairs_from_notes(test)