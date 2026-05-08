import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')  
nltk.download('stopwords')
nltk.download('vader_lexicon')
file_path = "Twitter_Data.csv"
df = pd.read_csv(file_path)
df.rename(columns={'clean_text': 'text'}, inplace=True)
df.columns = df.columns.str.strip()
print("Columns in dataset:", df.columns)
possible_cols = ['text', 'review', 'Review', 'sentence', 'Sentence']
text_col = None
for col in possible_cols:
    if col in df.columns:
        text_col = col
        break

if text_col is None:
    raise Exception("❌ No valid text column found. Rename your column to 'text' or 'review'.")


df.rename(columns={text_col: 'text'}, inplace=True)
df = df.dropna(subset=['text'])

stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

df['tokens'] = df['text'].apply(preprocess)
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df['sentiment'] = df['text'].apply(get_sentiment)

emotion_lexicon = {
    "love": "joy", "amazing": "joy", "happy": "joy", "fantastic": "joy",
    "good": "joy", "great": "joy",

    "hate": "anger", "worst": "anger", "angry": "anger", "waste": "anger",

    "sad": "sadness", "bad": "sadness", "disappointed": "sadness",

    "fear": "fear", "scared": "fear",

    "surprise": "surprise", "shocked": "surprise"
}

def detect_emotion(tokens):
    emotions = []
    for word in tokens:
        if word in emotion_lexicon:
            emotions.append(emotion_lexicon[word])
    return max(set(emotions), key=emotions.count) if emotions else "neutral"

df['emotion'] = df['tokens'].apply(detect_emotion)

print("\n===== SAMPLE OUTPUT =====\n")
print(df[['text', 'sentiment', 'emotion']].head())

df.to_csv("sentiment_output.csv", index=False)
df.to_excel("sentiment_output.xlsx", index=False)

print("\n✅ Output saved as:")
print("sentiment_output.csv")
print("sentiment_output.xlsx")

plt.figure()
sns.countplot(x='sentiment', data=df)
plt.title("Sentiment Distribution")
plt.show()

plt.figure()
sns.countplot(x='emotion', data=df)
plt.title("Emotion Distribution")
plt.show()

print("\n===== INSIGHTS =====")
print("Most common sentiment:", df['sentiment'].value_counts().idxmax())
print("Most common emotion:", df['emotion'].value_counts().idxmax())

while True:
    user_text = input("\nEnter text (or type 'exit'): ")

    if user_text.lower() == 'exit':
        break

    sentiment = get_sentiment(user_text)
    tokens = preprocess(user_text)
    emotion = detect_emotion(tokens)

    print("\nResult:")
    print("Sentiment:", sentiment)
    print("Emotion:", emotion)
