import json
import grpc
from concurrent import futures
import banks_pb2_grpc
from branch import Branch

def serve(input_file, port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Read input from JSON file
    with open(input_file, 'r') as f:
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
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()  # 添加这行
    print(f"Server started on port {port}")  # 添加服务器状态输出
    server.wait_for_termination()  # 添加这行

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python server.py input.json [port]")
        sys.exit(1)
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50051  # 确保port是整数
    serve(sys.argv[1], port)
