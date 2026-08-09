# LM Studio Prompt Enhancer for ComfyUI

A ComfyUI custom node that enhances prompts for **image generation** and **video generation** using an LLM running through **LM Studio's OpenAI-compatible API**.

The node can work from text alone or use up to two optional ComfyUI `IMAGE` inputs as visual context. It includes generation-mode-aware prompting, style compatibility checks, configurable system prompts, automatic LM Studio model selection, and support for multimodal/vision models when image inputs are used.

---

## Features

- Enhance prompts for **image generation**
- Enhance prompts for **video generation**
- Connect to a local or remote **LM Studio** server
- Use LM Studio's OpenAI-compatible API
- Automatic model selection with `model = auto`
- Manually specify an LM Studio model ID
- Optional `input_image_1` and `input_image_2` visual inputs
- Different image semantics for image and video prompt modes
- Image, cinematic, photographic, and motion-oriented style presets
- Generation-mode/style compatibility validation
- Editable system prompt
- Adjustable LLM temperature
- Configurable output limit up to **10,000 tokens**
- Manual LLM passthrough mode
- Cache-buster control for forcing fresh ComfyUI execution
- Automatic image resizing before sending visual context to LM Studio
- Local-first workflow when used with a local LM Studio server

---

## How It Works

```text
Original Prompt
     │
     ├── Optional input_image_1
     ├── Optional input_image_2
     │
     ▼
LM Studio Prompt Enhancer
     │
     ├── Validate generation mode
     ├── Validate style compatibility
     ├── Resolve LM Studio model
     ├── Prepare optional image context
     ├── Build multimodal prompt
     └── Send request to LM Studio
     │
     ▼
Enhanced Prompt
```

The node outputs a single ComfyUI `STRING`:

```text
enhanced_prompt
```

This can be connected to the prompt or text-conditioning portion of an image or video generation workflow.

---

## Generation Modes

### Image generation prompt

In image mode:

```text
input_image_1 = Base Image
input_image_2 = Reference Image
```

The enhancer instructs the LLM to preserve important content from the base image while using the reference image for relevant visual guidance such as:

- composition
- subject appearance
- lighting
- color palette
- materials
- environment
- visual style
- texture
- atmosphere

Both image inputs are optional.

### Video generation prompt

In video mode:

```text
input_image_1 = First Frame
input_image_2 = Last Frame
```

When images are connected, the LLM is instructed to construct a coherent video-generation prompt between those two frames.

Video-prompt enhancement can include:

- subject motion
- environmental motion
- camera movement
- framing
- shot evolution
- timing
- pacing
- continuity
- lighting
- atmosphere
- cinematic direction

Both frame inputs are optional.

> **Note:** The node does not accept or decode a ComfyUI `VIDEO` input. Video mode refers to generating a prompt intended for a video-generation model.

---

## Style Presets

### Image and Video

These styles can be used with either generation mode:

- cinematic
- cinematic anamorphic
- cinematic 35mm film
- large-format cinematic
- cinematic noir
- cinematic documentary
- cinematic commercial
- photorealistic
- anime
- fantasy art
- sci-fi concept art
- minimal enhancement

### Image Only

- editorial photography
- portrait photography
- product photography
- architectural photography
- macro photography

### Video Only

- cinematic music video
- cinematic slow motion
- dynamic action cinematography
- handheld realism
- drone / aerial cinematography
- timelapse cinematography
- macro cinematography
- product commercial video
- single-take / oner
- tracking shot
- orbit shot
- dolly zoom
- FPV action

If the selected style conflicts with the selected generation mode, the node stops before calling LM Studio and raises an error explaining the conflict.

Example:

```text
Generation mode: Image generation prompt
Style: cinematic slow motion
```

This combination will fail because `cinematic slow motion` is a video-only style.

---

## Requirements

- ComfyUI
- LM Studio
- Python 3.10 or newer
- An LLM supported by LM Studio

Python dependencies:

```text
openai>=1.0.0
numpy
Pillow
```

If you connect image inputs, the selected model must support image/multimodal input.

The node does **not** pre-check whether the selected model is vision-capable. If images are connected to an incompatible text-only model, LM Studio or the model runtime will return the corresponding error.

---

## Installation

### 1. Clone the repository

Clone the repository into your ComfyUI `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer.git
```

Your folder structure should look similar to:

```text
ComfyUI/
└── custom_nodes/
    └── comfyui-lmstudio-prompt-enhancer/
```

