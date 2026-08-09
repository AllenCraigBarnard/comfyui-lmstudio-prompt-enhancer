import os
import base64
from io import BytesIO

import numpy as np
from PIL import Image
from openai import OpenAI


class LMStudioPromptEnhancer:
    """
    ComfyUI prompt-enhancement node for LM Studio.

    Features:
    - Image-generation and video-generation prompt modes.
    - Mode-aware image semantics:
        Image mode: input_image_1 = base image, input_image_2 = reference image.
        Video mode: input_image_1 = first frame, input_image_2 = last frame.
    - Style/generation-mode compatibility validation.
    """

    CATEGORY = "prompt/LLM"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "enhance_prompt"

    IMAGE_MODE = "Image generation prompt"
    VIDEO_MODE = "Video generation prompt"

    # Keep vision payloads practical for local VLMs.
    MAX_IMAGE_SIDE = 1024

    STYLE_MODE_SUPPORT = {
        # Compatible with image and video prompting.
        "cinematic": "both",
        "cinematic anamorphic": "both",
        "cinematic 35mm film": "both",
        "large-format cinematic": "both",
        "cinematic noir": "both",
        "cinematic documentary": "both",
        "cinematic commercial": "both",
        "photorealistic": "both",
        "anime": "both",
        "fantasy art": "both",
        "sci-fi concept art": "both",
        "minimal enhancement": "both",

        # Image-only styles.
        "editorial photography": "image",
        "portrait photography": "image",
        "product photography": "image",
        "architectural photography": "image",
        "macro photography": "image",

        # Video-only / motion-centric styles.
        "cinematic music video": "video",
        "cinematic slow motion": "video",
        "dynamic action cinematography": "video",
        "handheld realism": "video",
        "drone / aerial cinematography": "video",
        "timelapse cinematography": "video",
        "macro cinematography": "video",
        "product commercial video": "video",
        "single-take / oner": "video",
        "tracking shot": "video",
        "orbit shot": "video",
        "dolly zoom": "video",
        "FPV action": "video",
    }

    STYLE_OPTIONS = list(STYLE_MODE_SUPPORT.keys())

    DEFAULT_SYSTEM_PROMPT = """Enhance prompts for image or video generation. The user specifies the mode. Preserve subject, intent, constraints, and visible evidence. Return only one positive prompt as one paragraph.

Image: describe subject, composition, framing, camera/lens when useful, lighting, color, materials, texture, environment, depth, mood, and key details. In image mode, input_image_1 is the base image and input_image_2 is the reference image.

Video: describe subject and scene, camera framing/movement, subject and environmental motion, timing, pacing, continuity, lighting, atmosphere, and shot evolution. In video mode, input_image_1 is the first frame and input_image_2 is the last frame.

Use attached images as visual evidence. Do not contradict them or the user's prompt. No negative prompt, markdown, explanation, or unrelated detail. Do not introduce artist names, celebrities, copyrighted characters, or trademarked IP unless the user supplied them."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Real socket so ComfyUI native bypass can pass it through.
                "prompt": (
                    "STRING",
                    {
                        "forceInput": True
                    }
                ),

                "generation_mode": (
                    [
                        cls.IMAGE_MODE,
                        cls.VIDEO_MODE,
                    ],
                    {
                        "default": cls.IMAGE_MODE
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
                    cls.STYLE_OPTIONS,
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

                # Obfuscated/password-style UI field.
                # Leave blank to use LM_STUDIO_API_KEY or the local dummy fallback.
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
                        "max": 10000,
                        "step": 10
                    }
                ),

                # False = return original prompt without validation/API calls.
                "enable_llm": (
                    "BOOLEAN",
                    {
                        "default": True
                    }
                ),

                # Change this to force ComfyUI to consider the node changed.
                "cache_buster": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 999999,
                        "step": 1
                    }
                ),
            },
            "optional": {
                # Image mode: base image.
                # Video mode: first frame.
                "input_image_1": ("IMAGE",),

                # Image mode: reference image.
                # Video mode: last frame.
                "input_image_2": ("IMAGE",)
            }
        }

    # -------------------------------------------------------------------------
    # Mode/style validation
    # -------------------------------------------------------------------------

    def _validate_generation_mode_and_style(self, generation_mode, style):
        """
        Reject incompatible generation-mode/style combinations before any
        LM Studio request.
        """

        if generation_mode not in (self.IMAGE_MODE, self.VIDEO_MODE):
            raise RuntimeError(
                f"Unsupported generation mode: {generation_mode!r}. "
                f"Choose '{self.IMAGE_MODE}' or '{self.VIDEO_MODE}'."
            )

        support = self.STYLE_MODE_SUPPORT.get(style)

        if support is None:
            raise RuntimeError(
                f"Unknown style: {style!r}. Choose a style provided by this node."
            )

        required_support = (
            "image"
            if generation_mode == self.IMAGE_MODE
            else "video"
        )

        if support not in ("both", required_support):
            compatible_styles = [
                name
                for name, mode_support in self.STYLE_MODE_SUPPORT.items()
                if mode_support in ("both", required_support)
            ]

            mode_label = (
                "image generation"
                if required_support == "image"
                else "video generation"
            )

            raise RuntimeError(
                f"Generation-mode/style conflict: style '{style}' is "
                f"{support}-only and cannot be used for {mode_label}. "
                f"Choose a compatible style such as: "
                f"{', '.join(compatible_styles)}."
            )

    # -------------------------------------------------------------------------
    # LM Studio model resolution
    # -------------------------------------------------------------------------

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

    def _resolve_model(self, client, model):
        """
        Resolve the model through LM Studio's OpenAI-compatible /v1/models API.

        No vision-capability check is performed. If visual inputs are connected
        to a model that does not support image input, LM Studio/model runtime
        will return the corresponding error.
        """

        requested_model = (model or "").strip()

        if not requested_model:
            raise RuntimeError(
                "The model field is empty. Enter an LM Studio model identifier "
                "or use 'auto'."
            )

        if requested_model.casefold() != "auto":
            return requested_model

        try:
            models = client.models.list()
        except Exception as e:
            raise RuntimeError(
                "Unable to list models from LM Studio while model='auto'. "
                "Check that LM Studio is running, the base URL is correct, and "
                f"authentication is configured correctly. Original error: {e}"
            ) from e

        if not models.data:
            raise RuntimeError(
                "LM Studio is reachable, but no model is available. "
                "Load a model in LM Studio or enter a valid model identifier."
            )

        return models.data[0].id

    # -------------------------------------------------------------------------
    # Image conversion
    # -------------------------------------------------------------------------

    def _to_numpy(self, image):
        """
        Convert a ComfyUI IMAGE tensor or compatible object to NumPy.

        Typical ComfyUI IMAGE:
            torch.Tensor [batch, height, width, channels], values 0..1
        """

        if image is None:
            return None

        if hasattr(image, "detach"):
            image = image.detach().cpu().numpy()

        return np.asarray(image)

    def _frame_to_pil(self, frame):
        """
        Convert one HWC frame to RGB PIL.
        """

        frame = np.asarray(frame)

        if frame.ndim != 3:
            raise ValueError(
                "Expected image frame with shape [height, width, channels], "
                f"got {frame.shape}."
            )

        if frame.shape[-1] > 4:
            frame = frame[..., :3]

        if frame.dtype != np.uint8:
            frame = np.clip(frame, 0.0, 1.0)
            frame = (frame * 255.0).round().astype(np.uint8)

        if frame.shape[-1] == 1:
            frame = np.repeat(
                frame,
                3,
                axis=-1
            )

        if frame.shape[-1] == 4:
            return Image.fromarray(
                frame,
                mode="RGBA"
            ).convert("RGB")

        if frame.shape[-1] != 3:
            raise ValueError(
                "Expected 1, 3, or 4 image channels, "
                f"got {frame.shape[-1]}."
            )

        return Image.fromarray(
            frame,
            mode="RGB"
        )

    def _resize_for_vision(self, pil_image):
        """
        Downscale large visual inputs while preserving aspect ratio.
        """

        width, height = pil_image.size
        max_side = max(width, height)

        if max_side <= self.MAX_IMAGE_SIDE:
            return pil_image

        scale = self.MAX_IMAGE_SIDE / max_side
        new_width = max(
            1,
            int(round(width * scale))
        )
        new_height = max(
            1,
            int(round(height * scale))
        )

        return pil_image.resize(
            (new_width, new_height),
            Image.LANCZOS
        )

    def _pil_to_data_url(self, pil_image):
        """
        Encode a PIL image as a PNG data URL.
        """

        pil_image = self._resize_for_vision(
            pil_image.convert("RGB")
        )

        buffer = BytesIO()
        pil_image.save(
            buffer,
            format="PNG",
            optimize=True
        )

        encoded = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        return f"data:image/png;base64,{encoded}"

    def _image_input_to_data_url(self, image, label):
        """
        Convert a ComfyUI IMAGE input to one PNG data URL.

        If a batch is supplied, use the first image.
        """

        image_np = self._to_numpy(image)

        if image_np is None:
            return None

        if image_np.ndim == 4:
            if image_np.shape[0] < 1:
                return None

            frame = image_np[0]

        elif image_np.ndim == 3:
            frame = image_np

        else:
            raise ValueError(
                f"{label} must be an IMAGE tensor with shape "
                f"[H,W,C] or [B,H,W,C], got {image_np.shape}."
            )

        return self._pil_to_data_url(
            self._frame_to_pil(frame)
        )

    # -------------------------------------------------------------------------
    # Prompt construction
    # -------------------------------------------------------------------------

    def _build_text_user_prompt(
        self,
        prompt,
        style,
        generation_mode,
        has_visual_context
    ):
        if generation_mode == self.VIDEO_MODE:
            mode_guidance = (
                "Mode: video generation. "
                "If supplied, input_image_1 is the FIRST FRAME and "
                "input_image_2 is the LAST FRAME. Build a coherent shot "
                "between them. Specify useful camera movement, subject and "
                "environmental motion, timing/pacing, continuity, lighting, "
                "atmosphere, and shot evolution."
            )
        else:
            mode_guidance = (
                "Mode: image generation. "
                "If supplied, input_image_1 is the BASE IMAGE and "
                "input_image_2 is the REFERENCE IMAGE. Preserve important "
                "base-image content and use the reference for relevant "
                "appearance, composition, lighting, material, color, or style cues."
            )

        visual_note = ""

        if has_visual_context:
            visual_note = (
                " Visual inputs are attached. Use visible evidence and do not "
                "invent details that conflict with the original prompt or imagery."
            )


        return (
            "Enhance this prompt for a generative model.\n\n"
            f"Requested style: {style}\n"
            f"Original prompt: {prompt}\n\n"
            f"{mode_guidance}{visual_note}\n\n"
            "Return one generator-friendly positive prompt only. Preserve the "
            "user's intent. No negative-prompt terms, markdown, analysis, or explanation."
        )

    def _build_multimodal_content(
        self,
        prompt,
        style,
        generation_mode,
        input_image_1=None,
        input_image_2=None
    ):
        """
        Build OpenAI-compatible multimodal chat content.
        """

        image_1_data_url = (
            self._image_input_to_data_url(
                input_image_1,
                "input_image_1"
            )
            if input_image_1 is not None
            else None
        )

        image_2_data_url = (
            self._image_input_to_data_url(
                input_image_2,
                "input_image_2"
            )
            if input_image_2 is not None
            else None
        )


        has_visual_context = bool(
            image_1_data_url
            or image_2_data_url
        )

        text_prompt = self._build_text_user_prompt(
            prompt=prompt,
            style=style,
            generation_mode=generation_mode,
            has_visual_context=has_visual_context
        )

        if not has_visual_context:
            return text_prompt

        content = [
            {
                "type": "text",
                "text": text_prompt
            }
        ]

        if generation_mode == self.VIDEO_MODE:
            image_1_label = "First video frame (input_image_1):"
            image_2_label = "Last video frame (input_image_2):"
        else:
            image_1_label = "Base image (input_image_1):"
            image_2_label = "Reference image (input_image_2):"

        if image_1_data_url:
            content.extend(
                [
                    {
                        "type": "text",
                        "text": image_1_label
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_1_data_url
                        }
                    }
                ]
            )

        if image_2_data_url:
            content.extend(
                [
                    {
                        "type": "text",
                        "text": image_2_label
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_2_data_url
                        }
                    }
                ]
            )

        return content

    # -------------------------------------------------------------------------
    # Main execution
    # -------------------------------------------------------------------------

    def enhance_prompt(
        self,
        prompt,
        generation_mode,
        system_prompt,
        style,
        lmstudio_base_url,
        lmstudio_api_key,
        model,
        temperature,
        max_tokens,
        enable_llm,
        cache_buster,
        input_image_1=None,
        input_image_2=None
    ):
        prompt = (prompt or "").strip()

        if not prompt:
            raise RuntimeError(
                "The prompt input is empty."
            )

        # Explicit passthrough: no validation or API calls.
        if not enable_llm:
            return (prompt,)

        # Required preflight #1:
        # generation mode and style must be compatible.
        self._validate_generation_mode_and_style(
            generation_mode,
            style
        )

        system_prompt = (
            system_prompt
            or ""
        ).strip()

        if not system_prompt:
            raise RuntimeError(
                "The system_prompt field is empty. "
                "Add instructions for the LLM."
            )

        base_url = (
            lmstudio_base_url
            or ""
        ).strip()

        if not base_url:
            raise RuntimeError(
                "The lmstudio_base_url field is empty."
            )

        api_key = self._get_api_key(
            lmstudio_api_key
        )

        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        # Resolve the requested model. No vision-capability preflight is used.
        resolved_model = self._resolve_model(
            client=client,
            model=model
        )

        # Build optional image context after mode/style validation.
        user_content = self._build_multimodal_content(
            prompt=prompt,
            style=style,
            generation_mode=generation_mode,
            input_image_1=input_image_1,
            input_image_2=input_image_2
        )

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
                        "content": user_content
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            if (
                not response.choices
                or response.choices[0].message is None
            ):
                raise RuntimeError(
                    "LM Studio returned no completion choice."
                )

            enhanced = (
                response.choices[0].message.content
                or ""
            ).strip()

            if not enhanced:
                enhanced = prompt

            return (enhanced,)

        except Exception as e:
            raise RuntimeError(
                "LM Studio prompt enhancement failed. "
                f"Server: {base_url}; model: {resolved_model}. "
                "Check that LM Studio is running, the selected model is loaded "
                "or available for JIT loading, the model accepts image inputs, "
                "and the API token is correct when authentication is enabled. "
                f"Original error: {e}"
            ) from e


NODE_CLASS_MAPPINGS = {
    "LMStudioPromptEnhancer": LMStudioPromptEnhancer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LMStudioPromptEnhancer": "LM Studio Prompt Enhancer",
}