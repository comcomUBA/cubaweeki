{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python3Packages.matplotlib
    python3Packages.requests
    python3Packages.pudb
  ];

  shellHook = ''
  '';
}