### 2. Install dependencies

From the Python environment used by ComfyUI:

```bash
pip install -r requirements.txt
```

For ComfyUI Portable on Windows, use ComfyUI's embedded Python environment.

Example:

```bat
python_embeded\python.exe -m pip install -r ComfyUI\custom_nodes\comfyui-lmstudio-prompt-enhancer\requirements.txt
```

### 3. Restart ComfyUI

Fully restart the ComfyUI backend after installing or updating the custom node.

The node should appear under:

```text
prompt/LLM
```

with the display name:

```text
LM Studio Prompt Enhancer
```

---

## LM Studio Setup

### 1. Install and launch LM Studio

Load or make available the LLM you want to use.

### 2. Start the LM Studio API server

The default server URL used by the node is:

```text
http://127.0.0.1:1234/v1
```

If your LM Studio server uses a different address or port, update:

```text
lmstudio_base_url
```

inside the node.

### 3. Choose a model

The default model setting is:

```text
auto
```

When `auto` is selected, the node asks LM Studio for the available model list and uses the first model returned.

If you have multiple models available and want deterministic selection, enter the exact LM Studio model identifier manually.

---

## Node Inputs

| Input | Type | Description |
|---|---|---|
| `prompt` | STRING | Original prompt to enhance |
| `generation_mode` | ENUM | Image generation or video generation |
| `system_prompt` | STRING | Instructions sent to the LLM |
| `style` | ENUM | Prompt enhancement style |
| `lmstudio_base_url` | STRING | LM Studio OpenAI-compatible API URL |
| `lmstudio_api_key` | STRING | Optional LM Studio API key/token |
| `model` | STRING | Model ID or `auto` |
| `temperature` | FLOAT | LLM sampling temperature |
| `max_tokens` | INT | Maximum completion tokens, up to 10,000 |
| `enable_llm` | BOOLEAN | Enable enhancement or return the original prompt |
| `cache_buster` | INT | Change to force a fresh ComfyUI execution |
| `input_image_1` | IMAGE | Base image in image mode; first frame in video mode |
| `input_image_2` | IMAGE | Reference image in image mode; last frame in video mode |

---

## Node Output

| Output | Type | Description |
|---|---|---|
| `enhanced_prompt` | STRING | Enhanced positive generation prompt |

---

## API Key Handling

The node resolves the LM Studio API key in the following order:

1. `lmstudio_api_key` entered directly in the node
2. `LM_STUDIO_API_KEY` environment variable
3. fallback value `lm-studio`

The fallback is suitable for normal local LM Studio installations where API authentication is not enabled.

Linux/macOS:

```bash
export LM_STUDIO_API_KEY="your-api-key"
```

Windows PowerShell:

```powershell
$env:LM_STUDIO_API_KEY="your-api-key"
```

---

## Image Processing

Connected ComfyUI `IMAGE` tensors are converted into RGB images and supplied to LM Studio as OpenAI-compatible base64 image URLs.

Large images are automatically resized while preserving aspect ratio.

Maximum image side:

```text
1024 px
```

Supported input tensor layouts:

```text
[H, W, C]
```

or:

```text
[B, H, W, C]
```

If an image batch is supplied, only the first image in that batch is used.

---

## Default System Prompt

The included default system prompt is intentionally compact so it remains practical for smaller local LLMs.

It instructs the model to:

- preserve the user's subject and intent
- respect user constraints
- enhance image or video generation prompts
- apply mode-specific image semantics
- improve composition and visual specificity
- add lighting, camera, material, environment, and atmosphere details when useful
- add motion, continuity, pacing, and camera movement for video prompts
- use connected images as visual evidence
- avoid contradicting visible content
- avoid explanations and Markdown
- return one positive prompt
- avoid introducing unrelated copyrighted characters, celebrities, artists, or trademarked IP

The `system_prompt` field can be replaced with model-specific system prompts.

---

## Example System Prompts

Example system prompts are available here:

https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer/tree/main/Example_System_Prompts

The repository includes prompt-enhancement system prompts optimized for:

- FLUX
- FLUX 3 Video
- SDXL
- Pony
- KREA2
- Z-Image Turbo
- Qwen Image

These can be copied into the node's `system_prompt` field and adapted to suit your chosen model or workflow.

---

## Example Workflows

Example ComfyUI workflows are available here:

https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer/tree/main/Workflows

The included workflows are optimized for:

