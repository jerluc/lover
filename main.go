package main

import (
    "github.com/spf13/cobra"
)

func main() {
	var configFile string
	var config *Config
	var rootCmd = &cobra.Command{
		Use: "lover",
		PersistentPreRun: func(cmd *cobra.Command, args []string) {
			config = LoadConfig(configFile)
		},
	}
    rootCmd.PersistentFlags().StringVarP(&configFile, "config", "c", ".lover.yaml", "Configuration file")

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
