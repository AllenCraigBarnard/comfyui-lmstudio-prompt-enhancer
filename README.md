# ComfyUI LM Studio Prompt Enhancer

A ComfyUI custom node that sends a prompt to a locally running LM Studio model, enhances it with an LLM, and returns the enhanced prompt as a `STRING` output for use with CLIP Text Encode, Flux text encoders, SDXL workflows, and similar prompt-input nodes.

This node uses LM Studio's OpenAI-compatible local API server.

---

## Repository

Install this node from:

```text
https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git
```

---

## Features

- Uses LM Studio as the LLM provider.
- Uses LM Studio's OpenAI-compatible `/v1` endpoint.
- Enhances positive prompts only.
- Supports ComfyUI bypass passthrough when the `prompt` input is connected as a string socket.
- Includes a manual `enable_llm` switch for passthrough without bypassing the node.
- Supports an obfuscated API-key field in the node UI.
- Falls back to the `LM_STUDIO_API_KEY` environment variable.
- Falls back to the dummy key `lm-studio` for normal unauthenticated local LM Studio servers.
- Supports model auto-detection using LM Studio's model list.
- Allows up to `5000` max output tokens.

---

## Requirements

You need:

- ComfyUI
- Git
- LM Studio
- A downloaded and loaded chat/instruct model in LM Studio
- Python package dependency: `openai`

Recommended LM Studio base URL for same-machine use:

```text
http://127.0.0.1:1234/v1
```

---

## Expected Node Folder

After cloning the repo, your folder should look like this:

```text
ComfyUI/
└── custom_nodes/
    └── comfyui-lmstudio-prompt-enhancer/
        ├── __init__.py
        ├── lmstudio_prompt_enhancer.py
        ├── requirements.txt
        └── README.md
```

Depending on the repository name or your `git clone` target folder, the folder may have a different name. That is fine as long as it is inside:

```text
ComfyUI/custom_nodes/
```

---

## Installation: Manually Installed ComfyUI

Use this section if you installed ComfyUI manually with Git and a normal Python environment or virtual environment.

### 1. Open a terminal

Go to your ComfyUI custom nodes folder.

Linux/macOS:

```bash
cd /path/to/ComfyUI/custom_nodes
```

Windows PowerShell:

```powershell
cd C:\path\to\ComfyUI\custom_nodes
```

### 2. Clone the node repository

```bash
git clone https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git
```

This should create:

```text
ComfyUI/custom_nodes/comfyui-lmstudio-prompt-enhancer/
```

If you want a clearer local folder name, clone it like this instead:

```bash
git clone https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git comfyui-lmstudio-prompt-enhancer
```

### 3. Install the node dependencies

From your main ComfyUI directory, run:

Linux/macOS:

```bash
cd /path/to/ComfyUI
python -m pip install -r custom_nodes/comfyui-lmstudio-prompt-enhancer/requirements.txt
```

Windows PowerShell:

```powershell
cd C:\path\to\ComfyUI
python -m pip install -r custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

If you cloned into a custom folder name, update the path accordingly.

Example:

```bash
python -m pip install -r custom_nodes/comfyui-lmstudio-prompt-enhancer/requirements.txt
```

### 4. Virtual environment users

If your manual ComfyUI installation uses a virtual environment, activate it before installing dependencies.

Linux/macOS example:

```bash
cd /path/to/ComfyUI
source venv/bin/activate
python -m pip install -r custom_nodes/comfyui-lmstudio-prompt-enhancer/requirements.txt
```

Windows PowerShell example:

```powershell
cd C:\path\to\ComfyUI
.\venv\Scripts\Activate.ps1
python -m pip install -r custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

### 5. Restart ComfyUI

Stop ComfyUI completely and start it again.

The node should appear under:

```text
prompt / LLM / LM Studio Prompt Enhancer
```

---

## Installation: ComfyUI Windows Portable / Embedded Python Package

Use this section if you use the Windows portable package that contains `python_embeded`.

The important rule is:

```text
Install dependencies into ComfyUI's embedded Python, not system Python.
```

### 1. Open PowerShell or Command Prompt

Go to the folder that contains:

```text
ComfyUI_windows_portable/
├── ComfyUI/
└── python_embeded/
```

Example:

```powershell
cd C:\AI\ComfyUI_windows_portable
```

### 2. Clone the node repository into `custom_nodes`

```powershell
cd .\ComfyUI\custom_nodes
git clone https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git
```

This should create:

```text
C:\AI\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer\
```

If you want a clearer local folder name, clone it like this instead:

