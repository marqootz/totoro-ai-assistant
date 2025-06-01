#!/usr/bin/env python3
"""
Enhanced Totoro Server with Fluid Expression System Integration
Provides real-time emotion analysis and WebSocket communication for avatar expressions
"""

import asyncio
import json
import logging
import os
import sys
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import nltk
from textblob import TextBlob

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import existing Totoro components
try:
    from src.assistant import TotoroAssistant
    from src.config import Config
except ImportError:
    print("Warning: Could not import Totoro components. Running in demo mode.")
    TotoroAssistant = None
    Config = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'totoro_expression_secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global state
assistant = None
expression_state = {
    'current_emotion': 'neutral',
    'sentiment_history': [],
    'animation_queue': [],
    'performance_metrics': {
        'fps': 60,
        'animation_count': 0,
        'queue_length': 0
    }
}

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpressionAnalyzer:
    """Advanced emotion analysis for avatar expressions"""
    
    def __init__(self):
        self.emotion_keywords = {
            'happy': ['excited', 'amazing', 'fantastic', 'great', 'wonderful', 'love', 'perfect', 'awesome'],
            'sad': ['disappointed', 'sad', 'unfortunate', 'terrible', 'awful', 'bad', 'wrong', 'failed'],
            'surprised': ['wow', 'incredible', 'unexpected', 'shocking', 'amazing', 'unbelievable'],
            'thinking': ['think', 'consider', 'analyze', 'evaluate', 'hmm', 'maybe', 'perhaps', 'wondering'],
            'speaking': ['say', 'tell', 'explain', 'describe', 'mentioned', 'stated']
        }
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze text sentiment and determine appropriate emotion"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine emotion based on polarity and keywords
            emotion = self._determine_emotion(text, polarity)
            confidence = min(abs(polarity) + 0.3, 1.0)
            
            result = {
                'emotion': emotion,
                'confidence': confidence,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'text': text,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add to history
            expression_state['sentiment_history'].append(result)
            
            # Keep only last 50 entries
            if len(expression_state['sentiment_history']) > 50:
                expression_state['sentiment_history'] = expression_state['sentiment_history'][-50:]
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'emotion': 'neutral',
                'confidence': 0.1,
                'polarity': 0,
                'subjectivity': 0,
                'text': text,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _determine_emotion(self, text: str, polarity: float) -> str:
        """Determine emotion based on text content and polarity"""
        text_lower = text.lower()
        
        # Check for specific emotion keywords
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # If specific emotions detected, use the highest scoring one
        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            return dominant_emotion
        
        # Fall back to polarity-based classification
        if polarity > 0.3:
            return 'happy'
        elif polarity < -0.3:
            return 'sad'
        elif abs(polarity) > 0.1:
            return 'surprised'
        else:
            return 'neutral'

# Initialize expression analyzer
expression_analyzer = ExpressionAnalyzer()

@app.route('/')
def index():
    """Serve the enhanced avatar demo"""
    return send_from_directory('.', 'avatar-demo.html')

@app.route('/avatar-expression-system.js')
def avatar_system():
    """Serve the avatar expression system JS"""
    return send_from_directory('.', 'avatar-expression-system.js')

@app.route('/api/status')
def get_status():
    """Get current system status"""
    global assistant
    
    status = {
        'state': expression_state['current_emotion'],
        'assistant_available': assistant is not None,
        'timestamp': datetime.now().isoformat(),
        'performance_metrics': expression_state['performance_metrics'],
        'sentiment_history_length': len(expression_state['sentiment_history'])
    }
    
    if assistant:
        try:
            # Get assistant-specific status if available
            assistant_status = getattr(assistant, 'get_status', lambda: {})()
            status.update(assistant_status)
        except Exception as e:
            logger.error(f"Error getting assistant status: {e}")
    
    return jsonify(status)

@app.route('/api/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of provided text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        result = expression_analyzer.analyze_sentiment(text)
        
        # Emit to connected clients for real-time updates
        socketio.emit('sentiment_analysis', result)
        
        # Update current emotion if confidence is high enough
        if result['confidence'] > 0.5:
            expression_state['current_emotion'] = result['emotion']
            socketio.emit('emotion_change', {
                'emotion': result['emotion'],
                'confidence': result['confidence']
            })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/set_emotion', methods=['POST'])
def set_emotion():
    """Manually set avatar emotion"""
    try:
        data = request.get_json()
        emotion = data.get('emotion', 'neutral')
        immediate = data.get('immediate', False)
        
        valid_emotions = ['neutral', 'happy', 'sad', 'surprised', 'thinking', 'speaking']
        if emotion not in valid_emotions:
            return jsonify({'error': f'Invalid emotion. Must be one of: {valid_emotions}'}), 400
        
        expression_state['current_emotion'] = emotion
        
        # Emit to connected clients
        socketio.emit('manual_emotion_change', {
            'emotion': emotion,
            'immediate': immediate,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'immediate': immediate
        })
        
    except Exception as e:
        logger.error(f"Error setting emotion: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance_metrics')
def get_performance_metrics():
    """Get current performance metrics"""
    return jsonify(expression_state['performance_metrics'])

@app.route('/api/sentiment_history')
def get_sentiment_history():
    """Get sentiment analysis history"""
    limit = request.args.get('limit', 20, type=int)
    history = expression_state['sentiment_history'][-limit:]
    return jsonify(history)

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_status', {
        'status': 'connected',
        'current_emotion': expression_state['current_emotion'],
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('request_emotion_change')
def handle_emotion_request(data):
    """Handle emotion change request from client"""
    try:
        emotion = data.get('emotion', 'neutral')
        confidence = data.get('confidence', 1.0)
        
        # Update state
        expression_state['current_emotion'] = emotion
        
        # Broadcast to all clients
        emit('emotion_change', {
            'emotion': emotion,
            'confidence': confidence,
            'source': 'client_request'
        }, broadcast=True)
        
    except Exception as e:
        logger.error(f"Error handling emotion request: {e}")
        emit('error', {'message': str(e)})

@socketio.on('performance_update')
def handle_performance_update(data):
    """Handle performance metrics update from client"""
    try:
        expression_state['performance_metrics'].update(data)
        
        # Broadcast performance update
        emit('performance_metrics', expression_state['performance_metrics'], broadcast=True)
        
    except Exception as e:
        logger.error(f"Error handling performance update: {e}")

@socketio.on('analyze_text')
def handle_text_analysis(data):
    """Handle real-time text analysis"""
    try:
        text = data.get('text', '')
        if not text.strip():
            return
        
        result = expression_analyzer.analyze_sentiment(text)
        
        # Emit back to sender and broadcast
        emit('sentiment_result', result)
        emit('sentiment_analysis', result, broadcast=True)
        
        # Update emotion if confidence is sufficient
        if result['confidence'] > 0.4:
            expression_state['current_emotion'] = result['emotion']
            emit('emotion_change', {
                'emotion': result['emotion'],
                'confidence': result['confidence'],
                'source': 'text_analysis'
            }, broadcast=True)
        
    except Exception as e:
        logger.error(f"Error in text analysis: {e}")
        emit('error', {'message': str(e)})

def initialize_assistant():
    """Initialize the Totoro assistant if available"""
    global assistant
    
    if TotoroAssistant and Config:
        try:
            config = Config()
            # Fix: Check if TotoroAssistant constructor takes config parameter
            import inspect
            if len(inspect.signature(TotoroAssistant.__init__).parameters) > 1:
                assistant = TotoroAssistant(config)
            else:
                assistant = TotoroAssistant()
            
            logger.info("Totoro assistant initialized successfully")
            
            # Connect assistant responses to expression system
            if hasattr(assistant, 'on_response'):
                assistant.on_response = handle_assistant_response
            
        except Exception as e:
            logger.error(f"Failed to initialize Totoro assistant: {e}")
            logger.info("Continuing in demo mode...")
            assistant = None
    else:
        logger.warning("Running in demo mode - Totoro assistant not available")

def handle_assistant_response(text: str, is_complete: bool = False):
    """Handle responses from the Totoro assistant"""
    try:
        # Analyze sentiment of assistant response
        result = expression_analyzer.analyze_sentiment(text)
        
        # Emit for real-time expression updates
        socketio.emit('llm_response_chunk', {
            'text': text,
            'sentiment': result,
            'is_complete': is_complete
        })
        
        if is_complete:
            socketio.emit('llm_response_complete', {
                'final_emotion': result['emotion'],
                'confidence': result['confidence']
            })
            
            # Return to neutral after a delay
            def return_to_neutral():
                time.sleep(3)
                expression_state['current_emotion'] = 'neutral'
                socketio.emit('emotion_change', {
                    'emotion': 'neutral',
                    'confidence': 0.8,
                    'source': 'auto_return'
                })
            
            threading.Thread(target=return_to_neutral, daemon=True).start()
        
    except Exception as e:
        logger.error(f"Error handling assistant response: {e}")

def simulate_conversation_flow():
    """Simulate realistic conversation flow for demo purposes"""
    def conversation_simulator():
        while True:
            try:
                time.sleep(10)  # Wait 10 seconds between simulations
                
                # Simulate user speaking
                socketio.emit('user_speaking', {'timestamp': datetime.now().isoformat()})
                time.sleep(2)
                
                # Simulate thinking
                expression_state['current_emotion'] = 'thinking'
                socketio.emit('emotion_change', {
                    'emotion': 'thinking',
                    'confidence': 0.9,
                    'source': 'conversation_simulation'
                })
                time.sleep(3)
                
                # Simulate assistant response
                sample_responses = [
                    "That's a really interesting question!",
                    "I'm happy to help you with that.",
                    "Let me think about this carefully...",
                    "Wow, that's quite surprising!",
                    "I understand what you're looking for."
                ]
                
                import random
                response = random.choice(sample_responses)
                handle_assistant_response(response, True)
                
            except Exception as e:
                logger.error(f"Error in conversation simulation: {e}")
            
            time.sleep(30)  # Wait 30 seconds before next simulation
    
    # Start simulation in background thread
    simulation_thread = threading.Thread(target=conversation_simulator, daemon=True)
    simulation_thread.start()

if __name__ == '__main__':
    # Initialize the assistant
    initialize_assistant()
    
    # Start conversation simulation for demo
    simulate_conversation_flow()
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting Enhanced Totoro Server with Expression System on port {port}")
    logger.info("Features enabled:")
    logger.info("- Real-time sentiment analysis")
    logger.info("- WebSocket communication")
    logger.info("- Performance monitoring")
    logger.info("- Fluid avatar expressions")
    
    # Run the server
    socketio.run(app, host='0.0.0.0', port=port, debug=False) 