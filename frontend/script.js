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
        // Use the command endpoint instead of start_voice
        const response = await fetch('/api/command/start_listening');
        const data = await response.json();
        
        if (data.success) {
            console.log('Voice command sent:', data.response);
            alert('✅ Voice activation attempted! Try saying your wake word now.\n\nResponse: ' + data.response);
            
            // Also try to start the main assistant loop
            try {
                const loopResponse = await fetch('/api/command/run_continuous');
                if (loopResponse.ok) {
                    const loopData = await loopResponse.json();
                    console.log('Continuous mode:', loopData);
                }
            } catch (e) {
                console.log('Continuous mode not available');
            }
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
        // Use the command endpoint instead of stop_voice
        const response = await fetch('/api/command/stop_listening');
        const data = await response.json();
        
        if (data.success) {
            console.log('Voice stopped:', data.response);
            alert('🔇 Voice stopping attempted.\n\nResponse: ' + data.response);
        } else {
            console.error('Failed to stop voice:', data.response);
            alert('❌ Response: ' + data.response);
        }
    } catch (error) {
        console.error('Error stopping voice:', error);
        alert('❌ Error stopping voice: ' + error.message);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.totoroFace = new TotoroFace();
    
    // Start demo mode if specified in URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo') === 'true') {
        window.totoroFace.startDemoMode();
    }
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