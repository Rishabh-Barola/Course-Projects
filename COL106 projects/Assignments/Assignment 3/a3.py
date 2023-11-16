
#---------------------------------------------------------------------------#assignment 3#--------------------------------------------------------

class node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None
        self.y = []
        self.max = val

    def is_leaf(self):
        if self.left == None and self.right ==None:
            return True
        else:
            return False

# -------------------------------------------------------PointDatabase----------------------------------------------------------------------------
class PointDatabase:
    def __init__(self, pointlist):
        self.root = None

        nodelist = [] # will store all points as nodes in this list
        pointlist.sort()
        for i in pointlist:
            x = node(i)
            x.y = [i, ]
            nodelist.append(x)

        def merge(L1, L2): # helper function to merge two sorted lists L1 and L2 and return their merged list newlist
            newlist = []
            m,n = len(L1),len(L2)
            i,j = 0,0
            while(i<m) and (j<n):
                a1,b1 = L1[i]
                a2,b2 = L2[j]
                if b1<=b2:
                    newlist+=[L1[i]]
                    i+=1
                else:
                    newlist+=[L2[j]]
                    j+=1
            if i==m:
                while j<n:
                    newlist+=[L2[j]]
                    j+=1

            else:
                while i<m:
                    newlist+=[L1[i]]
                    i+=1
            return newlist

        def create_tree(node_list, right=True): # helper function which will create the tree nodes from nodes list.
                                                # all data is stored in leaves of the tree and the internal nodes contain maximum 
                                                # element of their left subtree for query handling
            if len(node_list) == 0:             # base case when nodelist is empty
                return []
            if len(node_list) == 1:             #root element returned
                return node_list[0]

            elif len(node_list) == 2:           # when two elements then create a new node and make the two elements its children.
                new = node(node_list[0].max)
                new.left = node_list[0]
                new.right = node_list[1]
                new.max = max(new.left.max, new.right.max)
                new.y = merge(new.left.y, new.right.y)
                return new

            else :
                new_list = []

                if len(node_list) % 2 == 0:
                    for i in range(0, len(node_list), 2):
                        new_list.append(create_tree([node_list[i]]+[node_list[i+1]]))
                    return create_tree(new_list, right)

                else:
                    if right:
                        extra = node_list[0]
                        for i in range(1, len(node_list), 2):
                            new_list.append(create_tree(node_list[i:i + 2]))
                        return create_tree([extra] + new_list, not right)

                    else:
                        extra = node_list[-1]
                        for i in range(0, len(node_list) - 1, 2):
                            new_list.append(create_tree(node_list[i:i + 2]))
                        return create_tree(new_list + [extra], not right)

        self.root = create_tree(nodelist)



#----------------------------------------------Query handling----------------------------------------------------------------------------------


    def searchNearby(self,q,d):     # function which returns a list of points whose x-coordinates are in range q[0]-d,q[0]+d
                                    # function which returns a list of points whose y-coordinates are in range q[1]-d,q[1]+d
        anslist =[]
        a,b = q
        x1,x2 = a-d, a+d
        y1,y2 = b-d , b+d
        w = self.root
        if self.root == []:
            return []

        while w.is_leaf()==False and (x1>w.val[0] or x2<= w.val[0]):
            if x2 <= w.val[0]:
                w = w.left
            else:
                w = w.right
        # now w is split node

        if w.is_leaf():
            if y1 <=w.val[1]<= y2 and x1<= w.val[0]<=x2:
                anslist.append(w.val)
                
                
                
        else:
            v= w.left
            while not v.is_leaf():
                if x1 <= v.val[0]:
                    if v.right !=None:
                        self.find_in_array(v.right,y1,y2,anslist)
                    v = v.left
                
                else:
                    v = v.right

            if v.is_leaf():
                if y1 <= v.val[1] <= y2 and x1<= v.val[0]<=x2:
                    anslist.append(v.val)
                    

            v = w.right
            while not v.is_leaf():
                if x2 >= v.val[0]:
                    if v.left != None:
                        self.find_in_array(v.left,y1,y2,anslist)
                    v = v.right
                else:
                    v = v.left
            if v.is_leaf():

                if y1 <= v.val[1] <= y2 and x1<= v.val[0]<=x2:
                    anslist.append(v.val)
                    
        return anslist

    def find_in_array(self,node,y1,y2,anslist): # function which finds and appends tuples whose y-coordinate in range y1 to y2 to anslist.

        list_of_nodes = node.y     # list of tuples at node ordered with respect to y.
    
        i1 = self.binary_search_low(list_of_nodes,y1)
        i2 = self.binary_search_high(list_of_nodes,y2)

        if i1 == "outofrange" or i2 == "outofrange":
            pass
        
        elif i1!=i2 :

            anslist += list_of_nodes[i1:i2+1]
            
        else:
            if y1<=list_of_nodes[i1][1]<=y2:
                anslist.append(list_of_nodes[i1])
                
                


    def binary_search_low(self,ylist,y1):
        #returns index of element >= y1 in ylist.
        result1 = 0
        low = 0
        high = len(ylist)-1
        mid = 0
        
        if len(ylist)==1:
            if ylist[0][1]>=y1:

                return 0
            else:
                return "outofrange"
            
        if len(ylist)==2:
            if (ylist[1][1] < y1):
                return "outofrange"
            elif (ylist[1][1] >= y1):
                if (ylist[0][1] <y1):
                    return 1
                else:
                    return 0

        if (ylist[-1][1] < y1):
                return "outofrange"
            
        while low <= high:
            mid = (high+low)//2
            if (ylist[mid][1] < y1):
                low = mid+1
            elif (y1 < ylist[mid][1]):
                high = mid-1
                result1 = mid
            else:
                return mid
        return result1

    def binary_search_high(self,ylist,y2):
        #returns index of element <= y2 in ylist.
        result2 = 0
        low = 0
        high = len(ylist) - 1
        mid = 0

        if len(ylist)==1:
            if ylist[0][1]<=y2:
                return 0
            else:
                return "outofrange"

        if len(ylist)==2:
            if (ylist[0][1] > y2):
                return "outofrange"
            elif (ylist[0][1] <= y2):
                if (ylist[1][1] > y2):
                    return  0
                else:
                    return 1
                
        if (ylist[0][1] > y2):
                return "outofrange"
    
        while low <= high:
            mid = (high + low) // 2
            if (ylist[mid][1] < y2):
                low = mid + 1
                result2 = mid
            elif (y2 < ylist[mid][1]):
                high = mid - 1

            else:
                return mid
        return result2

   