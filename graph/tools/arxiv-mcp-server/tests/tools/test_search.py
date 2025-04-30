"""Tests for paper search functionality."""

import pytest
import json
from unittest.mock import patch
from arxiv_mcp_server.tools import handle_search


@pytest.mark.asyncio
async def test_basic_search(mock_client):
    """Test basic paper search functionality."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search({"query": "test query", "max_results": 1})

        assert len(result) == 1
        content = json.loads(result[0].text)
        assert content["total_results"] == 1
        paper = content["papers"][0]
        assert paper["id"] == "2103.12345"
        assert paper["title"] == "Test Paper"
        assert "resource_uri" in paper


@pytest.mark.asyncio
async def test_search_with_categories(mock_client):
    """Test paper search with category filtering."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {"query": "test query", "categories": ["cs.AI", "cs.LG"], "max_results": 1}
        )

        content = json.loads(result[0].text)
        assert content["papers"][0]["categories"] == ["cs.AI", "cs.LG"]


@pytest.mark.asyncio
async def test_search_with_dates(mock_client):
    """Test paper search with date filtering."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {
                "query": "test query",
                "date_from": "2022-01-01",
                "date_to": "2024-01-01",
                "max_results": 1,
            }
        )

        content = json.loads(result[0].text)
        assert content["total_results"] == 1
        assert len(content["papers"]) == 1


@pytest.mark.asyncio
async def test_search_with_invalid_dates(mock_client):
    """Test search with invalid date formats."""
    with patch("arxiv.Client", return_value=mock_client):
        result = await handle_search(
            {"query": "test query", "date_from": "invalid-date", "max_results": 1}
        )

        assert result[0].text.startswith("Error: Invalid date format")
