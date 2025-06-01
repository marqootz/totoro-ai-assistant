/**
 * Fluid Expression System for Big Hero 6-style Avatars
 * Features: SVG morphing, real-time LLM analysis, performance optimization
 */

class FluidExpressionSystem {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            enableSentimentAnalysis: true,
            useWebWorkers: true,
            fallbackToCanvas: false,
            maxControlPoints: 20,
            maxSimultaneousMorphs: 3,
            animationDuration: 800,
            ...options
        };
        
        this.currentEmotion = 'neutral';
        this.morphingQueue = [];
        this.isAnimating = false;
        this.sentimentWorker = null;
        this.socket = null;
        
        this.init();
    }

    init() {
        this.createSVGStructure();
        this.setupExpressionPaths();
        this.initializeAnimationSystem();
        
        if (this.options.enableSentimentAnalysis) {
            this.setupSentimentAnalysis();
        }
        
        this.setupWebSocket();
        this.setupPerformanceMonitoring();
    }

    createSVGStructure() {
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svg.setAttribute('viewBox', '0 0 300 300');
        this.svg.classList.add('avatar-face');
        
        // Create main face group
        this.faceGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        this.faceGroup.classList.add('face-group');
        
        // Head outline (Big Hero 6 style - rounded)
        this.headPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        this.headPath.classList.add('head-outline');
        this.headPath.setAttribute('fill', '#f8f9fa');
        this.headPath.setAttribute('stroke', '#2c3e50');
        this.headPath.setAttribute('stroke-width', '3');
        
        // Eyes
        this.leftEye = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        this.leftEye.classList.add('eye', 'left-eye');
        this.leftEye.setAttribute('fill', '#2c3e50');
        
        this.rightEye = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        this.rightEye.classList.add('eye', 'right-eye');
        this.rightEye.setAttribute('fill', '#2c3e50');
        
        // Mouth
        this.mouth = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        this.mouth.classList.add('mouth');
        this.mouth.setAttribute('fill', 'none');
        this.mouth.setAttribute('stroke', '#2c3e50');
        this.mouth.setAttribute('stroke-width', '2');
        this.mouth.setAttribute('stroke-linecap', 'round');
        
        // Assemble SVG
        this.faceGroup.appendChild(this.headPath);
        this.faceGroup.appendChild(this.leftEye);
        this.faceGroup.appendChild(this.rightEye);
        this.faceGroup.appendChild(this.mouth);
        this.svg.appendChild(this.faceGroup);
        this.container.appendChild(this.svg);
        
        this.addSVGStyles();
    }

    setupExpressionPaths() {
        // Define expression paths with <20 control points each
        this.expressions = {
            neutral: {
                head: 'M50,80 Q50,50 80,50 L220,50 Q250,50 250,80 L250,220 Q250,250 220,250 L80,250 Q50,250 50,220 Z',
                leftEye: 'M90,130 Q95,125 105,125 Q115,125 120,130 Q115,135 105,135 Q95,135 90,130 Z',
                rightEye: 'M180,130 Q185,125 195,125 Q205,125 210,130 Q205,135 195,135 Q185,135 180,130 Z',
                mouth: 'M130,190 Q150,195 170,190'
            },
            happy: {
                head: 'M50,80 Q50,50 80,50 L220,50 Q250,50 250,80 L250,220 Q250,250 220,250 L80,250 Q50,250 50,220 Z',
                leftEye: 'M90,125 Q105,115 120,125 Q105,140 90,125 Z',
                rightEye: 'M180,125 Q195,115 210,125 Q195,140 180,125 Z',
                mouth: 'M120,185 Q150,205 180,185'
            },
            sad: {
                head: 'M50,85 Q50,50 80,50 L220,50 Q250,50 250,85 L250,225 Q250,250 220,250 L80,250 Q50,250 50,225 Z',
                leftEye: 'M90,135 Q105,145 120,135 Q105,120 90,135 Z',
                rightEye: 'M180,135 Q195,145 210,135 Q195,120 180,135 Z',
                mouth: 'M120,205 Q150,185 180,205'
            },
            surprised: {
                head: 'M50,75 Q50,45 80,45 L220,45 Q250,45 250,75 L250,225 Q250,255 220,255 L80,255 Q50,255 50,225 Z',
                leftEye: 'M85,120 Q105,110 125,120 Q125,150 105,150 Q85,150 85,120 Z',
                rightEye: 'M175,120 Q195,110 215,120 Q215,150 195,150 Q175,150 175,120 Z',
                mouth: 'M140,185 Q150,200 160,185'
            },
            thinking: {
                head: 'M50,80 Q50,50 80,50 L220,50 Q250,50 250,80 L250,220 Q250,250 220,250 L80,250 Q50,250 50,220 Z',
                leftEye: 'M90,130 Q95,125 105,125 Q115,125 120,130 Q115,135 105,135 Q95,135 90,130 Z',
                rightEye: 'M185,130 Q190,125 200,125 Q210,125 215,130 Q210,135 200,135 Q190,135 185,130 Z',
                mouth: 'M135,188 Q150,192 165,188'
            },
            speaking: {
                head: 'M50,80 Q50,50 80,50 L220,50 Q250,50 250,80 L250,220 Q250,250 220,250 L80,250 Q50,250 50,220 Z',
                leftEye: 'M90,130 Q95,125 105,125 Q115,125 120,130 Q115,135 105,135 Q95,135 90,130 Z',
                rightEye: 'M180,130 Q185,125 195,125 Q205,125 210,130 Q205,135 195,135 Q185,135 180,130 Z',
                mouth: 'M125,185 Q150,200 175,185 Q150,215 125,185 Z'
            }
        };
    }

    initializeAnimationSystem() {
        // Initialize with neutral expression
        this.setInitialPaths();
        
        // Setup GSAP timeline for smooth animations
        this.timeline = gsap.timeline({ paused: true });
        
        // Create morphing animation functions
        this.setupMorphingAnimations();
    }

    setInitialPaths() {
        const neutral = this.expressions.neutral;
        this.headPath.setAttribute('d', neutral.head);
        this.leftEye.setAttribute('d', neutral.leftEye);
        this.rightEye.setAttribute('d', neutral.rightEye);
        this.mouth.setAttribute('d', neutral.mouth);
    }

    setupMorphingAnimations() {
        // Use Flubber for smooth path interpolation
        this.morphFunctions = {};
        
        Object.keys(this.expressions).forEach(emotion => {
            this.morphFunctions[emotion] = {};
            const paths = this.expressions[emotion];
            
            // Create morph functions for each facial element
            ['head', 'leftEye', 'rightEye', 'mouth'].forEach(element => {
                this.morphFunctions[emotion][element] = {};
                
                Object.keys(this.expressions).forEach(targetEmotion => {
                    if (emotion !== targetEmotion) {
                        try {
                            this.morphFunctions[emotion][element][targetEmotion] = 
                                flubber.interpolate(paths[element], this.expressions[targetEmotion][element]);
                        } catch (e) {
                            console.warn(`Failed to create morph from ${emotion} to ${targetEmotion} for ${element}`);
                        }
                    }
                });
            });
        });
    }

    setupSentimentAnalysis() {
        if (this.options.useWebWorkers && typeof Worker !== 'undefined') {
            this.createSentimentWorker();
        } else {
            this.loadSentimentLibrary();
        }
    }

    createSentimentWorker() {
        const workerScript = `
            importScripts('https://cdn.jsdelivr.net/npm/sentiment@5.0.2/build/sentiment.min.js');
            
            const sentiment = new Sentiment();
            
            self.onmessage = function(e) {
                const { text, id } = e.data;
                
                try {
                    const result = sentiment.analyze(text);
                    const emotion = determineEmotion(result);
                    
                    self.postMessage({
                        id: id,
                        sentiment: result,
                        emotion: emotion,
                        confidence: Math.abs(result.score) / Math.max(text.split(' ').length, 1)
                    });
                } catch (error) {
                    self.postMessage({
                        id: id,
                        error: error.message
                    });
                }
            };
            
            function determineEmotion(sentimentResult) {
                const score = sentimentResult.score;
                const comparative = sentimentResult.comparative;
                
                if (score > 3) return 'happy';
                if (score < -3) return 'sad';
                if (Math.abs(comparative) > 0.5) return 'surprised';
                if (sentimentResult.tokens.some(token => 
                    ['think', 'consider', 'maybe', 'perhaps'].includes(token.toLowerCase())
                )) return 'thinking';
                
                return 'neutral';
            }
        `;
        
        const blob = new Blob([workerScript], { type: 'application/javascript' });
        this.sentimentWorker = new Worker(URL.createObjectURL(blob));
        
        this.sentimentWorker.onmessage = (e) => {
            const { emotion, confidence, id } = e.data;
            if (emotion && confidence > 0.3) {
                this.queueExpressionChange(emotion, confidence);
            }
        };
    }

    setupWebSocket() {
        // Connect to real-time LLM response stream
        if (typeof io !== 'undefined') {
            this.socket = io();
            
            this.socket.on('llm_response_chunk', (data) => {
                if (data.text) {
                    this.analyzeSentiment(data.text);
                }
            });
            
            this.socket.on('llm_response_complete', (data) => {
                this.transitionToExpression('neutral', 0.8);
            });
            
            this.socket.on('user_speaking', () => {
                this.transitionToExpression('thinking', 0.9);
            });
            
            this.socket.on('assistant_speaking', () => {
                this.transitionToExpression('speaking', 1.0);
            });
        }
    }

    setupPerformanceMonitoring() {
        this.performanceMetrics = {
            animationFrames: 0,
            lastFrameTime: performance.now(),
            avgFrameTime: 16.67 // 60fps target
        };
        
        this.startPerformanceMonitoring();
    }

    startPerformanceMonitoring() {
        const monitor = () => {
            const currentTime = performance.now();
            const frameTime = currentTime - this.performanceMetrics.lastFrameTime;
            
            this.performanceMetrics.avgFrameTime = 
                (this.performanceMetrics.avgFrameTime * 0.9) + (frameTime * 0.1);
            
            this.performanceMetrics.lastFrameTime = currentTime;
            this.performanceMetrics.animationFrames++;
            
            // Switch to canvas fallback if performance drops
            if (this.performanceMetrics.avgFrameTime > 33.33 && this.options.fallbackToCanvas) {
                this.switchToCanvasFallback();
            }
            
            requestAnimationFrame(monitor);
        };
        
        requestAnimationFrame(monitor);
    }

    analyzeSentiment(text) {
        if (this.sentimentWorker) {
            const id = Date.now();
            this.sentimentWorker.postMessage({ text, id });
        } else if (typeof Sentiment !== 'undefined') {
            const sentiment = new Sentiment();
            const result = sentiment.analyze(text);
            const emotion = this.determineEmotion(result);
            const confidence = Math.abs(result.score) / Math.max(text.split(' ').length, 1);
            
            if (confidence > 0.3) {
                this.queueExpressionChange(emotion, confidence);
            }
        }
    }

    determineEmotion(sentimentResult) {
        const score = sentimentResult.score;
        const comparative = sentimentResult.comparative;
        
        if (score > 3) return 'happy';
        if (score < -3) return 'sad';
        if (Math.abs(comparative) > 0.5) return 'surprised';
        if (sentimentResult.tokens.some(token => 
            ['think', 'consider', 'maybe', 'perhaps'].includes(token.toLowerCase())
        )) return 'thinking';
        
        return 'neutral';
    }

    queueExpressionChange(emotion, confidence) {
        this.morphingQueue.push({
            emotion,
            confidence,
            timestamp: Date.now()
        });
        
        this.processMorphingQueue();
    }

    processMorphingQueue() {
        if (this.isAnimating || this.morphingQueue.length === 0) return;
        
        // Sort by confidence and recency
        this.morphingQueue.sort((a, b) => {
            const confidenceDiff = b.confidence - a.confidence;
            if (Math.abs(confidenceDiff) > 0.2) return confidenceDiff;
            return b.timestamp - a.timestamp;
        });
        
        const nextExpression = this.morphingQueue.shift();
        this.transitionToExpression(nextExpression.emotion, nextExpression.confidence);
    }

    transitionToExpression(emotion, confidence = 1.0) {
        if (emotion === this.currentEmotion || this.isAnimating) return;
        
        this.isAnimating = true;
        const duration = this.options.animationDuration * confidence;
        
        // Create smooth transition using GSAP
        this.timeline.clear();
        
        const elements = ['head', 'leftEye', 'rightEye', 'mouth'];
        const elementMappings = {
            head: this.headPath,
            leftEye: this.leftEye,
            rightEye: this.rightEye,
            mouth: this.mouth
        };
        
        // Limit simultaneous morphs for performance
        const morphCount = Math.min(elements.length, this.options.maxSimultaneousMorphs);
        
        elements.slice(0, morphCount).forEach((element, index) => {
            const domElement = elementMappings[element];
            const morphFunction = this.morphFunctions[this.currentEmotion]?.[element]?.[emotion];
            
            if (morphFunction) {
                this.timeline.to({}, {
                    duration: duration / 1000,
                    ease: "power2.inOut",
                    onUpdate: function() {
                        const progress = this.progress();
                        const newPath = morphFunction(progress);
                        domElement.setAttribute('d', newPath);
                    },
                    delay: index * 0.05 // Slight stagger for natural feel
                }, 0);
            }
        });
        
        this.timeline.call(() => {
            this.currentEmotion = emotion;
            this.isAnimating = false;
            this.processMorphingQueue(); // Process next in queue
        });
        
        this.timeline.play();
    }

    // Public API methods
    setExpression(emotion, immediate = false) {
        if (immediate) {
            this.setImmediateExpression(emotion);
        } else {
            this.queueExpressionChange(emotion, 1.0);
        }
    }

    setImmediateExpression(emotion) {
        if (!this.expressions[emotion]) return;
        
        const paths = this.expressions[emotion];
        this.headPath.setAttribute('d', paths.head);
        this.leftEye.setAttribute('d', paths.leftEye);
        this.rightEye.setAttribute('d', paths.rightEye);
        this.mouth.setAttribute('d', paths.mouth);
        
        this.currentEmotion = emotion;
    }

    enableSentimentAnalysis() {
        this.options.enableSentimentAnalysis = true;
        if (!this.sentimentWorker) {
            this.setupSentimentAnalysis();
        }
    }

    disableSentimentAnalysis() {
        this.options.enableSentimentAnalysis = false;
        if (this.sentimentWorker) {
            this.sentimentWorker.terminate();
            this.sentimentWorker = null;
        }
    }

    getPerformanceMetrics() {
        return {
            ...this.performanceMetrics,
            fps: 1000 / this.performanceMetrics.avgFrameTime,
            currentEmotion: this.currentEmotion,
            queueLength: this.morphingQueue.length
        };
    }

    switchToCanvasFallback() {
        console.warn('Switching to Canvas fallback due to performance issues');
        // Implementation for canvas-based rendering would go here
        // This would be a simplified version for mobile devices
    }

    addSVGStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .avatar-face {
                width: 100%;
                height: 100%;
                max-width: 300px;
                max-height: 300px;
            }
            
            .face-group {
                transform-origin: center;
            }
            
            .head-outline {
                filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1));
            }
            
            .eye {
                transition: opacity 0.2s ease;
            }
            
            .mouth {
                transition: opacity 0.2s ease;
            }
        `;
        document.head.appendChild(style);
    }

    destroy() {
        if (this.sentimentWorker) {
            this.sentimentWorker.terminate();
        }
        
        if (this.socket) {
            this.socket.disconnect();
        }
        
        if (this.timeline) {
            this.timeline.kill();
        }
        
        this.container.innerHTML = '';
    }
}

// Export for use in other modules
window.FluidExpressionSystem = FluidExpressionSystem; 