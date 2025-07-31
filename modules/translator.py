from googletrans import Translator as GoogleTranslator
import time

class Translator:
    def __init__(self):
        self.translator = GoogleTranslator()
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese (Simplified)',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish'
        }
    
    def translate_text(self, text, target_language, source_language='auto'):
        """Translate text to target language"""
        try:
            # Handle long text by splitting into chunks
            if len(text) > 5000:
                chunks = self._split_text(text, 4000)
                translated_chunks = []
                
                for chunk in chunks:
                    result = self.translator.translate(chunk, dest=target_language, src=source_language)
                    translated_chunks.append(result.text)
                    time.sleep(0.1)  # Small delay to avoid rate limiting
                
                return ' '.join(translated_chunks)
            else:
                result = self.translator.translate(text, dest=target_language, src=source_language)
                return result.text
                
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def _split_text(self, text, max_length):
        """Split text into chunks for translation"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_chunk.append(word)
                current_length += len(word) + 1
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return self.supported_languages
    
    def detect_language(self, text):
        """Detect the language of given text"""
        try:
            result = self.translator.detect(text)
            return {
                'language': result.lang,
                'confidence': result.confidence
            }
        except Exception as e:
            return {'language': 'unknown', 'confidence': 0}
