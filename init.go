package main

import (
	"archive/zip"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"text/template"
)

// TODO: Is this the best we can do?
const DownloadUrlTemplate = "https://bitbucket.org/rude/love/downloads/%s"

const CONF_LUA = `function love.conf(t)
    -- Package settings
    t.identity = "{{.Name}}"
    t.title = "{{.Name}}"
    t.version = "{{.LoveVersion}}"

    -- Window/display settings
    t.window.width = 800
    t.window.height = 600
    t.window.fullscreen = false
    t.window.fullscreentype = "desktop"
    t.window.highdpi = false
end
`

const MAIN_LUA = `function love.draw()
    love.graphics.print("Hello World", 400, 300)
end
`

var fileNameMappings = map[string]string{
	Win32: "win32",
	Win64: "win64",
	Mac: "macosx-x64",
	Linux: "<DOESN'T WORK YET>",
}

func RunInitCommand(config *Config) {
	downloadLoveDistributions(config.LoveVersion, config.TargetPlatforms)
	extractLoveDistributions(config.LoveVersion, config.TargetPlatforms)
	createDefaultFile(config, "conf.lua", CONF_LUA)
	createDefaultFile(config, "main.lua", MAIN_LUA)
}

func downloadLoveDistributions(version string, platforms []string) {
	var wg sync.WaitGroup

	// TODO: Check for failures
	reporter := func(downloadErr error) {
		if downloadErr != nil {
			fmt.Printf("Could not download LOVE distribution: %s\n", downloadErr)
		}
		wg.Done()
	}

	for _, platform := range platforms {
		wg.Add(1)
		go downloadLoveDistribution(version, platform, reporter)
	}

	fmt.Printf("Downloading LOVE distributions for platforms: %s\n", platforms)
	wg.Wait()
	fmt.Println("Finished downloading LOVE distributions")
}

func downloadLoveDistribution(version string, platform string, reporter func(error)) {
	downloadFile := fmt.Sprintf(FilenameTemplate, version, fileNameMappings[platform])
	downloadDirectory := DistroDirectory(version, platform)
	localFilePath := filepath.Join(downloadDirectory, DistroFilename)
	downloadUrl := fmt.Sprintf(DownloadUrlTemplate, downloadFile)

	// Only proceed if there isn't already a distro with the same
	// version and platform
	if _, err := os.Stat(localFilePath); !os.IsNotExist(err) {
		reporter(nil)
		return
	}

	// Create the local output file
	// TODO: Create the local output file into a temp directory?
	os.MkdirAll(downloadDirectory, os.ModePerm)
	out, err := os.Create(localFilePath)
	defer out.Close()
	if err != nil {
		reporter(err)
		return
	}

	// Download the distribution
	resp, err := http.Get(downloadUrl)
	defer resp.Body.Close()
	if err != nil {
		reporter(err)
		return
	}

	io.Copy(out, resp.Body)

	reporter(nil)
}

func extractLoveDistributions(version string, platforms []string) {
	var wg sync.WaitGroup

	// TODO: Check for failures
	reporter := func(extractErr error) {
		if extractErr != nil {
			fmt.Printf("Could not extract LOVE distribution: %s\n", extractErr)
		}
		wg.Done()
	}

	for _, platform := range platforms {
		wg.Add(1)
		go extractLoveDistribution(version, platform, reporter)
	}

	fmt.Printf("Extracting LOVE distributions for platforms: %s\n", platforms)
	wg.Wait()
	fmt.Println("Finished extracting LOVE distributions")
}

func extractLoveDistribution(version string, platform string, reporter func(error)) {
	distroDirectory := fmt.Sprintf(DirectoryTemplate, version, platform)
	localFilePath := filepath.Join(distroDirectory, DistroFilename)
	reporter(unzip(localFilePath, distroDirectory))
}

// Shamelessly stolen from http://blog.ralch.com/tutorial/golang-working-with-zip/
func unzip(archive, target string) error {
	reader, err := zip.OpenReader(archive)
	if err != nil {
		return err
	}

	if err := os.MkdirAll(target, 0755); err != nil {
		return err
	}

	for _, file := range reader.File {
		path := filepath.Join(target, file.Name)
		if file.FileInfo().IsDir() {
			os.MkdirAll(path, file.Mode())
			continue
		}

		fileReader, err := file.Open()
		if err != nil {
			return err
		}
		defer fileReader.Close()

		targetFile, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
		if err != nil {
			return err
		}
		defer targetFile.Close()

		if _, err := io.Copy(targetFile, fileReader); err != nil {
			return err
		}
	}

	// TODO: It's important to not remove the original file so as to not duplicate distro
	// downloading. We should put this back in once that behavior is fixed
	// return os.Remove(archive)
	return nil
}

func createDefaultFile(config *Config, path, contents string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		mainLua, err := os.Create(path)
		if err != nil {
			panic(err)
		}
		defer mainLua.Close()

		tmpl, err := template.New("test").Parse(contents)
		if err != nil {
			panic(err)
		}

		err = tmpl.Execute(mainLua, config)
		if err != nil {
			panic(err)
		}
	}
}
