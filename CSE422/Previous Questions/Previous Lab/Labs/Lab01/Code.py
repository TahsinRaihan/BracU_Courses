from queue import PriorityQueue
queue = PriorityQueue()

with open("input_file.txt", "r") as file:
    inp = file.readlines()
    h_value = {}
    graph = {}
    for i in inp:
        line = i.strip().split(" ")
        h_value[line[0]] = int(line[1])
        graph[line[0]] =  line[2:]
           
def fringe(start,goal):
    queue.put((h_value[start],start,'Null',0))
    distance = 0
    path = {}
    final_path = ''
    while True:
        value = queue.get()
        child, parent, dis = value[1], value[2], value[3]
        for i in range(0,len(graph[child]),2):
            queue.put((h_value[graph[child][i]]+int(graph[child][i+1])+dis,graph[child][i],child, dis+int(graph[child][i+1])))
            path[child] = [parent,dis]
        if child == goal:
            tempS = start
            tempE = goal
            for key in path.keys():
                if tempE == tempS:
                    final_path = tempE + final_path
                    return f"Path: {final_path} \nTotal distance: {dis} km"
                else:
                    final_path  = ' -> '+ tempE + final_path
                    tempE = path[tempE][0]
            return ('NO PATH FOUND')
        
start = 'Arad'
goal = 'Bucharest'  

print(fringe(start,goal))