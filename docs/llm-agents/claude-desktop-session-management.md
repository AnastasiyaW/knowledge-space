# Claude Desktop Session Management

Claude Desktop stores conversation history and environment state in local session files. On versions prior to 1.47 (macOS), these are stored as discrete files, while newer versions are migrating toward encapsulated virtual machine images.

## Storage Architecture and Paths
Session data is stored in platform-specific application support directories. These directories contain account-specific subfolders, often identified by hexadecimal `accountId` strings.

- **macOS Path:** `~/Library/Application Support/Claude/`
- **Windows Path:** `%AppData%\Roaming\Claude\`
- **Legacy Session Files:** Found within `sessions/` or account-specific folders.
- **VM Bundle (v1.47+):** `~/Library/Application Support/Claude/vm_bundles/claudevm.bundle/`

### VM Bundle Components
In Claude Desktop 1.4758.0+ (macOS), the architecture shifts to a disk-image-based storage system:
- `rootfs.img`: The base system image for the execution environment.
- `sessiondata.img`: Persistent storage for active session state.
- `efivars.fd`: Firmware variables for the virtualized environment.

## Ghost Sessions and Disk Accumulation
A known behavior in the desktop client results in "hidden" or "ghost" sessions. Data persists on disk even if the UI fails to populate the sidebar.

- **Persistence:** Local files can accumulate hundreds of sessions (e.g., 40-50MB of data) that are not reachable via the standard "History" view.
- **Account Switching:** Switching between multiple Anthropic accounts frequently triggers a visibility bug where the history sidebar appears empty, despite the `sessions/` folder containing the raw data.
- **Session Registry:** The client maintains a registry of sessions, often found in `.vite/build/index.js` or internal SQLite/LevelDB structures, which can desynchronize from the actual file system.

## Session Discovery and Recovery
Engineers can use Python scripts to inventory abandoned sessions by crawling the application support paths.

### Cross-Platform Session Inventory
```python
import sys
import os
from pathlib import Path

def get_claude_path():
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/Claude"
    elif sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "Claude"
    return None

def list_sessions():
    base_path = get_claude_path()
    if not base_path or not base_path.exists():
        return []
    
    # Search for session-related files or directories
    # Note: Structure varies between legacy and VM-based versions
    session_files = list(base_path.glob("**/sessions/*.json"))
    return session_files

print(f"Found {len(list_sessions())} potential session files.")
```

## External Synchronization
Since Claude Desktop lacks native cross-machine synchronization for the local execution state, community tools like `tawanorg/claude-sync` provide workarounds.

- **Mechanism:** CLI-based sync using Cloudflare R2 or S3 backends.
- **Security:** Implements end-to-end encryption (E2EE) to prevent session leakage.
- **Function:** Transfers the local environment state and session metadata between different machines.

## Gotchas
- **Issue: Account Switching History Loss** → **Fix:** Sessions are not deleted but become invisible in the UI. Manual restoration of the `sessions/` folder or using a discovery script is required to retrieve the `sessionId`.
- **Issue: Windows Update Content Failure** → **Fix:** In versions released late April 2026, Windows auto-updates may cause the sidebar to show sessions but the main chat window to be empty. This typically requires clearing the GPU cache and restarting the client.
- **Issue: Cross-Machine Copy Validation** → **Fix:** Starting with v2.1.9, simply copying session folders between machines may fail due to added validation checks. Use an encrypted sync tool like `claude-sync` rather than manual directory merging.
- **Issue: VM Migration Lock-in** → **Fix:** Once migrated to `claudevm.bundle`, individual session files are no longer accessible as standard JSON/Text files. They must be extracted from the `sessiondata.img` if the client fails to load.

## See Also
- [[claude-code-ecosystem]]
- [[agent-memory]]
- [[context-engineering]]
- [[managed-agents]]
- [[agentic-systems-landscape-2026]]

