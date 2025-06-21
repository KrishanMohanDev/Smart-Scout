import time
import hashlib
from functools import lru_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from concurrent.futures import ThreadPoolExecutor

# Initialize global cache
response_cache = {}


def generate_cache_key(dom_content, parse_description):
    """Generate a unique cache key for the request"""
    combined = f"{dom_content[:1000]}{parse_description}"  # Use first 1000 chars to avoid huge keys
    return hashlib.md5(combined.encode()).hexdigest()



template = (
    "You are an AI assistant designed to provide friendly, detailed, and specific product information, just like a helpful salesperson. "
    "You will extract only the relevant information from the provided content{dom_content}. Here's how to respond: \n\n"
    "1. **Provide Complete Information:** When extracting information for: {parse_description}, provide the specific data along with helpful context or benefits. "
    "2. **Friendly and Descriptive Tone:** Offer your response in a conversational way, explaining why the feature is useful or beneficial to the user. "
    "3. **Add Context:** Include relevant details about performance, benefits, or use cases when appropriate. "
    "4. **If Nothing Matches:** If the information isn't available, respond courteously with, 'I'm sorry, I couldn't find any details matching your request.'\n"
    "5. **Structure:** Start with the direct answer, then add helpful context in the same sentence.\n"
    "Remember, your goal is to be informative, helpful and engaging like a knowledgeable salesperson."
)


# Initialize the AI model to be used in the pipeline.
# Here, "llama3.1" is the model being loaded. You can change it to other supported models if needed.
model = OllamaLLM(model="llama3.1")
# Alternative model : model = OllamaLLM(model="mistral")

def parse_with_ollama(dom_chunks, parse_description):
    """
    This function takes chunks of DOM (Document Object Model) content and a description of what to extract, 
    and returns parsed and summarized results.

    Parameters:
    - dom_chunks: List of chunks of content from the DOM to process.
    - parse_description: Description of the specific information to extract.

    Returns:
    - A string containing the extracted and validated product information or an error message if nothing matches.
    """
    # Check cache first
    cache_key = generate_cache_key("".join(dom_chunks), parse_description)
    if cache_key in response_cache:
        print("📋 Returning cached response")
        return response_cache[cache_key]

    print(f"🔍 Processing {len(dom_chunks)} chunks...")
    start_time = time.time()
    
    # Create a prompt using the previously defined template.
    prompt = ChatPromptTemplate.from_template(template)
    # Define a chain that connects the prompt and model for sequential execution.
    chain = prompt | model

    # parsed_results = []  # List to store the results from each chunk.
    
    # Process all chunks in parallel (single pass)
    with ThreadPoolExecutor(max_workers=min(len(dom_chunks), 4)) as executor:
        parsed_results = list(executor.map(
            lambda chunk: chain.invoke({
                "dom_content": chunk,
                "parse_description": parse_description
            }),
            dom_chunks
        ))
    
    # Filter non-empty results
    valid_results = [result.strip() for result in parsed_results if result.strip()]
    
    # Filter non-empty results
    valid_results = [result.strip()
                     for result in parsed_results if result.strip()]

    print(
        f"⚡ Parallel processing completed in {time.time() - start_time:.2f} seconds")

    if not valid_results:
        response = "I'm sorry, I couldn't find any details matching your request."
    else:
        # Combine results and validate
        combined_results = "\n".join(valid_results)
        response = validate_and_summarize(combined_results, parse_description)

    # Cache the response
    response_cache[cache_key] = response
    print(f"💾 Response cached with key: {cache_key[:8]}...")

    # Measure the total time taken for parsing.
    start_time = time.time()
    print(f"Chaining started...")
    
    return response



summary_template = """
You are a knowledgeable product expert providing detailed, helpful responses. Format your answers to be informative and engaging.

Rules:
- Start with the direct factual answer
- Add helpful context, benefits, or use cases in the same response
- Make it conversational and friendly
- Explain why the feature matters or how it benefits the user
- If information unavailable, simply state "Information not available"
- Keep responses informative but concise
- Make it sound like a helpful salesperson explaining the product but not more then 20 words

Information: {responses}
User Question: {question}

Detailed Response:"""


@lru_cache(maxsize=100)
def cached_validate_and_summarize(responses_hash, question):
    """Cached version of validate_and_summarize"""
    prompt = ChatPromptTemplate.from_template(summary_template)
    chain = prompt | model

    # Note: Using responses_hash as key but actual responses for processing
    # This is a simplified version - you may need to store actual responses separately
    result = chain.invoke({
        "responses": responses_hash,  # This needs to be the actual responses
        "question": question
    })

    # Clean unwanted prefixes
    unwanted_prefixes = [
        "based on the provided information",
        "here is the summarized",
        "here is a concise",
        "the information shows",
        "direct answer:",
        ":"
    ]

    cleaned_result = result.strip()
    for prefix in unwanted_prefixes:
        if cleaned_result.lower().startswith(prefix.lower()):
            cleaned_result = cleaned_result[len(prefix):].strip()
            if cleaned_result.startswith(":"):
                cleaned_result = cleaned_result[1:].strip()

    return cleaned_result


def validate_and_summarize(responses, question):
    """Main validation function that handles caching properly"""
    try:
        # Create hash for caching but use actual responses for processing
        responses_hash = hashlib.md5(responses.encode()).hexdigest()

        # For now, let's avoid the caching issue and process directly
        prompt = ChatPromptTemplate.from_template(summary_template)
        chain = prompt | model

        result = chain.invoke({
            "responses": responses,
            "question": question
        })

        # Clean unwanted prefixes
        unwanted_prefixes = [
            "based on the provided information",
            "here is the summarized",
            "here is a concise",
            "the information shows",
            "direct answer:",
            "detailed response:",
            ":"
        ]

        cleaned_result = result.strip()
        for prefix in unwanted_prefixes:
            if cleaned_result.lower().startswith(prefix.lower()):
                cleaned_result = cleaned_result[len(prefix):].strip()
                if cleaned_result.startswith(":"):
                    cleaned_result = cleaned_result[1:].strip()

        # Enhance the response if it's too basic
        enhanced_result = enhance_response(cleaned_result, question)

        return enhanced_result

    except Exception as e:
        print(f"Error in validate_and_summarize: {e}")
        return f"An error occurred while processing your request: {str(e)}"

def enhance_response(basic_response, question):
    """Enhance basic responses with context and benefits"""

    # Context mapping for common queries
    enhancement_map = {
        'ram': 'which provides excellent performance for heavy gaming, multitasking, and running multiple apps simultaneously',
        'memory': 'which provides excellent performance for heavy gaming, multitasking, and running multiple apps simultaneously',
        'storage': 'giving you plenty of space for photos, videos, apps, and files',
        'camera': 'perfect for capturing high-quality photos and videos',
        'battery': 'ensuring all-day usage without frequent charging',
        'processor': 'delivering smooth performance for all your tasks',
        'display': 'providing an immersive viewing experience',
        'price': 'offering great value for the features provided'
    }

    # Check if response is too basic (just a number or very short)
    if basic_response and len(basic_response.strip()) < 20:
        question_lower = question.lower()

        for key, enhancement in enhancement_map.items():
            if key in question_lower:
                if basic_response.strip().replace('GB', '').replace('MP', '').replace('$', '').strip().isdigit():
                    return f"This phone comes with {basic_response.strip()} {enhancement}."
                else:
                    return f"{basic_response.strip()} {enhancement}."

    return basic_response
