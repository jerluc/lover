package main

import (
	"fmt"
	"os"
	"path/filepath"
	"github.com/blang/semver"
)

const LoverDir = ".lover"
const DistrosDir = LoverDir + "/distros"
const DirectoryTemplate = DistrosDir + "/%s/%s"
const DistroFilename = "love.zip"
const FilenameTemplate = "love-%s-%s.zip"

func DistroDirectory(version string, platform string) string {
	return fmt.Sprintf(DirectoryTemplate, version, platform)
}

func LatestLoveDistro(platform string) string {
	latestDistroDir := LatestLoveDistroDirectory(platform)
	if latestDistroDir == "" {
		return ""
	}

	if platform == Mac {
		return filepath.Join(latestDistroDir, "love.app", "Contents", "MacOS", "love")
	}

	panic("Not supported yet!")
}

func LatestLoveDistroDirectory(platform string) string {
	distrosDir, err := os.Open(DistrosDir)
	if err != nil {
		return ""
	}

	distroVersions, _ := distrosDir.Readdirnames(-1)

	var semvers semver.Versions
	for _, distroVersion := range distroVersions {
		sv, _ := semver.Make(distroVersion)
		semvers = append(semvers, sv)
	}
	semver.Sort(semvers)

	for i := len(semvers) - 1; i >= 0; i-- {
		ver := semvers[i].String()
		distroPath := filepath.Join(DistrosDir, ver, platform)
		if _, err := os.Stat(distroPath); err == nil {
			return distroPath
		}
	}

	return ""
}
