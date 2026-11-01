"""Source citations for the local RAG chatbot.

The current ``embedchain`` ``query()`` call in ``application.py``
returns an answer string, not per-chunk page or section numbers.
So this module never invents a page number: it cites what is
actually known, which is the file name of each document in the
knowledge base. If a source record ever does provide a page or
section, ``format_citation`` includes it; otherwise it is omitted.
"""


def format_citation(sources):
    """Format one citation line from a list of source records.

    Each source is a dict with at least ``file``; ``page`` and
    ``section`` are optional and are only shown when present.
    Returns "" when there are no sources.
    """
    parts = []
    for s in sources or []:
        name = s.get("file") if isinstance(s, dict) else str(s)
        if not name:
            continue
        detail = name
        if isinstance(s, dict):
            if s.get("page") is not None:
                detail += f" (page {s['page']}"
                if s.get("section"):
                    detail += f", {s['section']}"
                detail += ")"
            elif s.get("section"):
                detail += f" ({s['section']})"
        parts.append(detail)
    if not parts:
        return ""
    return "Sources: " + "; ".join(parts)


def format_citation_text(files):
    """Citation line for a plain list of file names."""
    return format_citation([{"file": f} for f in files])
