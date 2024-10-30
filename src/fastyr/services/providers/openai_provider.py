from fastyr.services.interfaces.llm_provider import LLMProvider
from fastyr.core.contracts.constants import ErrorCodes
from fastyr.core.exceptions import ProviderError
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import aiohttp
import os

load_dotenv()
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1")

class OpenAIProvider(LLMProvider):
    """OpenAI API provider implementation"""
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "gpt-4",
        base_url: str = OPENAI_URL,
        organization_id: Optional[str] = None,
        project_id: Optional[str] = None
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.organization_id = organization_id
        self.project_id = project_id
    
    async def generate_response(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate response using OpenAI's API
        
        Args:
            prompt: Input text prompt
            options: Additional options including:
                - temperature: Sampling temperature (0-2)
                - max_tokens: Maximum tokens to generate
                - top_p: Nucleus sampling parameter
                - frequency_penalty: Frequency penalty (-2 to 2)
                - presence_penalty: Presence penalty (-2 to 2)
                - stop: List of stop sequences
                - model: Override default model
                
        Returns:
            Generated response text
            
        Raises:
            ProviderError: If API call fails
        """
        options = options or {}
        
        # Construct headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Add optional organization and project headers
        if self.organization_id:
            headers["OpenAI-Organization"] = self.organization_id
        if self.project_id:
            headers["OpenAI-Project"] = self.project_id
            
        # Construct request payload
        payload = {
            "model": options.get("model", self.model),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": options.get("temperature", 0.7),
            "max_tokens": options.get("max_tokens", 2000),
            "top_p": options.get("top_p", 1.0),
            "frequency_penalty": options.get("frequency_penalty", 0.0),
            "presence_penalty": options.get("presence_penalty", 0.0)
        }
        
        # Add optional stop sequences if provided
        if "stop" in options:
            payload["stop"] = options["stop"]
            
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=options.get("timeout", 30)
                ) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        raise ProviderError(
                            f"OpenAI API error: {error_data.get('error', {}).get('message')}"
                        )
                        
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                    
            except aiohttp.ClientError as e:
                raise ProviderError(f"Failed to communicate with OpenAI API: {str(e)}")