# Error Resolution Assistant - Kubernetes/DevOps Troubleshooting
# Finds matching errors from knowledge base and returns solutions

import os
import json
from openai import OpenAI
from difflib import SequenceMatcher

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================
# KNOWLEDGE BASE - Errors & Resolutions
# ============================================
knowledge_base = {
    "pod oom": {
        "error_name": "Pod Out Of Memory (OOM)",
        "description": "Pod is killed when it exceeds memory limits",
        "resolution": "Increase memory limits in pod spec or optimize application to use less memory",
        "commands": [
            "kubectl get pods -o jsonpath='{.items[*].status.containerStatuses[*].lastState.terminated.reason}'",
            "kubectl describe pod <pod-name>",
            "kubectl set resources deployment <name> --limits=memory=512Mi"
        ]
    },
    "crashloopbackoff": {
        "error_name": "CrashLoopBackOff",
        "description": "Container crashes and Kubernetes keeps restarting it",
        "resolution": "Check application logs for errors, fix the code/config, or increase startup time with initialDelaySeconds",
        "commands": [
            "kubectl logs <pod-name>",
            "kubectl logs <pod-name> --previous",
            "kubectl describe pod <pod-name>"
        ]
    },
    "imagepullbackoff": {
        "error_name": "ImagePullBackOff",
        "description": "Kubernetes cannot pull the container image from registry",
        "resolution": "Verify image name, tag, registry credentials, or ensure registry is accessible",
        "commands": [
            "kubectl describe pod <pod-name>",
            "kubectl create secret docker-registry <secret-name> --docker-server=<registry>",
            "kubectl set serviceaccount deployment <name> <service-account>"
        ]
    },
    "pending": {
        "error_name": "Pod Stuck in Pending",
        "description": "Pod cannot be scheduled on any node",
        "resolution": "Check node resources, labels/selectors, PVC availability, or resource requests",
        "commands": [
            "kubectl describe pod <pod-name>",
            "kubectl top nodes",
            "kubectl get events --sort-by='.lastTimestamp'"
        ]
    },
    "init:0": {
        "error_name": "Init:0 Container Status",
        "description": "Init container failed during startup sequence",
        "resolution": "Check init container logs to identify the failure, fix configuration, or dependencies",
        "commands": [
            "kubectl logs <pod-name> -c <init-container-name>",
            "kubectl describe pod <pod-name> | grep Init",
            "kubectl logs <pod-name> --previous"
        ]
    },
    "evicted": {
        "error_name": "Pod Evicted",
        "description": "Pod is forcibly removed due to node resource pressure",
        "resolution": "Increase node resources, optimize pod resource usage, or add more nodes",
        "commands": [
            "kubectl describe pod <pod-name> | grep Reason",
            "kubectl get events",
            "kubectl top pod <pod-name>"
        ]
    },
    "backoff": {
        "error_name": "Back-off Restarting Failed Container",
        "description": "Container fails repeatedly and Kubernetes increases wait time between restarts",
        "resolution": "Check application logs, fix startup issues, or increase startupProbe initialDelaySeconds",
        "commands": [
            "kubectl logs <pod-name>",
            "kubectl logs <pod-name> --tail=50",
            "kubectl describe pod <pod-name>"
        ]
    },
    "error": {
        "error_name": "Container in Error State",
        "description": "Generic container error - application exited with non-zero status",
        "resolution": "Review application logs, check exit code, verify environment variables and configuration",
        "commands": [
            "kubectl logs <pod-name>",
            "kubectl describe pod <pod-name>",
            "kubectl exec -it <pod-name> -- /bin/sh"
        ]
    },
    "cpu throttle": {
        "error_name": "CPU Throttling",
        "description": "Pod CPU usage exceeds limits and is being throttled",
        "resolution": "Increase CPU limits or optimize application performance",
        "commands": [
            "kubectl top pod <pod-name>",
            "kubectl set resources deployment <name> --limits=cpu=1000m",
            "kubectl describe pod <pod-name>"
        ]
    },
    "connection refused": {
        "error_name": "Connection Refused",
        "description": "Application cannot connect to service or external resource",
        "resolution": "Verify service exists, DNS resolution works, firewall rules, or network policies",
        "commands": [
            "kubectl get svc",
            "kubectl get networkpolicies",
            "kubectl exec -it <pod-name> -- nslookup <service-name>",
            "kubectl logs <pod-name>"
        ]
    }
}

