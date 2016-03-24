package main

import (
	"io/ioutil"
)

const (
	Win32 = "win32"
	Win64 = "win64"
	Mac = "osx"
	Linux = "linux"
)

type Config struct {
	Name   string `yaml:"name"`
	Description string `yaml:"description"`
	Author string `yaml:"author"`
	License string `yaml:"license"`
	LoveVersion string `yaml:"loveVersion"`
	TargetPlatforms []string `yaml:"targetPlatforms"`
}

var DefaultConfig = Config{
	Name: "<PROJECT-NAME>",
	Description: "<PROJECT-DESCRIPTION>",
	Author: "<PROJECT-AUTHOR>",
	License: "Apache",
	LoveVersion: "0.10.1",
	// TODO: Allow Windows and Linux by default once the downloads are easier
	TargetPlatforms: []string{Mac},
}

func LoadConfig(configFile string) *Config {
	config := readOrDefaultConfig(configFile)
	// TODO: Do sanity checks on the config here
	return &config
}

func readOrDefaultConfig(configFile string) Config {
	fileContents, readErr := ioutil.ReadFile(configFile)
	if readErr != nil {
		return DefaultConfig
	}
	// TODO: Read in the config file as a YAML file and set it here
	fileContents = fileContents[:]
	return DefaultConfig
}
