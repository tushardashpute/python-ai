# Error Resolution Knowledge Base

**Generated:** April 21, 2026 at 08:24
**Total Errors:** 10

## Table of Contents

1. [Pod Out Of Memory (OOM)](#pod-out-of-memory-oom)
2. [CrashLoopBackOff](#crashloopbackoff)
3. [ImagePullBackOff](#imagepullbackoff)
4. [Pod Stuck in Pending](#pod-stuck-in-pending)
5. [Init:0 Container Status](#init0-container-status)
6. [Pod Evicted](#pod-evicted)
7. [Back-off Restarting Failed Container](#back-off-restarting-failed-container)
8. [Container in Error State](#container-in-error-state)
9. [CPU Throttling](#cpu-throttling)
10. [Connection Refused](#connection-refused)

---

## #1 Pod Out Of Memory (OOM)

**Error Key:** `pod oom`

### Description

Pod is killed when it exceeds memory limits

### Resolution

Increase memory limits in pod spec or optimize application to use less memory

### Debugging Commands

1. ```bash
   kubectl get pods -o jsonpath='{.items[*].status.containerStatuses[*].lastState.terminated.reason}'
   ```

2. ```bash
   kubectl describe pod <pod-name>
   ```

3. ```bash
   kubectl set resources deployment <name> --limits=memory=512Mi
   ```

---

## #2 CrashLoopBackOff

**Error Key:** `crashloopbackoff`

### Description

Container crashes and Kubernetes keeps restarting it

### Resolution

Check application logs for errors, fix the code/config, or increase startup time with initialDelaySeconds

### Debugging Commands

1. ```bash
   kubectl logs <pod-name>
   ```

2. ```bash
   kubectl logs <pod-name> --previous
   ```

3. ```bash
   kubectl describe pod <pod-name>
   ```

---

## #3 ImagePullBackOff

**Error Key:** `imagepullbackoff`

### Description

Kubernetes cannot pull the container image from registry

### Resolution

Verify image name, tag, registry credentials, or ensure registry is accessible

### Debugging Commands

1. ```bash
   kubectl describe pod <pod-name>
   ```

2. ```bash
   kubectl create secret docker-registry <secret-name> --docker-server=<registry>
   ```

3. ```bash
   kubectl set serviceaccount deployment <name> <service-account>
   ```

---

## #4 Pod Stuck in Pending

**Error Key:** `pending`

### Description

Pod cannot be scheduled on any node

### Resolution

Check node resources, labels/selectors, PVC availability, or resource requests

### Debugging Commands

1. ```bash
   kubectl describe pod <pod-name>
   ```

2. ```bash
   kubectl top nodes
   ```

3. ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```

---

## #5 Init:0 Container Status

**Error Key:** `init:0`

### Description

Init container failed during startup sequence

### Resolution

Check init container logs to identify the failure, fix configuration, or dependencies

### Debugging Commands

1. ```bash
   kubectl logs <pod-name> -c <init-container-name>
   ```

2. ```bash
   kubectl describe pod <pod-name> | grep Init
   ```

3. ```bash
   kubectl logs <pod-name> --previous
   ```

---

## #6 Pod Evicted

**Error Key:** `evicted`

### Description

Pod is forcibly removed due to node resource pressure

### Resolution

Increase node resources, optimize pod resource usage, or add more nodes

### Debugging Commands

1. ```bash
   kubectl describe pod <pod-name> | grep Reason
   ```

2. ```bash
   kubectl get events
   ```

3. ```bash
   kubectl top pod <pod-name>
   ```

---

## #7 Back-off Restarting Failed Container

**Error Key:** `backoff`

### Description

Container fails repeatedly and Kubernetes increases wait time between restarts

### Resolution

Check application logs, fix startup issues, or increase startupProbe initialDelaySeconds

### Debugging Commands

1. ```bash
   kubectl logs <pod-name>
   ```

2. ```bash
   kubectl logs <pod-name> --tail=50
   ```

3. ```bash
   kubectl describe pod <pod-name>
   ```

---

## #8 Container in Error State

**Error Key:** `error`

### Description

Generic container error - application exited with non-zero status

### Resolution

Review application logs, check exit code, verify environment variables and configuration

### Debugging Commands

1. ```bash
   kubectl logs <pod-name>
   ```

2. ```bash
   kubectl describe pod <pod-name>
   ```

3. ```bash
   kubectl exec -it <pod-name> -- /bin/sh
   ```

---

## #9 CPU Throttling

**Error Key:** `cpu throttle`

### Description

Pod CPU usage exceeds limits and is being throttled

### Resolution

Increase CPU limits or optimize application performance

### Debugging Commands

1. ```bash
   kubectl top pod <pod-name>
   ```

2. ```bash
   kubectl set resources deployment <name> --limits=cpu=1000m
   ```

3. ```bash
   kubectl describe pod <pod-name>
   ```

---

## #10 Connection Refused

**Error Key:** `connection refused`

### Description

Application cannot connect to service or external resource

### Resolution

Verify service exists, DNS resolution works, firewall rules, or network policies

### Debugging Commands

1. ```bash
   kubectl get svc
   ```

2. ```bash
   kubectl get networkpolicies
   ```

3. ```bash
   kubectl exec -it <pod-name> -- nslookup <service-name>
   ```

4. ```bash
   kubectl logs <pod-name>
   ```

---

