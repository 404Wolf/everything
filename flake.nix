{
  description = "Literally everything in Python";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells = {
          default = pkgs.mkShell {
            UV_VENV_CLEAR="1";
            EVERYTHING_DEBUG="1";
            shellHook = ''
              uv venv
              source .venv/bin/activate
              uv pip install -e .
            '';
            packages = with pkgs; [
              python313
              ruff
              uv
            ];
          };
        };
      }
    );
}
