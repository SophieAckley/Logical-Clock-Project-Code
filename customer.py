import grpc
import banks_pb2
import banks_pb2_grpc
import time

class Customer:
    def __init__(self, id, requests):
        self.id = id
        self.requests = requests
        self.logical_clock = 0
        self.events = []
    
    def execute_requests(self, stub):
        try:
            for request in self.requests:
                self.logical_clock += 1
            request_id = request['customer-request-id']
            interface = request['interface']
            money = request.get('money', 0)
            
            print(f"Customer {self.id} executing {interface} request {request_id}")
            
            # 执行请求
            if interface == 'query':
                response = stub.Query(banks_pb2.QueryRequest(
                    customer_id=self.id,
                    request_id=request_id,
                    logical_clock=self.logical_clock
                ))
            elif interface == 'deposit':
                response = stub.Deposit(banks_pb2.DepositRequest(
                    customer_id=self.id,
                    request_id=request_id,
                    amount=money,
                    logical_clock=self.logical_clock
                ))
            elif interface == 'withdraw':
                response = stub.Withdraw(banks_pb2.WithdrawRequest(
                    customer_id=self.id,
                    request_id=request_id,
                    amount=money,
                    logical_clock=self.logical_clock
                ))
            
            # 更新逻辑时钟
            self.logical_clock = max(self.logical_clock, response.logical_clock) + 1
            
            # 记录事件
            event = {
                "customer-request-id": request_id,
                "logical_clock": self.logical_clock,
                "interface": interface,
                "comment": f"event_sent from customer {self.id}"
            }
            print(f"Adding event: {event}")
            self.events.append(event)
            
            print(f"Request {request_id} completed, logical_clock: {self.logical_clock}")
            
        except Exception as e:
            print(f"Error executing requests for customer {self.id}: {str(e)}")
            raise
