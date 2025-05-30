import aiohttp
import asyncio
import json
import logging
from typing import Dict, List, Optional
import urllib.parse

logger = logging.getLogger(__name__)

class WebSearchTool:
    """Web search tool using DuckDuckGo Instant Answer API"""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.session = None
    
    async def search(self, query: str, max_results: int = 5) -> Dict:
        """Search the web for information"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # DuckDuckGo Instant Answer API
            encoded_query = urllib.parse.quote(query)
            url = f"{self.base_url}?q={encoded_query}&format=json&no_redirect=1&no_html=1&skip_disambig=1"
            
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._format_search_results(data, query)
                else:
                    return {"error": f"Search API returned status {response.status}"}
                    
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return {"error": str(e)}
    
    def _format_search_results(self, data: Dict, query: str) -> Dict:
        """Format DuckDuckGo results into a readable format"""
        results = {
            "query": query,
            "abstract": "",
            "related_topics": [],
            "infobox": {},
            "results": []
        }
        
        # Main abstract/answer
        if data.get("Abstract"):
            results["abstract"] = data["Abstract"]
            if data.get("AbstractSource"):
                results["abstract"] += f" (Source: {data['AbstractSource']})"
        
        # Infobox data
        if data.get("Infobox"):
            infobox = data["Infobox"]
            results["infobox"] = {
                "content": infobox.get("content", []),
                "meta": infobox.get("meta", [])
            }
        
        # Related topics
        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"][:3]:  # Limit to 3
                if isinstance(topic, dict) and topic.get("Text"):
                    results["related_topics"].append({
                        "text": topic["Text"],
                        "url": topic.get("FirstURL", "")
                    })
        
        # Instant answer
        if data.get("Answer"):
            results["instant_answer"] = {
                "text": data["Answer"],
                "type": data.get("AnswerType", ""),
                "source": data.get("AnswerSource", "")
            }
        
        return results
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()


class AdvancedWebSearchTool:
    """Advanced web search using multiple sources"""
    
    def __init__(self, serp_api_key: Optional[str] = None):
        self.serp_api_key = serp_api_key
        self.duckduckgo = WebSearchTool()
    
    async def comprehensive_search(self, query: str) -> Dict:
        """Perform comprehensive web search using multiple sources"""
        results = {
            "query": query,
            "sources": {},
            "summary": ""
        }
        
        # Try DuckDuckGo first (free)
        try:
            ddg_results = await self.duckduckgo.search(query)
            results["sources"]["duckduckgo"] = ddg_results
        except Exception as e:
            results["sources"]["duckduckgo"] = {"error": str(e)}
        
        # Try SerpAPI if available (requires API key)
        if self.serp_api_key:
            try:
                serp_results = await self._serp_search(query)
                results["sources"]["google"] = serp_results
            except Exception as e:
                results["sources"]["google"] = {"error": str(e)}
        
        # Create summary from available results
        results["summary"] = self._create_search_summary(results["sources"])
        
        return results
    
    async def _serp_search(self, query: str) -> Dict:
        """Search using SerpAPI (Google Search)"""
        if not self.serp_api_key:
            return {"error": "No SerpAPI key provided"}
        
        try:
            url = "https://serpapi.com/search.json"
            params = {
                "q": query,
                "api_key": self.serp_api_key,
                "num": 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_serp_results(data)
                    else:
                        return {"error": f"SerpAPI returned status {response.status}"}
                        
        except Exception as e:
            return {"error": str(e)}
    
    def _format_serp_results(self, data: Dict) -> Dict:
        """Format SerpAPI results"""
        results = {
            "organic_results": [],
            "answer_box": {},
            "knowledge_graph": {}
        }
        
        # Organic search results
        if data.get("organic_results"):
            for result in data["organic_results"][:5]:
                results["organic_results"].append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                })
        
        # Answer box (featured snippet)
        if data.get("answer_box"):
            answer_box = data["answer_box"]
            results["answer_box"] = {
                "answer": answer_box.get("answer", ""),
                "title": answer_box.get("title", ""),
                "link": answer_box.get("link", "")
            }
        
        # Knowledge graph
        if data.get("knowledge_graph"):
            kg = data["knowledge_graph"]
            results["knowledge_graph"] = {
                "title": kg.get("title", ""),
                "type": kg.get("type", ""),
                "description": kg.get("description", "")
            }
        
        return results
    
    def _create_search_summary(self, sources: Dict) -> str:
        """Create a summary from all search sources"""
        summary_parts = []
        
        # DuckDuckGo results
        ddg = sources.get("duckduckgo", {})
        if ddg.get("abstract"):
            summary_parts.append(f"Summary: {ddg['abstract']}")
        
        if ddg.get("instant_answer"):
            summary_parts.append(f"Quick Answer: {ddg['instant_answer']['text']}")
        
        # Google/SerpAPI results
        google = sources.get("google", {})
        if google.get("answer_box", {}).get("answer"):
            summary_parts.append(f"Featured Answer: {google['answer_box']['answer']}")
        
        if google.get("knowledge_graph", {}).get("description"):
            summary_parts.append(f"Knowledge: {google['knowledge_graph']['description']}")
        
        return " | ".join(summary_parts) if summary_parts else "No comprehensive summary available."
    
    async def close(self):
        """Close all connections"""
        await self.duckduckgo.close()


# Utility function for easy integration
async def quick_web_search(query: str, serp_api_key: Optional[str] = None) -> str:
    """Quick web search function that returns a formatted string"""
    search_tool = AdvancedWebSearchTool(serp_api_key)
    
    try:
        results = await search_tool.comprehensive_search(query)
        
        # Format for LLM consumption
        formatted_result = f"Search Results for '{query}':\n\n"
        
        if results["summary"]:
            formatted_result += f"Summary: {results['summary']}\n\n"
        
        # Add DuckDuckGo results
        ddg = results["sources"].get("duckduckgo", {})
        if ddg.get("related_topics"):
            formatted_result += "Related Information:\n"
            for topic in ddg["related_topics"]:
                formatted_result += f"- {topic['text']}\n"
        
        return formatted_result.strip()
        
    except Exception as e:
        return f"Search failed: {str(e)}"
    
    finally:
        await search_tool.close() 