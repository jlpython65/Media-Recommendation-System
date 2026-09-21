# Media Recommendation System

A prototype AI system that matches a personal essay to YouTube videos based on semantic similarity. The project combines NLP embeddings, transcript extraction, and recommendation-style ranking to identify videos whose themes align with a user’s writing.

This repository was built as a practical experiment in using modern language models and embedding-based retrieval to convert a written idea into relevant media recommendations.

## Why this project matters

The core concept is simple but powerful: instead of relying on channel subscriptions or keyword matching alone, the system compares the meaning of a written passage against the content of YouTube videos. By converting both into vector embeddings and measuring similarity, the project surfaces videos that are conceptually aligned with the essay’s themes.

This is a strong example of:

- Applied natural language processing
- Semantic search and recommendation logic
- Data pipeline design from raw web content to structured metadata
- AI-powered content understanding using embeddings
- Combining APIs, browser automation, and text analysis in one workflow

## What the system does

1. Takes a user-written essay or reflection as input.
2. Splits the text into overlapping chunks.
3. Uses OpenAI embeddings to convert each chunk into a vector representation.
4. Pulls relevant YouTube transcripts and metadata.
5. Compares essay chunks and transcript chunks using cosine similarity.
6. Produces the most semantically similar matches.

The result is a ranked list of videos that feel related to the essay’s themes, not just keyword matches.

## Project highlights

- Embedding-based semantic comparison instead of brittle keyword heuristics
- Overlapping chunking strategy to preserve context in longer texts
- YouTube transcript extraction for content analysis
- Video metadata enrichment via the YouTube Data API
- Browser-based extraction of recommendation data from YouTube
- Experimental recommendation pipeline that is easy to extend to other content sources

## Technical stack

- Python
- OpenAI embeddings API
- NumPy for similarity calculations
- YouTube Transcript API
- Playwright for browser automation
- Google YouTube Data API for metadata lookup
- Python dotenv for environment-based configuration

## Repository structure

- `embedding_llm.py` — core embedding pipeline, chunking, and semantic comparison logic
- `embedding_report.py` — detailed similarity reporting and comparison summaries
- `youtube/extract_recommendation_json.py` — extracts YouTube page data using Playwright
- `youtube/extract_video_ids.py` — parses recommendation JSON to collect video IDs
- `youtube/lookup_metadata_yt_api.py` — fetches metadata for collected video IDs via the YouTube API
- `outputs/` — generated JSON files containing extracted video IDs and metadata
- `transcripts/` — example transcript files used for experimentation
- `personal_essays/` — essay examples and concept data

## Example workflow

The end-to-end flow is:

1. Capture a user essay.
2. Extract a target YouTube transcript.
3. Generate embeddings for both text sources.
4. Compare chunk-by-chunk using cosine similarity.
5. Rank matches and review top matches.

This creates a recommendation engine that behaves more like meaning-based matching than classic content filtering.

## How it works technically

The system converts text into vectors using embedding models and then measures closeness in latent space. Cosine similarity is used to determine how aligned two segments are conceptually.

In other words, if the essay discusses identity, burnout, motivation, or self-optimization, the system can detect corresponding themes in YouTube transcripts even when the wording differs.

## Setup

1. Create a Python environment.
2. Install dependencies.
3. Add environment variables for OpenAI and YouTube APIs.
4. Run the extraction and embedding scripts in sequence.

Example dependencies include:

- `openai`
- `youtube-transcript-api`
- `tiktoken`
- `numpy`
- `python-dotenv`
- `playwright`
- `google-api-python-client`

## Environment variables

The project expects values such as:

- `OPENAI_API_KEY`
- `YOUTUBE_API_KEY`

These are loaded using Python dotenv and kept out of source control.

## Example use case

This project is designed for content discovery across ideation, essays, thought pieces, and video recommendation use cases. A practical application would be:

- feed a personal essay into the system
- compare it against a library of transcripts
- return the most conceptually relevant videos
- use the results to support research, curation, or reading recommendations

## What I would highlight to recruiters

This project demonstrates a blend of:

- AI and machine learning implementation
- Data engineering and API integration
- Browser automation and scraping workflows
- Practical experimentation with recommendation systems
- End-to-end problem solving from raw data to structured output

It is especially relevant for roles involving:

- ML engineering
- AI product development
- NLP and search
- Recommendation systems
- Data pipeline work
- Applied prototyping with LLMs and embeddings

## Current status

This is a research/prototype repository rather than a polished production application. The focus is on validating the concept: using embeddings to connect written ideas with relevant video content.

## Future improvements

Potential next steps include:

- building a small web interface for essay-to-video recommendations
- adding ranking and filtering by engagement, recency, or channel
- storing results in a database for repeatable retrieval
- supporting richer metadata and transcript summarization
- evaluating recommendation quality with human feedback or offline metrics

## Summary

This repository is a compact proof of concept for an intelligent recommendation system based on semantic understanding rather than simple keyword matching. It shows the ability to combine AI, APIs, and data processing into a single workflow that turns text into personalized content suggestions.
