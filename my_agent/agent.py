"""
This file is where you will implement your agent.
The `root_agent` is used to evaluate your agent's performance.
"""

from google.adk.agents import llm_agent
from .tools.calculator import calculator
from .tools.read_pdf import read_pdf
from .tools.web_search import web_search
from .tools.fetch_webpage import fetch_webpage
from .tools.analyze_image import analyze_image
from .tools.chess_engine import chess_best_move

root_agent = llm_agent.Agent(
    model="gemini-2.5-pro",
    name="agent",
    description="A helpful assistant.",
    instruction=(
        "You are a research assistant. Return ONLY the final "
        "answer with no extra explanation or reasoning. "
        "Be precise: if asked for a setting name, give only "
        "the name, not the full heading.\n\n"
        "Tools:\n"
        "- calculator: all arithmetic\n"
        "- read_pdf: read local PDF files\n"
        "- web_search: find URLs and snippets. If first query "
        "returns insufficient results, refine and search again.\n"
        "- fetch_webpage: read full page text or download and "
        "extract PDFs from a URL. Use after web_search to get "
        "details from a result page.\n"
        "- analyze_image: when a question references an image "
        "file (.png, .jpg, .webp), use this with the file path "
        "and a specific question about what you need from the image.\n"
        "- chess_best_move: for chess positions, pass the image "
        "file path and whose turn it is ('white' or 'black'). "
        "It handles FEN extraction and move computation internally.\n\n"
        "Strategies:\n"
        "- Multi-step research: search, read the page, then "
        "search again with new details you learned. Repeat "
        "until you find the specific fact requested.\n"
        "- Bot detection: if fetch_webpage reports a page is "
        "blocked, skip that URL and try the next result from "
        "your search instead of retrying the same source.\n"
        "- Verification: for multi-step questions, cross-check "
        "key facts against a second source when possible "
        "before giving your final answer.\n"
        "- Files: when files are mentioned (e.g. 'Note: The "
        "following files are relevant: benchmark/attachments/7.pdf'), "
        "use read_pdf for .pdf files and analyze_image for "
        ".png/.jpg files with the exact path given."
    ),
    tools=[calculator, read_pdf, web_search, fetch_webpage, analyze_image, chess_best_move],
    sub_agents=[],
)
