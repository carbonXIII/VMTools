import monitorcontrol as mc

VCP_INPUT = 0x60

def set_input(idx, input_code):
    with mc.get_monitors()[idx].vcp as monitor:
        monitor.set_vcp_feature(VCP_INPUT, input_code)

    return True

def toggle_input(idx, A, B):
    with mc.get_monitors()[idx].vcp as monitor:
        if monitor.get_vcp_feature(VCP_INPUT)[0] == A:
            monitor.set_vcp_feature(VCP_INPUT, B)
        else:
            monitor.set_vcp_feature(VCP_INPUT, A)

    return True

