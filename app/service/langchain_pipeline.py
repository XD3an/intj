from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
import logging

from core.config import settings

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("./logs/langchain.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class INTJPromptChain:
    def __init__(self, model: str = settings.model, base_url: str = settings.model_base_url):
        # Initialize the Ollama model
        self.llm = Ollama(
            model=model, 
            base_url=base_url,
            temperature=0.8,  # Adjust creativity
            top_p=0.9,  # Nucleus sampling
        )
        
        # Prompt template with more structured guidance
        self.prompt_template = PromptTemplate(
            template="""
            🐶🔒 INTJ: An LLM based IoT Network Threat Journeyman 🔒🐶

            ### Operational Context:
            {context}

            ### Chat History:
            {chat_history}

            ### Current Objective:
            {query}

            ### Response Guidelines:
            1. Provide technically precise analysis
            2. Focus on actionable security insights
            3. Explain potential threat vectors
            4. Recommend concrete mitigation strategies
            """,
            input_variables=["context", "chat_history", "query"]
        )
        
        # Initialize the chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            verbose=True
        )

    def process_query(self, query: str, context: str = "", chat_history: str = "") -> str:
        """
        Process query and return the response
        """
        try:
            # Run the chain
            response = self.chain.run({
                "context": context,
                "chat_history": chat_history,
                "query": query
            })
            
            # Log successful response
            logger.info(f"Successfully processed query: {query[:50]}...")
            return response.strip()
        
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return f"Error processing query: {str(e)}"

# Singleton instance for global use
INTJ_prompt_chain = INTJPromptChain()

def process_with_langchain(query: str, context: str = "", chat_history: str = "") -> str:
    """
    Wrapper function maintaining current interface
    """
    return INTJ_prompt_chain.process_query(query, context, chat_history)