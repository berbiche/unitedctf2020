{ pkgs ? import <nixpkgs> { }
, stdenv ? pkgs.stdenv
, lib ? pkgs.lib
}:

stdenv.mkDerivation {
  name = "bunch-of-things";
  src = ./.;
  sourceRoot = ".";

  dontConfigure = true;
  dontBuild = true;
  dontStrip = true;
  keepDebugInfo = true;

  preFixup = let
    libPath = lib.makeLibraryPath [
      stdenv.cc.cc.lib
    ];
  in ''
    find $out/bin -type f -exec \
    patchelf \
      --set-interpreter "$(cat $NIX_CC/nix-support/dynamic-linker)" \
      --set-rpath "${libPath}" \
      {} \;
  '';

  installPhase = ''
    mkdir -p $out/bin
    find . -type f -executable -exec cp {} $out/bin/ \;
  '';
}
