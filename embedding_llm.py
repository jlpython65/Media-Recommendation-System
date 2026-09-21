import os

from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import tiktoken
import numpy as np
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# --------------------------------------------------
# Split text into overlapping chunks
# --------------------------------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)

    chunks = []

    #Sliding window for overlapping tokens 
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]

        #Why must we decode? 

        #Tokenize to create partitions 
        #Chunk those partitions 
        #Decode to .. embed words?
        chunks.append(tokenizer.decode(chunk_tokens))

    return chunks


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------
def embed_text(text):
    chunks = chunk_text(text)

    #select model from openai

    #Embed the chunks
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    embeddings = [item.embedding for item in response.data]

    return chunks, embeddings


# --------------------------------------------------
# Cosine similarity
# --------------------------------------------------
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

#Avg similarity score
def average_similarity(essay_embeddings, transcript_embeddings):
    total_similarity = 0
    comparisons = 0

    for essay_vec in essay_embeddings:
        for transcript_vec in transcript_embeddings:
            total_similarity += cosine_similarity(essay_vec, transcript_vec)
            comparisons += 1

    average = total_similarity / comparisons

    print(f"Average Similarity: {average:.4f}")

    return average


# --------------------------------------------------
# Compare every chunk
# --------------------------------------------------
def compare_embeddings(
    essay_chunks,
    essay_embeddings,
    transcript_chunks,
    transcript_embeddings,
    top_k=10
):
    results = []

    for essay_idx, essay_vec in enumerate(essay_embeddings):
        for transcript_idx, transcript_vec in enumerate(transcript_embeddings):

            similarity = cosine_similarity(
                essay_vec,
                transcript_vec
            )

            results.append({
                "essay_chunk": essay_idx,
                "transcript_chunk": transcript_idx,
                "similarity": similarity
            })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    print(f"\nTop {top_k} Matches")
    print("=" * 80)

    for result in results[:top_k]:

        e = result["essay_chunk"]
        t = result["transcript_chunk"]

        print(f"\nSimilarity: {result['similarity']:.4f}")
        print("-" * 80)

        print(f"Essay Chunk #{e}")x
        print(essay_chunks[e])

        print("\nTranscript Chunk #{}".format(t))
        print(transcript_chunks[t])             

        print("=" * 80)

    return results


# --------------------------------------------------
# Download transcript
# --------------------------------------------------
ytt_api = YouTubeTranscriptApi()

#Falling behind video (has themes of chasing extrinsic motivation instead of intrinsic)
#Scores an average of 0.45 similarity score
video_id = "1e6n6RZeTWQ"

#Rammatra lore (completely unrelated example)]
#Similarity score of 0.2 - 0.35
#GUess the common theme is speaking out against cultures that has affected the speaker
# video_id = "kQ_y0QcorJ8"

fetched_transcript = ytt_api.fetch(video_id)

transcript = " ".join(
    snippet.text for snippet in fetched_transcript
)


# --------------------------------------------------
# Your essay
# --------------------------------------------------
essay = """
Auto-Exploitation_Robs_One_From_Following_Intrinsic_Motivation

Our society has shifted from one that punishes to elicit obedience to one that one that reward achievements. Instead of telling us we can't do something, we are told we can do anything. The depression we're seeing in the modern age has little to do about building oneself. Rather it's the pressure to build a self attached to achievements. It's one thing to enjoy learning, but an entirely different thing to place your entire self-hood on it. What makes this pressure so powerful is its efficiency. Exercsing punishment for obedience subjects is limited by the costs of the punisher. You can't follow a child all day and whack him when he doesn't do his homework. But what if you don't need to punish, but the subject themselves do it. In the achievement-subjects' despair, they will turn against themselves and experience self-loathing. To avoid such a fate, they must continue to achieve throughout most their day. The author coins this avoidance as "auto-exploitation". The most insidious part of this phenomenon is that the subject believes they are free while doing more work, just because there is no one present to deliver punishement.

I went through a major self-improvement phase in high school. But I learned everything for the wrong reasons. I studeied more efficinetly to play more games. I decided to pick up coding because I heard everyone needed to code. Funny, that was a message pushed by tech barons to create a cheaper labor force. I took a course on happiness because I thought people would want to be my friend. Social skills as well. I thought I was ahead of everyone. But I lost that lead when I realized I don't truly know myself. I dropped coding after a rage inducing project and I took a gap year because I was burnt out. For all my self-improvement, there was no future I found meaningful enough to keep my efforts consistent. Or had the guts to contemplate my life. Needless to say, I was in the grasp of auto-explotation and I was deluded to think I was ahead. It doesn't matter how fast you run on the treadmill, you're never reaching satisfaction or contentment.
"""


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------
essay_chunks, essay_embeddings = embed_text(essay)

transcript_chunks, transcript_embeddings = embed_text(transcript)


# --------------------------------------------------
# Compare them
# --------------------------------------------------
results = compare_embeddings(
    essay_chunks,
    essay_embeddings,
    transcript_chunks,
    transcript_embeddings,
    top_k=10
)

average_score = average_similarity(
    essay_embeddings,
    transcript_embeddings
)