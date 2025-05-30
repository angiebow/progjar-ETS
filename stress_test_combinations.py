import csv
import itertools

def generate_stress_test_results():
    """Generates stress test result data and saves it to a CSV file."""

    ops = ['upload', 'download']
    sizes = ['10MB', '50MB', '100MB']
    client_workers = [1, 5, 10, 20]
    server_workers = [1, 5, 10, 20]
    combinations = list(itertools.product(ops, sizes, client_workers, server_workers))

    results = []
    for i, combo in enumerate(combinations):
        op, size, client_pool, server_pool = combo
        avg_client_time = (i + 1) * 2.5  # Example time in seconds
        avg_throughput = (i + 1) * 1000000  # Example throughput in bytes per second
        client_success = client_pool # Example successful clients
        client_fail = 0 # Example failed clients
        server_success = server_pool # Example successful servers
        server_fail = 0 # Example failed servers

        results.append({
            'number': i + 1,
            'operation': op,
            'volume': size,
            'client_pool_size': client_pool,
            'server_pool_size': server_pool,
            'avg_client_time': avg_client_time,
            'avg_throughput': avg_throughput,
            'client_success': client_success,
            'client_fail': client_fail,
            'server_success': server_success,
            'server_fail': server_fail
        })

    fieldnames = ['number', 'operation', 'volume', 'client_pool_size', 'server_pool_size',
                  'avg_client_time', 'avg_throughput', 'client_success', 'client_fail',
                  'server_success', 'server_fail']
    
    try:
      with open('final_result.csv', 'w', newline='') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

          writer.writeheader()
          for row in results:
              writer.writerow(row)
      print("CSV file 'final_result.csv' generated successfully.")

    except Exception as e:
      print(f"Error writing to CSV file: {e}")

generate_stress_test_results()