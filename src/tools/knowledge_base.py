import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import pickle
import hashlib

logger = logging.getLogger(__name__)

class SimpleKnowledgeBase:
    """Simple in-memory knowledge base with semantic search capabilities"""
    
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(exist_ok=True)
        
        self.documents = {}  # document_id -> content
        self.embeddings = {}  # document_id -> embedding
        self.metadata = {}   # document_id -> metadata
        
        # Load existing knowledge
        self._load_knowledge_base()
    
    def add_document(self, content: str, doc_id: Optional[str] = None, metadata: Optional[Dict] = None) -> str:
        """Add a document to the knowledge base"""
        if doc_id is None:
            doc_id = self._generate_doc_id(content)
        
        self.documents[doc_id] = content
        self.metadata[doc_id] = metadata or {}
        
        # Generate simple embedding (word frequency based)
        self.embeddings[doc_id] = self._simple_embedding(content)
        
        # Save to disk
        self._save_document(doc_id, content, metadata)
        
        logger.info(f"Added document {doc_id} to knowledge base")
        return doc_id
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the knowledge base for relevant documents"""
        if not self.documents:
            return []
        
        query_embedding = self._simple_embedding(query)
        
        # Calculate similarity scores
        scores = []
        for doc_id, doc_embedding in self.embeddings.items():
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            scores.append((doc_id, similarity))
        
        # Sort by similarity and return top results
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in scores[:max_results]:
            if score > 0.1:  # Minimum relevance threshold
                results.append({
                    "doc_id": doc_id,
                    "content": self.documents[doc_id],
                    "metadata": self.metadata[doc_id],
                    "relevance_score": score
                })
        
        return results
    
    def get_context_for_query(self, query: str, max_length: int = 1000) -> str:
        """Get relevant context for a query"""
        results = self.search(query, max_results=3)
        
        if not results:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        current_length = 0
        
        for result in results:
            content = result["content"]
            if current_length + len(content) > max_length:
                # Truncate to fit
                remaining = max_length - current_length
                content = content[:remaining] + "..."
            
            context_parts.append(f"[Relevance: {result['relevance_score']:.2f}] {content}")
            current_length += len(content)
            
            if current_length >= max_length:
                break
        
        return "\n\n".join(context_parts)
    
    def _simple_embedding(self, text: str) -> Dict[str, float]:
        """Create a simple word frequency embedding"""
        words = text.lower().split()
        word_count = {}
        
        for word in words:
            # Basic cleaning
            word = ''.join(c for c in word if c.isalnum())
            if len(word) > 2:  # Skip very short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Normalize to create embedding
        total_words = sum(word_count.values())
        if total_words == 0:
            return {}
        
        return {word: count / total_words for word, count in word_count.items()}
    
    def _cosine_similarity(self, emb1: Dict[str, float], emb2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        if not emb1 or not emb2:
            return 0.0
        
        # Get common words
        common_words = set(emb1.keys()) & set(emb2.keys())
        if not common_words:
            return 0.0
        
        # Calculate dot product and magnitudes
        dot_product = sum(emb1[word] * emb2[word] for word in common_words)
        
        magnitude1 = sum(val ** 2 for val in emb1.values()) ** 0.5
        magnitude2 = sum(val ** 2 for val in emb2.values()) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _generate_doc_id(self, content: str) -> str:
        """Generate a unique document ID"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _save_document(self, doc_id: str, content: str, metadata: Optional[Dict]):
        """Save document to disk"""
        try:
            doc_file = self.knowledge_dir / f"{doc_id}.json"
            with open(doc_file, 'w') as f:
                json.dump({
                    "content": content,
                    "metadata": metadata or {},
                    "embedding": self.embeddings[doc_id]
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving document {doc_id}: {e}")
    
    def _load_knowledge_base(self):
        """Load existing knowledge base from disk"""
        try:
            for doc_file in self.knowledge_dir.glob("*.json"):
                doc_id = doc_file.stem
                
                with open(doc_file, 'r') as f:
                    data = json.load(f)
                
                self.documents[doc_id] = data["content"]
                self.metadata[doc_id] = data.get("metadata", {})
                self.embeddings[doc_id] = data.get("embedding", {})
                
            logger.info(f"Loaded {len(self.documents)} documents from knowledge base")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")


class DocumentProcessor:
    """Process various document types for the knowledge base"""
    
    @staticmethod
    def process_text_file(file_path: str) -> List[Dict]:
        """Process a text file into chunks"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks (simple sentence-based chunking)
            chunks = DocumentProcessor._chunk_text(content)
            
            return [{
                "content": chunk,
                "metadata": {
                    "source_file": file_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            } for i, chunk in enumerate(chunks)]
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []
    
    @staticmethod
    def _chunk_text(text: str, max_chunk_size: int = 500) -> List[str]:
        """Split text into manageable chunks"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += ". " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks


class RAGSystem:
    """Complete RAG (Retrieval Augmented Generation) system"""
    
    def __init__(self, knowledge_base: SimpleKnowledgeBase):
        self.kb = knowledge_base
    
    def enhance_query_with_context(self, query: str, system_prompt: str) -> str:
        """Enhance a query with relevant context from the knowledge base"""
        context = self.kb.get_context_for_query(query)
        
        if context and "No relevant information found" not in context:
            enhanced_prompt = f"""{system_prompt}

RELEVANT KNOWLEDGE BASE CONTEXT:
{context}

Use the above context to inform your response when relevant. If the context doesn't apply to the user's question, ignore it.

"""
            return enhanced_prompt
        
        return system_prompt
    
    def add_conversation_to_kb(self, user_query: str, assistant_response: str):
        """Add successful conversations to the knowledge base for future reference"""
        conversation = f"User: {user_query}\nAssistant: {assistant_response}"
        
        self.kb.add_document(
            conversation,
            metadata={
                "type": "conversation",
                "user_query": user_query,
                "timestamp": str(datetime.now())
            }
        )
    
    def load_documents_from_directory(self, directory: str) -> int:
        """Load all text documents from a directory"""
        directory_path = Path(directory)
        if not directory_path.exists():
            logger.warning(f"Directory {directory} does not exist")
            return 0
        
        count = 0
        for file_path in directory_path.glob("*.txt"):
            chunks = DocumentProcessor.process_text_file(str(file_path))
            
            for chunk in chunks:
                self.kb.add_document(
                    chunk["content"],
                    metadata=chunk["metadata"]
                )
                count += 1
        
        logger.info(f"Added {count} document chunks to knowledge base")
        return count


# Integration example
async def create_knowledge_enhanced_prompt(query: str, base_prompt: str, kb_path: str = "knowledge") -> str:
    """Create a knowledge-enhanced prompt for better LLM responses"""
    
    # Initialize RAG system
    kb = SimpleKnowledgeBase(kb_path)
    rag = RAGSystem(kb)
    
    # Enhance prompt with relevant context
    enhanced_prompt = rag.enhance_query_with_context(query, base_prompt)
    
    return enhanced_prompt 