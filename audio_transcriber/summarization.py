import os
import configparser
from datetime import datetime
from openai import OpenAI
from pathlib import Path

class TranscriptionSummarizer:
    """Summarizes transcriptions using OpenAI's GPT-4o model."""
    
    def __init__(self, transcription_file: str, output_dir: str = "output", config_file: str = "config.ini"):
        self.transcription_file = transcription_file
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load configuration
        self.config = configparser.ConfigParser()
        
        # Check if config file exists
        if os.path.exists(config_file):
            self.config.read(config_file)
        
        # Get OpenAI parameters from config or environment variables
        self.api_key = self._get_config_value("openai_api_key", "OPENAI_API_KEY")
        self.model = self._get_config_value("openai_model", "OPENAI_MODEL", "gpt-4o")
        
        # Parse temperature as float
        temp_str = self._get_config_value("openai_temperature", "OPENAI_TEMPERATURE", "0.3")
        try:
            self.temperature = float(temp_str)
        except ValueError:
            print(f"Invalid temperature value: {temp_str}, using default 0.3")
            self.temperature = 0.3
            
        if not self.api_key:
            raise ValueError("OpenAI API key is not set. Set it in config.ini or OPENAI_API_KEY environment variable.")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def _get_config_value(self, config_key: str, env_var: str, default: str = None) -> str:
        """Get a configuration value from config file or environment variable.
        
        Args:
            config_key: The key in the config file
            env_var: The environment variable name
            default: Default value if neither is set
            
        Returns:
            The configuration value
        """
        # Try to get from environment first (highest priority)
        value = os.getenv(env_var)
        
        # If not in environment, try config file
        if not value and self.config.has_option("DEFAULT", config_key):
            value = self.config["DEFAULT"][config_key]
            
            # Handle environment variable references in config
            if value.startswith("${") and value.endswith("}"):
                env_name = value[2:-1]
                value = os.getenv(env_name, "")
        
        # If still not found, use default
        if not value:
            value = default
            
        return value
    
    def summarize(self) -> str:
        """Summarize the transcription using OpenAI GPT."""
        # Read the transcription file
        with open(self.transcription_file, 'r', encoding='utf-8') as f:
            transcription_text = f.read()
            
        # Create OpenAI client
        client = OpenAI(api_key=self.api_key)
        
        # The prompt for summarization
        prompt = """Create a summary highlighting the key points from a conversation transcription divided by speaker roles.

The text is in Russian. Focus on extracting the main ideas exchanged in the discussion, highlighting any significant decisions, insights, or action items.

# Steps

1. **Review the transcription:** Carefully read through the entire transcription to understand the context of the conversation.
2. **Identify Key Points:** Look for recurring themes, important decisions, challenges discussed, strategies proposed, or any conclusions reached.
3. **Summarize by Speaker:** Briefly summarize each speaker's contribution, focusing on their main points and how they relate to the overall conversation.
4. **Synthesize Information:** Combine the speakers' contributions into a cohesive summary, ensuring it conveys the essential elements of the conversation without losing critical details.

# Output Format

The output should be a concise paragraph summarizing the key points of the conversation. It should include:
- A clear overview of the discussion context.
- Main themes and insights.
- Any decisions or conclusions made.
- Important details mentioned by the speakers.

# Notes

- Focus on clarity and conciseness, avoiding excessive detail.
- Ensure the summary reflects the Russian context and nuances accurately.
- Avoid using colloquial language or overly complex sentences for readability.

Here is the transcription to summarize:

"""
        
        # Complete the prompt with the transcription
        full_prompt = prompt + transcription_text
        
        try:
            # Call the OpenAI API
            print(f"Using OpenAI model: {self.model}, temperature: {self.temperature}")
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in summarizing conversations in Russian."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature
            )
            
            summary = response.choices[0].message.content
            
            # Save summary to file
            summary_file = os.path.join(self.output_dir, f"summary_{self.timestamp}.txt")
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
                
            print(f"Summary saved to: {summary_file}")
            return summary_file
            
        except Exception as e:
            print(f"Error during summarization: {str(e)}")
            raise 