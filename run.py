import main as mn

if __name__ == "__main__":
    layer = mn.ConvLayer(4, 64, 64, 64, 64, 3, 3)
    arch = mn.Arch([1024 * 1024 * 1024], [1])
    layer1 = [[1, 1, 1, 1, 1, 1, 1], [4, 64, 64, 64, 64, 3, 3], [0, 1, 2, 3, 4, 5, 6]]
    schedule = mn.Schedule([layer1])
    print(mn.validate(layer, schedule, arch))
    print(mn.get_energy(layer, schedule, arch))