```powershell
git clone https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git comfyui-lmstudio-prompt-enhancer
```

### 3. Return to the portable root folder

```powershell
cd ..\..
```

You should now be back in:

```text
C:\AI\ComfyUI_windows_portable
```

### 4. Install dependencies using embedded Python

If you used the default folder name:

```powershell
.\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

If you used the custom folder name:

```powershell
.\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

### 5. Restart ComfyUI Portable

Close the ComfyUI terminal/window completely.

Restart using your normal portable launch file, for example:

```text
run_nvidia_gpu.bat
```

or:

```text
run_cpu.bat
```

The node should appear under:

```text
prompt / LLM / LM Studio Prompt Enhancer
```

---

## Updating the Node

To update the node later, go into the cloned folder and pull the latest changes.

Manual ComfyUI example:

```bash
cd /path/to/ComfyUI/custom_nodes/comfyui-lmstudio-prompt-enhancer
git pull
```

Windows Portable example:

```powershell
cd C:\AI\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer
git pull
```

Then reinstall dependencies if `requirements.txt` changed.

Manual ComfyUI:

```bash
cd /path/to/ComfyUI
python -m pip install -r custom_nodes/comfyui-lmstudio-prompt-enhancer/requirements.txt
```

Windows Portable:

```powershell
cd C:\AI\ComfyUI_windows_portable
.\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

Restart ComfyUI after updating.

---

## LM Studio Setup

### 1. Install LM Studio

Download and install LM Studio from:

```text
https://lmstudio.ai/
```

### 2. Download a chat/instruct model

In LM Studio:

1. Open the model search/download area.
2. Download a chat or instruct model.
3. Load the model.

Good model families for prompt enhancement include instruction-tuned models such as:

```text
Qwen Instruct
Llama Instruct
Mistral Instruct
Gemma Instruct
```

Choose a model that fits your available VRAM/RAM.

### 3. Start the LM Studio local server

In LM Studio:

1. Open the `Developer` tab.
2. Go to the local server/API server area.
3. Load or select your model.
4. Click `Start Server`.
5. Confirm the server is listening on a URL similar to:

```text
http://127.0.0.1:1234
```

For this ComfyUI node, use the OpenAI-compatible `/v1` base URL:

```text
http://127.0.0.1:1234/v1
```

### 4. Localhost vs LAN access

If ComfyUI and LM Studio are running on the same computer, use:

```text
http://127.0.0.1:1234/v1
```

If ComfyUI is running on a different computer on your LAN, use the LAN IP address of the machine running LM Studio.

Example:

```text
http://192.168.1.50:1234/v1
```

Only expose LM Studio on a trusted private network. If you enable LAN access, use authentication and check your firewall rules.

---

## LM Studio API Key / Token Setup

By default, a local LM Studio server may not require authentication.

For unauthenticated local use, you can leave the node's API key field blank. The node will use this dummy fallback key:

```text
lm-studio
```

If you enable authentication in LM Studio, create an API token and provide it to the node.

### Generate an API token in LM Studio

In LM Studio:

1. Open the `Developer` tab.
2. Open `Server Settings`.
3. Enable authentication / require authentication.
4. Click `Manage Tokens`.
5. Click `Create Token`.
6. Give the token a name, for example:

```text
ComfyUI Prompt Enhancer
```

7. Select the required permissions.
8. Create the token.
9. Copy the token immediately and store it safely.

Important: the token may only be shown once. If you lose it, create a new token.

---

## Ways to Provide the API Key to the Node

The node checks for an API key in this order:

1. `lmstudio_api_key` field inside the node.
2. `LM_STUDIO_API_KEY` environment variable.
3. Dummy fallback value:

```text
lm-studio
```

For a local unauthenticated LM Studio server, leave the key field blank.

For an authenticated LM Studio server, use either:

- the obfuscated `lmstudio_api_key` field in the node, or
- the `LM_STUDIO_API_KEY` environment variable.

Environment variables are usually better for reusable workflows because the token is not typed directly into the node UI.

---

## Set `LM_STUDIO_API_KEY` on Windows

### Temporary PowerShell environment variable

This only applies to the current PowerShell window.

```powershell
$env:LM_STUDIO_API_KEY="your_lm_studio_token_here"
```

Then start ComfyUI from the same PowerShell window.

Manual ComfyUI example:

```powershell
cd C:\path\to\ComfyUI
python main.py
```

Windows Portable example:

```powershell
cd C:\AI\ComfyUI_windows_portable
.\run_nvidia_gpu.bat
```

### Permanent Windows user environment variable

PowerShell:

```powershell
setx LM_STUDIO_API_KEY "your_lm_studio_token_here"
```

After running `setx`, close and reopen PowerShell, then restart ComfyUI.

### Check the variable on Windows

PowerShell:

```powershell
echo $env:LM_STUDIO_API_KEY
```

Command Prompt:

```cmd
echo %LM_STUDIO_API_KEY%
```

---

## Set `LM_STUDIO_API_KEY` on Linux

### Temporary environment variable

This only applies to the current shell session.

```bash
export LM_STUDIO_API_KEY="your_lm_studio_token_here"
```

Then start ComfyUI from the same terminal:

```bash
cd /path/to/ComfyUI
python main.py
```

### Persistent environment variable for Bash

Add this line to `~/.bashrc`:

```bash
export LM_STUDIO_API_KEY="your_lm_studio_token_here"
```

Reload your shell config:

```bash
source ~/.bashrc
```

Then restart ComfyUI.

### Persistent environment variable for Zsh

Add this line to `~/.zshrc`:

```bash
export LM_STUDIO_API_KEY="your_lm_studio_token_here"
```

Reload your shell config:

```bash
source ~/.zshrc
```

Then restart ComfyUI.

### Check the variable on Linux

```bash
echo "$LM_STUDIO_API_KEY"
```

---

## Using the Node in ComfyUI

### Basic workflow

Use the node like this:

```text
Text/String Node
        ↓
