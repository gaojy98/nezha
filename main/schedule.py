class Schedule:
    '''
    Schedule: the slicing scheme
    Schedule object is a list of list of list
    There are three lists for each level, corresponding to each level of cache
    First list is loop_multiplier
    Second list is block_size
    Third list is loop_order (0..6, 0 outer most, 6 inner most)
    '''
    def __init__(self, schedule):
        self.schedule = schedule
        self.num = len(schedule)

    def get_level_loop_multiplier(self, level):
        '''
        Loop multiplier at each level
        return a len 7 list for each dimension
        '''
        return self.schedule[level][0]

    def get_level_block_size(self, level):
        '''
        Block size at each level
        return a len 7 list for each dimension
        '''
        return self.schedule[level][1]

    def get_level_loop_order(self, level):
        '''
        Loop order at each level
        return a len 7 list for each dimension
        '''
        return self.schedule[level][2]
        