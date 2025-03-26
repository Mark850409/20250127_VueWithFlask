import hashlib
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from snownlp import SnowNLP
import os
import requests
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.config import SQLALCHEMY_DATABASE_URI

# 建立資料庫連接
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

def batch_update_sentiment_scores(results):
    """批次更新情感分析分數到資料庫
    
    Args:
        results: 包含多筆情感分析結果的列表
    """
    try:
        print("\n開始批次更新資料庫...")
        session = Session()
        success_count = 0
        error_count = 0
        
        try:
            # 修改 SQL 使用 hash 作為條件
            update_sql = text("""
                UPDATE ratings 
                SET 
                    positive_prob_zh = :positive,
                    negative_prob_zh = :negative,
                    neutral_score_zh = :neutral,
                    compound_zh = :compound
                WHERE hash = :hash
            """)
            
            # 批次處理更新
            for result in results:
                try:
                    params = {
                        'hash': result['hash'],  # 使用 hash 替代 id
                        'positive': result['positive'],
                        'negative': result['negative'],
                        'neutral': result['neutral'],
                        'compound': result['compound']
                    }
                    
                    session.execute(update_sql, params)
                    success_count += 1
                    
                    # 每100筆提交一次事務並顯示進度
                    if success_count % 100 == 0:
                        session.commit()
                        print(f"已處理 {success_count + error_count} 筆資料...")
                        
                except Exception as e:
                    error_count += 1
                    print(f"更新 hash {result['hash']} 時發生錯誤: {str(e)}")
                    session.rollback()
                    continue
            
            # 提交剩餘的事務
            session.commit()
            print(f"\n批次更新完成!")
            print(f"成功更新: {success_count} 筆")
            print(f"更新失敗: {error_count} 筆")
            
        except Exception as e:
            print(f"批次更新過程發生錯誤: {str(e)}")
            session.rollback()
        
        finally:
            session.close()
            
    except Exception as e:
        print(f"資料庫連接錯誤: {str(e)}")

def fetch_data_from_api(offset=0, limit=100):
    """從資料庫獲取資料"""
    try:
        session = Session()
        query = text("""
            SELECT hash, text 
            FROM ratings 
            ORDER BY hash
            LIMIT :limit OFFSET :offset
        """)
        
        result = session.execute(query, {'limit': limit, 'offset': offset})
        texts = [(row.hash, row.text) for row in result if row.text.strip()]
        session.close()
        return texts
        
    except Exception as e:
        print(f"獲取資料時發生錯誤: {str(e)}")
        return []

def analyze_sentiment_with_SnowNLP(texts):
    """使用 SnowNLP 進行情感分析"""
    results = []
    for index, (hash_value, text) in enumerate(texts, 1):
        try:
            s = SnowNLP(text)
            sentiment_score = s.sentiments
            
            pos_score = round(sentiment_score, 2)
            neg_score = round(1 - sentiment_score, 2)
            neu_score = round(1 - abs(pos_score - neg_score), 2)
            compound_score = round(abs((sentiment_score - 0.5) * 2), 2)

            if compound_score >= 0.05:
                sentiment = 'positive'
            elif compound_score <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            result = {
                'hash': hash_value,  # 使用 hash 替代 id
                'text': text,
                'positive': pos_score,
                'negative': neg_score,
                'neutral': neu_score,
                'compound': compound_score,
                'sentiment': sentiment
            }
            
            print(f"\n分析第 {index} 筆資料 (Hash: {hash_value[:8]}...):")  # 只顯示 hash 的前8位
            print(f"文本: {text[:100]}..." if len(text) > 100 else f"文本: {text}")
            print(f"情感: {sentiment}")
            print(f"正面分數: {pos_score}")
            print(f"負面分數: {neg_score}")
            print(f"中性分數: {neu_score}")
            print(f"綜合分數: {compound_score}")
            print("-" * 50)
            
            results.append(result)
            
        except Exception as e:
            print(f"分析文本時發生錯誤 (Hash: {hash_value[:8]}...): {str(e)}")
            continue
    
    return results

def process_all_data():
    """處理所有資料"""
    offset = 0
    limit = 1000
    all_results = []
    batch_count = 1
    
    while True:
        print(f"\n開始處理第 {batch_count} 批資料...")
        print(f"處理範圍: 第 {offset+1} 到 {offset+limit} 筆")
        print("=" * 50)
        
        texts = fetch_data_from_api(offset, limit)
        
        if not texts:
            break
            
        results = analyze_sentiment_with_SnowNLP(texts)
        all_results.extend(results)
        
        # 當收集到1000筆資料或沒有更多資料時，進行批次更新
        if len(all_results) >= 1000 or not texts:
            print(f"\n已收集 {len(all_results)} 筆資料，開始批次更新...")
            batch_update_sentiment_scores(all_results)
            all_results = []
        
        # 顯示當前批次的統計資訊
        batch_sentiments = [r['sentiment'] for r in results]
        batch_total = len(batch_sentiments)
        if batch_total > 0:
            batch_positive = batch_sentiments.count('positive')
            batch_negative = batch_sentiments.count('negative')
            batch_neutral = batch_sentiments.count('neutral')
            
            print(f"\n第 {batch_count} 批次統計:")
            print(f"正面評價: {batch_positive} ({batch_positive/batch_total*100:.1f}%)")
            print(f"負面評價: {batch_negative} ({batch_negative/batch_total*100:.1f}%)")
            print(f"中性評價: {batch_neutral} ({batch_neutral/batch_total*100:.1f}%)")
            print("=" * 50)
        
        offset += limit
        batch_count += 1
        time.sleep(1)
        
    return all_results

if __name__ == "__main__":
    # 執行批次處理
    results = process_all_data()
    
    # 輸出最終統計資訊
    sentiments = [r['sentiment'] for r in results]
    total = len(sentiments)
    positive = sentiments.count('positive')
    negative = sentiments.count('negative')
    neutral = sentiments.count('neutral')
    
    print("\n最終情感分析統計:")
    print("=" * 50)
    print(f"總資料筆數: {total}")
    print(f"正面評價: {positive} ({positive/total*100:.1f}%)")
    print(f"負面評價: {negative} ({negative/total*100:.1f}%)")
    print(f"中性評價: {neutral} ({neutral/total*100:.1f}%)")
    print("=" * 50)