import requests
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import string
import matplotlib.pyplot as plt

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        return None
    
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def visualize_top_words(words, top_n=10):
    sorted_words = sorted(words.items(), key=lambda item: item[1], reverse=True)
    
    top_words = dict(sorted_words[:top_n])
    words = list(top_words.keys())
    counts = list(top_words.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='teal')
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title(f'TOP-{top_n} words')
    plt.xticks(rotation=45)  
    plt.show()

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

if __name__ == '__main__':
    url = "https://www.gutenberg.org/cache/epub/5131/pg5131.txt"
    text = get_text(url)
    if text:
        result = map_reduce(text)
        visualize_top_words(result, 10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
