# Install libraries (only needed in Colab)
!pip install seaborn scikit-learn matplotlib

# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Dataset
df = pd.read_csv('movie_dataset_named.csv')

# Display sample data
print(df.head())
print("\nColumns:", df.columns)

# Combine important features for similarity
df['Combined'] = df['Genre'] + ' ' + df['Actor'] + ' ' + df['Actress'] + ' ' + df['Director'] + ' ' + df['Language']

# Vectorization
vectorizer = CountVectorizer().fit_transform(df['Combined'])
similarity = cosine_similarity(vectorizer)

# Function to recommend movies
def recommend(title, num=5):
    if title not in df['Title'].values:
        print("Movie not found!")
        return
    index = df[df['Title'] == title].index[0]
    scores = list(enumerate(similarity[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:num+1]
    movie_indices = [i[0] for i in sorted_scores]
    
    print(f"\nTop {num} recommendations for '{title}':\n")
    for i in movie_indices:
        print(f"{df.iloc[i]['Title']} ({df.iloc[i]['Genre']}) ⭐{df.iloc[i]['Rating']}")

    # Plot recommendations
    recommended = df.iloc[movie_indices]
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Rating', y='Title', data=recommended, palette='coolwarm')
    plt.title(f"Top {num} Recommended Movies for '{title}'")
    plt.xlabel("Rating")
    plt.ylabel("Movie Title")
    plt.show()

# Example usage
recommend('The Last Battle', num=5)

# ---------------------- Additional Visualizations ----------------------

# 1. Genre Distribution
plt.figure(figsize=(10, 6))
sns.countplot(y='Genre', data=df, palette='magma', order=df['Genre'].value_counts().index)
plt.title('Genre Distribution')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.show()

# 2. Ratings Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df['Rating'], bins=20, kde=True, color='purple')
plt.title('Ratings Distribution')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

# 3. Year-wise Movie Count
plt.figure(figsize=(12, 5))
sns.countplot(x='Year', data=df, palette='cubehelix', order=sorted(df['Year'].unique()))
plt.title('Number of Movies Released per Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

# 4. Duration vs Rating Scatter
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Duration (min)', y='Rating', data=df, hue='Genre', palette='Set2')
plt.title('Duration vs Rating')
plt.xlabel('Duration (min)')
plt.ylabel('Rating')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
