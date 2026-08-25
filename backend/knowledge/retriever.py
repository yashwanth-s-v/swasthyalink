from pathlib import Path


DOCUMENTS_DIR = Path(__file__).parent / "documents"


def load_documents() -> dict[str, str]:
    """
    Load all Ayurveda knowledge documents from the
    knowledge/documents directory.
    """

    documents = {}

    if not DOCUMENTS_DIR.exists():
        return documents

    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            documents[file_path.stem] = content

        except Exception:
            continue

    return documents


def tokenize(text: str) -> set[str]:
    """
    Convert text into a simple set of searchable words.
    """

    return {
        word.lower().strip(
            ".,!?;:()[]{}\"'"
        )
        for word in text.split()
        if len(word) > 2
    }


def calculate_relevance(
    query: str,
    document: str
) -> int:
    """
    Calculate basic keyword overlap between the query
    and a document.
    """

    query_words = tokenize(query)
    document_words = tokenize(document)

    if not query_words:
        return 0

    common_words = query_words.intersection(
        document_words
    )

    return len(common_words)


def retrieve(
    query: str,
    top_k: int = 3
) -> list[dict]:
    """
    Retrieve the most relevant knowledge documents.
    """

    documents = load_documents()

    results = []

    for name, content in documents.items():

        score = calculate_relevance(
            query,
            content
        )

        results.append(
            {
                "document": name,
                "content": content,
                "score": score
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]