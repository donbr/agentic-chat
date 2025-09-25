# MCP Tools — Quick Setup (Claude Code on WSL/Ubuntu)

> Goal: enable **GitHub (remote HTTP)** + **YouTube transcripts (yt-dlp)** via a project-scoped `.mcp.json`, with latest yt-dlp and a fine-grained GitHub PAT.

---

## 1) Prereqs (WSL/Ubuntu)

```bash
# Update base packages
sudo apt-get update -y

# Useful tools for media/transcripts
sudo apt-get install -y ffmpeg curl

# (Optional) pipx for clean CLI installs
sudo apt-get install -y pipx && pipx ensurepath
```

### Install **yt-dlp** (latest)

**Recommended (standalone binary):**

```bash
# Remove old Debian-packaged yt-dlp so it won't shadow the new one
sudo apt-get remove -y yt-dlp

# Install latest static binary
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
  -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# Verify
which yt-dlp
yt-dlp --version
```

### Node (for `npx`-launched MCP servers)

```bash
# Easiest: nvm
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.nvm/nvm.sh
nvm install --lts
node -v && npm -v
```

---

## 2) Create a GitHub Personal Access Token (PAT)

Create a **fine-grained, read-only** PAT scoped to the org/repos you need. GitHub’s official README shows using a PAT with the remote server and includes a JSON example adding an `Authorization: Bearer ${input:github_mcp_pat}` header. ([GitHub][1])

* PAT creation page: [https://github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new) (fine-grained; select **Read** permissions for repository contents/issues as needed). ([GitHub][1])

Export it in your WSL shell so Claude Code CLI can expand it in `.mcp.json`:

```bash
echo 'export GITHUB_MCP_PAT=ghp_yourFineGrainedReadOnlyPAT' >> ~/.bashrc
source ~/.bashrc
```

---

## 3) Project config: `.mcp.json`

Place this at your repo root (Claude Code reads project-scoped config).
This uses **GitHub remote MCP (HTTP)** with a PAT header, and a **YouTube transcripts** server launched via `npx`.
(If yt-dlp lives in `/usr/local/bin`, the PATH line ensures the MCP finds it.)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_MCP_PAT}"
      }
    },
    "youtube-transcripts": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anaisbetts/mcp-youtube"],
      "env": { "PATH": "/usr/local/bin:/usr/bin:${PATH}" }
    }
  }
}
```

> Example `.mcp.json` from your project (same shape with PAT header + youtube server).&#x20;

**Why PAT header?** Claude Code’s remote GitHub MCP works with OAuth *or* PAT. If your host/flow blocks OAuth (e.g., dynamic client registration), the **PAT header** path is the simplest and officially documented alternative. ([GitHub][1])

---

## 4) Sanity checks

```bash
# Confirm env
printenv | grep GITHUB_MCP_PAT

# Confirm yt-dlp
which yt-dlp && yt-dlp --version

# Ask Claude Code CLI to list servers
claude mcp list
```

In a Claude chat:

* “List the tools on the **github** MCP server.”
* “For **youtube-transcripts**, fetch English subtitles for `https://www.youtube.com/watch?v=<VIDEO_ID>` and save to `sources/transcripts/<VIDEO_ID>.md`.”

> Tip: Normalize `/live/<ID>` → `https://www.youtube.com/watch?v=<ID>` and, for playlists, enumerate video IDs first (XML feed or `yt-dlp --flat-playlist`) before calling the transcript tool.

---

## 5) Minimal troubleshooting

* **GitHub shows “Authenticate” or fails OAuth** → You’re likely hitting dynamic-client-registration limits. Keep the **PAT header** setup above; restart the Claude Code CLI so it picks up the updated `.mcp.json` and env. ([GitHub][1])
* **YouTube errors** → Ensure `yt-dlp` is current, use **watch** URLs (not `/live`), and install `ffmpeg`. If a video is truly live, transcripts may be unavailable until processing completes.

---

That’s it—this gives you reliable, host-agnostic MCP wiring with the latest yt-dlp and a least-privilege GitHub PAT, tailored for Claude Code on WSL.

[1]: https://github.com/github/github-mcp-server?tab=readme-ov-file "GitHub - github/github-mcp-server: GitHub's official MCP Server"
