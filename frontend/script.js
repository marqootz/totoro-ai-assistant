class TotoroFace {
    constructor() {
        this.face = document.getElementById('totoroFace');
        this.statusText = document.getElementById('statusText');
        this.loadingProgress = document.getElementById('loadingProgress');
        this.loadingProgressBar = document.getElementById('loadingProgressBar');
        this.loadingText = document.getElementById('loadingText');
        this.currentState = 'initializing';
        
        // Initialize with loading state
        this.setState('loading');
        
        // Start periodic status check
        this.startStatusCheck();
    }
    
    setState(state) {
        // Remove previous state classes
        this.face.classList.remove('state-idle', 'state-awake', 'state-thinking', 'state-speaking', 'state-loading', 'state-error');
        
        // Add new state class
        this.face.classList.add(`state-${state}`);
        this.currentState = state;
        
        // Update status text
        this.updateStatusText(state);
        
        // Show/hide loading elements
        this.updateLoadingDisplay(state);
        
        console.log(`State changed to: ${state}`);
    }
    
    updateStatusText(state) {
        const statusMessages = {
            idle: 'Listening for wake word...',
            awake: 'I\'m listening!',
            thinking: 'Processing your request...',
            speaking: 'Speaking...',
            loading: 'Loading neural models...',
            error: 'Error occurred',
            initializing: 'Starting up...'
        };
        
        this.statusText.textContent = statusMessages[state] || 'Unknown state';
    }
    
    updateLoadingDisplay(state) {
        if (state === 'loading') {
            this.loadingProgress.style.display = 'block';
            this.loadingText.style.display = 'block';
        } else {
            this.loadingProgress.style.display = 'none';
            this.loadingText.style.display = 'none';
        }
    }
    
    updateLoadingProgress(stage, progress) {
        this.loadingProgressBar.style.width = `${progress}%`;
        this.loadingText.textContent = stage;
        
        // Update status text with more detail when loading
        if (this.currentState === 'loading') {
            this.statusText.textContent = `${stage} (${progress}%)`;
        }
    }
    
    async startStatusCheck() {
        // Check status every 500ms
        setInterval(async () => {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // Update state if changed
                if (data.state && data.state !== this.currentState) {
                    this.setState(data.state);
                }
                
                // Update loading progress if available
                if (data.loading && data.loading.is_loading) {
                    this.updateLoadingProgress(data.loading.stage, data.loading.progress);
                }
                
                // Update status based on assistant availability
                if (data.assistant_available && this.currentState === 'loading') {
                    this.setState('idle');
                }
                
            } catch (error) {
                // If we can't connect to the backend, stay in current state
                console.log('No backend connection, using demo mode');
            }
        }, 500);
    }
    
    // Demo mode for testing without backend
    startDemoMode() {
        const states = ['idle', 'awake', 'thinking', 'speaking'];
        let currentIndex = 0;
        
        setInterval(() => {
            this.setState(states[currentIndex]);
            currentIndex = (currentIndex + 1) % states.length;
        }, 3000);
    }
}

// Global function for manual state setting (used by test buttons)
function setState(state) {
    if (window.totoroFace) {
        window.totoroFace.setState(state);
    }
}

// Voice control functions
async function startVoice() {
    try {
        // Use the voice API endpoint
        const response = await fetch('/api/voice/start');
        const data = await response.json();
        
        if (data.success) {
            console.log('Voice listening started:', data.message);
            alert(`✅ Voice listening started!\n\nWake word: "${data.wake_word}"\n\nSay "${data.wake_word}" to activate the assistant.`);
        } else {
            console.error('Failed to start voice:', data.error);
            alert('❌ Failed to start voice: ' + data.error);
        }
    } catch (error) {
        console.error('Error starting voice:', error);
        alert('❌ Error starting voice: ' + error.message);
    }
}

async function stopVoice() {
    try {
        // Use the voice API endpoint
        const response = await fetch('/api/voice/stop');
        const data = await response.json();
        
        if (data.success) {
            console.log('Voice listening stopped:', data.message);
            alert('🔇 Voice listening stopped.');
        } else {
            console.error('Failed to stop voice:', data.error);
            alert('❌ Failed to stop voice: ' + data.error);
        }
    } catch (error) {
        console.error('Error stopping voice:', error);
        alert('❌ Error stopping voice: ' + error.message);
    }
}

