import pandas as pd
import networkx as nx
import math

#Importing the dataframes
df1 = pd.read_csv("student_subject_pref.csv", sep = '\s+',header = None)
df2 = pd.read_csv("subjectareas_fixed.csv", header = None)

print(df1)
print(df2)

#Creating lists from the data

students = df1.iloc[:, 0].tolist()

supervisors = list(set(df2.iloc[:, 1].tolist()))

subjects = df2.iloc[:, 0].tolist()

#Construct the graph

G = nx.DiGraph()

#Add students, suoervisors, subjects as nodes
G.add_nodes_from(students,with_labels=True,color = 'blue')
G.add_nodes_from(supervisors,with_labels=True,color = 'red')
G.add_nodes_from(subjects,with_labels=True,color = 'green')

numb_students = len(students)
num_subjects = len(subjects)
num_supervisors = len(set(supervisors))

#Finding an even capacity for how many students each supervisor should take

supervisors_numsubjects = []

for supervisor in supervisors:
    supervisor_subjects = df2[df2[1] == supervisor][0].tolist()
    
    numb_supervisor_subjects = len(supervisor_subjects)
    
    supervisors_numsubjects.append([supervisor,numb_supervisor_subjects])
    
students_to_supervisors = math.ceil(numb_students/num_supervisors)
print(f'each supervisor must accept {students_to_supervisors} students')

supervisor_capacity = []

for supervisor,numsubjects in supervisors_numsubjects:
    capacity_per_subject = math.ceil(students_to_supervisors/numsubjects)
    supervisor_capacity.append([supervisor,capacity_per_subject])

print(supervisor_capacity)



#Add edges from each supervisor to their connected subjects
for i in range(len(df2)):
    subject = df2.iat[i,0]
    supervisor = df2.iat[i,1]
    
    for s,c in supervisor_capacity:
        if s == supervisor:
            capacity = c
    
    G.add_edge(subject,supervisor,capacity = capacity)
    
#Add edges from each student to each of their preferences
index = 0
for student in students:
    choice_1 = df1.iat[index,1]
    choice_2 = df1.iat[index,2]
    choice_3 = df1.iat[index,3]
    choice_4 = df1.iat[index,4]
    choice_5 = df1.iat[index,5]
    choices = [(choice_1,5),(choice_2,4),(choice_3,3),(choice_4,2),(choice_5,1)]
    for c,capacity in choices:
        subject = subjects[c-1]
        G.add_edge(student,subject,capacity = capacity)
    index += 1

#Adding source:
G.add_node('s')
for student in students:
    G.add_edge('s',student,capacity = 1)
    
#Adding sink:
G.add_node('t')
for supervisor in supervisors:
    G.add_edge(supervisor,'t')
    

# Calculate maximum flow
flow_value, flow_dict = nx.maximum_flow(G, 's', 't')

print("Maximal flow value:", flow_value)
print("Flow through each edge:")
for u, v in G.edges():
    print(f"Edge {u} -> {v}: Flow = {flow_dict[u][v]}")

# Calculate sum of flows to each supervisor
print("\nSum of flows to each supervisor:")
for supervisor in supervisors:
    inflow_sum = sum(flow_dict.get(subject, {}).get(supervisor, 0) for subject in subjects)
    print(f"Supervisor {supervisor}: Sum of flows = {inflow_sum}")
