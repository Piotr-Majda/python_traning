# 🔥 Twoje rozgrzewkowe zadania na dziś (limit 15 min każde)

# 1. Odwróć słowa w zdaniu
# Napisz funkcję reverse_words(sentence: str) -> str, która odwraca kolejność liter w każdym słowie, ale nie zmienia kolejności słów.
# Przykład:
# reverse_words("Hello World")  
# "olleH dlroW"


def reverse_words(sentence: str) -> str:
    """Reverse characters of each word in the sentence, preserve word order."""
    words = sentence.split(' ')
    return ' '.join(w[::-1] for w in words)
