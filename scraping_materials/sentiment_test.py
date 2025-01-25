from transformers import pipeline

def test_huggingface_sentiment_analysis():
    sentiment_analyzer = pipeline('sentiment-analysis')

    comments = [
        "Great product! I really love it!",
        "Terrible service, I am very disappointed.",
        "It's okay, not the best but not the worst either.",
    ]

    for comment in comments:
        print(f"Analyzing sentiment for comment: {comment}")
        result = sentiment_analyzer(comment)[0]
        print(f"Sentiment: {result['label']}, Score: {result['score']:.2f}\n")

if __name__ == "__main__":
    print("Starting sentiment analysis test...")
    test_huggingface_sentiment_analysis()
    print("Sentiment analysis test completed.")