import os
import logging
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"
        logger.info("Initializing CodeService with Ollama...")
        
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
        
        self.debug_prompt = """You are an expert code debugger. Analyze the following code and:
        1. Identify any syntax errors
        2. Find logical errors
        3. Suggest improvements
        4. Provide a corrected version of the code
        
        Code language: {language}
        Code to debug:
        {code}
        """
        
        self.optimize_prompt = """You are an expert code optimizer. Analyze the following code and:
        1. Identify performance bottlenecks
        2. Suggest algorithmic improvements
        3. Recommend best practices
        4. Provide an optimized version of the code
        
        Code language: {language}
        Code to optimize:
        {code}
        """

    def debug_code(self, code, language):
        try:
            logger.info("Debugging code in %s", language)
            
            # Prepare the prompt
            full_prompt = self.debug_prompt.format(
                language=language,
                code=code
            )
            
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
                "analysis": response_content,
                "type": "debug",
                "original_code": code,
                "language": language
            }
            
            return formatted_response
            
        except Exception as e:
            logger.error("Error debugging code: %s", str(e))
            return {
                "error": str(e),
                "type": "error"
            }

    def optimize_code(self, code, language):
        try:
            logger.info("Optimizing code in %s", language)
            
            # Prepare the prompt
            full_prompt = self.optimize_prompt.format(
                language=language,
                code=code
            )
            
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
                "analysis": response_content,
                "type": "optimize",
                "original_code": code,
                "language": language
            }
            
            return formatted_response
            
        except Exception as e:
            logger.error("Error optimizing code: %s", str(e))
            return {
                "error": str(e),
                "type": "error"
            } 