from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
import logging
import tiktoken

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
        
        # Advanced memory management
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="query"
        )
        
        # Prompt template with more structured guidance
        self.prompt_template = PromptTemplate(
            template="""
            🔒 INTJ: An LLM based IoT Network Threat Journeyman 🔒

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
            memory=self.memory,
            verbose=True
        )

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count using tiktoken
        Supports more accurate context management
        """
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"Token counting failed: {e}")
            return len(text.split())

    def preprocess_context(self, context: str, max_tokens: int = 1000) -> str:
        """
        Intelligent context preprocessing
        - Truncates context based on token count
        - Preserves most relevant information
        """
        if not context:
            return ""
        
        tokens = self.count_tokens(context)
        if tokens <= max_tokens:
            return context
        
        # Truncate intelligently
        truncated_context = context[:max_tokens * 4]  # Rough estimate
        logger.info(f"Context truncated from {tokens} to {self.count_tokens(truncated_context)} tokens")
        return truncated_context

    def process_query(self, query: str, context: str = "") -> str:
        """
        Process query with enhanced error handling and logging
        """
        try:
            # Preprocess context
            processed_context = self.preprocess_context(context)
            
            # Run the chain
            response = self.chain.run({
                "context": processed_context,
                "query": query
            })
            
            # Log successful response
            logger.info(f"Successfully processed query: {query[:50]}...")
            return response.strip()
        
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            return f"Error processing query: {str(e)}"

    def reset_memory(self):
        """Reset conversation memory"""
        self.memory.clear()

# Singleton instance for global use
INJT_prompt_chain = INTJPromptChain()

def process_with_langchain(query: str, context: str = "") -> str:
    """
    Wrapper function maintaining current interface
    """
    return INJT_prompt_chain.process_query(query, context)