LM Studio Prompt Enhancer
        ↓
CLIP Text Encode / Flux Text Encode / SDXL Text Encode
```

The node takes a positive prompt string and returns an enhanced prompt string.

### Important: the prompt must be connected

The `prompt` input is a forced string input socket.

This is intentional because it allows ComfyUI bypass mode to pass the original string through the node.

Because of this, the node does not show a large internal prompt text box. Use a text/string/primitive node before it.

Example:

```text
Primitive String / Text Box
        ↓ prompt
LM Studio Prompt Enhancer
        ↓ enhanced_prompt
CLIP Text Encode
```

### Bypass behavior

Because the `prompt` input is a real socket, ComfyUI bypass should pass the input string through to the output.

Use bypass when you want:

```text
original prompt → output unchanged
```

### Manual passthrough mode

The node also has:

```text
enable_llm
```

When `enable_llm` is set to `False`, the node returns the original prompt without contacting LM Studio.

This is useful when you want passthrough behavior without using ComfyUI's bypass mode.

---

## Node Inputs

### `prompt`

Type:

```text
STRING input socket
```

The original prompt to enhance.

This must be connected from another text/string node.

### `system_prompt`

Type:

```text
Multiline STRING
```

Instructions sent to the LLM as the system message.

Edit this if you want the LLM to follow a different style, format, or prompt-enhancement policy.

### `style`

Type:

```text
Dropdown
```

Available options:

```text
cinematic
photorealistic
anime
fantasy art
sci-fi concept art
product photography
minimal enhancement
```

This is passed to the LLM as style guidance.

### `lmstudio_base_url`

Type:

```text
STRING
```

Default:

```text
http://127.0.0.1:1234/v1
```

Use this when LM Studio runs on the same machine.

For another machine on your LAN, use that machine's IP address:

```text
http://192.168.1.50:1234/v1
```

### `lmstudio_api_key`

Type:

```text
Obfuscated/password-style STRING
```

Use this if LM Studio authentication is enabled.

Leave blank to use the `LM_STUDIO_API_KEY` environment variable or dummy fallback.

### `model`

Type:

```text
STRING
```

Default:

```text
auto
```

When set to `auto`, the node uses the first model listed by LM Studio.

If you want to use a specific model, enter the exact model ID shown by LM Studio.

### `temperature`

Type:

```text
FLOAT
```

Default:

```text
0.7
```

Lower values produce more predictable prompt enhancements.

Higher values produce more varied and creative enhancements.

Suggested values:

```text
0.3 to 0.6: controlled prompt cleanup
0.7 to 1.0: creative enhancement
```

### `max_tokens`

Type:

```text
INT
```

Default:

```text
500
```

Maximum:

```text
5000
```

This controls how long the LLM response can be.

For most prompt enhancement, `300` to `800` is usually enough.

### `enable_llm`

Type:

```text
BOOLEAN
```

Default:

```text
True
```

If `False`, the node returns the original prompt unchanged.

### `cache_buster`

Type:

```text
INT
```

Change this value when you want to force ComfyUI to run the node again and request a fresh LLM response.

ComfyUI may cache node results when the inputs do not change.

---

## Node Output

### `enhanced_prompt`

Type:

```text
STRING
```

The enhanced positive prompt returned by LM Studio.

Connect this output to your positive text encoder.

---

## Example System Prompt

You can paste this into the node's `system_prompt` field:

```text
You enhance prompts for Stable Diffusion, SDXL, Flux, and Flux-style image-generation workflows.

