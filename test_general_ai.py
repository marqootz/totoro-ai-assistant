#!/usr/bin/env python3
"""
Test script for general AI assistant capabilities
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from llm.general_llm_processor import GeneralLLMProcessor
from tools.web_search import quick_web_search
from tools.knowledge_base import SimpleKnowledgeBase, RAGSystem

async def test_general_conversation():
    """Test general conversation capabilities"""
    print("🤖 Testing General AI Conversation Capabilities")
    print("=" * 60)
    
    # Initialize general LLM processor
    processor = GeneralLLMProcessor()
    
    # Test queries that require different capabilities
    test_queries = [
        "What's the weather like in Tokyo today?",
        "Can you calculate 15 * 23 + 45 / 3?",
        "Tell me about quantum computing",
        "What time is it right now?",
        "Explain the difference between machine learning and AI",
        "Search for the latest news about electric vehicles"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: {query}")
        print("-" * 40)
        
        try:
            result = await processor.process_general_query(query)
            
            if result["success"]:
                print(f"✅ Response: {result['response']}")
                if result["tool_calls"]:
                    print(f"🔧 Tools used: {[call['tool'] for call in result['tool_calls']]}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

async def test_web_search():
    """Test web search capabilities"""
    print("\n🌐 Testing Web Search Capabilities")
    print("=" * 60)
    
    search_queries = [
        "latest AI developments 2024",
        "Python programming best practices",
        "climate change news"
    ]
    
    for query in search_queries:
        print(f"\nSearching: {query}")
        print("-" * 40)
        
        try:
            result = await quick_web_search(query)
            print(f"✅ Search Result:\n{result}")
        except Exception as e:
            print(f"❌ Search failed: {e}")

def test_knowledge_base():
    """Test knowledge base and RAG capabilities"""
    print("\n📚 Testing Knowledge Base & RAG")
    print("=" * 60)
    
    # Create knowledge base
    kb = SimpleKnowledgeBase("test_knowledge")
    rag = RAGSystem(kb)
    
    # Add some sample documents
    sample_docs = [
        {
            "content": "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, and artificial intelligence.",
            "metadata": {"topic": "programming", "language": "python"}
        },
        {
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
            "metadata": {"topic": "ai", "subtopic": "machine_learning"}
        },
        {
            "content": "Climate change refers to long-term shifts in global temperatures and weather patterns. Human activities are the main driver of climate change since the 1800s.",
            "metadata": {"topic": "environment", "subtopic": "climate"}
        }
    ]
    
    # Add documents to knowledge base
    for doc in sample_docs:
        doc_id = kb.add_document(doc["content"], metadata=doc["metadata"])
        print(f"✅ Added document: {doc_id}")
    
    # Test knowledge retrieval
    test_queries = [
        "What is Python programming?",
        "Tell me about machine learning",
        "What causes climate change?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 30)
        
        # Get relevant context
        context = kb.get_context_for_query(query)
        print(f"📖 Retrieved context:\n{context}")
        
        # Test RAG enhancement
        base_prompt = "You are a helpful AI assistant."
        enhanced_prompt = rag.enhance_query_with_context(query, base_prompt)
        
        if "RELEVANT KNOWLEDGE BASE CONTEXT" in enhanced_prompt:
            print("✅ RAG enhancement successful")
        else:
            print("ℹ️ No relevant context found")

def compare_capabilities():
    """Compare current capabilities with Claude/ChatGPT"""
    print("\n📊 Capability Comparison")
    print("=" * 60)
    
    capabilities = {
        "Smart Home Control": {
            "Your System": "🟢 Excellent (10/10)",
            "Claude/ChatGPT": "🔴 Poor (2/10) - No device integration"
        },
        "Privacy": {
            "Your System": "🟢 Excellent (10/10) - Fully local",
            "Claude/ChatGPT": "🟡 Moderate (6/10) - Cloud-based"
        },
        "General Knowledge": {
            "Your System": "🟡 Good (7/10) - Training data cutoff",
            "Claude/ChatGPT": "🟢 Excellent (9/10) - Larger training data"
        },
        "Current Information": {
            "Your System": "🟡 Good (7/10) - With web search",
            "Claude/ChatGPT": "🟢 Excellent (9/10) - Built-in web access"
        },
        "Code Generation": {
            "Your System": "🟡 Good (7/10) - Depends on model",
            "Claude/ChatGPT": "🟢 Excellent (9/10) - Specialized training"
        },
        "Reasoning": {
            "Your System": "🟡 Good (7/10) - Model dependent",
            "Claude/ChatGPT": "🟢 Excellent (9/10) - Advanced reasoning"
        },
        "Cost": {
            "Your System": "🟢 Excellent (10/10) - Free after setup",
            "Claude/ChatGPT": "🟡 Moderate (6/10) - $5-20/month"
        },
        "Response Speed": {
            "Your System": "🟡 Good (7/10) - Hardware dependent",
            "Claude/ChatGPT": "🟢 Excellent (9/10) - Optimized servers"
        }
    }
    
    for capability, scores in capabilities.items():
        print(f"\n{capability}:")
        print(f"  Your System: {scores['Your System']}")
        print(f"  Claude/GPT:  {scores['Claude/ChatGPT']}")

def improvement_recommendations():
    """Provide recommendations for achieving Claude-like capabilities"""
    print("\n🚀 Recommendations for Claude-like Capabilities")
    print("=" * 60)
    
    recommendations = [
        {
            "area": "Model Upgrade",
            "current": "llama3.1:8b (2GB)",
            "recommended": "llama3.1:70b (40GB) or CodeLlama:34b",
            "benefit": "Better reasoning, code generation, general knowledge",
            "requirement": "64GB+ RAM"
        },
        {
            "area": "Fine-tuning",
            "current": "Base model",
            "recommended": "Fine-tune on conversation data",
            "benefit": "Better instruction following, personality",
            "requirement": "Training pipeline, quality data"
        },
        {
            "area": "Tool Integration",
            "current": "Basic tools (calc, time)",
            "recommended": "Advanced tools (code execution, file ops, APIs)",
            "benefit": "More capabilities, better problem solving",
            "requirement": "Tool development, safety measures"
        },
        {
            "area": "Knowledge Base",
            "current": "Simple word-frequency embeddings",
            "recommended": "Sentence transformers, vector DB",
            "benefit": "Better semantic search, more accurate retrieval",
            "requirement": "sentence-transformers library, ChromaDB"
        },
        {
            "area": "Prompt Engineering",
            "current": "Basic prompts",
            "recommended": "Advanced prompting techniques",
            "benefit": "Better responses, more consistent behavior",
            "requirement": "Prompt optimization, A/B testing"
        }
    ]
    
    for rec in recommendations:
        print(f"\n🎯 {rec['area']}")
        print(f"   Current: {rec['current']}")
        print(f"   Recommended: {rec['recommended']}")
        print(f"   Benefit: {rec['benefit']}")
        print(f"   Requirement: {rec['requirement']}")

async def main():
    """Run all tests"""
    print("🧪 Totoro General AI Capabilities Test")
    print("=" * 60)
    
    # Test general conversation
    await test_general_conversation()
    
    # Test web search
    await test_web_search()
    
    # Test knowledge base
    test_knowledge_base()
    
    # Compare capabilities
    compare_capabilities()
    
    # Provide recommendations
    improvement_recommendations()
    
    print("\n✅ Testing complete!")
    print("\n💡 Summary:")
    print("- Your system excels at smart home control (10/10)")
    print("- General AI capabilities are good (7/10) but can be improved")
    print("- Key advantages: Privacy, cost, customization")
    print("- Key improvements needed: Larger model, better tools, advanced RAG")

if __name__ == "__main__":
    asyncio.run(main()) 