# Helper functions

def dict_to_tuple(alist):
    """
    Tested: Works 
    Converts a list of dictonaries to a list of tuples, with a seperate list of the dict keys
    Requires python 3.6+ since standard dicts are ordered
    Input: [ {A:B,...},... ]
    Output:[ (B,...), ... ], [A,..]
    """
    keys = []
    first_loop = True
    lst = []
    
    for item in alist:
        _ = [] #this will be converted to a tuple
        
        for key,value in item.items():
            if first_loop == True:
                keys.append(key)
            _.append(value)
        
        first_loop = False
        tple = tuple(_)
        lst.append(tple)
    
    return lst,keys