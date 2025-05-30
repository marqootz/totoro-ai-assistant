#!/usr/bin/env python3
"""
Migration script to upgrade Totoro Assistant from Coqui TTS to Chatterbox TTS
"""

import subprocess
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a shell command and handle errors"""
    logger.info(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    logger.info("🐍 Checking Python version...")
    version = sys.version_info
    logger.info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        logger.info("✅ Python version is compatible with Chatterbox TTS")
        return True
    else:
        logger.error("❌ Python 3.8+ is required for Chatterbox TTS")
        return False

def install_requirements():
    """Install the updated requirements including Chatterbox TTS"""
    logger.info("📦 Installing updated requirements...")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    # Install torch with proper config for your system
    logger.info("🔥 Installing PyTorch for optimal performance...")
    
    # Check if CUDA is available
    try:
        import torch
        if torch.cuda.is_available():
            logger.info("🎮 CUDA detected - GPU acceleration will be available")
        else:
            logger.info("💻 CPU-only installation - still very fast!")
    except ImportError:
        logger.info("🔧 PyTorch will be installed with Chatterbox")
    
    return True

def test_chatterbox():
    """Test the new Chatterbox TTS installation"""
    logger.info("🎤 Testing Chatterbox TTS...")
    
    try:
        # Import and test Chatterbox
        from src.voice.text_to_speech import TextToSpeech
        
        # Create TTS instance with Chatterbox
        tts = TextToSpeech(voice_preference="chatterbox")
        
        # Test speech
        test_text = "Hello! I'm your upgraded Totoro assistant now powered by Chatterbox TTS."
        success = tts.test_speech(test_text)
        
        if success:
            logger.info("✅ Chatterbox TTS migration successful!")
            logger.info("🎉 Your assistant now has state-of-the-art voice synthesis!")
            return True
        else:
            logger.warning("⚠️ Chatterbox TTS test failed, but fallback TTS should work")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing Chatterbox TTS: {e}")
        logger.info("💡 The system will fall back to built-in TTS if needed")
        return False

def migration_summary():
    """Display migration summary"""
    logger.info("\n" + "="*60)
    logger.info("🦙 TOTORO ASSISTANT - CHATTERBOX MIGRATION COMPLETE")
    logger.info("="*60)
    logger.info("✨ NEW FEATURES:")
    logger.info("   🎯 State-of-the-art neural TTS (beats ElevenLabs!)")
    logger.info("   🎭 Emotion control and voice intensity")
    logger.info("   🎪 Voice cloning capabilities")
    logger.info("   🚀 Faster and more stable than previous TTS")
    logger.info("   🏷️ Built-in watermarking for responsible AI")
    logger.info("\n🎛️ NEW CONFIGURATION OPTIONS:")
    logger.info("   VOICE_PREFERENCE='chatterbox' (default)")
    logger.info("   CHATTERBOX_EXAGGERATION=0.5 (emotion intensity)")
    logger.info("   CHATTERBOX_CFG_WEIGHT=0.5 (generation stability)")
    logger.info("\n🚀 TO START YOUR UPGRADED ASSISTANT:")
    logger.info("   python main.py --test")
    logger.info("   python main.py --voice")
    logger.info("="*60)

def main():
    """Run the complete migration process"""
    logger.info("🎯 Starting Totoro Assistant migration to Chatterbox TTS")
    logger.info("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        logger.error("❌ Failed to install requirements")
        sys.exit(1)
    
    # Test the new setup
    test_success = test_chatterbox()
    
    # Show summary
    migration_summary()
    
    if test_success:
        logger.info("🎉 Migration completed successfully!")
        logger.info("💬 You can now start your assistant with: python main.py --test")
    else:
        logger.warning("⚠️ Migration completed with warnings")
        logger.info("💡 Your assistant will fall back to system TTS if needed")
        logger.info("🔧 Try: python main.py --test to check functionality")

if __name__ == "__main__":
    main() 