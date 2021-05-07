#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(_: [ ((import (builtins.fetchTarball ''https://github.com/nix-community/NUR/archive/master.tar.gz'') { inherit pkgs; }).repos.angr.python3Packages.angr) ])"

import sys
import string
import angr
import claripy
import logging

logging.getLogger('angr').setLevel('INFO')

def should_abort(state):
    return b'Wrong password' in state.posix.dumps(sys.stdout.fileno())

p = angr.Project("crackme")

addr_main = p.loader.find_symbol("main").rebased_addr

addr_target = p.loader.find_symbol("check").rebased_addr + 42
baddr_target = p.loader.find_symbol("check").rebased_addr + 28

"""
flag_chars = [claripy.BVS('flag_%d' %i, 8) for i in range(25)]
extra_chars = [claripy.BVS('flag_0_%d' % i, 8) for i in range(2)]
all_chars = *flag_chars + [claripy.BVV(b'\0')]
all_chars = all_chars ++ extra_chars
flag = claripy.Concat(all_chars)
"""
"""
t1 = claripy.BVV('flag-')
t2 = claripy.BVV(0x31337, 32)
t2 = [claripy.BVS(f'{i}', 8) for i in range(8)]
t3 = claripy.BVV('-')
t4 = [claripy.BVS(f'{i}', 8) for i in range(8)]
t5 = claripy.BVV('.')
t6 = [claripy.BVS(f'{i}', 8) for i in range(6)]
flag = claripy.Concat(t1, *t2, t3, *t4, t5, *t6)
all_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(40)]
"""
all_chars = [claripy.BVS(f'arg1_{i}', 8) for i in range(35)]
flag = claripy.Concat(claripy.BVV('flag-'), *all_chars)
print(flag)

print(angr.options)

st = p.factory.full_init_state(
        args = ['./result/bin/crackme', flag],
        options = angr.options.unicorn
        # addr=addr_main
        # stdin=flag
)

for k in all_chars:
    st.solver.add(k < 0x7f)
    st.solver.add(k >= 0)
    # st.solver.add(k > 0x20)
#st.add_constraints(arg1.get_byte(5) == claripy.BVV('-'))

"""
for k in extra_chars:
    st.solver.add(k != 0)
    st.solver.add(k != 10)
"""

sm = p.factory.simulation_manager(st)
#sm = p.factory.simulation_manager(st, save_unconstrained = True, threads = 8)

sm.explore(find=addr_target, avoid=baddr_target)
while len(sm.found) == 0:
    sm.step()

if len(sm.found) > 0:
    print("Found!")
    fond_input = sm.found[0].solver.eval(flag, cast_to=bytes)
    print(found_input)
else:
    print("Nothing found")

