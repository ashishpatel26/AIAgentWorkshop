import streamlit as st
import pandas as pd
from typing import Union, List, Dict
from groq import Groq
import os
from duckduckgo_search import DDGS

class DuckDuckGoSearch:
    """
    Custom DuckDuckGo search implementation with robust error handling and result processing.
    Uses the duckduckgo_search library to fetch and format news results.
    """
    def __init__(self):
        # Initialize the DuckDuckGo search session
        self.ddgs = DDGS()
    
    def __call__(self, query: str, max_results: int = 5) -> str:
        try:
            # Perform the search and get results
            # The news method is more appropriate for recent news analysis
            search_results = list(self.ddgs.news(
                query,
                max_results=max_results,
                region='wt-wt',  # Worldwide results
                safesearch='on'
            ))
            
            if not search_results:
                return "No results found. Try modifying your search query."
            
            # Format the results into a readable string
            formatted_results = []
            for idx, result in enumerate(search_results, 1):
                # Extract available fields with fallbacks for missing data
                title = result.get('title', 'No title available')
                snippet = result.get('body', result.get('snippet', 'No description available'))
                source = result.get('source', 'Unknown source')
                url = result.get('url', result.get('link', 'No link available'))
                date = result.get('date', 'Date not available')
                
                # Format each result with available information
                formatted_results.append(
                    f"{idx}. Title: {title}\n"
                    f"   Date: {date}\n"
                    f"   Source: {source}\n"
                    f"   Summary: {snippet}\n"
                    f"   URL: {url}\n"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            # Provide detailed error information for debugging
            error_msg = f"Search error: {str(e)}\nTry again with a different search term or check your internet connection."
            print(f"DuckDuckGo search error: {str(e)}")  # For logging
            return error_msg

class GroqLLM:
    """
    LLM interface using Groq's LLama model.
    Handles API communication and response processing.
    """
    def __init__(self, model_name="deepseek-r1-distill-llama-70b"):
        self.client = Groq(api_key="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")
        self.model_name = model_name
    
    def __call__(self, prompt: Union[str, dict, List[Dict]]) -> str:
        try:
            # Convert prompt to string if it's a complex structure
            prompt_str = str(prompt) if isinstance(prompt, (dict, list)) else prompt
            
            # Make API call to Groq
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": prompt_str
                }],
                temperature=0.7,
                max_tokens=1024,
                stream=False
            )
            
            return completion.choices[0].message.content if completion.choices else "Error: No response generated"
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)  # For logging
            return error_msg

def create_analysis_prompt(topic: str, search_results: str) -> str:
    """
    Creates a detailed prompt for news analysis, structuring the request
    to get comprehensive and well-organized results from the LLM.
    """
    return f"""Analyze the following news information about {topic}. 
    Search Results: {search_results}
    
    Please provide a comprehensive analysis including:
    1. Key Points Summary:
       - Main events and developments
       - Critical updates and changes
    
    2. Stakeholder Analysis:
       - Primary parties involved
       - Their roles and positions
    
    3. Impact Assessment:
       - Immediate implications
       - Potential long-term effects
       - Broader context and significance
    
    4. Multiple Perspectives:
       - Different viewpoints on the issue
       - Areas of agreement and contention
    
    5. Fact Check & Reliability:
       - Verification of major claims
       - Consistency across sources
       - Source credibility assessment
    
    Please format the analysis in a clear, journalistic style with section headers."""

def log_agent_activity(prompt: str, result: str, agent_name: str):
    """
    Creates an expandable log of agent activities in the Streamlit interface
    for transparency and debugging purposes.
    """
    with st.expander("View Agent Activity Log"):
        st.write(f"### Agent Activity ({agent_name}):")
        st.write("**Input Prompt:**")
        st.code(prompt, language="text")
        st.write("**Analysis Output:**")
        st.code(result, language="text")

# Initialize Streamlit app
st.set_page_config(page_title="News Analysis Tool", layout="wide")

# Title and description
st.title("🔍 AI News Analysis Tool")
st.write("""
This tool combines the power of Groq's 🐬DeepSeek-r1 Instant model with DuckDuckGo 
search to provide in-depth news analysis. Get comprehensive insights and multiple 
perspectives on any news topic.
""")

# Initialize the components
try:
    # Initialize LLM and search tool
    llm = GroqLLM()
    search_tool = DuckDuckGoSearch()
    
    # Input section
    news_topic = st.text_input(
        "Enter News Topic or Query:",
        placeholder="E.g., Recent developments in renewable energy"
    )
    
    # Analysis options
    col1, col2 = st.columns(2)
    with col1:
        search_depth = st.slider(
            "Search Depth (number of results)",
            min_value=3,
            max_value=10,
            value=5
        )
    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Comprehensive", "Quick Summary", "Technical", "Simplified"]
        )
    
    # Generate analysis button
    if st.button("Analyze News"):
        if news_topic:
            with st.spinner("Gathering information and analyzing..."):
                try:
                    # Show search progress
                    search_placeholder = st.empty()
                    search_placeholder.info("Searching for recent news...")
                    
                    # Perform search
                    search_results = search_tool(
                        f"Latest news about {news_topic} last 7 days",
                        max_results=search_depth
                    )
                    
                    if not search_results.startswith(("Search error", "No results")):
                        # Update progress
                        search_placeholder.info("Analyzing search results...")
                        
                        # Create analysis prompt
                        analysis_prompt = create_analysis_prompt(news_topic, search_results)
                        
                        # Get analysis from LLM
                        analysis_result = llm(analysis_prompt)
                        
                        # Clear progress messages
                        search_placeholder.empty()
                        
                        # Display results
                        st.subheader("📊 Analysis Results")
                        st.markdown(analysis_result)
                        
                        # Log the activity
                        log_agent_activity(
                            analysis_prompt,
                            analysis_result,
                            "News Analysis Agent"
                        )
                    else:
                        search_placeholder.empty()
                        st.error(search_results)
                        
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
        else:
            st.warning("Please enter a news topic to analyze.")

    # Add helpful tips
    with st.expander("💡 Tips for Better Results"):
        st.write("""
        - Be specific with your topic for more focused analysis
        - Use keywords related to recent events for timely information
        - Consider including timeframes in your query
        - Try different analysis types for various perspectives
        - For complex topics, start with a broader search and then narrow down
        """)

except Exception as e:
    st.error(f"""
    Failed to initialize the application: {str(e)}
    
    Please ensure:
    1. Your GROQ_API_KEY is properly set in environment variables
    2. All required packages are installed:
       - pip install streamlit groq duckduckgo-search
    3. You have internet connectivity for DuckDuckGo searches
    """)

# Footer
st.markdown("---")
st.caption(
    "Powered by Groq LLama 3.1 8B Instant, DuckDuckGo, and Streamlit | "
    "Created for news analysis and research purposes"
)
