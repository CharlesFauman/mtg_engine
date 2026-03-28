# %%
# --- DSL Framework ---
def add_properties(cls, **annotations):
    """
    Dynamically adds typed properties to a class and updates its __init__
    so it can accept them as kwargs, preserving previous properties.
    """
    if not hasattr(cls, '__annotations__'):
        cls.__annotations__ = {}
    cls.__annotations__.update(annotations)

    if not hasattr(cls, '_dsl_properties'):
        cls._dsl_properties = []
        
    # Only add new properties to avoid duplicates if called multiple times on the same class
    for key in annotations:
        if key not in cls._dsl_properties:
            cls._dsl_properties.append(key)

    def new_init(self, **kwargs):
        for prop in self.__class__._dsl_properties:
            setattr(self, prop, kwargs.get(prop))
            
    cls.__init__ = new_init
    return cls
