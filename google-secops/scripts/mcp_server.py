#!/usr/bin/env python3
"""
Standard Stdio MCP Server template for Google SecOps.
This server implements the Model Context Protocol (MCP) using a standard-library-only
stdio JSON-RPC implementation so it runs out-of-the-box without requiring external packages.

You can also use the official Python MCP SDK by running:
    pip install mcp

And rewrite this using the official SDK (see commented code at the end of the file).
"""

import sys
import json
import traceback

# A simple logger that writes to stderr since stdout is used for JSON-RPC messages
def log(msg):
    sys.stderr.write(f"[google-secops-server] {msg}\n")
    sys.stderr.flush()

class StdioMCPServer:
    def __init__(self):
        self.tools = {
            "greet_user": {
                "name": "greet_user",
                "description": "Returns a warm greeting to a user by name.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the user to greet."
                        }
                    },
                    "required": ["name"]
                },
                "handler": self.tool_greet_user
            },
            "system_info": {
                "name": "system_info",
                "description": "Returns standard system and environment information for the plugin.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                },
                "handler": self.tool_system_info
            }
        }

    def tool_greet_user(self, arguments):
        name = arguments.get("name", "Developer")
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Hello, {name}! Welcome to the Google SecOps environment. Your plugin is running perfectly!"
                }
            ]
        }

    def tool_system_info(self, arguments):
        import platform
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Plugin: google-secops\nAuthor: Google Antigravity Developer\nOS: {platform.system()} {platform.release()}\nPython: {platform.python_version()}"
                }
            ]
        }

    def run(self):
        log("Stdio MCP Server starting...")
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                request = json.loads(line)
                self.handle_request(request)
            except json.JSONDecodeError:
                log("Error: Invalid JSON received")
            except Exception as e:
                log(f"Error: {str(e)}\n{traceback.format_exc()}")

    def send_response(self, response):
        raw = json.dumps(response)
        sys.stdout.write(raw + "\n")
        sys.stdout.flush()

    def handle_request(self, req):
        if "method" not in req:
            return

        method = req["method"]
        req_id = req.get("id")

        if method == "initialize":
            self.send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "google-secops-server",
                        "version": "0.1.0"
                    }
                }
            })
            log("Initialized successfully.")
        
        elif method == "notifications/initialized":
            log("Client confirmed initialization notification.")

        elif method == "tools/list":
            tools_list = [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "inputSchema": t["inputSchema"]
                }
                for t in self.tools.values()
            ]
            self.send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": tools_list
                }
            })
            log("Listed tools.")

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})

            if name in self.tools:
                log(f"Calling tool: {name}")
                try:
                    result = self.tools[name]["handler"](arguments)
                    self.send_response({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": result
                    })
                except Exception as err:
                    self.send_response({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32603,
                            "message": str(err)
                        }
                    })
            else:
                self.send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {name}"
                    }
                })

        elif method == "ping":
            self.send_response({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {}
            })

if __name__ == "__main__":
    server = StdioMCPServer()
    server.run()

"""
# =====================================================================
# ALTERNATIVE IMPLEMENTATION USING THE OFFICIAL PYTHON MCP SDK
# =====================================================================
# To use this approach, run:
#     pip install mcp
# Or with uv:
#     uv pip install mcp
#
# Then replace the script above with the code below:

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Google SecOps")

@mcp.tool()
def greet_user(name: str = "Developer") -> str:
    \"\"\"Returns a warm greeting to a user by name.\"\"\"
    return f"Hello, {name}! Welcome to the Google SecOps environment. Your plugin is running perfectly!"

@mcp.tool()
def system_info() -> str:
    \"\"\"Returns standard system and environment information for the plugin.\"\"\"
    import platform
    return f"Plugin: google-secops\\nAuthor: Google Antigravity Developer\\nOS: {platform.system()} {platform.release()}\\nPython: {platform.python_version()}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
"""
