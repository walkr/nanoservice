def print_stats(n, duration):
    pairs = [
        ('Total messages', n),
        ('Total duration (s)', duration),
        ('Throughput (msg/s)', n/duration)
    ]
    for pair in pairs:
        label, value = pair
        print('* {:<25}: {:10,.2f}'.format(label, value))
    print('\n')