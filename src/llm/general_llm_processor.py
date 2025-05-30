import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class GeneralLLMProcessor:
    """General-purpose LLM processor for conversational AI capabilities"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        self.conversation_history = []
        self.tools = {}
        self._register_tools()
        
        # Test connection
        if not self._test_connection():
            logger.warning("Could not connect to local LLM. Make sure Ollama is running.")
        else:
            logger.info(f"Connected to general LLM: {model_name}")
    
    def _test_connection(self) -> bool:
        """Test connection to local LLM"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Local LLM connection error: {e}")
            return False
    
    def _register_tools(self):
        """Register available tools for the LLM"""
        self.tools = {
            "web_search": {
                "description": "Search the web for current information",
                "parameters": ["query"],
                "function": self._web_search
            },
            "get_weather": {
                "description": "Get current weather information",
                "parameters": ["location"],
                "function": self._get_weather
            },
            "calculate": {
                "description": "Perform mathematical calculations",
                "parameters": ["expression"],
                "function": self._calculate
            },
            "get_time": {
                "description": "Get current date and time",
                "parameters": [],
                "function": self._get_time
            }
        }
    
    async def process_general_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process a general conversational query"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": query})
            
            # Create system prompt for general conversation
            system_prompt = self._create_general_system_prompt(context)
            
            # Build conversation context
            conversation_context = self._build_conversation_context()
            
            # Call LLM
            response = await self._call_general_llm(system_prompt, conversation_context, query)
            
            # Check if LLM wants to use tools
            tool_calls = self._extract_tool_calls(response)
            
            if tool_calls:
                # Execute tools and get results
                tool_results = await self._execute_tools(tool_calls)
                
                # Call LLM again with tool results
                enhanced_prompt = f"{system_prompt}\n\nTool results: {json.dumps(tool_results)}\n\nNow provide a comprehensive response to the user."
                response = await self._call_general_llm(enhanced_prompt, conversation_context, query)
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return {
                "success": True,
                "response": response,
                "tool_calls": tool_calls if tool_calls else [],
                "conversation_length": len(self.conversation_history)
            }
            
        except Exception as e:
            logger.error(f"Error processing general query: {e}")
            return {
                "success": False,
                "response": "I encountered an error processing your request. Could you try rephrasing it?",
                "error": str(e)
            }
    
    def _create_general_system_prompt(self, context: Optional[Dict] = None) -> str:
        """Create system prompt for general conversation"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        tools_desc = "\n".join([
            f"- {name}: {info['description']} (parameters: {', '.join(info['parameters']) if info['parameters'] else 'none'})"
            for name, info in self.tools.items()
        ])
        
        context_info = ""
        if context:
            context_info = f"\nContext: {json.dumps(context, indent=2)}"
        
        return f"""You are Totoro, a helpful AI assistant. You have access to tools and can help with a wide variety of tasks.

Current time: {current_time}
{context_info}

Available tools:
{tools_desc}

Instructions:
1. Engage in natural, helpful conversation
2. Use tools when you need current information or specific capabilities
3. To use a tool, include: TOOL_CALL: tool_name(parameter1="value1", parameter2="value2")
4. Be honest about your limitations
5. Provide accurate, helpful responses
6. Ask clarifying questions when needed

Examples of tool usage:
- For current events: TOOL_CALL: web_search(query="latest news about topic")
- For weather: TOOL_CALL: get_weather(location="New York")
- For math: TOOL_CALL: calculate(expression="15 * 23 + 45")
- For time: TOOL_CALL: get_time()

Remember: You are knowledgeable but not omniscient. Use tools for current information."""
    
    def _build_conversation_context(self) -> str:
        """Build conversation context from history"""
        if not self.conversation_history:
            return ""
        
        context = "Conversation history:\n"
        for msg in self.conversation_history[-6:]:  # Last 3 exchanges
            role = msg["role"].title()
            content = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
            context += f"{role}: {content}\n"
        
        return context
    
    async def _call_general_llm(self, system_prompt: str, context: str, user_query: str) -> str:
        """Call LLM for general conversation"""
        try:
            full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_query}\nAssistant:"
            
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,  # Higher for more creative responses
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "").strip()
                    else:
                        raise Exception(f"HTTP {response.status}")
                        
        except Exception as e:
            logger.error(f"General LLM API error: {e}")
            raise
    
    def _extract_tool_calls(self, response: str) -> List[Dict]:
        """Extract tool calls from LLM response"""
        import re
        
        tool_pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        matches = re.findall(tool_pattern, response)
        
        tool_calls = []
        for tool_name, params_str in matches:
            if tool_name in self.tools:
                # Parse parameters
                params = {}
                if params_str.strip():
                    # Simple parameter parsing (could be enhanced)
                    param_pairs = re.findall(r'(\w+)="([^"]*)"', params_str)
                    params = dict(param_pairs)
                
                tool_calls.append({
                    "tool": tool_name,
                    "parameters": params
                })
        
        return tool_calls
    
    async def _execute_tools(self, tool_calls: List[Dict]) -> Dict[str, Any]:
        """Execute tool calls and return results"""
        results = {}
        
        for call in tool_calls:
            tool_name = call["tool"]
            parameters = call["parameters"]
            
            try:
                if tool_name in self.tools:
                    func = self.tools[tool_name]["function"]
                    if asyncio.iscoroutinefunction(func):
                        result = await func(**parameters)
                    else:
                        result = func(**parameters)
                    results[tool_name] = result
                else:
                    results[tool_name] = f"Unknown tool: {tool_name}"
                    
            except Exception as e:
                results[tool_name] = f"Error: {str(e)}"
        
        return results
    
    # Tool implementations
    async def _web_search(self, query: str) -> str:
        """Search the web for information"""
        try:
            # This is a placeholder - you'd integrate with a real search API
            # Options: DuckDuckGo API, SerpAPI, Bing Search API, etc.
            
            # For demo, return a simulated response
            return f"Web search for '{query}': This is a placeholder. To implement real web search, integrate with DuckDuckGo API, SerpAPI, or similar service."
            
        except Exception as e:
            return f"Web search failed: {str(e)}"
    
    async def _get_weather(self, location: str) -> str:
        """Get weather information"""
        try:
            # Placeholder - integrate with OpenWeatherMap, WeatherAPI, etc.
            return f"Weather for {location}: This is a placeholder. To implement real weather, get an API key from OpenWeatherMap or similar service."
            
        except Exception as e:
            return f"Weather lookup failed: {str(e)}"
    
    def _calculate(self, expression: str) -> str:
        """Perform safe mathematical calculations"""
        try:
            # Safe evaluation of mathematical expressions
            import ast
            import operator
            
            # Allowed operations
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.USub: operator.neg,
            }
            
            def eval_expr(node):
                if isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.BinOp):
                    return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
                elif isinstance(node, ast.UnaryOp):
                    return ops[type(node.op)](eval_expr(node.operand))
                else:
                    raise TypeError(node)
            
            result = eval_expr(ast.parse(expression, mode='eval').body)
            return str(result)
            
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def _get_time(self) -> str:
        """Get current date and time"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        return {
            "message_count": len(self.conversation_history),
            "tools_available": list(self.tools.keys()),
            "last_messages": self.conversation_history[-4:] if self.conversation_history else []
        } 