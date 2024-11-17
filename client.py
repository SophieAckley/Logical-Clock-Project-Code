import grpc
import json
import banks_pb2_grpc
import banks_pb2
from customer import Customer

def run(input_file):
    try:
        # 创建与服务器的连接
        print("Connecting to server...")
        channel = grpc.insecure_channel('localhost:50051')
        stub = banks_pb2_grpc.BankStub(channel)
        
        # 读取输入文件
        print("Reading input file...")
        with open(input_file, 'r') as f:
            data = json.load(f)
    
        # 分离客户和分支数据
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
    
        # 执行所有客户请求
        for customer in customers:
            customer.execute_requests(stub)
    
        # 生成输出文件
        output = []
    
        # 1. 添加客户进程
        for customer in customers:
            output.append({
            "id": customer.id,
            "type": "customer",
                "events": customer.events
            })
    
        # 2. 添加分支进程
        for branch in branches:
            output.append({
                "id": branch['id'],
                "type": "branch",
                "events": []  # 分支事件将由服务器端记录
        })
           
    # 3. 输出结果   
        # 3. 添加所有事件（按逻辑时钟排序）
        all_events = []
        
        # 收集客户事件
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
        
        # 按逻辑时钟排序
        all_events.sort(key=lambda x: x["logical_clock"])
        
        # 将排序后的事件添加到输出
        output.extend(all_events)
        
        # 写入输出文件
        print("Writing output.json...")
        with open('output.json', 'w') as f:
            json.dump(output, f, indent=2)
        print("Successfully generated output.json")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise         

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python client.py input.json")
        sys.exit(1)
    run(sys.argv[1])
