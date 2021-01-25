class qtComponent():
    
    required_args = set()  # To be overridden by subclasses
    required_props = set()  # To be overridden by subclasses
    
    def __init__(self, *a, args: dict = None, props: dict = None, **kwargs):
        '''
        :param a: other arguments to pass to the next constructor on the MRO
        :type a: tuple
        :param args: arguments, not expected to change after construction
        :type args: dict
        :param props: properties, set externally and expected to be changed after construction
        :type props: dict
        :param kwargs: other keyword arguments to pass to the next constructor on the MRO
        :type kwargs: dict
        '''
        super().__init__(*a, **kwargs)
        missing_args = {arg for arg in self.__class__.required_args if arg not in args}
        if missing_args:
            raise ValueError(f'Missing arguments {missing_args}')
        self.args = args or {}
        self.props = props or {}
        self.props_changed = set(self.props.keys())
        self.state = {}
        self.state_changed = set()
        self.children = {}
        self.ui_initialized = False
        
        self.uiInit()
        self.update()

    def uiInit(self):
        pass  # To be overridden by subclasses
    def update(self):
        pass  # To be overridden by subclasses

    def setProps(self, **kwargs):
        'For use by parent widgets.'
        self.props.update(**kwargs)
        self.props_changed = self.props_changed.union(set(kwargs.keys()))  # So that you can save some computations
        return self.update()
    
    def setState(self, **kwargs):
        'For use by self.'
        self.state.update(**kwargs)
        self.state_changed = self.state_changed.union(set(kwargs.keys()))  # So that you can save some computations
        return self.update()