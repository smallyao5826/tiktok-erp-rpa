import ddddocr
import logging

class OCRUtil:
    def __init__(self, show_ad=False):
        if not show_ad:
            logging.getLogger("ddddocr").setLevel(logging.ERROR)
        # beta=True 识别率通常更高
        self.ocr = ddddocr.DdddOcr(show_ad=show_ad, beta=True)

    def recognize(self, image_bytes):
        if not image_bytes:
            return ""
        try:
            return self.ocr.classification(image_bytes).strip()
        except Exception:
            return ""

ocr_tool = OCRUtil()