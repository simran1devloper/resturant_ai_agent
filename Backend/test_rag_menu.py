#!/usr/bin/env python3
"""Test RAG-based menu retrieval without API server"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

try:
    print("Testing food agent with RAG-only menu queries...\n")
    from Backend.agents.food_agent import food_agent
    
    # Test queries
    test_queries = [
        "Show me all available pizzas",
        "What vegetarian dishes do you have?",
        "Recommend a spicy dish under ₹300"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {query}")
        print('='*80)
        
        response = food_agent.run(query)
        print(response.content)
        print('='*80)
    
    print("\n✅ All RAG menu tests completed successfully!")
    print("💡 The agent can now answer menu queries without the API server running!")
    
except Exception as e:
    print(f"❌ Error during RAG test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
