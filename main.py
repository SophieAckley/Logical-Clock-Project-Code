import json
import time
from concurrent import futures
from branch import Branch
from customer import Customer
import server  # The `serve` function from server.py


def run_branch(branch_data):
    """Initialize and start a branch server."""
    branch = Branch(branch_data['id'], branch_data['balance'], [b['id'] for b in branches])
    server.serve(branch)


def run_customer(customer_data):
    """Create and execute events for a customer."""
    customer = Customer(customer_data['id'], customer_data['events'])
    return customer.executeEvents()


if __name__ == '__main__':
    # Load the input data
    with open('input.json', 'r') as f:
        data = json.load(f)

    # Separate branch and customer data
    branches = [item for item in data if item['type'] == 'branch']
    customers = [item for item in data if item['type'] == 'customer']

    # Unified output list
    output = []

    # Start the branch servers
    executor = futures.ThreadPoolExecutor(max_workers=len(branches))
    branch_futures = [executor.submit(run_branch, branch) for branch in branches]

    # Give the branch servers time to initialize
    time.sleep(2)

    # Process customer events and collect event data
    all_events = []  # Collect all events to include in the branch data

    for customer in customers:
        result = run_customer(customer)
        for event in result:
            all_events.append({
                "customer_request_id": event.get("id"),
                "logical_clock": event.get("logical_clock"),
                "interface": event.get("interface"),
                "comment": f"event_{event.get('action', 'unknown')} from customer {customer['id']}"
            })

    # Generate branch data based on events
    for branch in branches:
        branch_events = [event for event in all_events if event["customer_request_id"] in branch.get("balance", [])]
        output.append({
            "id": branch["id"],
            "type": "branch",
            "events": branch_events
        })

    # Write the combined output to a JSON file
    with open('output.json', 'w') as f:
        json.dump(output, f, indent=2)

    # Ensure all branch servers complete their tasks
    for future in branch_futures:
        future.result()

    print("All processes completed. Output written to output.json.")
