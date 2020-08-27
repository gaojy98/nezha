class Arch:
    '''
    Arch:the hardware with multi-level cache
    From top level cache (L3) to bottom level cache (L0)
    TODO: support parallelism
    '''
    def __init__(self, cache_sizes, cache_energies):
        assert len(cache_sizes) == len(cache_energies)
        self.num = len(cache_sizes)
        self.sizes = cache_sizes
        self.energies = cache_energies

    def get_size(self, level):
        return self.sizes[level]

    def get_energy(self, level):
        return self.energies[level]
