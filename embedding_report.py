import numpy as np


def cosine_similarity(vec1, vec2):
    vec1 = np.asarray(vec1)
    vec2 = np.asarray(vec2)

    denominator = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if denominator == 0:
        return 0.0

    return float(np.dot(vec1, vec2) / denominator)


def detailed_report(
    essay_chunks,
    essay_embeddings,
    transcript_chunks,
    transcript_embeddings,
    video_id,
    video_title,
):
    """Print chunk-level comparisons and return the average similarity."""
    if len(essay_chunks) != len(essay_embeddings):
        raise ValueError("Essay chunks and embeddings must have the same length")
    if len(transcript_chunks) != len(transcript_embeddings):
        raise ValueError(
            "Transcript chunks and embeddings must have the same length"
        )
    if not essay_embeddings or not transcript_embeddings:
        raise ValueError("Both the essay and transcript need at least one chunk")

    similarities = []

    print("=" * 100)
    print(f"Video: {video_title}")
    print(f"Video ID: {video_id}")
    print("=" * 100)

    for essay_number, (essay_chunk, essay_embedding) in enumerate(
        zip(essay_chunks, essay_embeddings),
        start=1,
    ):
        for transcript_number, (
            transcript_chunk,
            transcript_embedding,
        ) in enumerate(
            zip(transcript_chunks, transcript_embeddings),
            start=1,
        ):
            similarity = cosine_similarity(
                essay_embedding,
                transcript_embedding,
            )
            similarities.append(similarity)

            print(
                f"\nEssay chunk {essay_number} | "
                f"Transcript chunk {transcript_number} | "
                f"Similarity: {similarity:.4f}"
            )
            print("-" * 100)
            print("ESSAY CHUNK")
            print(essay_chunk)
            print("\nTRANSCRIPT CHUNK")
            print(transcript_chunk)

    average_similarity = float(np.mean(similarities))
    print("\n" + "=" * 100)
    print(f"Average similarity for {video_title} ({video_id}): "
          f"{average_similarity:.4f}")
    print("=" * 100)

    return average_similarity
