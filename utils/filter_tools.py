def filter_error_logs(md_content):
    """
    Filters out lines containing 'ERROR' from a Markdown string of logs 
    and returns a new Markdown string with only the field headers and error logs.

    Parameters:
    md_content (str): The log content in Markdown format as a single string.

    Returns:
    str: A Markdown string of filtered error logs, including the header.
    """
    lines = md_content.splitlines()
    if not lines:
        return ""  # Return empty if content is empty

    # Assume the first line is the header
    header = lines[0]
    error_logs = [header]

    # Filter for lines containing 'ERROR' and add them to the list
    for line in lines[1:]:
        if 'ERROR' in line:
            error_logs.append(line.strip())

    # Join the filtered logs into a single Markdown string
    return '\n'.join(error_logs)


def filter_metric_data(md_content, success_rate_threshold=20, cpu_usage_threshold=10):
    """
    Filters metric data from a Markdown string where `PodSuccessRate` equals 0 
    or `NodeCpuUsageRate` is above a given threshold.

    Parameters:
    md_content (str): The metric data in Markdown format as a single string.
    success_rate_threshold (float): Threshold for `PodSuccessRate` to filter for errors.
    cpu_usage_threshold (float): Threshold for `NodeCpuUsageRate` to filter for high usage.

    Returns:
    str: A Markdown string of filtered metric data, including the header.
    """
    lines = md_content.splitlines()
    if not lines:
        return ""  # Return empty if content is empty

    # Assume the first line is the header
    header = lines[0]
    filtered_metrics = [header]

    # Process each line after the header
    for line in lines[2:]:
        columns = line.split('|')
        
        # print('col', columns)
        try:
            # Extract relevant fields for filtering
            pod_success_rate = float(columns[3].strip())
            node_cpu_usage = float(columns[17].strip())
            # print(pod_success_rate)
            # print(node_cpu_usage)
            # Apply the filter conditions
            if pod_success_rate <= success_rate_threshold or node_cpu_usage < cpu_usage_threshold:
                filtered_metrics.append(line.strip())

        except (ValueError, IndexError):
            # Handle lines that don't have the expected format or are non-numeric
            # print(columns[0])
            continue

    # Join the filtered metrics into a single Markdown string
    return '\n'.join(filtered_metrics)



def filter_trace_data(md_content, duration_threshold=10000):
    """
    Filters trace data from a Markdown string where `Duration` is above a given threshold.

    Parameters:
    md_content (str): The trace data in Markdown format as a single string.
    duration_threshold (int): Threshold for `Duration` to filter for longer traces.

    Returns:
    str: A Markdown string of filtered trace data, including the header.
    """
    lines = md_content.splitlines()
    if not lines:
        return ""  # Return empty if content is empty

    # Assume the first line is the header
    header = lines[0]
    filtered_traces = [header]

    # Process each line after the header
    for line in lines[2:]:
        columns = line.split('|')

        # Check that we have the expected number of columns
        if len(columns) < 8:
            continue

        # Extract the `Duration` field and check if it's a number
        duration_str = columns[3].strip()
        
        if duration_str.isdigit():
            duration = int(duration_str)
            # print(duration)
            # Apply the filter condition
            if duration > duration_threshold:
                filtered_traces.append(line.strip())

    # Join the filtered traces into a single Markdown string
    return '\n'.join(filtered_traces)


