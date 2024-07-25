
# Fault 1

## Summary
Recent anomalies were detected in the ts-contacts-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:** Multiple error logs indicating issues with finding contacts in the ContactsServiceImpl and errors in the dispatcherServlet.
2. **Metrics:** Significant variations in CPU usage, memory usage, and network transmission rates in the ts-contacts-service pod. There were also abnormal latencies observed in client and server requests.
3. **Trace Data:** Delays and errors were noted in various operations within the ts-contacts-service, including contact retrieval and database transactions.

## Reference root cause
Return type fault injection in ts-contacts-service.





# Fault 2

## Summary

Recent anomalies were detected in the ts-travel-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:** 
   - Error log indicating no instances available for ts-security-service.
   - FoodServiceImpl error related to a failed request for getting food details.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-travel-service pod.
   - Abnormal latencies observed in client and server requests.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage.

3. **Trace Data:**
   - Delays and errors in various operations within the ts-travel-service, including API calls and database transactions.
   - High variability in operation durations, with some operations taking significantly longer than others.

## Reference root cause

Exception type fault injection in ts-travel-service.



# Fault 3

## Summary

Recent anomalies were detected in the ts-contacts-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - No specific log entries were available for analysis.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-contacts-service pod. CPU usage had extreme values, reaching up to 100%.
   - Abnormal latencies observed in client and server requests. Client latency reached up to 20 seconds, indicating severe performance issues.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage, with CPU usage peaking at 34%.

3. **Trace Data:**
   - No trace data was available for analysis.

## Reference root cause

CPU contention fault injection in ts-contacts-service.







# Fault 4

## Summary

Recent anomalies were detected in the ts-contacts-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - An error log indicating a ticket execution error related to an incorrect order status in ExecuteServiceImpl.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-contacts-service pod.
   - Abnormal latencies observed in client and server requests. Client latency reached up to 4.87 seconds, and server latency peaked at 266.4 seconds, indicating severe performance issues.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage, with CPU usage peaking at 57%.

3. **Trace Data:**
   - No trace data was available for analysis.

## Reference root cause

Network delay fault injection in ts-contacts-service.

