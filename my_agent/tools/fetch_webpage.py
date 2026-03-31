from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import fitz


def fetch_webpage(url: str, search_term: str) -> str:
    """Fetch a webpage or PDF from a URL and return its text content.

    Use this tool to read the full content of a specific URL. Works with
    both regular web pages (HTML) and PDF files. If the URL contains a
    fragment (e.g. #section-id), only that section is returned.

    For large documents, use the search_term parameter to find only the
    relevant sections instead of reading the entire document.

    Args:
        url: The URL to fetch and read.
        search_term: A keyword or phrase to search for in the document. If provided, only paragraphs or pages containing this term are returned. Pass an empty string to get the full content.

    Returns:
        The extracted text content of the page or PDF.
    """
    parsed = urlparse(url)
    fragment = parsed.fragment
    fetch_url = parsed._replace(fragment="").geturl()

    try:
        response = requests.get(fetch_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

    content_type = response.headers.get("Content-Type", "")

    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        try:
            doc = fitz.open(stream=response.content, filetype="pdf")
            if search_term:
                # Return only pages containing the search term
                matching_pages = []
                for i, page in enumerate(doc):
                    text = page.get_text("text", sort=True, flags=fitz.TEXT_PRESERVE_WHITESPACE)
                    if search_term.lower() in text.lower():
                        matching_pages.append(f"--- Page {i + 1} ---\n{text}")
                doc.close()
                if matching_pages:
                    return f"Found '{search_term}' on {len(matching_pages)} page(s):\n\n" + "\n\n".join(matching_pages)
                return f"'{search_term}' not found in the PDF ({doc.page_count} pages total)."
            else:
                parts = []
                for page in doc:
                    parts.append(page.get_text("text", sort=True, flags=fitz.TEXT_PRESERVE_WHITESPACE))
                doc.close()
                text = "\n".join(parts)
        except Exception as e:
            return f"Error reading PDF: {e}"
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # If URL has a fragment, try to extract just that section
        if fragment:
            target = soup.find(id=fragment)
            if target:
                section_parts = [target.get_text(separator="\n", strip=True)]
                for sibling in target.find_next_siblings():
                    if sibling.name and sibling.name == target.name:
                        break
                    section_parts.append(sibling.get_text(separator="\n", strip=True))
                text = "\n".join(section_parts)
            else:
                text = soup.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        # Filter by search_term for HTML too
        if search_term and len(text) > 10000:
            lines = text.split("\n")
            matching = [l for l in lines if search_term.lower() in l.lower()]
            if matching:
                text = f"Found '{search_term}' in {len(matching)} lines:\n\n" + "\n".join(matching)

    max_length = 50000
    if len(text) > max_length:
        text = text[:max_length] + "\n\n[Content truncated]"
    return text
