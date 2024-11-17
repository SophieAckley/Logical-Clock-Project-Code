import banks_pb2
import banks_pb2_grpc
import grpc

class Branch(banks_pb2_grpc.BankServicer):
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.logical_clock = 0
        self.other_branches = []
        self.events = []
        # 创建与其他分支的gRPC连接
        self.branch_stubs = {}

    def set_other_branches(self, branches):
        self.other_branches = branches
        # 为每个分支创建gRPC stub
        for branch in branches:
            channel = grpc.insecure_channel(f'localhost:50051')
            self.branch_stubs[branch.id] = banks_pb2_grpc.BankStub(channel)

    def update_logical_clock(self, received_clock):
        self.logical_clock = max(self.logical_clock, received_clock) + 1

    def add_event(self, customer_request_id, interface, comment):
        event = {
            "customer-request-id": customer_request_id,
            "logical_clock": self.logical_clock,
            "interface": interface,
            "comment": comment
        }
        print(f"Branch {self.id} adding event: {event}")  # 调试日志
        self.events.append(event)

    def Query(self, request, context):
        try:
            self.update_logical_clock(request.logical_clock)
            self.add_event(
                request.request_id,
                "query",
                f"event_recv from customer {request.customer_id}"
            )
            return banks_pb2.QueryResponse(
                balance=self.balance,
                logical_clock=self.logical_clock
            )
        except Exception as e:
            print(f"Error in Query: {str(e)}")
            raise

    def Deposit(self, request, context):
        try:
            self.update_logical_clock(request.logical_clock)
            self.balance += request.amount
            
            self.add_event(
                request.request_id,
                "deposit",
                f"event_recv from customer {request.customer_id}"
            )

            # 使用gRPC stub传播存款到其他分支
            for branch_id, stub in self.branch_stubs.items():
                try:
                    self.logical_clock += 1
                    prop_request = banks_pb2.PropagateDepositRequest(
                        customer_id=request.customer_id,
                        request_id=request.request_id,
                        amount=request.amount,
                        logical_clock=self.logical_clock
                    )
                    stub.PropagateDeposit(prop_request)
                    self.add_event(
                        request.request_id,
                        "propogate_deposit",
                        f"event_sent to branch {branch_id}"
                    )
                except Exception as e:
                    print(f"Error propagating deposit to branch {branch_id}: {str(e)}")

            return banks_pb2.DepositResponse(
                success=True,
                logical_clock=self.logical_clock
            )
        except Exception as e:
            print(f"Error in Deposit: {str(e)}")
            raise

    def Withdraw(self, request, context):
        try:
            self.update_logical_clock(request.logical_clock)
            success = False
            
            if self.balance >= request.amount:
                self.balance -= request.amount
                success = True
                
                self.add_event(
                    request.request_id,
                    "withdraw",
                    f"event_recv from customer {request.customer_id}"
                )

                # 使用gRPC stub传播取款到其他分支
                if success:
                    for branch_id, stub in self.branch_stubs.items():
                        try:
                            self.logical_clock += 1
                            prop_request = banks_pb2.PropagateWithdrawRequest(
                                customer_id=request.customer_id,
                                request_id=request.request_id,
                                amount=request.amount,
                                logical_clock=self.logical_clock
                            )
                            stub.PropagateWithdraw(prop_request)
                            self.add_event(
                                request.request_id,
                                "propogate_withdraw",
                                f"event_sent to branch {branch_id}"
                            )
                        except Exception as e:
                            print(f"Error propagating withdraw to branch {branch_id}: {str(e)}")

            return banks_pb2.WithdrawResponse(
                success=success,
                logical_clock=self.logical_clock
            )
        except Exception as e:
            print(f"Error in Withdraw: {str(e)}")
            raise

    def PropagateDeposit(self, request, context):
        try:
            self.update_logical_clock(request.logical_clock)
            self.balance += request.amount
            
            self.add_event(
                request.request_id,
                "propogate_deposit",
                f"event_recv from branch {request.customer_id}"
            )
            
            return banks_pb2.PropagateDepositResponse(
                success=True,
                logical_clock=self.logical_clock
            )
        except Exception as e:
            print(f"Error in PropagateDeposit: {str(e)}")
            raise

    def PropagateWithdraw(self, request, context):
        try:
            self.update_logical_clock(request.logical_clock)
            success = False
            
            if self.balance >= request.amount:
                self.balance -= request.amount
                success = True
            
            self.add_event(
                request.request_id,
                "propogate_withdraw",
                f"event_recv from branch {request.customer_id}"
            )
            
            return banks_pb2.PropagateWithdrawResponse(
                success=success,
                logical_clock=self.logical_clock
            )
        except Exception as e:
            print(f"Error in PropagateWithdraw: {str(e)}")
            raise
