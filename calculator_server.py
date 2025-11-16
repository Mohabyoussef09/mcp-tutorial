"""
Calculator MCP Server - Simple math operations
Demonstrates: Tools, Resources, and Prompts using FastMCP
"""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("calculator-server")

# ========== TOOLS ==========
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

# ========== RESOURCES ==========
@mcp.resource("calc://formulas")
def get_formulas() -> str:
    """Get common mathematical formulas"""
    return """
    Common Formulas:
    - Area of Circle: π × r²
    - Pythagorean: a² + b² = c²
    - Percentage: (part/whole) × 100
    """

@mcp.resource("calc://constants")
def get_constants() -> str:
    """Get mathematical constants"""
    return """
    Mathematical Constants:
    - π (Pi): 3.14159
    - e (Euler): 2.71828
    - φ (Golden Ratio): 1.61803
    """

# ========== PROMPTS ==========
@mcp.prompt()
def math_tutor() -> str:
    """A helpful math tutor prompt"""
    return "You are a friendly math tutor. Explain concepts clearly with examples."

@mcp.prompt()
def solve_word_problem(problem: str) -> str:
    """Help solve a math word problem"""
    return f"Solve this word problem step by step: {problem}"

# Run the server
if __name__ == "__main__":
    mcp.run()
