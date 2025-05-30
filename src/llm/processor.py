import logging
import datetime
from .unified_processor import UnifiedLLMProcessor
import config

logger = logging.getLogger(__name__)

class LLMProcessor:
    """Main LLM processor that handles all queries"""
    
    def __init__(self):
        # Use the unified processor by default
        self.processor = UnifiedLLMProcessor(
            model_name=getattr(config, 'OLLAMA_MODEL', 'llama3.1:8b'),
            base_url=getattr(config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        )
        logger.info("LLM processor initialized with unified backend")
    
    def process_query(self, query: str) -> str:
        """Process any type of query"""
        try:
            # Handle simple time queries directly
            if 'time' in query.lower() and ('what' in query.lower() or 'current' in query.lower()):
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                return f"The current time is {current_time}."
            
            # Use the unified processor for other queries
            result = self.processor.process_command(query, current_room="living room")
            
            if hasattr(result, 'response'):
                return result.response
            else:
                return str(result)
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return "I'm sorry, I'm having trouble processing that request right now." 