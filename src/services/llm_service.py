import json
import re
from typing import List, Dict, Any
from openai import OpenAI
import os

class LLMService:
    def __init__(self):
        # Initialize OpenAI client
        # For demo purposes, we'll use a mock implementation
        # In production, you would set up your OpenAI API key
        self.client = None
        self.use_mock = True  # Set to False when you have an API key
        
        # Try to initialize OpenAI if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.use_mock = False

    def process_products(self, query: str, raw_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw scraped products using LLM for matching, extraction, and ranking.
        """
        if self.use_mock:
            return self._mock_process_products(query, raw_products)
        else:
            return self._llm_process_products(query, raw_products)

    def _mock_process_products(self, query: str, raw_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Mock implementation for product processing when LLM is not available.
        """
        processed_products = []
        
        for product in raw_products:
            # Simple keyword matching for relevance
            relevance_score = self._calculate_relevance(query, product.get('productName', ''))
            
            # Only include products with reasonable relevance
            if relevance_score > 0.3:
                processed_product = {
                    'link': product.get('link', ''),
                    'price': product.get('price', '0'),
                    'currency': product.get('currency', 'USD'),
                    'productName': product.get('productName', ''),
                    'rating': product.get('rating'),
                    'reviewsCount': product.get('reviewsCount'),
                    'source': product.get('source', 'Amazon'),
                    'relevanceScore': relevance_score
                }
                processed_products.append(processed_product)
        
        # Sort by relevance score (descending) and then by price (ascending)
        processed_products.sort(key=lambda x: (-x['relevanceScore'], float(x['price'])))
        
        return processed_products

    def _llm_process_products(self, query: str, raw_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Use LLM to process products for better matching and ranking.
        """
        try:
            # Prepare prompt for LLM
            prompt = self._create_processing_prompt(query, raw_products)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a product matching and ranking expert. Your task is to analyze scraped product data and determine which products best match the user's query, then rank them appropriately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            # Parse LLM response
            result = response.choices[0].message.content
            processed_products = self._parse_llm_response(result)
            
            return processed_products
            
        except Exception as e:
            print(f"Error using LLM: {e}")
            # Fallback to mock processing
            return self._mock_process_products(query, raw_products)

    def _create_processing_prompt(self, query: str, raw_products: List[Dict[str, Any]]) -> str:
        """
        Create a prompt for the LLM to process products.
        """
        products_json = json.dumps(raw_products, indent=2)
        
        prompt = f"""
        User Query: "{query}"
        
        Scraped Products:
        {products_json}
        
        Please analyze these products and:
        1. Determine which products actually match the user's query
        2. Rank them by relevance to the query and overall value (considering price, rating, reviews)
        3. Return only the products that are good matches
        
        Return the result as a JSON array with the same structure, but add a "relevanceScore" field (0-1) and ensure products are sorted by relevance and value.
        
        Only return the JSON array, no additional text.
        """
        
        return prompt

    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse the LLM response to extract processed products.
        """
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # If no JSON found, try to parse the entire response
                return json.loads(response)
        except json.JSONDecodeError:
            print("Error parsing LLM response as JSON")
            return []

    def _calculate_relevance(self, query: str, product_name: str) -> float:
        """
        Simple relevance calculation based on keyword matching.
        """
        if not query or not product_name:
            return 0.0
        
        query_words = set(query.lower().split())
        product_words = set(product_name.lower().split())
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        query_words -= common_words
        product_words -= common_words
        
        if not query_words:
            return 0.0
        
        # Calculate intersection
        intersection = query_words.intersection(product_words)
        
        # Calculate relevance score
        relevance = len(intersection) / len(query_words)
        
        # Boost score if product name contains exact query phrases
        if query.lower() in product_name.lower():
            relevance += 0.3
        
        return min(relevance, 1.0)

