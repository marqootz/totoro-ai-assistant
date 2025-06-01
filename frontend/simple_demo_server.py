#!/usr/bin/env python3
"""
Simple Demo Server for Fluid Expression System
Using basic Flask without eventlet for better compatibility
"""

import json
import logging
import os
import threading
import time
from datetime import datetime
from typing import Dict

from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import nltk
from textblob import TextBlob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'expression_demo_secret'

# Use threading instead of eventlet for better compatibility
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state
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
            'happy': ['excited', 'amazing', 'fantastic', 'great', 'wonderful', 'love', 'perfect', 'awesome', 'brilliant', 'excellent'],
            'sad': ['disappointed', 'sad', 'unfortunate', 'terrible', 'awful', 'bad', 'wrong', 'failed', 'upset', 'depressed'],
            'surprised': ['wow', 'incredible', 'unexpected', 'shocking', 'amazing', 'unbelievable', 'astonishing', 'remarkable'],
            'thinking': ['think', 'consider', 'analyze', 'evaluate', 'hmm', 'maybe', 'perhaps', 'wondering', 'ponder', 'contemplate'],
            'speaking': ['say', 'tell', 'explain', 'describe', 'mentioned', 'stated', 'discuss', 'communicate']
        }
        
        # Try to download required NLTK data but continue if it fails
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt')
            except Exception as e:
                logger.warning(f"Could not download NLTK data: {e}")
    
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
    status = {
        'state': expression_state['current_emotion'],
        'assistant_available': False,  # Demo mode
        'demo_mode': True,
        'timestamp': datetime.now().isoformat(),
        'performance_metrics': expression_state['performance_metrics'],
        'sentiment_history_length': len(expression_state['sentiment_history'])
    }
    
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
        if result['confidence'] > 0.4:
            expression_state['current_emotion'] = result['emotion']
            socketio.emit('emotion_change', {
                'emotion': result['emotion'],
                'confidence': result['confidence'],
                'source': 'sentiment_analysis'
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
        'demo_mode': True,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

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

def simulate_conversation_flow():
    """Simulate realistic conversation flow for demo purposes"""
    def conversation_simulator():
        while True:
            try:
                time.sleep(15)  # Wait 15 seconds between simulations
                
                sample_responses = [
                    "That's a really interesting question! I'm excited to help.",
                    "I'm happy to assist you with that task.",
                    "Let me think about this carefully and analyze the options...",
                    "Wow, that's quite a surprising development!",
                    "I understand what you're looking for perfectly.",
                    "This is amazing work you've done here!",
                    "Hmm, this is quite challenging to solve properly.",
                    "I'm disappointed that didn't work as expected.",
                ]
                
                import random
                response = random.choice(sample_responses)
                
                # Analyze the simulated response
                result = expression_analyzer.analyze_sentiment(response)
                
                # Update emotion based on analysis
                if result['confidence'] > 0.4:
                    expression_state['current_emotion'] = result['emotion']
                    socketio.emit('emotion_change', {
                        'emotion': result['emotion'],
                        'confidence': result['confidence'],
                        'source': 'simulated_response'
                    })
                
                # Return to neutral after a delay
                socketio.sleep(4)
                expression_state['current_emotion'] = 'neutral'
                socketio.emit('emotion_change', {
                    'emotion': 'neutral',
                    'confidence': 0.8,
                    'source': 'auto_return'
                })
                
            except Exception as e:
                logger.error(f"Error in conversation simulation: {e}")
            
            socketio.sleep(20)  # Wait 20 seconds before next simulation
    
    # Start simulation in background thread
    socketio.start_background_task(conversation_simulator)

if __name__ == '__main__':
    logger.info("Starting Expression System Demo Server (Simple Version)")
    logger.info("Features enabled:")
    logger.info("- Real-time sentiment analysis")
    logger.info("- WebSocket communication")
    logger.info("- Performance monitoring")
    logger.info("- Fluid avatar expressions")
    logger.info("- Conversation simulation")
    
    # Start conversation simulation for demo
    simulate_conversation_flow()
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Demo server starting on port {port}")
    logger.info("Navigate to http://localhost:5000 to see the expression system")
    
    # Run the server
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True) 