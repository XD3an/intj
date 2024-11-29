from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
import logging

from core.config import settings

# Initialize the Ollama model
llm = Ollama(model=settings.model, base_url=settings.model_base_url)

# LangChain prompt template
prompt_template = """
You are an expert in IoT Network Security. Given the following context, answer the user's query with a clear and structured response. Ensure that your answer includes the current situation, relevant suggestions, and any further considerations.

### Context:
{context}

### User Query:
{query}

### Response:
1. **Current Situation**: Summarize the existing state of IoT network security based on the context.
2. **Suggestions**: Provide actionable recommendations for improving IoT network security.
3. **Further Considerations**: Mention any additional aspects, such as potential risks, compliance requirements, or best practices, that the user should consider.
"""

# Initialize the chain once during startup
chain = LLMChain(llm=llm, prompt=PromptTemplate(template=prompt_template, input_variables=["context", "query"]))

def preprocess_context(context: str) -> str:
    """Preprocess the context to ensure it's manageable for the model."""
    return context[:1000]  # Example: truncate to the first 1000 characters

def process_with_langchain(query: str, context: str = "") -> str:
    try:
        if context:
            # Preprocess the context to make it more manageable
            processed_context = preprocess_context(context)
            response = chain.run({"context": processed_context, "query": query})
            logging.info("Generated response successfully with template")
            return response.strip()
        else:
            response = chain.run({"context": "", "query": query})
            logging.info("Generated response successfully without context")
            return response.strip()
    except Exception as e:
        logging.error(f"Error while processing with LangChain: {e}")
        raise e