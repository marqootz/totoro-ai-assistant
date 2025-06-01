#!/usr/bin/env python3
"""
Basic Demo Server for Fluid Expression System
Minimal Flask server without SocketIO for basic testing
Auto-kills existing servers to prevent conflicts
"""

import json
import logging
import os
import subprocess
import signal
import time
from datetime import datetime
from typing import Dict

from flask import Flask, request, jsonify, send_from_directory
from textblob import TextBlob

app = Flask(__name__)

# Global state
expression_state = {
    'current_emotion': 'neutral',
    'sentiment_history': [],
    'performance_metrics': {
        'fps': 60,
        'animation_count': 0,
        'queue_length': 0
    }
}

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_existing_servers():
    """Kill any existing demo servers and processes on common ports"""
    logger.info("Checking for existing servers to terminate...")
    
    # Get the port we want to use
    port = int(os.environ.get('PORT', 3000))
    
    # Kill processes by name patterns
    server_patterns = [
        'demo_expression_server',
        'simple_demo_server',
        'basic_demo_server',
        'enhanced_totoro_server'
    ]
    
    for pattern in server_patterns:
        try:
            # Use pkill to kill processes matching the pattern
            result = subprocess.run(['pkill', '-f', pattern], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Killed existing {pattern} processes")
        except Exception as e:
            logger.debug(f"No {pattern} processes found or error: {e}")
    
    # Kill any process using our target port
    try:
        # Find processes using the port
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    subprocess.run(['kill', '-9', pid], check=True)
                    logger.info(f"Killed process {pid} using port {port}")
                except Exception as e:
                    logger.debug(f"Could not kill process {pid}: {e}")
    except Exception as e:
        logger.debug(f"No processes found on port {port} or error: {e}")
    
    # Give processes time to clean up
    time.sleep(2)
    logger.info("Server cleanup completed")

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
    return send_from_directory('.', 'avatar-demo-basic.html')

@app.route('/llm')
def llm_demo():
    return send_from_directory('.', 'llm-enhanced-avatar.html')

@app.route('/basic')
def basic_demo():
    return send_from_directory('.', 'avatar-demo-basic.html')

@app.route('/avatar-expression-system.js')
def avatar_system():
    """Serve the avatar expression system JS"""
    return send_from_directory('.', 'avatar-expression-system.js')

@app.route('/comparison')
def eye_comparison():
    return send_from_directory('.', 'eye-comparison-demo.html')

@app.route('/api/status')
def get_status():
    """Get current system status"""
    status = {
        'state': expression_state['current_emotion'],
        'assistant_available': False,  # Demo mode
        'demo_mode': True,
        'basic_mode': True,
        'server_type': 'basic_demo_server',
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
        
        # Update current emotion if confidence is high enough
        if result['confidence'] > 0.4:
            expression_state['current_emotion'] = result['emotion']
        
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

@app.route('/api/restart', methods=['POST'])
def restart_server():
    """Restart the server by killing existing processes and restarting"""
    try:
        kill_existing_servers()
        return jsonify({
            'success': True,
            'message': 'Server cleanup completed. Restart the server manually.'
        })
    except Exception as e:
        logger.error(f"Error restarting server: {e}")
        return jsonify({'error': str(e)}), 500

def cleanup_on_exit():
    """Cleanup function called on exit"""
    logger.info("Shutting down Basic Demo Server...")

if __name__ == '__main__':
    # Kill any existing servers first
    kill_existing_servers()
    
    logger.info("Starting Basic Expression System Demo Server")
    logger.info("Features enabled:")
    logger.info("- Real-time sentiment analysis")
    logger.info("- Basic API endpoints")
    logger.info("- Fluid avatar expressions")
    logger.info("- Automatic server cleanup")
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 3000))
    
    logger.info(f"Basic demo server starting on port {port}")
    logger.info(f"Navigate to http://localhost:{port} to see the expression system")
    logger.info("Previous servers have been automatically terminated")
    
    # Register cleanup function
    import atexit
    atexit.register(cleanup_on_exit)
    
    try:
        # Run the server
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        cleanup_on_exit() 