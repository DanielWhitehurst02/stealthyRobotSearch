
import numpy as np

frontiersqueue = [[0,0],[0,1],[5,6],[9,7],[1,2],[8,8],[20,20],[21,21]]



def queue_process(frontiersqueue):
    search = True
    i = 0
    grouped = []
    current_group = []
    adjacent = True
    while search:
        
        if frontiersqueue:
            

            if current_group:
                while adjacent:
                    adjacent = False
                    for j in range(len(current_group)):
                        print(current_group)
                        for h in range(len(frontiersqueue)):
                            # print( str(h) + " len: " + str(len(frontiersqueue)))
                            if h >= (len(frontiersqueue)):
                                continue
                            x_o, y_o = current_group[j][0],current_group[j][1]
                            x_1, y_1 = frontiersqueue[h][0],frontiersqueue[h][1]
                            # if x_o == x_1 and y_o == y_1:
                            # print(str(abs(x_o - x_1))+str(abs(y_o - y_1)))
                            if (abs(x_o - x_1) <= 1 and abs(y_o - y_1) <= 1):
                                
                                adjacent = True
                                current_group.append(frontiersqueue[h])
                                del frontiersqueue[h]
                
                grouped.append(current_group)
                current_group = []
                
                        


            else:
                current_group.append(frontiersqueue[0])
                del frontiersqueue[0]
                adjacent = True
        else:
            search = False
    return grouped


print(queue_process(frontiersqueue))