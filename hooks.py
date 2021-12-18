from androidemu.emulator import Emulator
from androidemu.java.helpers.native_method import native_method
from androidemu.utils import memory_helpers

emulator = Emulator()

@native_method
def __aeabi_memclr(mu, addr, size):
    mu.mem_write(addr, bytes(size))

@native_method
def __aeabi_memcpy(mu, dist, source, size):
    data = mu.mem_read(source, size)
    mu.mem_write(dist, bytes(data))

@native_method
def sprintf(mu, buffer, fmt, a1, a2):
    fmt1 = memory_helpers.read_utf8(mu, fmt)
    data1 = memory_helpers.read_utf8(mu, a1)
    mu.mem_write(buffer, bytes((fmt1 % (data1, a2) + '\x00').encode('utf-8')))
    
emulator.modules.add_symbol_hook('__aeabi_memclr', emulator.hooker.write_function(__aeabi_memclr) + 1)
emulator.modules.add_symbol_hook('__aeabi_memcpy', emulator.hooker.write_function(__aeabi_memcpy) + 1)
emulator.modules.add_symbol_hook('sprintf', emulator.hooker.write_function(sprintf) + 1)
