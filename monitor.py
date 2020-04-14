import monitorcontrol as mc
from pyddcci.ddcci import DDCCIDevice

def find_monitor_busses():
    return [int(m.vcp.bus_number)
            for m in mc.get_monitors()]

VCP_INPUT = 0x60

def set_input(idx, input_code):
    bus_id = find_monitor_busses()[idx]
    monitor = DDCCIDevice(bus_id)

    monitor.write(VCP_INPUT, input_code)

    return True

def toggle_input(idx, A, B):
    bus_id = find_monitor_busses()[idx]
    monitor = DDCCIDevice(bus_id)

    if monitor.read(VCP_INPUT) == A:
        monitor.write(VCP_INPUT, B)
    else:
        monitor.write(VCP_INPUT, A)

    return True

