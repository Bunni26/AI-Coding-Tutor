import os
import logging
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"
        logger.info("Initializing ChatService with Ollama...")
        
        # Test Ollama connection
        try:
            response = requests.get(f"{self.base_url}/tags")
            if response.status_code == 200:
                logger.info("Successfully connected to Ollama")
            else:
                raise Exception(f"Failed to connect to Ollama: {response.status_code}")
        except Exception as e:
            logger.error("Error connecting to Ollama: %s", str(e))
            raise ValueError(f"Error connecting to Ollama: {str(e)}")
        
        self.system_prompt = """You are an AI Coding Tutor, designed to help users learn programming concepts and solve coding problems. Your role is to:

1. Provide clear, concise explanations of programming concepts
2. Help debug code issues with step-by-step guidance
3. Suggest best practices and coding standards
4. Offer code examples and explanations
5. Guide users through problem-solving approaches
6. Explain the reasoning behind your suggestions

When helping users:
- Break down complex concepts into simpler parts
- Use relevant code examples
- Explain the "why" behind your suggestions
- Encourage good coding practices
- Be patient and supportive
- Ask clarifying questions when needed
- Provide resources for further learning

Remember to:
- Be clear and concise
- Use proper code formatting
- Explain technical terms
- Encourage problem-solving skills
- Promote best practices
- Be encouraging and supportive"""

    def process_message(self, user_message, context=None):
        try:
            logger.info("Processing message: %s", user_message)
            
            # Prepare the prompt with context
            full_prompt = self.system_prompt + "\n\n"
            
            if context:
                for msg in context:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    full_prompt += f"{role}: {content}\n"
            
            full_prompt += f"user: {user_message}"
            
            # Send request to Ollama
            logger.info("Sending request to Ollama")
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": "mistral",
                    "prompt": full_prompt,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code}")
                
            response_data = response.json()
            response_content = response_data.get("response", "")
            
            if not response_content:
                raise ValueError("Empty response received from Ollama")
            
            logger.info("Received response from Ollama")
            
            # Format the response
            formatted_response = {
                "response": response_content,
                "type": "chat",
                "context": context or []
            }
            
            return formatted_response
            
        except Exception as e:
            logger.error("Error processing message: %s", str(e))
            return {
                "error": str(e),
                "type": "error"
            } 