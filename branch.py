import banks_pb2
import banks_pb2_grpc

class Branch(banks_pb2_grpc.BankServicer):
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.logical_clock = 0
        self.other_branches = []
        self.events = []
    
    def set_other_branches(self, branches):
        self.other_branches = branches
    
    def update_logical_clock(self, received_clock):
        self.logical_clock = max(self.logical_clock, received_clock) + 1
    
    def Query(self, request, context):
        self.update_logical_clock(request.logical_clock)
        self.events.append({
            "customer-request-id": request.request_id,
            "logical_clock": self.logical_clock,
            "interface": "query",
            "comment": f"event_recv from customer {request.customer_id}"
        })
        return banks_pb2.QueryResponse(balance=self.balance, logical_clock=self.logical_clock)
    
    def Deposit(self, request, context):
        self.update_logical_clock(request.logical_clock)
        self.balance += request.amount
        self.events.append({
            "customer-request-id": request.request_id,
            "logical_clock": self.logical_clock,
            "interface": "deposit",
            "comment": f"event_recv from customer {request.customer_id}"
        })
        
        # Propagate deposit to other branches
        for branch in self.other_branches:
            self.logical_clock += 1
            branch.PropagateDeposit(banks_pb2.PropagateDepositRequest(
                customer_id=request.customer_id,
                request_id=request.request_id,
                amount=request.amount,
                logical_clock=self.logical_clock
            ))
        
        return banks_pb2.DepositResponse(success=True, logical_clock=self.logical_clock)
    
    def Withdraw(self, request, context):
        self.update_logical_clock(request.logical_clock)
        if self.balance >= request.amount:
            self.balance -= request.amount
            success = True
        else:
            success = False
        
        self.events.append({
            "customer-request-id": request.request_id,
            "logical_clock": self.logical_clock,
            "interface": "withdraw",
            "comment": f"event_recv from customer {request.customer_id}"
        })
        
        # Propagate withdraw to other branches if successful
        if success:
            for branch in self.other_branches:
                self.logical_clock += 1
                branch.PropagateWithdraw(banks_pb2.PropagateWithdrawRequest(
                    customer_id=request.customer_id,
                    request_id=request.request_id,
                    amount=request.amount,
                    logical_clock=self.logical_clock
                ))
        
        return banks_pb2.WithdrawResponse(success=success, logical_clock=self.logical_clock)
    
    def PropagateDeposit(self, request, context):
        self.update_logical_clock(request.logical_clock)
        self.balance += request.amount
        self.events.append({
            "customer-request-id": request.request_id,
            "logical_clock": self.logical_clock,
            "interface": "propogate_deposit",
            "comment": f"event_recv from branch {request.customer_id}"
        })
        return banks_pb2.PropagateDepositResponse(success=True, logical_clock=self.logical_clock)
    
    def PropagateWithdraw(self, request, context):
        self.update_logical_clock(request.logical_clock)
        if self.balance >= request.amount:
            self.balance -= request.amount
            success = True
        else:
            success = False
        
        self.events.append({
            "customer-request-id": request.request_id,
            "logical_clock": self.logical_clock,
            "interface": "propogate_withdraw",
            "comment": f"event_recv from branch {request.customer_id}"
        })
        return banks_pb2.PropagateWithdrawResponse(success=success, logical_clock=self.logical_clock)
