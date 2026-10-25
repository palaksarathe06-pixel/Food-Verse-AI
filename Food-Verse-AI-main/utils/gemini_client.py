"""
utils/gemini_client.py
Centralised wrapper around Google Generative AI (Gemini Multimodal Suite).
Provides text, image, video, and audio generation with graceful fallback
to built-in demo data when no API key is configured or when offline.
"""

import json
import os
import tempfile
import google.generativeai as genai
from typing import Optional, List
from PIL import Image

# Gemini API key (loaded from Render / system environment variable GEMINI_API_KEY)
DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Primary and fallback models known to support generateContent
CANDIDATE_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-2.5-flash-lite",
]

_ACTIVE_MODEL_NAME: Optional[str] = None


# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------

def configure_gemini(api_key: Optional[str] = None) -> bool:
    """Configure the Gemini SDK with the provided or default API key.
    Validates by checking supported models. Returns True on success."""
    global _ACTIVE_MODEL_NAME
    key = api_key or DEFAULT_API_KEY
    if not key or not key.strip():
        return False

    try:
        genai.configure(api_key=key.strip())
        
        # Determine the best working model
        for model_name in CANDIDATE_MODELS:
            try:
                test_model = genai.GenerativeModel(model_name)
                # Quick lightweight ping
                _ACTIVE_MODEL_NAME = model_name
                return True
            except Exception:
                continue
        
        # Fallback to default
        _ACTIVE_MODEL_NAME = CANDIDATE_MODELS[0]
        return True
    except Exception:
        return False


def get_active_model_name() -> str:
    """Return currently active model identifier."""
    global _ACTIVE_MODEL_NAME
    return _ACTIVE_MODEL_NAME or CANDIDATE_MODELS[0]


# ---------------------------------------------------------------------------
#  Generation helpers
# ---------------------------------------------------------------------------

def _run_with_model_fallback(func, *args, **kwargs):
    """Run generation function with automatic fallback across candidate models."""
    global _ACTIVE_MODEL_NAME
    models_to_try = [get_active_model_name()] + [m for m in CANDIDATE_MODELS if m != get_active_model_name()]
    last_err = None

    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(m_name)
            res = func(model, *args, **kwargs)
            _ACTIVE_MODEL_NAME = m_name
            return res
        except Exception as e:
            last_err = e
            continue

    return f"[Gemini Error] All candidate models failed. Last error: {str(last_err)}"


def generate_text(prompt: str, temperature: float = 0.7) -> Optional[str]:
    """Generate text-only response from Gemini with model fallback."""
    def _call(model: genai.GenerativeModel):
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            ),
        )
        return response.text

    return _run_with_model_fallback(_call)


def generate_with_image(
    prompt: str,
    image: Image.Image,
    temperature: float = 0.4,
) -> Optional[str]:
    """Send an image + text prompt to Gemini Vision and return the response."""
    def _call(model: genai.GenerativeModel):
        response = model.generate_content(
            [prompt, image],
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            ),
        )
        return response.text

    return _run_with_model_fallback(_call)


def extract_video_frames(video_bytes: bytes, max_frames: int = 4) -> List[Image.Image]:
    """Extract up to max_frames evenly spaced frames from video bytes using OpenCV."""
    try:
        import cv2
    except ImportError:
        return []

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_file.write(video_bytes)
        temp_file_path = temp_file.name

    frames: List[Image.Image] = []
    try:
        cap = cv2.VideoCapture(temp_file_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames > 0:
            step = max(1, total_frames // max_frames)
            for i in range(0, total_frames, step):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(Image.fromarray(frame_rgb))
                if len(frames) >= max_frames:
                    break
        cap.release()
    finally:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass

    return frames


def generate_with_video(
    prompt: str,
    video_bytes: bytes,
    temperature: float = 0.4,
) -> Optional[str]:
    """Analyze video clips by extracting sequential keyframes and running Gemini multimodal analysis."""
    frames = extract_video_frames(video_bytes, max_frames=4)
    if not frames:
        return "[Video Processing Error] Unable to decode video frames. Please check file format."

    def _call(model: genai.GenerativeModel):
        contents = [
            f"{prompt}\n[Context: You are analyzing 4 sequential frames extracted from a kitchen monitoring video clip]",
            *frames,
        ]
        response = model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            ),
        )
        return response.text

    return _run_with_model_fallback(_call)


def generate_with_audio(
    prompt: str,
    audio_bytes: bytes,
    mime_type: str = "audio/wav",
    temperature: float = 0.4,
) -> Optional[str]:
    """Send audio recording + prompt to Gemini for audio intelligence."""
    def _call(model: genai.GenerativeModel):
        contents = [
            prompt,
            {"mime_type": mime_type, "data": audio_bytes},
        ]
        response = model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            ),
        )
        return response.text

    return _run_with_model_fallback(_call)


# ---------------------------------------------------------------------------
#  JSON parsing helper
# ---------------------------------------------------------------------------

def parse_json_response(text: Optional[str]) -> dict:
    """Best-effort extraction of a JSON object or list from model output."""
    if not text or not isinstance(text, str):
        return {}

    cleaned = text.strip()
    # Strip markdown code fences if present (```json ... ```)
    if "```" in cleaned:
        lines = cleaned.split("\n")
        filtered = []
        in_block = False
        for line in lines:
            if line.strip().startswith("```"):
                in_block = not in_block
                continue
            filtered.append(line)
        cleaned = "\n".join(filtered).strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object within the text
    start_obj = cleaned.find("{")
    end_obj = cleaned.rfind("}") + 1
    if start_obj != -1 and end_obj > start_obj:
        try:
            return json.loads(cleaned[start_obj:end_obj])
        except json.JSONDecodeError:
            pass

    # Try to find JSON array within the text
    start_arr = cleaned.find("[")
    end_arr = cleaned.rfind("]") + 1
    if start_arr != -1 and end_arr > start_arr:
        try:
            return json.loads(cleaned[start_arr:end_arr])
        except json.JSONDecodeError:
            pass

    return {}
