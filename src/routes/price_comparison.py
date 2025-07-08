from flask import Blueprint, request, jsonify
import asyncio
import json
import time
from typing import List, Dict, Any
from src.services.scraper_service import ScraperService
from src.services.llm_service import LLMService
from src.services.cache_service import CacheService

price_comparison_bp = Blueprint('price_comparison', __name__)

# Initialize services
scraper_service = ScraperService()
llm_service = LLMService()
cache_service = CacheService()

@price_comparison_bp.route('/test', methods=['GET'])
def test_route():
    """Test route to verify blueprint is working"""
    return jsonify({"message": "Price comparison blueprint is working!"})

@price_comparison_bp.route('/compare-prices', methods=['POST'])
def compare_prices():
    """
    Compare prices for a given product across multiple websites.
    
    Expected input:
    {
        "country": "US",
        "query": "iPhone 16 Pro, 128GB"
    }
    
    Returns:
    [
        {
            "link": "https://amazon.com/...",
            "price": "999",
            "currency": "USD",
            "productName": "Apple iPhone 16 Pro",
            "parameter1": "..."
        },
        ...
    ]
    """
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        country = data.get('country')
        query = data.get('query')
        
        if not country or not query:
            return jsonify({"error": "Both 'country' and 'query' are required"}), 400
        
        # For now, return mock data to test the frontend
        mock_products = [
            {
                "link": "https://amazon.com/iphone-16-pro",
                "price": "999",
                "currency": "USD",
                "productName": "Apple iPhone 16 Pro 128GB",
                "rating": "4.5",
                "reviewsCount": "1234",
                "source": "Amazon",
                "relevanceScore": 0.95
            },
            {
                "link": "https://amazon.com/iphone-16-pro-alt",
                "price": "1099",
                "currency": "USD", 
                "productName": "Apple iPhone 16 Pro 128GB (Different Seller)",
                "rating": "4.3",
                "reviewsCount": "567",
                "source": "Amazon",
                "relevanceScore": 0.90
            }
        ]
        
        return jsonify(mock_products)
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@price_comparison_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": time.time()})