Rules:
- Preserve the user's core subject and intent.
- Improve the prompt with concrete visual detail.
- Add composition, lighting, camera, material, environment, and mood when useful.
- Keep the prompt as one paragraph.
- Do not add negative prompt terms.
- Do not mention copyrighted characters, artists, real celebrities, or trademarked IP unless the user already included them.
- Do not explain your changes.
- Return only the enhanced prompt.
```

---

## Example Workflow

Original text node:

```text
a woman standing in a neon city at night
```

LM Studio Prompt Enhancer output might be:

```text
A cinematic full-body portrait of a woman standing in a rain-soaked neon city at night, glowing signs reflected in wet pavement, dramatic rim lighting, soft atmospheric haze, detailed futuristic streetwear, shallow depth of field, high contrast, realistic textures, vibrant cyberpunk color palette, dynamic urban composition.
```

Then connect:

```text
enhanced_prompt → CLIP Text Encode positive prompt
```

---

## Troubleshooting

### Node does not appear in ComfyUI

Check:

1. The repo was cloned inside:

```text
ComfyUI/custom_nodes/
```

2. The cloned folder contains:

```text
__init__.py
lmstudio_prompt_enhancer.py
requirements.txt
```

3. ComfyUI was restarted after cloning.
4. The ComfyUI console does not show Python import errors.

### `git clone` fails

Check:

1. Git is installed.
2. The local Git server at `https://127.0.0.1/` is running.
3. The repo path is correct.
4. Your local HTTPS certificate is trusted.

For local testing with a self-signed certificate only:

```bash
git -c http.sslVerify=false clone https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git
```

### `ModuleNotFoundError: No module named 'openai'`

The `openai` package was not installed into the Python environment used by ComfyUI.

Manual ComfyUI:

```bash
python -m pip install -r custom_nodes/comfyui-lmstudio-prompt-enhancer/requirements.txt
```

Windows Portable:

```powershell
.\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

### LM Studio connection failed

Check:

1. LM Studio is open.
2. A model is loaded.
3. The server is started.
4. The node's base URL is correct:

```text
http://127.0.0.1:1234/v1
```

5. Your firewall is not blocking the connection.

### Authentication error

If LM Studio authentication is enabled:

1. Create an API token in LM Studio.
2. Put it in either:
   - the node's `lmstudio_api_key` field, or
   - the `LM_STUDIO_API_KEY` environment variable.
3. Restart ComfyUI after setting environment variables.

If authentication is not enabled, leave the key field blank.

### Bypass does not pass the prompt through

Make sure the prompt comes from a connected text/string node.

Bypass passthrough requires this structure:

```text
Text/String Node
        ↓
LM Studio Prompt Enhancer
        ↓
Text Encoder
```

If the prompt is only a widget inside a node, bypass cannot pass it through as a socket value.

### The same enhanced prompt keeps appearing

ComfyUI may be reusing cached results.

Change the `cache_buster` value to force a fresh request.

### The output is too long

Lower `max_tokens`.

Recommended range:

```text
300 to 800
```

### The output is too random

Lower `temperature`.

Recommended range for controlled prompt enhancement:

```text
0.3 to 0.6
```

---

## Security Notes

- Do not share workflows that contain real API tokens typed into node fields.
- Prefer environment variables for tokens when possible.
- For same-machine use, prefer:

```text
http://127.0.0.1:1234/v1
```

- If exposing LM Studio on your LAN, enable authentication.
- Do not expose LM Studio directly to the public internet unless you understand the security implications and have proper network controls.
- Do not disable Git SSL verification for remote or untrusted servers.

---

## References

- LM Studio OpenAI-compatible endpoints: https://lmstudio.ai/docs/developer/openai-compat
- LM Studio local server docs: https://lmstudio.ai/docs/developer/core/server
- LM Studio authentication docs: https://lmstudio.ai/docs/developer/core/authentication
- LM Studio REST API docs: https://lmstudio.ai/docs/developer/rest
- ComfyUI custom node installation docs: https://docs.comfy.org/installation/install_custom_node
- ComfyUI Windows Portable docs: https://docs.comfy.org/installation/comfyui_portable_windows
- ComfyUI custom nodes developer docs: https://docs.comfy.org/development/core-concepts/custom-nodes
