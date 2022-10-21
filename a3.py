class Trees:
    class node:
        def __init__(self,element,left_list = [],right_list = [],parent = None,left = None,right = None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right
            self.left_list = left_list
            self.right_list = right_list
    def __init__(self):
        self.list = []
        self.root = None
    def median(self,p):
        n = len(p)
        if n==1 or n==0:
            return None
        if n%2==0:
            return p[(n//2)-1][0], (n//2)-1
        else:
            return p[(n-1)//2][0], (n-1)//2
    def insert(self,e,p = None):
        if self.root is None:
            self.root = e
        else:
            if p.left is None:
                e.parent = p
                p.left = e
            elif p.right is None:
                e.parent = p
                p.right = e     
    def create_tree(self,parent,list):
        if self.median(list) is not None:
            (i,index) = self.median(list)
            q = self.node(f'x<={i}',list[0:index+1],list[index+1:]) 
            self.insert(q,parent)
            self.create_tree(q, q.left_list)
            self.create_tree(q, q.right_list)          
    def list_sorted(self):
        r = self.root 
        out = []
        if r is not None:
            self.list.append(r.element)
            out.append(r)
            i = 0
            level = 0
            while len(out)!=0:     
                x = out.pop(0)
                if type(x)!=list:
                    level+=1
                    if x.left is not None:
                        i +=1
                        self.list.append(x.left.element)
                        out.append(x.left) 
                    if x.right is not None:
                        i+=1
                        self.list.append(x.right.element)
                        out.append(x.right)     
                    if x.left is None:
                        if x.left_list is not None:
                            self.list.append(x.left_list[0])
                            out.append(x.left_list)
                    if x.right is None:
                        if x.right_list is not None:
                            self.list.append(x.right_list[0])
                            out.append(x.right_list)
    def __str__(self):
        self.list_sorted()
        return str(self.list)
class PointDatabase:
    def __init__(self,list):
        def sort_x(x):
            return x[0]
        list_copy_x = list.copy()
        list_copy_x.sort(key = sort_x)
        self.x_tree = Trees()
        self.x_tree.create_tree(None, list_copy_x)
        self.out = []
    def canonical_set(self,limit,limit_y,root):
        if root is not None:
            r = float(root.element[3:])
            if r < limit[0]:
                range = []
            elif r >= limit[1]:
                range = [limit[0],limit[1]]
            elif r == limit[0]:
                range = [r,r]
            elif r > limit[0] and r < limit[1]:
                range = [limit[0],r]
            if root.left is None:
                if range!=[] and range!=limit:
                    if root.left_list[0][1]>=limit_y[0] and root.left_list[0][1]<=limit_y[1]:
                        self.out.extend(root.left_list)
                elif range==limit:
                    if root.left_list[0][0]<=limit[1] and root.left_list[0][0]>=limit[0]:
                        if root.left_list[0][1]>=limit_y[0] and root.left_list[0][1]<=limit_y[1]:
                            self.out.extend(root.left_list)
            if root.right is None:
                if range!=[] and range!=limit:
                    if root.right_list[0][0]<=limit[1] and root.right_list[0][0]>=limit[0]:
                        if root.right_list[0][1]>=limit_y[0] and root.right_list[0][1]<=limit_y[1]:
                            self.out.extend(root.right_list)
            if range==[]:
                if root.right is not None:                    
                    self.canonical_set(limit, limit_y, root.right)
                else:
                    if root.right_list[0][0]<=limit[1] and root.right_list[0][0]>=limit[0]:
                        if root.right_list[0][1]<=limit_y[1] and root.right_list[0][1]>=limit_y[0]:
                            self.out.extend(root.right_list)
            elif range == limit:
                self.canonical_set(limit, limit_y, root.left)
            else:
                self.canonical_set(limit, limit_y, root.left)
                self.canonical_set(limit, limit_y, root.right) 
    def searchNearby(self,q,d):
        x1 = q[0]
        y1 = q[1]
        x11 = x1-d
        x12 = x1+d
        y11 = y1-d
        y12 = y1+d
        self.out = []
        self.canonical_set([x11,x12], [y11,y12], self.x_tree.root)
        return self.out

