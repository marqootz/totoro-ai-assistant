import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class SpotifyClient:
    """Client for interacting with Spotify"""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
        # Set up OAuth
        scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-read-private,playlist-read-collaborative,user-library-read"
        
        self.sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache"
        )
        
        self.sp = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Spotify"""
        try:
            token_info = self.sp_oauth.get_cached_token()
            if not token_info:
                auth_url = self.sp_oauth.get_authorize_url()
                logger.info(f"Please visit this URL to authorize the application: {auth_url}")
                response = input("Enter the URL you were redirected to: ")
                code = self.sp_oauth.parse_response_code(response)
                token_info = self.sp_oauth.get_access_token(code)
            
            self.sp = spotipy.Spotify(auth=token_info['access_token'])
            logger.info("Successfully authenticated with Spotify")
        except Exception as e:
            logger.error(f"Spotify authentication failed: {e}")
    
    def get_devices(self) -> List[Dict]:
        """Get available playback devices"""
        try:
            if not self.sp:
                return []
            devices = self.sp.devices()
            return devices.get('devices', [])
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            return []
    
    def get_active_device(self) -> Optional[Dict]:
        """Get currently active device"""
        devices = self.get_devices()
        for device in devices:
            if device.get('is_active'):
                return device
        return None
    
    def set_device(self, device_id: str) -> bool:
        """Set active playback device"""
        try:
            self.sp.transfer_playback(device_id=device_id)
            logger.info(f"Switched to device: {device_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting device: {e}")
            return False
    
    def search_track(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for tracks"""
        try:
            if not self.sp:
                return []
            results = self.sp.search(q=query, type='track', limit=limit)
            return results.get('tracks', {}).get('items', [])
        except Exception as e:
            logger.error(f"Error searching tracks: {e}")
            return []
    
    def search_artist(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for artists"""
        try:
            results = self.sp.search(q=query, type='artist', limit=limit)
            return results.get('artists', {}).get('items', [])
        except Exception as e:
            logger.error(f"Error searching artists: {e}")
            return []
    
    def search_playlist(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for playlists"""
        try:
            results = self.sp.search(q=query, type='playlist', limit=limit)
            return results.get('playlists', {}).get('items', [])
        except Exception as e:
            logger.error(f"Error searching playlists: {e}")
            return []
    
    def play_track(self, track_uri: str, device_id: Optional[str] = None) -> bool:
        """Play a specific track"""
        try:
            if not self.sp:
                return False
            self.sp.start_playback(device_id=device_id, uris=[track_uri])
            logger.info(f"Playing track: {track_uri}")
            return True
        except Exception as e:
            logger.error(f"Error playing track: {e}")
            return False
    
    def play_playlist(self, playlist_uri: str, device_id: Optional[str] = None) -> bool:
        """Play a playlist"""
        try:
            self.sp.start_playback(device_id=device_id, context_uri=playlist_uri)
            logger.info(f"Playing playlist: {playlist_uri}")
            return True
        except Exception as e:
            logger.error(f"Error playing playlist: {e}")
            return False
    
    def play_artist(self, artist_uri: str, device_id: Optional[str] = None) -> bool:
        """Play an artist's top tracks"""
        try:
            self.sp.start_playback(device_id=device_id, context_uri=artist_uri)
            logger.info(f"Playing artist: {artist_uri}")
            return True
        except Exception as e:
            logger.error(f"Error playing artist: {e}")
            return False
    
    def pause(self, device_id: Optional[str] = None) -> bool:
        """Pause playback"""
        try:
            if not self.sp:
                return False
            self.sp.pause_playback(device_id=device_id)
            logger.info("Playback paused")
            return True
        except Exception as e:
            logger.error(f"Error pausing: {e}")
            return False
    
    def resume(self, device_id: Optional[str] = None) -> bool:
        """Resume playback"""
        try:
            if not self.sp:
                return False
            self.sp.start_playback(device_id=device_id)
            logger.info("Playback resumed")
            return True
        except Exception as e:
            logger.error(f"Error resuming: {e}")
            return False
    
    def next_track(self, device_id: Optional[str] = None) -> bool:
        """Skip to next track"""
        try:
            self.sp.next_track(device_id=device_id)
            logger.info("Skipped to next track")
            return True
        except Exception as e:
            logger.error(f"Error skipping track: {e}")
            return False
    
    def previous_track(self, device_id: Optional[str] = None) -> bool:
        """Go to previous track"""
        try:
            self.sp.previous_track(device_id=device_id)
            logger.info("Went to previous track")
            return True
        except Exception as e:
            logger.error(f"Error going to previous track: {e}")
            return False
    
    def set_volume(self, volume: int, device_id: Optional[str] = None) -> bool:
        """Set volume (0-100)"""
        try:
            if not self.sp:
                return False
            volume = max(0, min(100, volume))
            self.sp.volume(volume, device_id=device_id)
            logger.info(f"Volume set to {volume}")
            return True
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            return False
    
    def get_current_playback(self) -> Optional[Dict]:
        """Get current playback information"""
        try:
            return self.sp.current_playback()
        except Exception as e:
            logger.error(f"Error getting current playback: {e}")
            return None
    
    def get_current_track(self) -> Optional[Dict]:
        """Get currently playing track"""
        try:
            current = self.sp.current_user_playing_track()
            if current and current.get('item'):
                return current['item']
            return None
        except Exception as e:
            logger.error(f"Error getting current track: {e}")
            return None
    
    def find_device_by_name(self, name: str) -> Optional[Dict]:
        """Find device by name (case insensitive)"""
        devices = self.get_devices()
        name_lower = name.lower()
        for device in devices:
            if name_lower in device.get('name', '').lower():
                return device
        return None
    
    def play_on_device(self, device_name: str, content_uri: Optional[str] = None) -> bool:
        """Play content on a specific device by name"""
        device = self.find_device_by_name(device_name)
        if not device:
            logger.error(f"Device not found: {device_name}")
            return False
        
        device_id = device['id']
        
        # Transfer playback to device first
        if not self.set_device(device_id):
            return False
        
        # Play content if provided
        if content_uri:
            if content_uri.startswith('spotify:track:'):
                return self.play_track(content_uri, device_id)
            elif content_uri.startswith('spotify:playlist:'):
                return self.play_playlist(content_uri, device_id)
            elif content_uri.startswith('spotify:artist:'):
                return self.play_artist(content_uri, device_id)
        else:
            # Just resume on the device
            return self.resume(device_id)
        
        return True 