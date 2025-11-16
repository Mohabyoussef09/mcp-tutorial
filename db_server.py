"""
PostgreSQL MCP Server - Database operations
Demonstrates: Tools, Resources, and Prompts using FastMCP
"""

from mcp.server import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor

# Initialize FastMCP server
mcp = FastMCP("postgres-server")

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "database": <db_name>,
    "user": <db_user>,
    "password": <db_password>
}

# ========== TOOLS ==========
@mcp.tool()
def query_database(sql: str) -> str:
    """Execute a SQL query on PostgreSQL database"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)

        if sql.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            return str([dict(row) for row in results])
        else:
            conn.commit()
            return f"Success: {cursor.rowcount} rows affected"
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error: {str(e)}"
    finally:
        if conn:
            conn.close()

@mcp.tool()
def list_tables() -> str:
    """List all tables in the database"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        return f"Tables: {', '.join(tables)}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if conn:
            conn.close()

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Get the structure of a specific table"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        columns = [dict(row) for row in cursor.fetchall()]
        return str(columns)
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if conn:
            conn.close()

# ========== RESOURCES ==========
@mcp.resource("db://connection-info")
def get_connection_info() -> str:
    """Get database connection information"""
    return f"""
    Database Connection Info:
    - Host: {DB_CONFIG['host']}
    - Database: {DB_CONFIG['database']}
    - User: {DB_CONFIG['user']}
    """

@mcp.resource("db://common-queries")
def get_common_queries() -> str:
    """Get common SQL query examples"""
    return """
    Common SQL Queries:

    - List all records: SELECT * FROM table_name;
    - Count records: SELECT COUNT(*) FROM table_name;
    - Filter data: SELECT * FROM table_name WHERE column = 'value';
    - Insert data: INSERT INTO table_name (col1, col2) VALUES ('val1', 'val2');
    - Update data: UPDATE table_name SET col1 = 'new_val' WHERE id = 1;
    - Delete data: DELETE FROM table_name WHERE id = 1;
    """

# ========== PROMPTS ==========
@mcp.prompt()
def sql_assistant() -> str:
    """A helpful SQL query assistant"""
    return "You are a SQL expert. Help users write correct and efficient SQL queries for PostgreSQL."

@mcp.prompt()
def database_analyzer(table_name: str) -> str:
    """Analyze a database table"""
    return f"Analyze the '{table_name}' table structure and suggest optimizations or improvements."

# Run the server
if __name__ == "__main__":
    mcp.run()
