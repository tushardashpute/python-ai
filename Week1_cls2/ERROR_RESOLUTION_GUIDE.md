# Error Resolution Assistant - User Guide

## Overview
The **Error Resolution Assistant** helps troubleshoot Kubernetes/DevOps errors by:
1. ✅ Matching your error against a knowledge base
2. 🔍 Finding the best matching error pattern
3. 💡 Returning immediate resolutions
4. 🤖 Using AI to provide context-specific suggestions
5. 🛠️ Suggesting debugging commands

---

## How It Works

### Step 1: User Provides Error Message
```
User enters: "My pod is out of memory"
```

### Step 2: Fuzzy Matching Against Knowledge Base
```
The system searches the knowledge base and finds:
- Exact matches (100% confidence)
- Partial matches (fuzzy matching with ~40%+ threshold)
```

### Step 3: AI Enhancement
```
AI analyzes the error context and provides:
- Immediate action items
- Root cause analysis
- Best practices
```

### Step 4: Display Results
```
Returns:
- Error Name
- Description
- One-liner Resolution
- AI-enhanced suggestions  
- Debugging commands with examples
```

---

## Knowledge Base - Available Errors

### 1. **Pod OOM (Out of Memory)**
- **Pattern:** `pod oom`, `out of memory`
- **Resolution:** Increase memory limits or optimize application
- **Quick Fix:** `kubectl set resources deployment <name> --limits=memory=512Mi`

### 2. **CrashLoopBackOff**
- **Pattern:** `crashloopbackoff`, `crash loop`
- **Resolution:** Check application logs, fix code/config, increase startup time
- **Quick Fix:** `kubectl logs <pod-name>`

### 3. **ImagePullBackOff**
- **Pattern:** `imagepullbackoff`, `image pull failed`
- **Resolution:** Verify image name, tag, registry credentials
- **Quick Fix:** Check image: `kubectl describe pod <pod-name>`

### 4. **Pod Stuck in Pending**
- **Pattern:** `pending`, `pod pending`
- **Resolution:** Check node resources, labels/selectors, PVC availability
- **Quick Fix:** `kubectl describe pod <pod-name>`

### 5. **Init Container Failed (Init:0)**
- **Pattern:** `init:0`, `init container`
- **Resolution:** Check init container logs and fix configuration
- **Quick Fix:** `kubectl logs <pod-name> -c <init-container-name>`

### 6. **Pod Evicted**
- **Pattern:** `evicted`, `pod evicted`
- **Resolution:** Increase node resources or optimize pod usage
- **Quick Fix:** `kubectl describe pod <pod-name>`

### 7. **BackOff Restarting**
- **Pattern:** `backoff`, `restarting failed container`
- **Resolution:** Check logs and increase startupProbe delay
- **Quick Fix:** `kubectl logs <pod-name>`

### 8. **Generic Error**
- **Pattern:** `error`, `container error`
- **Resolution:** Review logs, check exit codes, verify environment
- **Quick Fix:** `kubectl logs <pod-name>`

### 9. **CPU Throttling**
- **Pattern:** `cpu throttle`, `cpu limit`
- **Resolution:** Increase CPU limits or optimize performance
- **Quick Fix:** `kubectl set resources deployment <name> --limits=cpu=1000m`

### 10. **Connection Refused**
- **Pattern:** `connection refused`, `cannot connect`
- **Resolution:** Verify service exists, DNS resolution, firewall, network policies
- **Quick Fix:** `kubectl exec -it <pod-name> -- nslookup <service-name>`

---

## Usage Examples

### Example 1: OOM Error
```
Input:  "Pod is getting killed - OOM error"

Output:
📌 ERROR: Pod Out Of Memory (OOM)
📖 Description: Pod is killed when it exceeds memory limits
💡 Resolution: Increase memory limits or optimize application

🔧 AI Suggestion: 
  Increase the memory limit in your deployment or pod spec. 
  You can use 'kubectl set resources deployment <name> --limits=memory=1Gi' 
  to adjust memory constraints.

🛠️ Debugging Commands:
  1. kubectl get pods -o jsonpath='{.items[*].status.containerStatuses[*].lastState.terminated.reason}'
  2. kubectl describe pod <pod-name>
  3. kubectl set resources deployment <name> --limits=memory=512Mi
```

