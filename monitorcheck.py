from screeninfo import get_monitors

monitors = get_monitors()

for monitor in monitors:
    print(f"Monitor: {monitor.name}")
    print(f"Resolution: {monitor.width}x{monitor.height}")
    print(f"Position: ({monitor.x}, {monitor.y})")
    print('-'*40)
