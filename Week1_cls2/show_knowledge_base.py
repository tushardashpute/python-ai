#!/usr/bin/env python3
"""
Simple test without emojis - for demonstrating functionality
"""
from error_resolution_assistant import knowledge_base

print("\n" + "="*80)
print("ERROR RESOLUTION ASSISTANT - KNOWLEDGE BASE")
print("="*80)

print(f"\nTotal Errors in Knowledge Base: {len(knowledge_base)}\n")

for i, (key, info) in enumerate(knowledge_base.items(), 1):
    print(f"{i:2d}. {info['error_name']:<30}")
    print(f"    Description: {info['description']}")
    print(f"    Fix: {info['resolution']}")
    print()

print("="*80)
print("\nKNOWN ERROR PATTERNS:")
print("="*80)

patterns = {
    "oom": "Out of Memory Errors",
    "crash": "Container Crash Issues",
    "pull": "Image Pull Failures",
    "pending": "Scheduling Issues",
    "connection": "Network/Service Issues",
}

for pattern, category in patterns.items():
    matching = [k for k in knowledge_base.keys() if pattern.lower() in k.lower()]
    if matching:
        print(f"\n{category}:")
        for match in matching:
            print(f"  - {match}")

print("\n" + "="*80)
print("To use the assistant, run: python error_resolution_assistant.py")
print("="*80)
