import libvirt
from config import config
from sys import stderr

conn = libvirt.open()

def _find_domain(hint):
    doms = conn.listAllDomains()

    if len(doms) == 0:
        return None
    if len(doms) == 1 or hint is None:
        return doms[0]

    return conn.lookupByName(hint)

def attach(xml, vm = None):
    dom = _find_domain(vm)

    try:
        return (dom.attachDevice(xml) == 0, dom)
    except libvirt.libvirtError as e:
        # print('in attach():', e, file=stderr)
        return (False, dom)

def detach(xml, vm = None):
    dom = _find_domain(vm)

    try:
        return (dom.detachDevice(xml) == 0, dom)
    except libvirt.libvirtError as e:
        # print('in detach():', e, file=stderr)
        return (False, dom)

def startup(vm = None):
    dom = _find_domain(vm)
    if not dom.isActive():
        try:
            return (dom.create() == 0, dom)
        except libvirt.libvirtError as e:
            # print('in startup():', e, file=stderr)
            return (False, dom)
    return (False, dom)

def shutdown(vm = None):
    dom = _find_domain(vm)
    if dom.isActive():
        try:
            return(dom.shutdown() == 0, dom)
        except libvirt.libvirtError as e:
            # print('in startup():', e, file=stderr)
            return (False, dom)
    return (False, dom)
