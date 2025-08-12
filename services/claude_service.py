# services/claude_service.py
import os
import anthropic
import streamlit as st
from typing import List, Dict, Optional

class ClaudeService:
    def __init__(self):
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        
        if not api_key:
            st.error("Claude API key not found. Please check your .env file.")
            st.stop()
            
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def get_response(self, 
                    user_message: str, 
                    context: Optional[Dict] = None,
                    chat_history: Optional[List] = None) -> str:
        """Get response from Claude"""
        try:
            # Build system prompt
            system_prompt = """You are a helpful personal assistant that helps manage daily life. 
            You have access to the user's calendar and budget information when provided.
            Be concise, friendly, and practical in your responses."""
            
            # Build messages
            messages = []
            
            # Add context if provided
            if context:
                context_message = "Current context:\n"
                if "calendar" in context:
                    context_message += f"\nCalendar: {context['calendar']}"
                if "budget" in context:
                    context_message += f"\nBudget: {context['budget']}"
                
                messages.append({
                    "role": "user",
                    "content": context_message
                })
                messages.append({
                    "role": "assistant",
                    "content": "I understand the context. How can I help you?"
                })
            
            # Add chat history (last 5 exchanges)
            if chat_history:
                for msg in chat_history[-10:]:  # Last 5 exchanges (user + assistant)
                    messages.append(msg)
            
            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Get response from Claude
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Using Haiku for cost efficiency
                max_tokens=500,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error getting response from Claude: {str(e)}"
    
    def summarize_text(self, text: str, max_length: int = 100) -> str:
        """Summarize text using Claude"""
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=max_length,
                messages=[{
                    "role": "user",
                    "content": f"Summarize this in one sentence: {text}"
                }]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error summarizing: {str(e)}"