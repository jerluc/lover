package main

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
)

func main() {
	var configFile string
	var config *Config
	var rootCmd = &cobra.Command{
		Use: "lover",
		PersistentPreRun: func(cmd *cobra.Command, args []string) {
			loadedConfig, configErr := LoadConfig(configFile)
			if configErr != nil {
				fmt.Println("Failed to load lover configuration:", configErr)
				os.Exit(127)
			}
			// This is really stupid...
			// TODO: Let's not use this silly CLI library
			config = loadedConfig
		},
	}
	rootCmd.PersistentFlags().StringVarP(&configFile, "config", "c", "", "Configuration file")

	var cmdInit = &cobra.Command{
		Use:   "init",
		Short: "Creates a new project in the current directory",
		Long: `Creates a new LOVE project in the current directory.
		`,
		Run: func(cmd *cobra.Command, args []string) {
			RunInitCommand(config)
		},
	}

	var cmdRun = &cobra.Command{
		Use:   "run",
		Short: "Runs the current project",
		Long: `Runs the current LOVE project found in the current directory. The appropriate distro
		will be selected for your current environment.
		`,
		Run: func(cmd *cobra.Command, args []string) {
			RunRunCommand(config)
		},
	}

	rootCmd.AddCommand(cmdInit, cmdRun)
	rootCmd.Execute()
}
