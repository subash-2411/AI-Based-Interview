import os
import google.generativeai as genai

# Save the original method
_original_generate_content = genai.GenerativeModel.generate_content

def _rotated_generate_content(self, *args, **kwargs):
    try:
        api_key_str = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
        keys = [k.strip() for k in api_key_str.split(",") if k.strip()]
        
        if len(keys) <= 1:
            return _original_generate_content(self, *args, **kwargs)
            
        last_error = None
        for key in keys:
            try:
                # Reconfigure Google Generative AI globally
                genai.configure(api_key=key)
                
                # Reset lazy clients to force re-generation with the new key
                self._client = None
                self._async_client = None
                
                return _original_generate_content(self, *args, **kwargs)
            except Exception as e:
                import traceback
                print(f"[Key Rotation] Key failed: {e}")
                traceback.print_exc()
                last_error = e
                continue
                
        raise last_error
    except Exception as outer_err:
        raise outer_err

# Monkeypatch the method
genai.GenerativeModel.generate_content = _rotated_generate_content
