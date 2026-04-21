#!/usr/bin/env python3
# Test script for error resolution assistant

import sys
sys.path.append('.')

from error_resolution_assistant import resolve_error, display_resolution

# Test cases
test_errors = [
    "My pod keeps crashing - CrashLoopBackOff error",
    "Container failed to pull image from registry",
    "Pod is stuck in pending state",
    "Getting Out of Memory error"
]

print("\n" + "="*70)
print("TESTING ERROR RESOLUTION ASSISTANT")
print("="*70)

for error in test_errors:
    print(f"\n\n🧪 TEST: {error}")
    result = resolve_error(error)
    display_resolution(result)
