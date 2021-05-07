#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(_: [ ((import (builtins.fetchTarball ''https://github.com/nix-community/NUR/archive/master.tar.gz'') { inherit pkgs; }).repos.angr.python3Packages.angr) ])"

import sys
import string
import angr
import claripy

def should_abort(state):
    return b'Wrong password' in state.posix.dumps(sys.stdout.fileno())

p = angr.Project("./result/bin/crackme")

addr_main = p.loader.find_symbol("main").rebased_addr

addr_target = p.loader.find_symbol("check").rebased_addr + 42
baddr_target = p.loader.find_symbol("check").rebased_addr + 28

flag_chars = [claripy.BVS('flag_%d' %i, 8) for i in range(32)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\0')])

st = p.factory.full_init_state(
        #options=angr.options.unicorn,
        #addr=addr_main,
        stdin=flag
)

for k in flag_chars:
    st.solver.add(k != 0)
    st.solver.add(k != 10)

sm = p.factory.simulation_manager(st)
sm.run()

if 

sm.explore(find=addr_target)
while len(sm.found) == 0:
    sm.step()

if len(sm.found) > 0:
    print("Found!")
    found_input = sm.found[0].posix.dumps(0)
    print(found_input)

