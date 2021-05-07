#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(_: [ ((import (builtins.fetchTarball ''https://github.com/nix-community/NUR/archive/master.tar.gz'') { inherit pkgs; }).repos.angr.python3Packages.angr) ])"

import angr

p = angr.Project("./result/bin/onetimepad")

addr_main = p.loader.find_symbol("main").rebased_addr

addr_target = addr_main + 365

print(addr_main)

state = p.factory.entry_state(addr=addr_main)
sm = p.factory.simulation_manager(state)

sm.explore(find=addr_target)
while len(sm.found) == 0:
    sm.step()

if len(sm.found) > 0:
    print("Found!")
    found_input = sm.found[0].posix.dumps(0)
    print(found_input)