- FLUX
- FLUX 3 Video
- SDXL
- Pony
- KREA2
- Z-Image Turbo

Use them as starting points for integrating the LM Studio Prompt Enhancer into model-specific image and video generation pipelines.

---

## Example: Image Prompt Enhancement

Original prompt:

```text
a futuristic sports car in the rain
```

Suggested settings:

```text
Generation mode: Image generation prompt
Style: cinematic
```

Possible enhanced output:

```text
A futuristic high-performance sports car parked on a rain-soaked neon-lit city street at night, low three-quarter camera angle, reflective bodywork, wet pavement catching colorful urban reflections, dramatic rim lighting, volumetric mist, shallow depth of field, realistic water droplets, detailed materials, atmospheric contrast, polished cinematic automotive photography.
```

Actual output depends on the selected LLM, temperature, system prompt, and connected images.

---

## Example: Video Prompt Enhancement

Original prompt:

```text
a motorcycle drives through a futuristic city
```

Suggested settings:

```text
Generation mode: Video generation prompt
Style: tracking shot
```

Possible enhanced output:

```text
A high-speed motorcycle races through a dense futuristic city at night as the camera performs a smooth low-angle tracking shot alongside the rider, neon signs and illuminated towers streak through the background, the wheels spray water from the reflective street, subtle suspension movement and rider body motion create realistic momentum, dynamic parallax and controlled motion blur reinforce speed while consistent vehicle appearance, dramatic rim lighting, atmospheric haze, and continuous forward motion maintain cinematic continuity.
```

---

## Bypass / Passthrough Mode

Set:

```text
enable_llm = false
```

to return the original prompt unchanged.

When passthrough mode is enabled, the node does not contact LM Studio.

---

## Cache Buster

ComfyUI may reuse previously calculated node results when none of its inputs have changed.

Change:

```text
cache_buster
```

to another integer to make ComfyUI treat the node as changed and request a fresh LLM completion.

The `cache_buster` value itself is not included in the LLM prompt.

---

## Troubleshooting

### LM Studio connection failed

Check that:

- LM Studio is running
- the API server has been started
- `lmstudio_base_url` is correct
- the configured port is correct
- authentication settings are correct
- your firewall is not blocking the connection

Default endpoint:

```text
http://127.0.0.1:1234/v1
```

### `auto` selects the wrong model

`auto` uses the first model returned by LM Studio.

If several models are available, enter the exact model identifier manually.

### Images cause an LLM/API error

The node does not pre-validate vision capability.

If `input_image_1` or `input_image_2` is connected, make sure the selected model supports image/multimodal input.

If it does not, either:

- switch to a multimodal/vision-capable model, or
- disconnect the image inputs

### Images appear to be ignored

Confirm that:

- the selected model supports image input
- `input_image_1` or `input_image_2` is connected
- the model performs well at visual instruction following
- the system prompt instructs the model to use visual context

### Generation-mode/style conflict

The selected style is restricted to the other generation mode.

Choose a style compatible with the current mode.

### Prompt output changes the original intent too much

Try:

- lowering `temperature`
- choosing `minimal enhancement`
- using a more restrictive system prompt
- explicitly stating required constraints in the original prompt

### Prompt output is too conservative

Try:

- increasing `temperature`
- selecting a more specific style
- adding an image reference
- using one of the model-specific example system prompts

---

## Privacy

When using the default local LM Studio endpoint, prompt enhancement can run entirely on your own machine.

If you change:

```text
lmstudio_base_url
```

to a remote endpoint, prompt text and any connected image data will be sent to that server.

Review the privacy and security policies of any remote endpoint you use.

---

## Repository Resources

### Example System Prompts

https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer/tree/main/Example_System_Prompts

### Example Workflows

https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer/tree/main/Workflows

### Issues

https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer/issues

---

## Contributing

Bug reports, compatibility reports, improvements, and pull requests are welcome.

When reporting an issue, please include:

- ComfyUI version
- LM Studio version
- model name
- operating system
- relevant node settings
- ComfyUI console/error output
- whether image inputs were connected

Do not include API keys, tokens, or other credentials in issue reports.

---

## License

See the repository's `LICENSE` file for licensing information.

---

## Disclaimer

This project is an independent ComfyUI custom node for use with LM Studio.

It is not an official ComfyUI, LM Studio, Black Forest Labs, Stability AI, Krea, Qwen, or other model-provider project.
