from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

mcp = FastMCP("WebSearch")

@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web for information.
    
    Args:
        query: The search query
        
    Returns:
        Search results as a string
    """
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            
        if not results:
            return "No results found."
        
        formatted_results = "\n\n".join(
            f"Title: {r.get('title', 'No title')}\n"
            f"URL: {r.get('href', 'No URL')}\n"
            f"Description: {r.get('body', 'No description')}"
            for r in results
        )
        return f"Search results for '{query}':\n{formatted_results}"
    except Exception as e:
        return f"Error performing search: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
