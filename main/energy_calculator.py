import math

DIM_TO_INT = {'N': 0, 'W': 1, 'H': 2, 'C': 3, 'K': 4, 'R': 5, 'S': 6}
INT_TO_DIM = ['N', 'W', 'H', 'C', 'K', 'R', 'S']
N = 0; W = 1; H = 2; C = 3; K = 4; R = 5; S = 6

def get_level_access(layer, schedule):
    '''
    Input: a layer and a schedule
    Output: a list of access number for each level of cache
    '''
    accesses = []
    cumulative_loop_mul = 1 # total product of loop numbers so far
    prev_block_sizes = layer.get_sizes()
    prev_access = [layer.get_image_size(), layer.get_filter_size(), layer.get_output_size()]

    for level in range(schedule.num):
        cur_loop_mul = schedule.get_level_loop_multiplier(level)
        cur_block_size = schedule.get_level_block_size(level)
        cur_loop_order = schedule.get_level_loop_order(level)
        new_image, new_filter, new_output = 0, 0, 0

        image_para = [N, W, H, C, R, S]
        if all([cur_loop_mul[i] == 1 for i in image_para]):
            new_image = prev_access[0]
        else:
            new_image = cumulative_loop_mul
            im = [0] * 7
            last_dim = max([cur_loop_order[i] for i in image_para])
            for i in range(7):
                if cur_loop_order[i] < last_dim:
                    new_image *= cur_loop_mul[i]
                    im[i] = cur_block_size[i]
                elif cur_loop_order[i] == last_dim:
                    im[i] = block_sizes[i]
            new_image *= im[N] * im[C] * (im[W] *layer.strW + im[R]) * (im[H] *layer.strH + im[S])

        filter_para = [C, K, R, S]
        if all([cur_loop_mul[i] == 1 for i in filter_para]):
            new_filter = prev_access[1]
        else:
            new_filter = cumulative_loop_mul
            last_dim = max([cur_loop_order[i] for i in filter_para])
            for i in range(7):
                if cur_loop_order[i] < last_dim:
                    new_filter *= cur_loop_mul[i]
                    if i in filter_para:
                        new_filter *= cur_block_size[i]
                elif cur_loop_order[i] == last_dim:
                    new_filter *= block_sizes[i]

        output_para = [N, W, H, K]
        if all([cur_loop_mul[i] == 1 for i in output_para]):
            new_output = prev_access[2]
        else:
            new_output = cumulative_loop_mul
            last_dim = max([cur_loop_order[i] for i in output_para])
            for i in range(7):
                if cur_loop_order[i] < last_dim:
                    new_output *= cur_loop_mul[i]
                    if i in output_para:
                        new_output *= cur_block_size[i]
                elif cur_loop_order[i] == last_dim:
                    new_output *= block_sizes[i]

        for mul in cur_loop_mul:
            cumulative_loop_mul *= mul
        block_sizes = cur_block_size
        prev_access = [new_image, new_filter, new_output]
        access_num = new_image + new_filter + new_output * 2 - layer.get_output_size()
        accesses.append(access_num)
    return accesses

def validate(layer, schedule, arch):
    '''
    Input: a layer, a schedule, and an arch
    Output: return True if the following two conditions are satisfies:
        * at each level, the block size * the loop multiplier >= previous block size
        * at each level, the sum of block sizes <= cache size
    '''
    block_sizes = layer.get_sizes()
    for level in range(schedule.num):
        m = schedule.get_level_loop_multiplier(level)
        b = schedule.get_level_block_size(level)
        cache_size = arch.get_size(level)
        for i in range(7):
            if b[i] * m[i] < block_sizes[i]:
                return False
        image = b[N] * b[C] * (b[W] *layer.strW + b[R]) * (b[H] *layer.strH + b[S])
        filte = b[C] * b[K] * b[R] * b[S]
        outpu = b[N] * b[K] * b[W] * b[H]
        if image + filte + outpu > cache_size:
            return False
        block_sizes = b
    return True

def get_energy(layer, schedule, arch):
    '''
    return the total energy cost
    '''
    energy = 0
    accesses = get_level_access(layer, schedule)
    for level in range(arch.num):
        energy += accesses[level] * arch.get_energy(level)
    return energy








