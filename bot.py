import os
import logging
import requests
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BotService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("Groq API key not found!")
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        self.model_name = os.getenv("MODEL_NAME", "llama3-8b-8192")
        logger.info(f"Using model: {self.model_name}")
            
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        logger.info("Initializing BotService with Groq...")
        
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

    def process_message(self, user_message: str, context: Optional[List[Dict[str, str]]] = None) -> Dict:
        try:
            logger.info("Processing message: %s", user_message)
            
            # Prepare messages array
            messages = [
                {"role": "system", "content": self.system_prompt},
            ]
            
            # Add context if provided
            if context:
                for msg in context:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    messages.append({"role": role, "content": content})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Send request to Groq
            logger.info("Sending request to Groq")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "top_p": 1,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                error_msg = f"Groq API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']['message']}"
                except:
                    pass
                raise Exception(error_msg)
            
            response_data = response.json()
            if not response_data.get("choices"):
                raise ValueError("Empty response received from Groq")
                
            response_content = response_data["choices"][0]["message"]["content"]
            logger.info("Received response from Groq")
            
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
            
    def debug_code(self, code: str, language: str) -> Dict:
        try:
            logger.info("Debugging code in %s", language)
            
            debug_prompt = f"""Please analyze this {language} code and provide:
1. Any syntax errors
2. Logical errors or bugs
3. Suggested improvements
4. A corrected version if needed

Here's the code:
```{language}
{code}
```"""
            
            # Send request to Groq
            logger.info("Sending request to Groq")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are an expert code debugger."},
                        {"role": "user", "content": debug_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "top_p": 1,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                error_msg = f"Groq API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']['message']}"
                except:
                    pass
                raise Exception(error_msg)
            
            response_data = response.json()
            if not response_data.get("choices"):
                raise ValueError("Empty response received from Groq")
                
            response_content = response_data["choices"][0]["message"]["content"]
            logger.info("Received response from Groq")
            
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
            
    def optimize_code(self, code: str, language: str) -> Dict:
        try:
            logger.info("Optimizing code in %s", language)
            
            optimize_prompt = f"""Please analyze this {language} code for optimization and provide:
1. Performance bottlenecks
2. Algorithmic improvements
3. Best practices recommendations
4. An optimized version of the code

Here's the code:
```{language}
{code}
```"""
            
            # Send request to Groq
            logger.info("Sending request to Groq")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": "You are an expert code optimizer."},
                        {"role": "user", "content": optimize_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "top_p": 1,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                error_msg = f"Groq API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']['message']}"
                except:
                    pass
                raise Exception(error_msg)
            
            response_data = response.json()
            if not response_data.get("choices"):
                raise ValueError("Empty response received from Groq")
                
            response_content = response_data["choices"][0]["message"]["content"]
            logger.info("Received response from Groq")
            
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