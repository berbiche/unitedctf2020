{
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system:
  let
    pkgs = nixpkgs.legacyPackages.${system};
    inputs = with pkgs; [
      binutils
      gdb
      ghidra-bin
      strace
      patchelf
      gcc
      checksec
      volatility
    ];
  in rec {
    devShell = pkgs.mkShell {
      src = null;
      buildInputs = inputs;
    };

    defaultPackage = pkgs.buildEnv {
      src = null;
      name = "unitedctf2020-packages";
      paths = inputs;
    };
  });
}