### Example 2: CrashLoopBackOff
```
Input:  "Container keeps crashing with CrashLoopBackOff"

Output:
📌 ERROR: CrashLoopBackOff
📖 Description: Container crashes and keeps restarting
💡 Resolution: Check application logs, fix code/config, increase startup time

🔧 AI Suggestion:
  Check the pod logs to identify the crash cause. Use 'kubectl logs <pod-name>'
  to see error messages. Common causes include misconfigurations, missing 
  environment variables, or application code errors.

🛠️ Debugging Commands:
  1. kubectl logs <pod-name>
  2. kubectl logs <pod-name> --previous
  3. kubectl describe pod <pod-name>
```

### Example 3: ImagePullBackOff
```
Input:  "Failed to pull image from registry"

Output:
📌 ERROR: ImagePullBackOff
📖 Description: Kubernetes cannot pull container image
💡 Resolution: Verify image name, tag, registry credentials

🔧 AI Suggestion:
  First check if the image name and tag are correct in your deployment.
  Ensure your Kubernetes cluster has credentials to access the registry
  and that the registry server is accessible from your cluster.

🛠️ Debugging Commands:
  1. kubectl describe pod <pod-name>
  2. kubectl create secret docker-registry <secret-name> --docker-server=<registry>
  3. kubectl set serviceaccount deployment <name> <service-account>
```

---

## Running the Assistant

### Interactive Mode
```bash
python error_resolution_assistant.py

# Then:
# 1. Enter error message
# 2. View all known errors
# 3. Exit
```

### Testing Mode
```bash
python test_error_assistant.py
```

---

## Key Features

✅ **Fuzzy Matching** - Finds errors even with slightly different wording  
✅ **AI Enhancement** - Context-specific resolutions using GPT-4o-mini  
✅ **Knowledge Base** - 10+ common Kubernetes/DevOps errors  
✅ **Debugging Commands** - Ready-to-use kubectl commands  
✅ **Confidence Scoring** - Shows match confidence percentage  
✅ **Interactive Menu** - Easy-to-use command interface  

---

## Adding New Errors to Knowledge Base

To add a new error, edit `error_resolution_assistant.py`:

```python
knowledge_base = {
    "your_error_key": {
        "error_name": "Readable Error Name",
        "description": "What the error means",
        "resolution": "One-liner fix",
        "commands": [
            "kubectl command 1",
            "kubectl command 2",
            "kubectl command 3"
        ]
    }
}
```

---

## Architecture

```
User Input
    ↓
Fuzzy Matching (SequenceMatcher)
    ↓
Knowledge Base Lookup
    ↓
No Match Found? → Suggest generic troubleshooting
Match Found? → AI Enhancement
    ↓
Display Results with Commands
```

---

## Requirements

- Python 3.8+
- OpenAI API key (for AI enhancement)
- kubectl installed (for executing commands)

---

## Future Enhancements

- [ ] Add more error patterns
- [ ] Support multiple cloud platforms (AWS, Azure, GCP)
- [ ] Add container registry specific errors
- [ ] Machine learning based matching
- [ ] Integration with logging systems
- [ ] Automated error detection from logs

---

## Tips & Best Practices

1. **Always check logs first:**
   ```bash
   kubectl logs <pod-name>
   kubectl logs <pod-name> --previous
   ```

2. **Describe pods for full context:**
   ```bash
   kubectl describe pod <pod-name>
   ```

3. **Check resources:**
   ```bash
   kubectl top nodes
   kubectl top pod <pod-name>
   ```

4. **Get events for cluster status:**
   ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```

5. **Use namespace filter:**
   ```bash
   kubectl get pods -n <namespace>
   kubectl logs <pod-name> -n <namespace>
   ```

---

**Version:** 1.0  
**Last Updated:** April 2026  
**Maintained By:** DevOps Team
