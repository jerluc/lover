package main

import (
	"io/ioutil"
	"os"
	"gopkg.in/yaml.v2"
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

func LoadConfig(configFile string) (*Config, error) {
	config, err := readOrDefaultConfig(configFile)
	// TODO: Do sanity checks on the config here
	return config, err
}

func readOrDefaultConfig(configFile string) (*Config, error) {
	if configFile == "" {
		configFile = ".lover.yaml"
		if _, statErr := os.Stat(configFile); os.IsNotExist(statErr) {
			config := DefaultConfig
			// TODO: Prompt for missing values (project name, description, etc)?
			configBytes, marshalErr := yaml.Marshal(config)
			if marshalErr != nil {
				return nil, marshalErr
			}
			ioutil.WriteFile(configFile, configBytes, 0644)
		}
	}

	return readConfig(configFile)
}

func readConfig(configFile string) (*Config, error) {
	fileContents, readErr := ioutil.ReadFile(configFile)
	if readErr != nil {
		return nil, readErr
	}
	var config Config
	unmarshalErr := yaml.Unmarshal(fileContents[:], &config)
	if unmarshalErr != nil {
		return nil, unmarshalErr
	}
	return &config, nil
}
