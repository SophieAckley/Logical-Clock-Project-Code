import grpc
import banks_pb2
import banks_pb2_grpc

class Customer:
    def __init__(self, id, requests):
        self.id = id
        self.requests = requests
        self.logical_clock = 0
        self.events = []
    
    def execute_requests(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = banks_pb2_grpc.BankStub(channel)
            
            for request in self.requests:
                self.logical_clock += 1
                request_id = request['customer-request-id']
                interface = request['interface']
                money = request['money']
                
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
                
                self.logical_clock = max(self.logical_clock, response.logical_clock) + 1
                
                self.events.append({
                    "customer-request-id": request_id,
                    "logical_clock": self.logical_clock,
                    "interface": interface,
                    "comment": f"event_sent from customer {self.id}"
                })
