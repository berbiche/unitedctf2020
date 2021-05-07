#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(_: [ ((import (builtins.fetchTarball ''https://github.com/nix-community/NUR/archive/master.tar.gz'') { inherit pkgs; }).repos.angr.python3Packages.angr) ])"

import angr
import claripy
import rex

crash = rex.Crash("./result/bin/crackme", b"\x41"*300)
print(crash.explorable())

crash.explore()

print(crash.crash_types)

ar = crash.exploit()

ar.best_type2.test_binary()

