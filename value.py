class ValInfo:
    def __init__(self, v, v_type, lines=0, is_set=True):
        # number, idx or 2 idx for 'AKU'
        self.value = v
        # v_type:
        # 'NUM' - number
        # 'PIDENTIFIER' - identifier or identifier[number]
        # 'AKU' - identifier[identifier]
        # 'EXPRESSION' - result of '+', '-', '/', '*', '%'
        self.v_type = v_type
        # lines used to get value
        self.lines = lines
        # If value is set
        self.is_set = is_set
