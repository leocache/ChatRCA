
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

# Fault 5

# Fault in ts-basic-service

## Summary

Recent anomalies were detected in the ts-basic-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - Errors in FoodServiceImpl due to failed requests for retrieving food data.
   - ExecuteServiceImpl errors indicating incorrect order statuses for ticket execution.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-basic-service pod. CPU usage spiked to over 10%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 22 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage, with CPU usage peaking at 18%.

3. **Trace Data:**
   - High variability in operation durations within the ts-basic-service, with some operations taking significantly longer than expected.

## Reference root cause

Network delay fault injection in ts-basic-service.


# Fault 6

# Fault in ts-basic-service

## Summary

Recent anomalies were detected in the ts-basic-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - Multiple errors in DispatcherServlet due to no available instances for ts-user-service.
   - ExecuteServiceImpl error indicating an incorrect order status for ticket execution.
   - FoodServiceImpl error due to a failed request for retrieving food data.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-basic-service pod. CPU usage spiked to nearly 12%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 2340 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage, with CPU usage peaking at 41%.

3. **Trace Data:**
   - High variability in operation durations within the ts-basic-service, with some operations taking significantly longer than expected.

## Reference root cause

Network delay fault injection in ts-basic-service.


# Fault 7

# Fault in ts-verification-code-service

## Summary

Recent anomalies were detected in the ts-verification-code-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - An error in DispatcherServlet due to no available instances for ts-travel2-service.
   - FoodServiceImpl error due to a failed request for retrieving food data.
   - ExecuteServiceImpl error indicating an incorrect order status for ticket execution.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-verification-code-service pod. CPU usage spiked to nearly 90%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 3600 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage, with CPU usage peaking at 32%.

3. **Trace Data:**
   - High variability in operation durations within the ts-verification-code-service, with some operations taking significantly longer than expected.

## Reference root cause

CPU contention fault injection in ts-verification-code-service.


# Fault 8

# Fault in ts-contacts-service

## Summary

Recent anomalies were detected in the ts-contacts-service following a fault injection event. The following issues were observed in the metrics:

1. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-contacts-service pod. CPU usage spiked to over 100%.
   - Abnormal latencies observed in client and server requests. Client latency reached up to 20 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage, with CPU usage peaking at 34%.

2. **Trace Data:**
   - No trace data was available for analysis.

## Reference root cause

CPU contention fault injection in ts-contacts-service.


# Fault 9

# Fault in ts-travel2-service

## Summary

Recent anomalies were detected in the ts-travel2-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - Multiple errors in DispatcherServlet due to no available instances for ts-seat-service.
   - ExecuteServiceImpl error indicating incorrect order status for ticket execution.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-travel2-service pod. CPU usage spiked to nearly 11%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 14 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage.

3. **Trace Data:**
   - High variability in operation durations within the ts-travel2-service, with some operations taking significantly longer than expected.

## Reference root cause

Exception type fault injection in ts-travel2-service.


# Fault 10

# Fault in ts-travel-service

## Summary

Recent anomalies were detected in the ts-travel-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - Multiple errors in DispatcherServlet due to no available instances for ts-basic-service.
   - ExecuteServiceImpl errors indicating incorrect order statuses for ticket execution.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-travel-service pod. CPU usage spiked to nearly 10%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 156 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage.

3. **Trace Data:**
   - High variability in operation durations within the ts-travel-service, with some operations taking significantly longer than expected.

## Reference root cause

Exception type fault injection in ts-travel-service.


# Fault 11

# Fault in ts-contacts-service

## Summary

Recent anomalies were detected in the ts-contacts-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - Multiple error logs in the ContactsServiceImpl indicating no contacts found for given IDs.
   - Errors in FoodServiceImpl due to failed requests for retrieving food data.
   - DispatcherServlet encountered exceptions due to unavailability of instances for ts-basic-service.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-contacts-service pod. CPU usage spiked to over 46%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 60 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage.

3. **Trace Data:**
   - High variability in operation durations within the ts-contacts-service, with some operations taking significantly longer than expected.

## Reference root cause

Return type fault injection in ts-contacts-service.


# Fault 12

# Fault in ts-contacts-service

## Summary

Recent anomalies were detected in the ts-contacts-service following a fault injection event. The following issues were observed in the metrics and logs:

1. **Log Entries:**
   - Multiple error logs indicating issues with finding contacts by ID in ContactsServiceImpl.
   - Errors in FoodServiceImpl regarding failed requests to get food details.
   - DispatcherServlet errors due to unavailable instances for ts-food-service.

2. **Metrics:**
   - Significant variations in CPU usage, memory usage, and network transmission rates in the ts-contacts-service pod. CPU usage spiked to nearly 40%.
   - Abnormal latencies observed in client and server requests, with client latencies reaching up to 156 seconds.
   - Pod success rate was consistently zero, indicating failures in service operations.
   - Node metrics showed fluctuations in CPU and memory usage.

3. **Trace Data:**
   - High variability in operation durations within the ts-contacts-service, with some operations taking significantly longer than expected.

## Reference root cause

Return type fault injection in ts-contacts-service.