// New function for single wake word session
async function startWakeSession() {
    try {
        const response = await fetch('/api/voice/wake_session');
        const data = await response.json();
        
        if (data.success) {
            console.log('Wake session started:', data.message);
            
            // Show listening status in UI
            const statusText = document.getElementById('statusText');
            const originalText = statusText.textContent;
            
            statusText.textContent = `👂 Listening for "totoro"... (${data.timeout}s timeout)`;
            
            // Update Totoro face to show listening state
            setState('idle');
            
            // Start a timer to show countdown
            let timeLeft = data.timeout;
            const countdown = setInterval(() => {
                timeLeft--;
                if (timeLeft > 0) {
                    statusText.textContent = `👂 Listening for "totoro"... (${timeLeft}s left)`;
                } else {
                    statusText.textContent = originalText;
                    clearInterval(countdown);
                }
            }, 1000);
            
            // Clear countdown after timeout
            setTimeout(() => {
                clearInterval(countdown);
                statusText.textContent = originalText;
            }, data.timeout * 1000 + 1000);
            
            alert(`👂 LISTENING FOR WAKE WORD!\n\n🎯 Say "totoro" clearly now\n⏱️ Timeout: ${data.timeout} seconds\n\n💡 Tip: Speak clearly and wait for response`);
        } else {
            console.error('Failed to start wake session:', data.error);
            alert('❌ Failed to start wake session: ' + data.error);
        }
    } catch (error) {
        console.error('Error starting wake session:', error);
        alert('❌ Error starting wake session: ' + error.message);
    }
}

// Check voice system status
async function checkVoiceStatus() {
    try {
        const response = await fetch('/api/voice/status');
        const data = await response.json();
        
        if (data.success) {
            const status = `Voice System Status:
• Running: ${data.is_running ? 'Yes' : 'No'}
• Wake word: "${data.wake_word}"
• Voice preference: ${data.voice_preference}
• Microphone: ${data.microphone_available ? 'Available' : 'Not available'}`;
            
            alert(status);
        } else {
            alert('❌ Failed to get voice status: ' + data.error);
        }
    } catch (error) {
        alert('❌ Error checking voice status: ' + error.message);
    }
}

// Monitor assistant state more frequently during active sessions
function startStateMonitoring() {
    let monitoringActive = false;
    
    return {
        start: function() {
            if (monitoringActive) return;
            monitoringActive = true;
            
            const monitorInterval = setInterval(async () => {
                if (!monitoringActive) {
                    clearInterval(monitorInterval);
                    return;
                }
                
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    
                    // Update state if changed and show in console for debugging
                    if (data.state && data.state !== window.totoroFace.currentState) {
                        console.log(`🎭 State change detected: ${window.totoroFace.currentState} → ${data.state}`);
                        window.totoroFace.setState(data.state);
                        
                        // Show state changes in status text temporarily
                        const statusText = document.getElementById('statusText');
                        const stateMessages = {
                            'awake': '👂 Wake word detected!',
                            'thinking': '🤔 Processing your command...',
                            'speaking': '🗣️ Responding...',
                            'idle': '😌 Ready and listening...'
                        };
                        
                        if (stateMessages[data.state]) {
                            const originalText = statusText.textContent;
                            statusText.textContent = stateMessages[data.state];
                            
                            // Restore original text after a delay (unless it's a listening state)
                            if (data.state !== 'idle') {
                                setTimeout(() => {
                                    if (statusText.textContent === stateMessages[data.state]) {
                                        statusText.textContent = originalText;
                                    }
                                }, 2000);
                            }
                        }
                    }
                } catch (error) {
                    console.log('State monitoring error (normal if backend disconnected):', error.message);
                }
            }, 200); // Check every 200ms for responsive feedback
        },
        
        stop: function() {
            monitoringActive = false;
        }
    };
}

// Create global state monitor
window.stateMonitor = startStateMonitoring();

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.totoroFace = new TotoroFace();
    
    // Start demo mode if specified in URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo') === 'true') {
        window.totoroFace.startDemoMode();
    }
    
    // Start state monitoring
    window.stateMonitor.start();
});

// Additional helper functions for eye animations
function addCustomEyeMovement() {
    const leftPupil = document.getElementById('leftPupil');
    const rightPupil = document.getElementById('rightPupil');
    
    // Add mouse tracking for eyes when idle
    document.addEventListener('mousemove', (e) => {
        if (window.totoroFace?.currentState === 'idle') {
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;
            
            const deltaX = (e.clientX - centerX) / centerX;
            const deltaY = (e.clientY - centerY) / centerY;
            
            const moveX = deltaX * 8; // Limit movement
            const moveY = deltaY * 8;
            
            leftPupil.style.transform = `translate(${-50 + moveX}%, ${-50 + moveY}%)`;
            rightPupil.style.transform = `translate(${-50 + moveX}%, ${-50 + moveY}%)`;
        }
    });
} 