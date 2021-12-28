def flatten_dic(dic):
    """
    Flatten dictionnary with nested keys into a single level : usable in a dataframe
        Args:
            dic -- a dictionnary
        Returns:
            out -- the flatenned dictionnary (df(out) is a Series)
    """
    out = {}

    def flatten(x, name=""):
        """
        Recursive axuiliary function
            Args:
                x -- an element (a dict, a list, or a value)
                name -- The inherited parent naming
        """
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(dic)
    return out

