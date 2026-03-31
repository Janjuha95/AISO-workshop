from ddgs import DDGS


def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return a list of results.

    Use this tool when you need to find information on the internet,
    look up current facts, or find URLs to read in more detail.
    If the first query returns insufficient results, call this tool
    again with a refined query.

    Args:
        query: The search query string.

    Returns:
        A formatted list of search results with titles, URLs, and snippets.
    """
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as e:
        return f"Search error: {e}"
    if not results:
        return "No results found. Try a different query."
    parts = []
    for r in results:
        parts.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
    return "\n".join(parts)
