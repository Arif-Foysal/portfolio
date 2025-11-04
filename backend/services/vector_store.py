"""
Vector store service for semantic caching using Supabase pgvector
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime

from openai import AsyncOpenAI
from supabase import create_client, Client


class VectorStore:
    """Vector database integration using Supabase pgvector"""
    
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY are required")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI text-embedding-3-small model"""
        try:
            response = await self.openai_client.embeddings.create(
                model="text-embedding-3-small",  # Cheapest embedding model
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
    
    async def store_response(self, query: str, response: str, metadata: Dict = None, response_type: str = "text"):
        """Store query-response pair in vector database
        
        Args:
            query: The user's query text
            response: The response text or JSON
            metadata: Additional metadata about the response
            response_type: The MessageType enum value (e.g., "text", "projects_list", "skills_list")
        """
        try:
            embedding = await self.get_embedding(query)
            
            # Store response as JSON for consistency with retrieval
            response_data = {
                "type": response_type,  # Use proper MessageType enum value
                "data": response
            }
            
            self.client.table("chat_responses").insert({
                "query": query,
                "response": json.dumps(response_data),  # Store as JSON string
                "embedding": embedding,
                "metadata": json.dumps(metadata or {}),
                "created_at": datetime.now().isoformat()
            }).execute()
            
            print(f"Stored response for query: {query[:50]}...")
            
        except Exception as e:
            print(f"Error storing response in vector store: {e}")
    
    async def search_similar_responses(self, query: str, limit: int = 1, threshold: float = 0.85) -> List[Dict]:
        """Search for similar past queries using vector similarity"""
        try:
            embedding = await self.get_embedding(query)
            
            # Use Supabase RPC function for vector similarity search
            results = self.client.rpc(
                "match_chat_responses",
                {
                    "query_embedding": embedding,
                    "match_threshold": threshold,
                    "match_count": limit
                }
            ).execute()
            
            if results.data:
                print(f"Found {len(results.data)} similar responses for query: {query[:50]}...")
                return results.data
            
            return []
            
        except Exception as e:
            print(f"Error searching similar responses: {e}")
            return []
    
    async def delete_old_responses(self, days: int = 30):
        """Clean up old cached responses (optional maintenance)"""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            self.client.table("chat_responses").delete().lt("created_at", cutoff_date).execute()
            print(f"Deleted responses older than {days} days")
            
        except Exception as e:
            print(f"Error deleting old responses: {e}")
