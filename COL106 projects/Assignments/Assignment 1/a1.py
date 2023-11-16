"""COL106 assignment -1
 
"""

class linked_stack:
    class node:
        __slots__ = ['element', 'next']

        def __init__(self, element, next):
            self.element = element
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def top(self):
        if self.is_empty():
            raise EOFError('stack is empty')

        return self.head.element

    def push(self, e):
        self.head = self.node(e, self.head)
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise EOFError('stack is empty')
        answer = self.head.element
        self.head = self.head.next
        self.size -= 1
        return answer

    def __str__(self):
        arr = ''
        start = self.head
        for i in range(self.size):
            arr += str(start.element) + ', '
            start = start.next

        return '<' + arr + ']'
    



"""
ALGORITHM:
we traverse the input string using loop as soon as we encounter a number we know that it will be followed by an "(" bracket later 
so we update the factorstack by pushing into it factor*number that we are currently traversing(using length_of_integer method)
and as soon as we encounter ")" we pop that to element from the stack as we no longer require it inour calculations as multiplication 
of that number was only limited to the elements of the bracket
now whenever we encounter any expression like +X or -Z we simply add or subtract factor or factorstack's top element to that coordinate
 to keep on updating our calculations.



Time complexity analysis:
linked_Stack() uses O(1) time for each of the operations pop(), push(), top()
and our function findPositionandDistance(S)
uses a loop which will run at a maximun of n times where n is len(S)
and as all operations in our loop takes O(1) time except slicing which increases if the numbers preceding the brakets are large
but still  overall time complexity of this function is still O(n) .


"""

factorstack = linked_stack()                          #create an object factorstack of datatype linked_stack().
                                                      # in other words instantiation of linked_stack() class

def findPositionandDistance(S):                       #function specification:
                                                      #Input: a string consisting of X,Y,Z,+,-,(,),numbers which 
                                                      #       denote drone program
                                                      #Output:a list with x,y,z coordinates and total distance travelled.
                                                      

    factorstack.push(1)                               #push 1 into stack so that we never multiply by zero .

    x, y, z, d = 0, 0, 0, 0                           #initialisation of x,y,z,d
    
    length_of_integer =0                              # create an identifier which will store the length of number
                                                      # preceding the '(' . to be used later to slice that number from the list.
    
    i=0
    while i <len(S):                           # loop to read the string input

        factor = factorstack.top()                    #created an identifier called factor to store the top 
                                                      #element of the stack using stack operations

        if S[i] == '+':                               #cond 1: when we detect "+" while traversing through string 
            d += factor                               # we will add factor that is the top element of the stack to d 
            i+=1                                      # increment the loop variable i
            if  S[i]== 'X':                           #increase x or y or z by amount factor 
                x += factor
            elif S[i] == 'Y':
                y += factor
            elif S[i] == 'Z':
                z += factor
            i+=1                                      ## increment the loop variable i again to move to next term

        elif S[i] == '-':
            d += factor
            i+=1
            if S[i] == 'X':
                x -= factor
            elif S[i] == 'Y':
                y -= factor
            elif S[i] == 'Z':
                z -= factor
            i+=1

        elif S[i].isdigit():                           # when you detect a number increase the length_of_integer by 1
                                                       # do this until there is no digit followed by an digit that is we meet a "("
            length_of_integer+=1

            if S[i+1]=="(":

                factorstack.push(int(S[i-length_of_integer+1:i+1])*int(factor)) # now slice that number from the string based on length_of_integer 
                                                                                # and push it into stack after multiplying it by factor .
                length_of_integer=0                                             # assign it to 0 for next iteration of the loop
            i+=1

        elif S[i] == '(':                                # if we detect this bracket we move forward
            i+=1

        elif S[i] == ')':                                 # if we detect this bracket then we remove the top element form factorstack
            factorstack.pop()
            i+=1

    return [x, y, z, d]




"""
example : findPositionandDistance(’+Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))’)

the following lines depict factorstack and pointer which moves along the string printed using:
        print("pathinput",S)
        print("pointer  " +"_"*i+"^")
        print("factorstack",factorstack)

pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  __^
factorstack <1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ___^
factorstack <6, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ____^
factorstack <6, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ______^
factorstack <6, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ________^
factorstack <6, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  __________^
factorstack <6, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ____________^
factorstack <6, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _____________^
factorstack <1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ______________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _______________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _________________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ___________________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _____________________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _______________________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ________________________^
factorstack <72, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _________________________^
factorstack <72, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ___________________________^
factorstack <72, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _____________________________^
factorstack <72, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _______________________________^
factorstack <72, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ________________________________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  __________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ____________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ______________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ________________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  __________________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ______________________________________________________^
factorstack <324, 81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _______________________________________________________^
factorstack <81, 9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  ________________________________________________________^
factorstack <9, 1, ]
pathinput +Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))
pointer  _________________________________________________________^
factorstack <1, ]
[-339, 396, -476, 2221]






"""