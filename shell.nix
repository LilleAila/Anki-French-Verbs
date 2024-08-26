with import <nixpkgs> {}; mkShell {
  nativeBuildInputs = [
    (python311.withPackages (ps: with ps; [genanki]))
  ];
}
