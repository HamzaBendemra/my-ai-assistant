# services/supabase_client.py
import os
from datetime import datetime, timedelta
from supabase import create_client, Client
import streamlit as st

class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            st.error("Supabase credentials not found. Please check your .env file.")
            st.stop()
            
        self.client: Client = create_client(url, key)
    
    def save_chat(self, user_message: str, assistant_response: str):
        """Save chat interaction to database"""
        try:
            result = self.client.table("chat_history").insert({
                "user_message": user_message,
                "assistant_response": assistant_response
            }).execute()
            return result
        except Exception as e:
            st.error(f"Error saving chat: {str(e)}")
            return None
    
    def get_chat_history(self, limit: int = 10):
        """Get recent chat history"""
        try:
            result = self.client.table("chat_history")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            st.error(f"Error fetching chat history: {str(e)}")
            return []
    
    def get_cached_data(self, cache_key: str, max_age_minutes: int = 60):
        """Get cached data if not expired"""
        try:
            current_time = datetime.now().isoformat()
            result = self.client.table("api_cache")\
                .select("*")\
                .eq("cache_key", cache_key)\
                .gte("expires_at", current_time)\
                .single()\
                .execute()
            
            if result.data:
                return result.data.get("data")
            return None
        except Exception as e:
            st.error(f"Error fetching cached data: {str(e)}")
            return None
    
    def set_cached_data(self, cache_key: str, data: dict, ttl_minutes: int = 60):
        """Cache data with expiration"""
        try:
            expires_at = (datetime.now() + timedelta(minutes=ttl_minutes)).isoformat()
            
            # Upsert (insert or update)
            result = self.client.table("api_cache").upsert({
                "cache_key": cache_key,
                "data": data,
                "expires_at": expires_at
            }).execute()
            return result
        except Exception as e:
            st.error(f"Error caching data: {str(e)}")
            return None