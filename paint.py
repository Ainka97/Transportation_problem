import pulp
import numpy as np
# i denotes factory
Fac = ['Bristol','Leeds']
Fac_cap = {'Bristol': 50000, 'Leeds': 60000}
# j denotes warehouses
War = ['London', 'Birmingham', 'Glasgow']
War_lim={'London': 25000, 'Birmingham': 20000, 'Glasgow': 16000}
# k denotes wholesalers
Sal =['1', '2', '3', '4', '5']
Sal_demand = {'1': 20000, '2': 25000, '3': 13000, '4': 19000, '5': 21000}
#SUPPLIERS
Sup = Fac + War

#CUSTOMERS
Cust = War + Sal

Cost_Matrix = {("Bristol", "London"):27,
               ("Bristol", "Birmingham"):25,
               ("Bristol", "Glasgow"):100000,
               ("Bristol", "1"):82,
               ("Bristol", "2"):100000,
               ("Bristol", "3"):93,
               ("Bristol", "4"):100,
               ("Bristol", "5"):88,
               ("Leeds", "London"):32,
               ("Leeds", "Birmingham"):29,
               ("Leeds", "Glasgow"):33,
               ("Leeds", "1"):100000,
               ("Leeds", "2"):72,
               ("Leeds", "3"):57,
               ("Leeds", "4"):100000,
               ("Leeds", "5"):100,
               ("London", "Birmingham"):100000,
               ("London", "Glasgow"):380000,
               ("London", "1"):38,
               ("London", "2"):34,
               ("London", "3"):1000000,
               ("London", "4"):42,
               ("London", "5"):45,
               ("Birmingham", "London"):3800000,
               ("Birmingham", "Glasgow"):380000,
               ("Birmingham", "1"):38,
               ("Birmingham", "2"):42,
               ("Birmingham", "3"):45,
               ("Birmingham", "4"):42,
               ("Birmingham", "5"):48,
               ("Glasgow", "London"):380000,
               ("Glasgow", "Birmingham"):380000,
               ("Glasgow", "1"):38,
               ("Glasgow", "2"):45,
               ("Glasgow", "3"):32,
               ("Glasgow", "4"):1000000,
               ("Glasgow", "5"):38
               }


#Instantiate the problem
prob = pulp.LpProblem("Paint Transhipment Problem", pulp.LpMinimize)
#Decision Variables
x = {}
for i in Sup:
    for j in Cust:
        if i != j:
            x[i, j] = pulp.LpVariable('x_' + i + '_' + j, cat='Continuous',lowBound=0)
#Objective function
b_sum = 0
for i in Sup:
    for j in Cust:
        if i != j:
            b_sum += Cost_Matrix[i, j]*x[i, j]
prob += b_sum

#Constraints
#Factory Capacity constraint
for i in Fac:
    a_sum = 0
    for j in Cust:
        if i != j:
            a_sum += x[i, j]
    prob += a_sum <= Fac_cap[i]
for i in Sal:
    sum=0
    for j in Sup:
        sum+= x[j,i]
    prob+=sum>=Sal_demand[i]
print(prob)

#Warhouse limit
for i in War:
    c_val = 0
    for j in Sal:
        if i != j:
            c_val += x[i, j]
    prob += c_val <= War_lim[i]
print(prob)

#flow balancing
for j in War:
    d_sum=0
    e_sum =0
    for i in Fac:
        d_sum += x[i, j]

    for k in Sal:
        e_sum += x[j, k]
    prob += d_sum - e_sum == 0
    print(prob)
prob.solve()
print("Objective function:", pulp.value(prob.objective))

#Show the status of the solution optimal or not
print('Status:', pulp.LpStatus[prob.status])

#Show the optimal solution
for s in prob.variables():
    print(s.name, "=", s.varValue)