# ============================================
# FUZZY MATCHING FUNCTION
# ============================================
def find_matching_error(user_error_message):
    """
    Find matching error in knowledge base using similarity matching
    Returns the best match if similarity > 0.5
    """
    user_error_lower = user_error_message.lower()
    best_match = None
    highest_similarity = 0
    
    for error_key, error_info in knowledge_base.items():
        # Check similarity with error key and error name
        similarity_key = SequenceMatcher(None, user_error_lower, error_key.lower()).ratio()
        similarity_name = SequenceMatcher(None, user_error_lower, error_info["error_name"].lower()).ratio()
        
        current_similarity = max(similarity_key, similarity_name)
        
        if current_similarity > highest_similarity:
            highest_similarity = current_similarity
            best_match = error_info
    
    # Return match if similarity is above threshold
    if highest_similarity > 0.4:
        return best_match, highest_similarity
    return None, 0

# ============================================
# AI-POWERED ERROR EXPLANATION
# ============================================
def enhance_resolution_with_ai(error_message, resolution_info):
    """
    Use AI to provide more context-specific resolution based on error details
    """
    prompt = f"""
You are a Kubernetes/DevOps expert. A user encountered this error:

ERROR: {error_message}

KNOWN SOLUTION: {resolution_info['resolution']}

Based on the error message and known solution, provide a brief, actionable resolution (2-3 sentences max).
Focus on immediate steps the user should take.

Return as JSON with key "ai_resolution".
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Kubernetes/DevOps troubleshooting expert. Always respond in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        content = response.choices[0].message.content
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        
        return json.loads(content)
    except Exception as e:
        return {"ai_resolution": f"Could not enhance resolution: {str(e)}"}

# ============================================
# MAIN ERROR RESOLUTION LOGIC
# ============================================
def resolve_error(error_message):
    """
    Main function to resolve user error
    """
    print("\n" + "="*60)
    print("🔍 SEARCHING KNOWLEDGE BASE...")
    print("="*60)
    
    # Find matching error
    matched_error, similarity = find_matching_error(error_message)
    
    if matched_error is None:
        print("\n❌ No matching error found in knowledge base")
        print(f"Try describing your error more clearly or check logs with: kubectl logs <pod-name>")
        return None
    
    print(f"\n✅ MATCH FOUND! (Confidence: {similarity:.0%})")
    print("\n" + "="*60)
    print("ERROR RESOLUTION")
    print("="*60)
    
    result = {
        "error_name": matched_error["error_name"],
        "description": matched_error["description"],
        "resolution": matched_error["resolution"],
        "debugging_commands": matched_error["commands"],
        "confidence": f"{similarity:.0%}"
    }
    
    # Enhance with AI if enabled
    print("\n🤖 Generating context-specific resolution...")
    ai_enhancement = enhance_resolution_with_ai(error_message, matched_error)
    result["ai_enhanced_resolution"] = ai_enhancement.get("ai_resolution", "")
    
    return result

# ============================================
# OUTPUT FORMATTING
# ============================================
def display_resolution(result):
    """
    Display resolution in a user-friendly format
    """
    if result is None:
        return
    
    print(f"\n📌 ERROR: {result['error_name']}")
    print(f"   Confidence: {result['confidence']}")
    print(f"\n📖 Description: {result['description']}")
    print(f"\n💡 Resolution: {result['resolution']}")
    if result['ai_enhanced_resolution']:
        print(f"\n🔧 AI Suggestion: {result['ai_enhanced_resolution']}")
    print(f"\n🛠️  Debugging Commands:")
    for i, cmd in enumerate(result['debugging_commands'], 1):
        print(f"   {i}. {cmd}")
    
    print("\n" + "="*60)
    
    return result

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("\n" + "🚀 "*20)
    print("ERROR RESOLUTION ASSISTANT - Kubernetes/DevOps")
    print("🚀 "*20)
    
    while True:
        print("\n1. Enter error message")
        print("2. View all known errors")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            error_msg = input("\n📝 Enter the error message you encountered:\n> ")
            if error_msg.strip():
                result = resolve_error(error_msg)
                display_resolution(result)
        
        elif choice == "2":
            print("\n" + "="*60)
            print("KNOWN ERRORS IN KNOWLEDGE BASE")
            print("="*60)
            for i, (key, info) in enumerate(knowledge_base.items(), 1):
                print(f"\n{i}. {info['error_name']}")
                print(f"   Pattern: {key}")
                print(f"   Quick Fix: {info['resolution']}")
        
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
