from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import arxiv

mcp = FastMCP("ResearchPapers")

@mcp.tool()
async def search_papers(query: str, max_results: int = 3) -> str:
    """Search for research papers on ArXiv.
    
    Args:
        query: Search query for papers
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        Formatted string with paper information
    """
    try:
        # Search for papers
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        results = []
        for result in search.results():
            # Format authors
            authors = ", ".join(author.name for author in result.authors)
            if len(authors) > 100:  # Truncate long author lists
                authors = authors[:100] + "..."
                
            # Format the result
            paper_info = (
                f"Title: {result.title}\n"
                f"Authors: {authors}\n"
                f"Published: {result.published.strftime('%Y-%m-%d')}\n"
                f"Summary: {result.summary[:200]}...\n"
                f"URL: {result.pdf_url}"
            )
            results.append(paper_info)
        
        if not results:
            return "No papers found matching your query."
            
        return "\n\n" + "\n" + "-"*80 + "\n".join(results)
        
    except Exception as e:
        return f"Error searching for papers: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
