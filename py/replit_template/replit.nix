{ pkgs }: {
    deps = [
        pkgs.bashInteractive
        pkgs.python310.out
        pkgs.python39Packages.pip.out
    ];
}
