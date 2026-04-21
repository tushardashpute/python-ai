#!/usr/bin/env python3
"""
Demo: Error Resolution Assistant in Action
Shows how the system matches errors and returns solutions
"""

from error_resolution_assistant import resolve_error, display_resolution, knowledge_base

print("\n" + "="*80)
print(" "*20 + "ERROR RESOLUTION ASSISTANT - DEMO")
print("="*80)

print("\n📚 KNOWLEDGE BASE SUMMARY:")
print("-"*80)
print(f"Total Errors Tracked: {len(knowledge_base)}\n")

for i, (key, info) in enumerate(knowledge_base.items(), 1):
    print(f"{i:2d}. {info['error_name']:<30} | Key: {key}")

print("\n" + "="*80)
print("DEMO: Testing Real Error Messages")
print("="*80)

# Demo test cases
test_cases = [
    ("My pod keeps getting OOM killed", "Testing OOM detection"),
    ("CrashLoopBackOff on deployment", "Testing crash loop detection"),
    ("Cannot pull image from docker registry", "Testing image pull failure"),
    ("Pod stuck in pending state", "Testing pending state"),
    ("Connection refused when accessing service", "Testing connection errors"),
]

for error_message, test_name in test_cases:
    print(f"\n\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"Input: {error_message}")
    print('='*80)
    
    result = resolve_error(error_message)
    
    if result:
        print(f"\n✅ MATCHED: {result['error_name']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"\n📖 What it means:")
        print(f"   {result['description']}")
        print(f"\n💡 Quick Fix:")
        print(f"   {result['resolution']}")
        print(f"\n🤖 AI Suggestion:")
        print(f"   {result['ai_enhanced_resolution']}")
        print(f"\n🛠️  Top Debugging Commands:")
        for cmd in result['debugging_commands'][:2]:
            print(f"   → {cmd}")
    else:
        print("❌ No matching error found")

print("\n\n" + "="*80)
print("✅ DEMO COMPLETED")
print("="*80)
print("\nTo use the interactive mode, run:")
print("  python error_resolution_assistant.py")
print("\nTo view the full user guide:")
print("  cat ERROR_RESOLUTION_GUIDE.md")
