import warnings
warnings.filterwarnings("ignore")

import os
import json
fromc import BaseModel, Field typing import List, Optional, Dict
from pydanti
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# LangChain setup
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from langchain.prompts import ChatPromptTemplate            
from langchain.schema.output_parser import StrOutputParser  
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.runnable import RunnableMap, RunnableLambda, RunnablePassthrough
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.prompts import MessagesPlaceholder

# LangGraph setup
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults

# Default configuration
DEFAULT_CONFIG = {
    "active_model": "openai",  # Which model to use by default
    "models": {
        "openai": {
            "model_name": "gpt-4o-mini",
            "api_key_env": "OPENAI_API_KEY"
        },
        "groq": {
            "model_name": "llama-3.3-70b-versatile",
            "api_key_env": "GROQ_API_KEY"
        },
        "google": {
            "model_name": "gemini-1.5-flash",
            "api_key_env": "GOOGLE_API_KEY"
        },
        "huggingface": {
            "repo_id": "meta-llama/Llama-3.3-70B-Instruct",
            "api_key_env": "HUGGINGFACE_API_KEY"
        }
    }
}

def load_config():
    """Load configuration from config.json if it exists, otherwise use defaults"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                logger.info("Loaded configuration from config.json")
                # Merge user config with defaults
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            logger.warning(f"Error loading config.json: {e}. Using default configuration.")
            return DEFAULT_CONFIG
    else:
        logger.info("No config.json found. Using default configuration.")
        return DEFAULT_CONFIG

def create_sample_config():
    """Create a sample config.json file if it doesn't exist"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    if not os.path.exists(config_path):
        try:
            with open(config_path, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            logger.info("Created sample config.json file")
        except Exception as e:
            logger.warning(f"Could not create sample config.json: {e}")

def initialize_model(config):
    """Initialize the model based on configuration"""
    active_model = config["active_model"]
    models_config = config["models"]
    
    if active_model not in models_config:
        logger.error(f"Active model '{active_model}' not found in configuration")
        raise ValueError(f"Model '{active_model}' not configured")
    
    model_config = models_config[active_model]
    
    # Check for API key
    api_key_env = model_config.get("api_key_env")
    api_key = os.environ.get(api_key_env)
    
    if not api_key and api_key_env:
        logger.warning(f"API key environment variable {api_key_env} not set")
    
    # Initialize the appropriate model
    try:
        if active_model == "openai":
            return ChatOpenAI(
                model=model_config.get("model_name", "gpt-4o-mini"),
                api_key=api_key,
                cache=False
            )
        elif active_model == "groq":
            return ChatGroq(
                model=model_config.get("model_name", "llama-3.3-70b-versatile"),
                api_key=api_key
            )
        elif active_model == "google":
            return ChatGoogleGenerativeAI(
                model=model_config.get("model_name", "gemini-1.5-flash"),
                google_api_key=api_key
            )
        elif active_model == "huggingface":
            hf_endpoint = HuggingFaceEndpoint(
                repo_id=model_config.get("repo_id", "meta-llama/Llama-3.3-70B-Instruct"),
                token=api_key
            )
            return ChatHuggingFace(llm=hf_endpoint)
        else:
            logger.error(f"Unknown model type: {active_model}")
            raise ValueError(f"Unknown model type: {active_model}")
    except Exception as e:
        logger.error(f"Error initializing {active_model} model: {e}")
        raise

# Load configuration
config = load_config()

# Create sample config file if it doesn't exist
create_sample_config()

# Initialize the main model
try:
    model_gpt = initialize_model(config)
    logger.info(f"Successfully initialized model: {config['active_model']}")
except Exception as e:
    logger.error(f"Failed to initialize model: {e}")
    logger.warning("Falling back to default OpenAI model")
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    model_gpt = ChatOpenAI(model="gpt-4o-mini", cache=False)

# For backward compatibility - initialize other model variables
# These will point to the same model instance, but preserved for compatibility
model_gemini = model_gpt
model_llama = model_gpt
model_mistral = model_gpt
model_llama_vision = model_gpt


