#!/usr/bin/env python3
"""Generate the GitHub-safe, no-JavaScript chess simulation SVG."""

from __future__ import annotations

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPOSITORY_ROOT / "assets" / "chess-board.svg"
BOARD_X = 56
BOARD_Y = 104
SQUARE = 64
KEY_TIMES = "0;0.125;0.25;0.375;0.5;0.625;0.75;1"

STATES = [
    {
        "label": "START POSITION",
        "turn": "WHITE",
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "highlight": None,
        "values": "1;0;0;0;0;0;0;0",
    },
    {
        "label": "1. e4",
        "turn": "BLACK",
        "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        "highlight": ("e2", "e4"),
        "values": "0;1;0;0;0;0;0;0",
    },
    {
        "label": "1... e5",
        "turn": "WHITE",
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2",
        "highlight": ("e7", "e5"),
        "values": "0;0;1;0;0;0;0;0",
    },
    {
        "label": "2. Nf3",
        "turn": "BLACK",
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
        "highlight": ("g1", "f3"),
        "values": "0;0;0;1;0;0;0;0",
    },
    {
        "label": "2... Nc6",
        "turn": "WHITE",
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
        "highlight": ("b8", "c6"),
        "values": "0;0;0;0;1;0;0;0",
    },
    {
        "label": "3. Bc4",
        "turn": "BLACK",
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
        "highlight": ("f1", "c4"),
        "values": "0;0;0;0;0;1;0;0",
    },
    {
        "label": "3... Bc5",
        "turn": "WHITE",
        "fen": "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        "highlight": ("f8", "c5"),
        "values": "0;0;0;0;0;0;1;1",
    },
]

PIECE_IDS = {
    "K": "wK", "Q": "wQ", "R": "wR", "B": "wB", "N": "wN", "P": "wP",
    "k": "bK", "q": "bQ", "r": "bR", "b": "bB", "n": "bN", "p": "bP",
}


def square_rect(square: str) -> tuple[int, int]:
    file_index = ord(square[0]) - ord("a")
    rank = int(square[1])
    return BOARD_X + file_index * SQUARE, BOARD_Y + (8 - rank) * SQUARE


def pieces_from_fen(fen: str) -> list[tuple[str, int, int]]:
    pieces: list[tuple[str, int, int]] = []
    rows = fen.split()[0].split("/")
    for rank_index, row in enumerate(rows):
        file_index = 0
        for token in row:
            if token.isdigit():
                file_index += int(token)
                continue
            x = BOARD_X + file_index * SQUARE + SQUARE // 2
            y = BOARD_Y + rank_index * SQUARE + SQUARE // 2
            pieces.append((PIECE_IDS[token], x, y))
            file_index += 1
        if file_index != 8:
            raise ValueError(f"Invalid FEN row: {row}")
    return pieces


def animate(values: str) -> str:
    return (
        f'<animate attributeName="opacity" dur="16s" repeatCount="indefinite" '
        f'calcMode="discrete" keyTimes="{KEY_TIMES}" values="{values}"/>'
    )


def board_state(index: int, state: dict[str, object]) -> str:
    base_opacity = "1" if index == 0 else "0"
    parts = [
        f'    <g id="state-{index}" class="board-state" opacity="{base_opacity}" data-fen="{state["fen"]}" aria-label="{state["label"]}">',
        f'      {animate(str(state["values"]))}',
    ]
    highlight = state["highlight"]
    if highlight:
        origin, destination = highlight
        ox, oy = square_rect(origin)
        dx, dy = square_rect(destination)
        parts.extend(
            [
                f'      <rect class="origin" x="{ox}" y="{oy}" width="64" height="64"/>',
                f'      <rect class="destination" x="{dx}" y="{dy}" width="64" height="64"/>',
            ]
        )
    for piece_id, x, y in pieces_from_fen(str(state["fen"])):
        parts.append(f'      <use href="#{piece_id}" transform="translate({x} {y})"/>')
    parts.append("    </g>")
    return "\n".join(parts)


def current_move(index: int, state: dict[str, object]) -> str:
    base_opacity = "1" if index == 0 else "0"
    return "\n".join(
        [
            f'      <g id="move-{index}" opacity="{base_opacity}">',
            f'        {animate(str(state["values"]))}',
            f'        <text x="146" y="203" fill="#00f5ff" font-size="17" font-weight="700">{state["label"]}</text>',
            f'        <text x="494" y="203" text-anchor="end" fill="#e6edf3" font-size="14">{state["turn"]} TO MOVE</text>',
            "      </g>",
        ]
    )


