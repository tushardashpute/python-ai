# Error Resolution Assistant - Quick Reference Card

## 🚀 Quick Start (30 seconds)

```bash
# 1. Run the assistant
python error_resolution_assistant.py

# 2. Enter your error (e.g., "Pod out of memory")

# 3. Get resolution with debugging commands
```

---

## 🎯 10 Supported Errors

### Memory & Resources
```
1. Pod OOM (Out of Memory)
   → Fix: kubectl set resources deployment <name> --limits=memory=512Mi

2. CPU Throttling  
   → Fix: kubectl set resources deployment <name> --limits=cpu=1000m
```

### Container Issues
```
3. CrashLoopBackOff
   → Fix: kubectl logs <pod-name>

4. ImagePullBackOff
   → Fix: kubectl describe pod <pod-name>

5. Back-off Restarting
   → Fix: Check logs and fix configuration
```

### Scheduling Issues
```
6. Pod Pending
   → Fix: kubectl describe pod <pod-name>

7. Pod Evicted
   → Fix: Free up node resources
```

### Runtime Issues
```
8. Init:0 Container Failure
   → Fix: kubectl logs <pod-name> -c <init-container-name>

9. Connection Refused
   → Fix: kubectl exec -it <pod-name> -- nslookup <service-name>

10. Generic Container Error
    → Fix: kubectl logs <pod-name>
```

---

## 🔍 How to Use

### For Each Error:

1. **Get Description**
   ```
   "What does this error mean?"
   ```

2. **Get Resolution**
   ```
   "How do I fix it?"
   ```

3. **Get Commands**
   ```
   "What kubectl commands to run?"
   ```

4. **Get AI Suggestions**
   ```
   "What else should I check?"
   ```

---

## 💻 Common Usage Patterns

### Pattern 1: Copy-Paste Error
```
Your Error: "Back-off Restarting Failed Container"
↓
System: Matches to "backoff" pattern
↓
Run: kubectl logs <pod-name>
```

### Pattern 2: Describe Issue
```
Your Error: "Container keeps crashing and restarting"
↓
System: Fuzzy matches to "crashloopbackoff"
↓
Run: kubectl logs <pod-name> --previous
```

### Pattern 3: View All Errors
```
Your Request: "Show all known errors"
↓
System: Lists all 10 error types
↓
Pick one for help
```

---

## 🛠️ Essential Kubectl Commands

```bash
# View logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl logs <pod-name> -c <container-name>

# Describe resources
kubectl describe pod <pod-name>
kubectl describe node <node-name>

# Set resources
kubectl set resources deployment <name> --limits=memory=512Mi
kubectl set resources deployment <name> --limits=cpu=1000m

# Check status
kubectl get pods
kubectl get events
kubectl top pod <pod-name>
kubectl top nodes

# Execute commands
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec -it <pod-name> -- nslookup <service-name>
```

---

## 📊 Error Matching Confidence

| Confidence | Action | Example |
|-----------|--------|---------|
| 90-100% | Act immediately | "Pod OOM error" |
| 70-89% | Review carefully | "pod memory killed" |
| 40-69% | Verify match | "container stopped" |
| <40% | Manual investigation | "something wrong" |

---

## 🎓 Learning Resources

### Quick Guides
- 📖 `ERROR_RESOLUTION_GUIDE.md` - Full documentation
- 📊 `ASSISTANT_SUMMARY.md` - Feature overview
- 🎁 `WHATS_NEW.md` - What's included

### Running Utilities
- 🏃 `error_resolution_assistant.py` - Main tool
- 📋 `show_knowledge_base.py` - View errors
- ✅ `test_error_assistant.py` - Run tests
- 🎬 `demo_error_assistant.py` - See demo

---

## 💡 Pro Tips

### Tip 1: Check Logs First
```bash
kubectl logs <pod-name>
# Usually shows the actual error message
```

### Tip 2: Use --previous for Crashes
```bash
kubectl logs <pod-name> --previous
# Shows logs from crashed container
```

### Tip 3: Check Node Resources
```bash
kubectl top nodes
# See if node is running out of resources
```

### Tip 4: Get Events
```bash
kubectl get events --sort-by='.lastTimestamp'
# Shows what happened and when
```

### Tip 5: Describe is Your Friend
```bash
kubectl describe pod <pod-name>
# Shows complete pod details and recent events
```

---

## 🔄 Troubleshooting Workflow

```
1. Pod has issues
   ↓
2. Describe pod: kubectl describe pod <pod-name>
   ↓
3. Check logs: kubectl logs <pod-name>
   ↓
4. Enter error in assistant
   ↓
5. Get suggested resolution
   ↓
6. Run suggested commands
   ↓
7. Fix the issue!
```

---

## ⚡ Speed Comparison

### Before Assistant (Manual)
```
1. Read error message (2 min)
2. Search online (5-10 min)
3. Read Stack Overflow (5 min)
4. Try solutions (10-15 min)
Total: 22-32 minutes
```

### With Assistant
```
1. Copy error message (30 sec)
2. Run error-resolver (30 sec)
3. Get resolution + commands (instant)
4. Execute commands (2-5 min)
Total: 3-6 minutes
```

**Improvement: 70% faster** ⚡

---

## 📌 Keyboard Shortcuts

When running the assistant:
```
1 = Enter error message
2 = View all known errors
3 = Exit
```

---

## 🆘 Stuck? Do This

1. **No match found?**
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Need more info?**
   ```bash
   kubectl get events
   kubectl top pod <pod-name>
   ```

3. **Want to see all errors?**
   ```bash
   python show_knowledge_base.py
   ```

4. **Run tests?**
   ```bash
   python test_error_assistant.py
   ```

---

## 🎯 Next Steps

- [ ] Save this quick reference
- [ ] Run `python error_resolution_assistant.py`
- [ ] Try resolving your current errors
- [ ] Add custom error patterns
- [ ] Integrate with your team's tools

---

## 📞 When to Use

### Perfect For:
✅ Kubernetes errors  
✅ Container runtime issues  
✅ Pod scheduling problems  
✅ Resource constraints  
✅ Quick troubleshooting  

### Not For:
❌ Application code bugs  
❌ Database issues (not K8s related)  
❌ Network infrastructure  
❌ Hardware problems  

---

## 💎 Key Takeaways

1. **Fast**: Get resolutions in seconds
2. **Smart**: Fuzzy matching understands your intent
3. **Actionable**: Ready-to-use kubectl commands
4. **AI-Enhanced**: Context-specific advice
5. **Extensible**: Easy to add new errors

---

**Quick Ref v1.0** | April 2026 | Error Resolution System
