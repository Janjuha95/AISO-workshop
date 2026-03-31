import base64
import mimetypes
import os

import chess
from stockfish import Stockfish
from google import genai

STOCKFISH_PATH = r"C:\Users\sarth\stockfish_dir\stockfish\stockfish-windows-x86-64-avx2.exe"

FEN_EXTRACTION_PROMPT = """You are a chess grandmaster and expert at reading chess diagrams.

TASK: Convert this chess board image to a FEN string.

STEP 1 - BOARD ORIENTATION:
Look at the coordinate labels on the board edges.
- Numbers on the side: which rank is at top vs bottom?
- Letters on the bottom/top: which file is on left vs right?
- If rank 1 is at top and h-file is on the left, the board is from Black's perspective.
- ALWAYS convert to standard coordinates where a1 = White's bottom-left, h8 = White's top-right.

STEP 2 - IDENTIFY EVERY PIECE:
Go through each square systematically. For each occupied square state:
- The square in standard algebraic notation (e.g., e4)
- The piece type (King, Queen, Rook, Bishop, Knight, Pawn)
- The color (White=light colored pieces, Black=dark colored pieces)

Piece shapes:
- King: cross on top, tallest
- Queen: crown/coronet, second tallest
- Rook: battlements/castle tower shape
- Bishop: pointed diagonal-cut top (miter)
- Knight: horse head
- Pawn: small, round head

STEP 3 - BUILD FEN:
Construct the FEN rank by rank from rank 8 to rank 1.
Use: K Q R B N P for White, k q r b n p for Black.
Digits for empty squares.

{turn_info}
No castling rights: "-"
No en passant: "-"
Halfmove clock: 0, Fullmove: 1

STEP 4 - OUTPUT:
On the very last line, output ONLY the complete FEN string, nothing else."""


def chess_best_move(image_path: str, active_color: str) -> str:
    """Analyze a chess board image and find the best move using Stockfish.

    Use this tool when asked to find the best chess move from a board image.
    It reads the image, extracts the position, and computes the best move.

    Args:
        image_path: Path to the chess board image file.
        active_color: Whose turn it is to move: "white" or "black".

    Returns:
        The best move in standard algebraic notation (e.g. "Rd5", "Nf3").
    """
    turn_char = "b" if active_color.lower() == "black" else "w"
    turn_info = f"The side to move is {active_color} ('{turn_char}' in FEN)."

    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/png"

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    models = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-pro"]
    valid_fens = []

    for i, model in enumerate(models):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[{
                    "parts": [
                        {"inline_data": {"mime_type": mime_type, "data": image_data}},
                        {"text": FEN_EXTRACTION_PROMPT.format(turn_info=turn_info)},
                    ]
                }],
            )

            lines = response.text.strip().split("\n")
            fen_candidate = lines[-1].strip().strip("`").strip()

            board = chess.Board(fen_candidate)
            if board.is_valid():
                valid_fens.append(fen_candidate)
        except (ValueError, Exception):
            continue

    if not valid_fens:
        return "Error: Could not extract a valid FEN from the image."

    # Use the most common FEN, or the first valid one
    best_fen = max(set(valid_fens), key=valid_fens.count)

    sf = Stockfish(STOCKFISH_PATH, depth=25)
    sf.set_fen_position(best_fen)
    best_move_uci = sf.get_best_move()

    board = chess.Board(best_fen)
    move = chess.Move.from_uci(best_move_uci)
    san = board.san(move)
    return san
