import grpc
import banks_pb2
import banks_pb2_grpc
import json
from customer import Customer

def run():
    # Read input from JSON file
    with open('input.json', 'r') as f:
        data = json.load(f)
    
    # Create customers and execute their requests
    customers = []
    branches = []
    for process in data:
        if process['type'] == 'customer':
            customer_id = process['id']
            requests = process['customer-requests']
            customer = Customer(customer_id, requests)
            customers.append(customer)
        elif process['type'] == 'branch':
            branches.append(process)
    
    # Execute customer requests
    for customer in customers:
        customer.execute_requests()
    
    # Generate output
    generate_output(customers, branches)

def generate_output(customers, branches):
    output = []
    
    # Part 1: Customer events
    for customer in customers:
        output.append({
            "id": customer.id,
            "type": "customer",
            "events": customer.events
        })
    
    # Part 2: Branch events
    for branch in branches:
        branch_events = []  # This should be populated with actual branch events
        output.append({
            "id": branch['id'],
            "type": "branch",
            "events": branch_events
        })
    
    # Part 3: All events triggered by customer requests
    all_events = []
    for customer in customers:
        for event in customer.events:
            all_events.append({
                "id": customer.id,
                "customer-request-id": event["customer-request-id"],
                "type": "customer",
                "logical_clock": event["logical_clock"],
                "interface": event["interface"],
                "comment": event["comment"]
            })
    
    # Sort all events by logical clock
    all_events.sort(key=lambda x: x["logical_clock"])
    
    # Add sorted events to output
    output.extend(all_events)
    
    # Write output to JSON file
    with open('output.json', 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    run()
