import grpc
from concurrent import futures
import banks_pb2
import banks_pb2_grpc
from branch import Branch
import json

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Read input from JSON file
    with open('input.json', 'r') as f:
        data = json.load(f)
    
    # Create branches
    branches = {}
    for process in data:
        if process['type'] == 'branch':
            branch_id = process['id']
            balance = process['balance']
            branch = Branch(branch_id, balance)
            banks_pb2_grpc.add_BankServicer_to_server(branch, server)
            branches[branch_id] = branch
    
    # Set other branches for each branch
    for branch in branches.values():
        branch.set_other_branches([b for b in branches.values() if b.id != branch.id])
    
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
