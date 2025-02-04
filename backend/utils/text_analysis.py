import hashlib
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from ollama import Client
import os

# 確保已下載VADER字典
nltk.download('vader_lexicon')

# 初始化VADER情感分析器
sid = SentimentIntensityAnalyzer()

def translate_to_english(texts):
    """使用 Ollama API 將中文翻譯成英文"""
    client = Client(host=os.getenv('OLLAMA_API_HOST'))
    translations = []

    for text in texts:
        try:
            if not text or text.isspace():  # 檢查空文本
                translations.append("")
                continue
                
            response = client.chat(
                model=os.getenv('OLLAMA_MODEL'),
                messages=[
                    {
                        "role": "system",
                        "content": os.getenv('OLLAMA_SYSTEM_PROMPT')
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )
            
            # 解析回應
            translation = response["message"]["content"].strip()
            
            # 檢查翻譯結果
            if not translation or translation.isspace():
                translations.append(text)  # 如果翻譯為空，保留原文
            else:
                translations.append(translation)
                
        except Exception as e:
            print(f"翻譯出錯: {str(e)}")
            translations.append(text)  # 出錯時保留原文
            
    return translations

def analyze_sentiment_with_NLTK(texts):
    """使用 NLTK VADER 進行情感分析"""
    results = []
    for text in texts:
        scores = sid.polarity_scores(text)
        
        # 提取情感分析結果
        pos_score = round(scores['pos'], 2)
        neg_score = round(scores['neg'], 2)
        neu_score = round(scores['neu'], 2)
        compound_score = round(scores['compound'], 2)

        # 判斷情感類別
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        results.append([pos_score, neg_score, neu_score, compound_score, sentiment])
    
    return results

def tokenize_and_clean_comments(comments, stopwords):
    """使用 jieba 進行斷詞，並過濾停用詞"""
    if isinstance(stopwords, str):
        stopwords = eval(stopwords)
    return [" ".join(jieba.cut(comment)) for comment in comments if comment not in stopwords]

def calculate_score(tfidf_scores, feature_names, keywords_weights, default_weight=1):
    """計算每個評論的總評分"""
    if isinstance(keywords_weights, str):
        keywords_weights = eval(keywords_weights)
    
    total_scores = []
    for row in tfidf_scores:
        score = 0
        for i, word_score in enumerate(row):
            word = feature_names[i]
            weight = keywords_weights.get(word, default_weight)
            score += word_score * weight
        total_scores.append(score)
    return total_scores

def generate_hash(value):
    """生成字符串的 SHA-256 雜湊值"""
    return hashlib.sha256(value.encode()).hexdigest() 