[{
"id":1,
"type":"customer",
"events": [
{"customer-request-id": 1, "logical_clock": 1, "interface": "deposit", "comment": "event_sent from
customer 1"},
{"customer-request-id": 2, "logical_clock": 2, "interface": "withdraw", "comment": "event_sent from
customer 1"}]
},
{
"id":2,
"type":"customer",
"events": [
{"customer-request-id": 3, "logical_clock": 1, "interface": "deposit", "comment": "event_sent from
customer 2"},
{"customer-request-id": 4, "logical_clock": 2, "interface": "withdraw", "comment": "event_sent from
customer 2"}
]
},
{
"id":3,
"type":"customer",
"events": [
{"customer-request-id": 5, "logical_clock": 1, "interface": "deposit", "comment": "event_sent from
customer 3"},
{"customer-request-id": 6, "logical_clock": 2, "interface": "withdraw", "comment": "event_sent from
customer 3"}]
}]
// Part 2: List all the events taken place on each branch
[{
"id": 1,
"type": "branch",
"events":
[{"customer-request-id": 1, "logical_clock": 2, "interface": "deposit", "comment": "event_recv from customer
1"},
{"customer-request-id": 1, "logical_clock": 3, "interface": "propogate_deposit", "comment": "event_sent to
branch 2"},
{"customer-request-id": 1, "logical_clock": 4, "interface": "propogate_deposit", "comment": "event_sent to
branch 3"},
{"customer-request-id": 3, "logical_clock": 7, "interface": "propogate_deposit", "comment": "event_recv
from branch 2"},
{"customer-request-id": 5, "logical_clock": 8, "interface": "propogate_deposit", "comment": "event_recv
from branch 3"},
{"customer-request-id": 2, "logical_clock": 9, "interface": "withdraw", "comment": "event_recv from
customer 1"},
{"customer-request-id": 2, "logical_clock": 10, "interface": "propogate_withdraw", "comment": "event_sent
to branch 2"},
{"customer-request-id": 2, "logical_clock": 11, "interface": "propogate_withdraw", "comment": "event_sent
to branch 3"},
{"customer-request-id": 4, "logical_clock": 14, "interface": "propogate_withdraw", "comment": "event_recv
from branch 2"},
{"customer-request-id": 6, "logical_clock": 15, "interface": "propogate_withdraw", "comment": "event_recv
from branch 3"}]
},
{
"id": 2,
"type": "branch",
"events":
[{"customer-request-id": 1, "logical_clock": 4, "interface": "propogate_deposit", "comment": "event_recv
from branch 1"},
{"customer-request-id": 3, "logical_clock": 5, "interface": "deposit", "comment": "event_recv from customer
2"},
{"customer-request-id": 3, "logical_clock": 6, "interface": "propogate_deposit", "comment": "event_sent to
branch 1"},
{"customer-request-id": 3, "logical_clock": 7, "interface": "propogate_deposit", "comment": "event_sent to
branch 3"},
{"customer-request-id": 2, "logical_clock": 11, "interface": "propogate_withdraw", "comment": "event_recv
from branch 1"},
{"customer-request-id": 4, "logical_clock": 12, "interface": "withdraw", "comment": "event_recv from
customer 2"},
{"customer-request-id": 4, "logical_clock": 13, "interface": "propogate_withdraw", "comment": "event_sent
to branch 1"},
{"customer-request-id": 5, "logical_clock": 14, "interface": "propogate_deposit", "comment": "event_recv
from branch 3"},
{"customer-request-id": 4, "logical_clock": 15, "interface": "propogate_withdraw", "comment": "event_sent
to branch 3"},
{"customer-request-id": 6, "logical_clock": 18, "interface": "propogate_withdraw", "comment": "event_recv
from branch 3"}]
},
{
"id": 3,
"type": "branch",
"events":
[{"customer-request-id": 5, "logical_clock": 2, "interface": "deposit", "comment": "event_recv from customer
3"},
{"customer-request-id": 5, "logical_clock": 3, "interface": "propogate_deposit", "comment": "event_sent to
branch 1"},
{"customer-request-id": 1, "logical_clock": 5, "interface": "propogate_deposit", "comment": "event_recv
from branch 1"},
{"customer-request-id": 5, "logical_clock": 6, "interface": "propogate_deposit", "comment": "event_sent to
branch 2"},
{"customer-request-id": 3, "logical_clock": 8, "interface": "propogate_deposit", "comment": "event_recv
from branch 2"},
{"customer-request-id": 2, "logical_clock": 12, "interface": "propogate_withdraw", "comment": "event_recv
from branch 1"},
{"customer-request-id": 6, "logical_clock": 13, "interface": "withdraw", "comment": "event_recv from
customer 3"},
{"customer-request-id": 6, "logical_clock": 14, "interface": "propogate_withdraw", "comment": "event_sent
to branch 1"},
{"customer-request-id": 4, "logical_clock": 16, "interface": "propogate_withdraw", "comment": "event_recv
from branch 2"},
{"customer-request-id": 6, "logical_clock": 17, "interface": "propogate_withdraw", "comment": "event_sent
to branch 2"}]
}]
// Part 3: List all the events (along with their logical times) triggered by each customer Deposit/Withdraw
request
[{"id": 1,"customer-request-id":1,"type": "customer","logical_clock": 1,"interface": "deposit","comment":
"event_sent from customer 1"},
{"id": 1,"customer-request-id":1,"type": "branch","logical_clock": 2,"interface": "deposit","comment":
"event_recv from customer 1"},
pe": "branch","logical_clock": 10,"interface":
"propogate_withdraw","comment": "event_sent to branch 2"},
{"id": 2,"customer-request-id":2,"type": "branch","logical_clock": 11,"interface":
"propogate_withdraw","comment": "event_recv from branch 1"},
{"id": 1,"customer-request-id":2,"type": "branch","logical_clock": 11,"interface":
"propogate_withdraw","comment": "event_sent to branch 3"},
{"id": 3,"customer-request-id":2,"type": "branch","logical_clock": 12,"interface":
"propogate_withdraw","comment": "event_recv from branch 1"},
{"id": 2,"customer-request-id":3,"type": "customer","logical_clock": 1,"interface": "deposit","comment":
"event_sent from customer 2"},
{"id": 2,"customer-request-id":3,"type": "branch","logical_clock": 5,"interface": "deposit","comment":
"event_recv from customer 2"},
{"id": 2,"customer-request-id":3,"type": "branch","logical_clock": 6,"interface":
"propogate_deposit","comment": "event_sent to branch 1"},
{"id": 2,"customer-request-id":3,"type": "branch","logical_clock": 7,"interface":
"propogate_deposit","comment": "event_sent to branch 3"},
{"id": 1,"customer-request-id":3,"type": "branch","logical_clock": 7,"interface":
"propogate_deposit","comment": "event_recv from branch 2"},
{"id": 3,"customer-request-id":3,"type": "branch","logical_clock": 8,"interface":
"propogate_deposit","comment": "event_recv from branch 2"},
{"id": 2,"customer-request-id":4,"type": "customer","logical_clock": 2,"interface": "withdraw","comment":
"event_sent from customer 2"},
{"id": 2,"customer-request-id":4,"type": "branch","logical_clock": 12,"interface": "withdraw","comment":
"event_recv from customer 2"},
{"id": 2,"customer-request-id":4,"type": "branch","logical_clock": 13,"interface":
"propogate_withdraw","comment": "event_sent to branch 1"},
{"id": 1,"customer-request-id":4,"type": "branch","logical_clock": 14,"interface":
"propogate_withdraw","comment": "event_recv from branch 2"},
{"id": 2,"customer-request-id":4,"type": "branch","logical_clock": 15,"interface":
"propogate_withdraw","comment": "event_sent to branch 3"},
{"id": 3,"customer-request-id":4,"type": "branch","logical_clock": 16,"interface":
"propogate_withdraw","comment": "event_recv from branch 2"},
{"id": 3,"customer-request-id":5,"type": "customer","logical_clock": 1,"interface": "deposit","comment":
"event_sent from customer 3"},
{"id": 3,"customer-request-id":5,"type": "branch","logical_clock": 2,"interface": "deposit","comment":
"event_recv from customer 3"},
{"id": 3,"customer-request-id":5,"type": "branch","logical_clock": 3,"interface":
"propogate_deposit","comment": "event_sent to branch 1"},
{"id": 3,"customer-request-id":5,"type": "branch","logical_clock": 6,"interface":
"propogate_deposit","comment": "event_sent to branch 2"},
{"id": 1,"customer-request-id":5,"type": "branch","logical_clock": 8,"interface":
"propogate_deposit","comment": "event_recv from branch 3"},
{"id": 2,"customer-request-id":5,"type": "branch","logical_clock": 14,"interface":
"propogate_deposit","comment": "event_recv from branch 3"},
{"id": 3,"customer-request-id":6,"type": "customer","logical_clock": 2,"interface": "withdraw","comment":
"event_sent from customer 3"},
{"id": 3,"customer-request-id":6,"type": "branch","logical_clock": 13,"interface": "withdraw","comment":
"event_recv from customer 3"},
{"id": 3,"customer-request-id":6,"type": "branch","logical_clock": 14,"interface":
"propogate_withdraw","comment": "event_sent to branch 1"},
{"id": 1,"customer-request-id":6,"type": "branch","logical_clock": 15,"interface":
"propogate_withdraw","comment": "event_recv from branch 3"},
{"id": 3,"customer-request-id":6,"type": "branch","logical_clock": 17,"interface":
"propogate_withdraw","comment": "event_sent to branch 2"},
{"id": 2,"customer-request-id":6,"type": "branch","logical_clock": 18,"interface":
"propogate_withdraw","comment": "event_recv from branch 3"}]
