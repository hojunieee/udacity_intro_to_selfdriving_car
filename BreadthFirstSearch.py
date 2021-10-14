#This is pseudocode for Breadth First Search
#Garanteed to have optimized answer

function Graph.Search(problem):
    frontier = {[initial}
    explored={}
    if frontier is empty:
        return Fail
    path = remove.choice(frontier)
    s=path.end:
    add s to explored
    
    if s is a goal:
        return path
    
    for a in actions:
        add [path+a -> Resault(s,a)] to frontier unless Resault(s,a) in frontier or explored
