from collections import Counter
import re
from statistics import mean, stdev

def find_different_products(product_list):

    def tokenize_product(text):

        clean_text = re.sub(r'["\\\-+.,/]', ' ', text)
        size_match = re.findall(r'(\d+)(?:\s?[Ii]nch)', clean_text)
        words = [w for w in clean_text.split() if w]
        
        return {
            'original': text,
            'size': size_match[0] if size_match else None,
            'words': words,
            'word_set': set(words)
        }

    def calculate_similarity_matrix(tokens_list):
        n = len(tokens_list)
        similarity_matrix = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    set_i = tokens_list[i]['word_set']
                    set_j = tokens_list[j]['word_set']
                    intersection = len(set_i.intersection(set_j))
                    union = len(set_i.union(set_j))
                    similarity_matrix[i][j] = intersection / union if union > 0 else 0
                    
        return similarity_matrix

    def analyze_patterns(tokens_list, similarity_matrix):

        n = len(tokens_list)

        all_words = []
        for token in tokens_list:
            all_words.extend(token['words'])
        word_freq = Counter(all_words)

        avg_similarities = []
        for i in range(n):
            avg_sim = sum(similarity_matrix[i]) / (n - 1)
            avg_similarities.append(avg_sim)

        mean_similarity = mean(avg_similarities)
        std_similarity = stdev(avg_similarities)

        sizes = [t['size'] for t in tokens_list if t['size']]
        size_freq = Counter(sizes)
        most_common_size = size_freq.most_common(1)[0][0] if sizes else None
        
        return {
            'word_freq': word_freq,
            'mean_similarity': mean_similarity,
            'std_similarity': std_similarity,
            'most_common_size': most_common_size,
            'size_freq': size_freq,
            'total_products': n,
            'avg_similarities': avg_similarities
        }

    def find_differences(idx, token, patterns, similarity_matrix):
        reasons = []

        if token['size'] and token['size'] != patterns['most_common_size']:
            if patterns['size_freq'][token['size']] < patterns['total_products'] * 0.3:
                reasons.append(f"karena sizenya {token['size']}")

        avg_sim = patterns['avg_similarities'][idx]
        if avg_sim < patterns['mean_similarity'] - patterns['std_similarity']:

            unique_words = []
            for word in token['words']:
                word_frequency = patterns['word_freq'][word]
                if word_frequency < patterns['total_products'] * 0.2:
                    unique_words.append(word)
            
            if unique_words:
                most_unique_word = max(unique_words, key=lambda w: patterns['word_freq'][w])
                reasons.append(f"karena mengandung kata unik: {most_unique_word}")
        
        return reasons

    tokenized_products = [tokenize_product(p) for p in product_list]
    similarity_matrix = calculate_similarity_matrix(tokenized_products)
    patterns = analyze_patterns(tokenized_products, similarity_matrix)
    different_products = []
    
    for i, token in enumerate(tokenized_products):
        differences = find_differences(i, token, patterns, similarity_matrix)
        if differences:
            for reason in differences:
                different_products.append(f'"{token["original"]}" ({reason})')
    
    return different_products

list_nama = [
    "Monitor Xiaomi Mi 34 Inch G34WQi WQHD Ultrawide 180Hz SRGB Curved Gaming Monitor",                      
    "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi 3 Tahun - Packing Bubble"
    "Xiaomi Mi Monitor 30\" G30WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",                 
    "Xiaomi Curved Gaming Monitor 34 Inch G34WQi Garansi Resmi",                                             
    "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi 3 Tahun - bubble",       
    "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming",                                      
    "Xiaomi Mi Monitor 34 Inch G34WQi WQHD Ultrawide 180Hz Curved Gaming Monitor - +Kayu JNE/Sicpt",         
    "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",                 
    "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming ",                                     
    "Xiaomi Monitor Curved Gaming Monitor 34 Inch 180Hz 34\" WQHD G34WQi 34inch",                            
    "Monitor Xiaomi Mi 34 Inch G34WQi WQHD Ultrawide 180Hz SRGB Curved Gaming Monitor",                      
    "Xiaomi Mi Monitor 34 Inch G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi",                     
    "Xiaomi Mi Monitor G34WQi 34 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",            
    "Xiaomi Mi Monitor G30WQi 30 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",            
    "Monitor G34WQi 34 Inch WQHD Samsung Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",            
]

output = [
    "Xiaomi Mi Monitor 30\" G30WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",
    "Xiaomi Mi Monitor G30WQi 30 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",
    "Monitor G34WQi 34 Inch WQHD Samsung Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",
]

results = find_different_products(list_nama)

for result in results:
    print(result)