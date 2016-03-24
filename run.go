package main

import (
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strconv"
)

const (
	WinPlatform = "win"
	MacPlatform = "darwin"
)

func platformToDistro(platform string, _32or64 int) string {
	if platform == MacPlatform {
		return LatestLoveDistro(Mac)
	} else {
		panic("Not implemented")
	}
}

func RunRunCommand(config *Config) {
	// First try to find LOVE in the current directory
	distroToUse := platformToDistro(runtime.GOOS, strconv.IntSize)

	// Then try to find the LOVE binary on the user's path
	if distroToUse == "" {
		distroToUse, _ = exec.LookPath("love")
	}

	if distroToUse == "" {
		fmt.Println("Could not find a suitable LOVE distribution for your current platform!")
		fmt.Println("Maybe try running:\n\n    lover init\n\nto download a distro that works?")
		return
	}

	cmd := exec.Command(distroToUse, ".")
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		panic(err)
	}
}
