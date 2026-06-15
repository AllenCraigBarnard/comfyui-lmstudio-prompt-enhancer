import os
from openai import OpenAI


class LMStudioPromptEnhancer:
    CATEGORY = "prompt/LLM"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "enhance_prompt"

    DEFAULT_SYSTEM_PROMPT = """You enhance prompts for Stable Diffusion, SDXL, Flux, and other image-generation models.

Rules:
- Preserve the user's subject and intent.
- Improve the prompt with concrete visual detail.
- Add composition, lighting, camera, material, environment, and detail when useful.
- Do not add copyrighted characters, real celebrities, artist names, or trademarked IP unless the user already provided them.
- Do not explain your changes.
- Return only the enhanced positive prompt.
- Return one paragraph only."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Real input socket so ComfyUI bypass can pass it through.
                "prompt": (
                    "STRING",
                    {
                        "forceInput": True
                    }
                ),

                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": cls.DEFAULT_SYSTEM_PROMPT
                    }
                ),

                "style": (
                    [
                        "cinematic",
                        "photorealistic",
                        "anime",
                        "fantasy art",
                        "sci-fi concept art",
                        "product photography",
                        "minimal enhancement"
                    ],
                    {
                        "default": "cinematic"
                    }
                ),

                "lmstudio_base_url": (
                    "STRING",
                    {
                        "default": "http://127.0.0.1:1234/v1"
                    }
                ),

                # Obfuscated/password-style field in the node UI.
                # Leave blank to use LM_STUDIO_API_KEY or dummy fallback.
                "lmstudio_api_key": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "password": True
                    }
                ),

                "model": (
                    "STRING",
                    {
                        "default": "auto"
                    }
                ),

                "temperature": (
                    "FLOAT",
                    {
                        "default": 0.7,
                        "min": 0.0,
                        "max": 2.0,
                        "step": 0.05
                    }
                ),

                "max_tokens": (
                    "INT",
                    {
                        "default": 500,
                        "min": 50,
                        "max": 5000,
                        "step": 10
                    }
                ),

                # When False, the node returns the original prompt unchanged.
                "enable_llm": (
                    "BOOLEAN",
                    {
                        "default": True
                    }
                ),

                # Change this when you want ComfyUI to force a fresh LLM call.
                "cache_buster": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 999999,
                        "step": 1
                    }
                ),
            }
        }

    def _resolve_model(self, client, model):
        model = model.strip()

        if model.lower() != "auto":
            return model

        models = client.models.list()

        if not models.data:
            raise RuntimeError(
                "LM Studio server is running, but no model is available. "
                "Load a model in LM Studio first."
            )

        return models.data[0].id

    def _get_api_key(self, lmstudio_api_key):
        """
        API key priority:
        1. lmstudio_api_key field in the node.
        2. LM_STUDIO_API_KEY environment variable.
        3. Dummy fallback for normal unauthenticated local LM Studio.
        """

        node_api_key = (lmstudio_api_key or "").strip()

        if node_api_key:
            return node_api_key

        env_api_key = os.environ.get("LM_STUDIO_API_KEY", "").strip()

        if env_api_key:
            return env_api_key

        return "lm-studio"

    def enhance_prompt(
        self,
        prompt,
        system_prompt,
        style,
        lmstudio_base_url,
        lmstudio_api_key,
        model,
        temperature,
        max_tokens,
        enable_llm,
        cache_buster
    ):
        prompt = prompt.strip()

        if not prompt:
            raise RuntimeError("The prompt input is empty.")

        # Manual passthrough mode.
        # This is separate from ComfyUI's native bypass.
        if not enable_llm:
            return (prompt,)

        system_prompt = system_prompt.strip()

        if not system_prompt:
            raise RuntimeError(
                "The system_prompt field is empty. Add instructions for the LLM."
            )

        base_url = lmstudio_base_url.strip()

        if not base_url:
            raise RuntimeError("The lmstudio_base_url field is empty.")

        api_key = self._get_api_key(lmstudio_api_key)

        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        resolved_model = self._resolve_model(client, model)

        user_prompt = f"""
Enhance the following Stable Diffusion / SDXL / Flux prompt.

Requested style:
{style}

Original prompt:
{prompt}

Rules:
- Preserve the user's core subject and intent.
- Make the prompt more visually specific and generator-friendly.
- Add useful visual details such as composition, lighting, camera, environment, texture, material, and mood.
- Do not include negative prompt terms.
- Do not include markdown.
- Do not include explanations.
- Return only the enhanced prompt as a single paragraph.
"""

        try:
            response = client.chat.completions.create(
                model=resolved_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt.strip()
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            enhanced = response.choices[0].message.content.strip()

            if not enhanced:
                enhanced = prompt

            return (enhanced,)

        except Exception as e:
            raise RuntimeError(
                f"LM Studio prompt enhancement failed. "
                f"Check that LM Studio server is running at {base_url}, "
                f"a model is loaded, the model name is valid, "
                f"and the API key is correct if LM Studio authentication is enabled. "
                f"Original error: {e}"
            )