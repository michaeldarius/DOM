class IndexSelectorBase:
    """
    This is the IndexSelectorBase abstract base class. It serves as the
    foundation for an index selector concrete class. All concrete classes must
    override both the constructor and the getIndex member function. The id
    passed to the getIndex function is interpreted based on the implementation
    provided by the concrete class. The format of the id object that the
    concrete classes should expect to work on are of the form:
    (\"bankN\", (i, j)) which is a tuple containing a string and a tuple of
    two numbers and where N, i and j are numbers particular to the data
    set read from a NeXus file.
    """
    
    def __init__(self,**kwargs):
        """
        MUST OVERRIDE
        """
        
        raise NotImplementedError

    def getIndex(self, id):
        """
        MUST OVERRIDE
        """
        raise NotImplementedError


def getIndexSelector(selector_name,**kwargs):
    """
    This is the factory function for obtaining concrete index selector objects.

    Parameters:
    ----------
    -> selector_name is the class name of the concrete index selector
    -> kwargs is a list of key word arguments that the requested index selector
       will accept

    Returns:
    -------
    <- The requested index selector object

    Exceptions:
    ----------
    <- Exception is raised if the requested index selector name is not
       present in the factory list
    """
    
    import simpleselector

    if selector_name == "ISelector":
        return simpleselector.ISelector(**kwargs)
    elif selector_name == "JSelector":
        return simpleselector.JSelector(**kwargs)
    elif selector_name == "ZSelector":
        return simpleselector.ZSelector(**kwargs)
    elif selector_name == "IJSelector":
        return simpleselector.IJSelector(**kwargs)
    else:
        raise Exception, "Do not understand selector %s" % selector_name


