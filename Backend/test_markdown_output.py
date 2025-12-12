#!/usr/bin/env python3
"""Test script to verify improved markdown menu presentation"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

try:
    print("Testing food agent with menu query...")
    from Backend.agents.food_agent import food_agent
    
    # Test with a menu query
    response = food_agent.run("Show me all available pizzas and pasta dishes")
    
    print("\n" + "="*80)
    print("AGENT RESPONSE (Markdown Output):")
    print("="*80)
    print(response.content)
    print("="*80)
    print("\n✅ Agent test completed successfully!")
    
except Exception as e:
    print(f"❌ Error during agent test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
