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
    for process in data:
        if process['type'] == 'customer':
            customer_id = process['id']
            requests = process['customer-requests']
            customer = Customer(customer_id, requests)
            customers.append(customer)
    
    # Execute customer requests
    for customer in customers:
        customer.execute_requests()
    
    # Generate output
    generate_output(customers)

def generate_output(customers):
    output = []
    
    # Part 1: Customer events
    for customer in customers:
        output.append({
            "id": customer.id,
            "type": "customer",
            "events": customer.events
        })
    
    # Part 2: Branch events (to be implemented)
    
    # Part 3: All events triggered by customer requests (to be implemented)
    
    # Write output to JSON file
    with open('output.json', 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    run()