def history_highlight(index: int, state: dict[str, object]) -> str:
    if index == 0:
        return ""
    ply = index - 1
    row = ply // 2
    column = ply % 2
    x = 88 if column == 0 else 258
    y = 62 + row * 30
    return "\n".join(
        [
            f'      <rect id="history-{index}" x="{x}" y="{y}" width="164" height="26" rx="2" fill="#39ff14" fill-opacity=".14" opacity="0" stroke="#39ff14">',
            f'        {animate(str(state["values"]))}',
            "      </rect>",
        ]
    )


def render() -> str:
    states = "\n".join(board_state(i, state) for i, state in enumerate(STATES))
    moves = "\n".join(current_move(i, state) for i, state in enumerate(STATES))
    history = "\n".join(history_highlight(i, state) for i, state in enumerate(STATES) if i)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="0 0 1200 650" role="img" aria-labelledby="title desc">
  <title id="title">Italian Game chess simulation</title>
  <desc id="desc">A legal 16-second chess loop plays e4, e5, Nf3, Nc6, Bc4, and Bc5, then pauses before restarting.</desc>
  <defs>
    <pattern id="hud-grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#163326" opacity=".22"/></pattern>
    <pattern id="board" width="128" height="128" patternUnits="userSpaceOnUse"><rect width="128" height="128" fill="#0c1411"/><rect width="64" height="64" fill="#182620"/><rect x="64" y="64" width="64" height="64" fill="#182620"/></pattern>
    <linearGradient id="silver" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#f4f7f5"/><stop offset=".58" stop-color="#c5d0ca"/><stop offset="1" stop-color="#7f9188"/></linearGradient>
    <filter id="glow" x="-35%" y="-35%" width="170%" height="170%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <g id="wK"><text class="white-piece">♔</text></g><g id="wQ"><text class="white-piece">♕</text></g><g id="wR"><text class="white-piece">♖</text></g><g id="wB"><text class="white-piece">♗</text></g><g id="wN"><text class="white-piece">♘</text></g><g id="wP"><text class="white-piece">♙</text></g>
    <g id="bK"><text class="black-piece">♚</text></g><g id="bQ"><text class="black-piece">♛</text></g><g id="bR"><text class="black-piece">♜</text></g><g id="bB"><text class="black-piece">♝</text></g><g id="bN"><text class="black-piece">♞</text></g><g id="bP"><text class="black-piece">♟</text></g>
  </defs>
  <style>
    .mono{{font-family:Consolas,Menlo,monospace}}.label{{font:12px Consolas,Menlo,monospace;letter-spacing:2px;fill:#6b7280}}.value{{font:16px Consolas,Menlo,monospace;fill:#e6edf3}}.white-piece,.black-piece{{font-family:"DejaVu Sans","Segoe UI Symbol","Noto Sans Symbols 2",serif;font-size:48px;text-anchor:middle;dominant-baseline:central;paint-order:stroke fill}}.white-piece{{fill:url(#silver);stroke:#43564d;stroke-width:.8}}.black-piece{{fill:#07100b;stroke:#00f5ff;stroke-width:1.25}}.coord{{font:15px Consolas,Menlo,monospace;fill:#6b7280}}.origin{{fill:#a855f7;fill-opacity:.2;stroke:#a855f7;stroke-width:2}}.destination{{fill:#39ff14;fill-opacity:.18;stroke:#39ff14;stroke-width:2;filter:url(#glow)}}
  </style>

  <rect width="1200" height="650" rx="4" fill="#050805"/>
  <rect x="1" y="1" width="1198" height="648" rx="4" fill="none" stroke="#1d3d29"/>
  <rect width="1200" height="650" fill="url(#hud-grid)"/>
  <path d="M20 72V20h52M1128 20h52v52M20 578v52h52M1128 630h52v-52" fill="none" stroke="#39ff14" stroke-width="2" opacity=".72"/>

  <g class="mono">
    <text x="42" y="47" fill="#39ff14" font-size="16" letter-spacing="2">03 // CHESS SIMULATION</text>
    <text x="1158" y="47" text-anchor="end" fill="#6b7280" font-size="12">ITALIAN GAME // 16S LOOP</text>
  </g>
  <path d="M42 62h1116" stroke="#173b27"/>

  <g aria-label="Animated chess board, White at the bottom">
    <rect x="56" y="104" width="512" height="512" fill="url(#board)" stroke="#28573a" stroke-width="2"/>
    <g class="coord" text-anchor="middle">
      <text x="38" y="141">8</text><text x="38" y="205">7</text><text x="38" y="269">6</text><text x="38" y="333">5</text><text x="38" y="397">4</text><text x="38" y="461">3</text><text x="38" y="525">2</text><text x="38" y="589">1</text>
      <text x="88" y="639">a</text><text x="152" y="639">b</text><text x="216" y="639">c</text><text x="280" y="639">d</text><text x="344" y="639">e</text><text x="408" y="639">f</text><text x="472" y="639">g</text><text x="536" y="639">h</text>
    </g>
{states}
    <path d="M56 122v-18h18M550 104h18v18M56 598v18h18M550 616h18v-18" fill="none" stroke="#00f5ff" opacity=".65"/>
  </g>

  <g transform="translate(610 96)" class="mono">
    <rect width="550" height="520" fill="#070b08" stroke="#20452d"/>
    <path d="M0 18V0h18M532 0h18v18M0 502v18h18M532 520h18v-18" fill="none" stroke="#39ff14" opacity=".65"/>

    <g transform="translate(18 18)">
      <rect width="166" height="68" fill="#08110b" stroke="#28573a"/><text class="label" x="13" y="23">PLAYER</text><text x="13" y="49" fill="#39ff14" font-size="15">PUNEET-2005</text>
      <rect x="174" width="190" height="68" fill="#071216" stroke="#17515a"/><text class="label" x="187" y="23">OPENING</text><text x="187" y="49" fill="#00f5ff" font-size="15">ITALIAN GAME</text>
      <rect x="372" width="142" height="68" fill="#0c1a10" stroke="#28573a"/><text class="label" x="385" y="23">STATE</text>
      <g opacity="1"><animate attributeName="opacity" dur="16s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.875;1" values="1;0;0"/><circle cx="388" cy="47" r="4" fill="#39ff14"/><text x="401" y="52" fill="#39ff14" font-size="14">SIMULATING</text></g>
      <g opacity="0"><animate attributeName="opacity" dur="16s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.875;1" values="0;1;1"/><circle cx="388" cy="47" r="4" fill="#a855f7"/><text x="401" y="52" fill="#a855f7" font-size="14">PAUSE</text></g>
    </g>

    <text x="18" y="119" fill="#39ff14" font-size="15" letter-spacing="2">CHESS // STRATEGY MODULE</text>
    <path d="M18 132h514" stroke="#173b27"/>
    <text x="18" y="164" fill="#e6edf3" font-size="22" font-weight="700">CALCULATE.</text>
    <text x="190" y="164" fill="#00f5ff" font-size="22" font-weight="700">ADAPT.</text>
    <text x="310" y="164" fill="#a855f7" font-size="22" font-weight="700">EXECUTE.</text>
    <text x="18" y="190" fill="#9aa4b2" font-size="13">Plan ahead // weigh trade-offs // adapt under pressure.</text>

    <g transform="translate(18 202)">
      <rect width="514" height="228" fill="#050805" stroke="#20452d"/>
      <text x="18" y="27" fill="#00f5ff" font-size="13" letter-spacing="2">MOVE TERMINAL</text>
      <text x="494" y="27" text-anchor="end" fill="#6b7280" font-size="11">WHITE AT BOTTOM</text>
      <path d="M18 39h478" stroke="#173b27"/>
      <text class="label" x="20" y="57">NO.</text><text class="label" x="105" y="57">WHITE</text><text class="label" x="285" y="57">BLACK</text>
{history}
      <g fill="#e6edf3" font-size="15">
        <text x="20" y="82" fill="#6b7280">01</text><text x="105" y="82">e4</text><text x="285" y="82">e5</text>
        <text x="20" y="112" fill="#6b7280">02</text><text x="105" y="112">Nf3</text><text x="285" y="112">Nc6</text>
        <text x="20" y="142" fill="#6b7280">03</text><text x="105" y="142">Bc4</text><text x="285" y="142">Bc5</text>
      </g>
      <path d="M18 158h478" stroke="#173b27"/>
      <text class="label" x="18" y="183">CURRENT</text>
{moves}
    </g>

    <g transform="translate(18 448)">
      <rect width="160" height="52" fill="#08110b" stroke="#20452d"/><text class="label" x="12" y="21">BOARD</text><text class="value" x="12" y="43">8 × 8</text>
      <rect x="168" width="168" height="52" fill="#08110b" stroke="#20452d"/><text class="label" x="180" y="21">ENGINE</text><text class="value" x="180" y="43">HUMAN</text>
      <rect x="344" width="170" height="52" fill="#08110b" stroke="#20452d"/><text class="label" x="356" y="21">LOOP</text><text x="356" y="43" fill="#39ff14" font-size="16">ACTIVE // 16S</text>
    </g>
  </g>
</svg>
'''


if __name__ == "__main__":
    OUTPUT.write_text(render(), encoding="utf-8", newline="\n")
    print(f"Rendered {OUTPUT}")
