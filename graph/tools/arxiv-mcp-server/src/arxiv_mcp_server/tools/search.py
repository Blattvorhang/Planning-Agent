"""Search functionality for the arXiv MCP server."""

import arxiv
import json
from typing import Dict, Any, List
from datetime import datetime, timezone
from dateutil import parser
import mcp.types as types
from ..config import Settings

settings = Settings()

search_tool = types.Tool(
    name="search_papers",
    description="Search for papers on arXiv with advanced filtering",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "max_results": {"type": "integer"},
            "date_from": {"type": "string"},
            "date_to": {"type": "string"},
            "categories": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["query"],
    },
)


def _is_within_date_range(
    date: datetime, start: datetime | None, end: datetime | None
) -> bool:
    """Check if a date falls within the specified range."""
    if start and not start.tzinfo:
        start = start.replace(tzinfo=timezone.utc)
    if end and not end.tzinfo:
        end = end.replace(tzinfo=timezone.utc)

    if start and date < start:
        return False
    if end and date > end:
        return False
    return True


def _process_paper(paper: arxiv.Result) -> Dict[str, Any]:
    """Process paper information with resource URI."""
    return {
        "id": paper.get_short_id(),
        "title": paper.title,
        "authors": [author.name for author in paper.authors],
        "abstract": paper.summary,
        "categories": paper.categories,
        "published": paper.published.isoformat(),
        "url": paper.pdf_url,
        "resource_uri": f"arxiv://{paper.get_short_id()}",
    }


async def handle_search(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle paper search requests."""
    try:
        client = arxiv.Client()
        max_results = min(int(arguments.get("max_results", 10)), settings.MAX_RESULTS)

        # Build search query with category filtering
        query = arguments["query"]
        if categories := arguments.get("categories"):
            category_filter = " OR ".join(f"cat:{cat}" for cat in categories)
            query = f"({query}) AND ({category_filter})"

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        # Process results with date filtering
        results = []
        try:
            date_from = (
                parser.parse(arguments["date_from"]).replace(tzinfo=timezone.utc)
                if "date_from" in arguments
                else None
            )
            date_to = (
                parser.parse(arguments["date_to"]).replace(tzinfo=timezone.utc)
                if "date_to" in arguments
                else None
            )
        except (ValueError, TypeError) as e:
            return [
                types.TextContent(
                    type="text", text=f"Error: Invalid date format - {str(e)}"
                )
            ]

        for paper in client.results(search):
            if _is_within_date_range(paper.published, date_from, date_to):
                results.append(_process_paper(paper))

            if len(results) >= max_results:
                break

        response_data = {"total_results": len(results), "papers": results}

        return [
            types.TextContent(type="text", text=json.dumps(response_data, indent=2))
        ]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]
