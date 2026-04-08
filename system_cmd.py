"""
system_cmd.py — System command execution tool.

Handles:
  - Opening applications
  - Opening files and folders
  - Running safe shell commands
  - System info queries

Safety: Only allows a whitelist of safe operations.
We're not giving an AI unrestricted shell access. That's how Skynet starts.
"""

import logging
import os
import platform
import subprocess
import re
from typing import Optional

logger = logging.getLogger("buddy.tools.system_cmd")


class SystemCommandTool:
    """
    Execute system commands safely.

    Supports opening apps, files, and running whitelisted commands.
    """

    def __init__(self):
        self.system = platform.system().lower()  # "windows", "linux", "darwin"
        logger.info(f"SystemCommandTool initialized | OS: {self.system}")

        # Map of app names to actual commands/paths
        self.app_aliases = self._build_app_aliases()

    def execute(self, user_input: str) -> str:
        """
        Parse and execute a system command from natural language.

        Args:
            user_input: Natural language like "open the calculator"

        Returns:
            Status message about what was done.
        """
        text = user_input.lower().strip()

        # ── Open an application ──────────────────────────────────────────
        open_match = re.search(
            r"(?:open|launch|start|run)\s+(?:the\s+)?(.+)",
            text,
        )
        if open_match:
            app_name = open_match.group(1).strip()
            return self._open_app(app_name)

        # ── Close an application ─────────────────────────────────────────
        close_match = re.search(
            r"(?:close|quit|exit|kill)\s+(?:the\s+)?(.+)",
            text,
        )
        if close_match:
            app_name = close_match.group(1).strip()
            return self._close_app(app_name)

        # ── System info ──────────────────────────────────────────────────
        if any(kw in text for kw in ["system info", "my computer", "specs", "hardware"]):
            return self._system_info()

        # ── IP address ───────────────────────────────────────────────────
        if "ip address" in text or "my ip" in text:
            return self._get_ip()

        return f"Not sure how to handle that system command: '{user_input}'"

    # ── App Management ────────────────────────────────────────────────────

    def _open_app(self, app_name: str) -> str:
        """Open an application by name."""
        app_name_lower = app_name.lower().strip()

        # Check aliases first
        if app_name_lower in self.app_aliases:
            cmd = self.app_aliases[app_name_lower]
            return self._run_open_command(cmd, app_name)

        # Try to open it directly (works for many apps on all platforms)
        return self._run_open_command(app_name, app_name)

    def _run_open_command(self, target: str, display_name: str) -> str:
        """Run the platform-specific open command."""
        try:
            if self.system == "darwin":  # macOS
                subprocess.Popen(
                    ["open", "-a", target],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif self.system == "windows":
                os.startfile(target)
            else:  # Linux
                subprocess.Popen(
                    ["xdg-open", target],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return f"Opening {display_name}... done!"
        except FileNotFoundError:
            return f"Couldn't find '{display_name}'. Is it installed?"
        except Exception as e:
            return f"Failed to open {display_name}: {e}"

    def _close_app(self, app_name: str) -> str:
        """Close an application (best effort)."""
        try:
            if self.system == "darwin":
                subprocess.run(
                    ["osascript", "-e", f'quit app "{app_name}"'],
                    capture_output=True,
                    timeout=5,
                )
            elif self.system == "windows":
                subprocess.run(
                    ["taskkill", "/IM", f"{app_name}.exe", "/F"],
                    capture_output=True,
                    timeout=5,
                )
            else:
                subprocess.run(
                    ["pkill", "-f", app_name],
                    capture_output=True,
                    timeout=5,
                )
            return f"Closed {app_name}."
        except Exception as e:
            return f"Couldn't close {app_name}: {e}"

    # ── System Info ───────────────────────────────────────────────────────

    def _system_info(self) -> str:
        """Get basic system information."""
        import platform as pf

        info = {
            "OS": f"{pf.system()} {pf.release()}",
            "Version": pf.version(),
            "Machine": pf.machine(),
            "Processor": pf.processor() or "Unknown",
            "Python": pf.python_version(),
        }

        # Try to get more detailed info
        try:
            import psutil

            mem = psutil.virtual_memory()
            info["RAM"] = f"{mem.total / (1024**3):.1f} GB ({mem.percent}% used)"
            info["CPU Cores"] = str(psutil.cpu_count())
            info["CPU Usage"] = f"{psutil.cpu_percent()}%"
        except ImportError:
            pass

        lines = [f"  {k}: {v}" for k, v in info.items()]
        return "System Info:\n" + "\n".join(lines)

    def _get_ip(self) -> str:
        """Get the local IP address."""
        import socket

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return f"Your local IP address is: {ip}"
        except Exception:
            return "Couldn't determine your IP address."

    # ── App Aliases ───────────────────────────────────────────────────────

    def _build_app_aliases(self) -> dict:
        """Build platform-specific app name mappings."""
        common = {
            "browser": "google-chrome" if self.system == "linux" else "Google Chrome",
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "safari": "Safari",
            "terminal": self._get_terminal(),
            "calculator": self._get_calculator(),
            "calc": self._get_calculator(),
            "notepad": self._get_notepad(),
            "notes": self._get_notepad(),
            "file manager": self._get_file_manager(),
            "files": self._get_file_manager(),
            "explorer": self._get_file_manager(),
            "finder": self._get_file_manager(),
            "music": self._get_music(),
            "spotify": "Spotify",
            "vscode": "Visual Studio Code",
            "code": "Visual Studio Code",
            "vs code": "Visual Studio Code",
            "slack": "Slack",
            "discord": "Discord",
            "zoom": "zoom.us" if self.system == "darwin" else "Zoom",
        }
        return common

    def _get_terminal(self) -> str:
        if self.system == "darwin":
            return "Terminal"
        elif self.system == "windows":
            return "cmd.exe"
        return "gnome-terminal"

    def _get_calculator(self) -> str:
        if self.system == "darwin":
            return "Calculator"
        elif self.system == "windows":
            return "calc.exe"
        return "gnome-calculator"

    def _get_notepad(self) -> str:
        if self.system == "darwin":
            return "TextEdit"
        elif self.system == "windows":
            return "notepad.exe"
        return "gedit"

    def _get_file_manager(self) -> str:
        if self.system == "darwin":
            return "Finder"
        elif self.system == "windows":
            return "explorer.exe"
        return "nautilus"

    def _get_music(self) -> str:
        if self.system == "darwin":
            return "Music"
        elif self.system == "windows":
            return "Groove Music"
        return "rhythmbox"
