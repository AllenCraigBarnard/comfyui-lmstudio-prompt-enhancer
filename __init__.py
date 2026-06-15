from .lmstudio_prompt_enhancer import LMStudioPromptEnhancer

NODE_CLASS_MAPPINGS = {
    "LMStudioPromptEnhancer": LMStudioPromptEnhancer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LMStudioPromptEnhancer": "LM Studio Prompt Enhancer",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]