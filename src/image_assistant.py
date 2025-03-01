from abc import ABC, abstractmethod

from logger import LOG

import requests
import base64
from io import BytesIO
from PIL import Image


class ImageAssistant(ABC):
    """
    Image processing assistant that specializes in handling image-related tasks.
    Uses Stable Diffusion model for AI processing with custom image-specific prompts.
    """
    def __init__(self):
        super().__init__()

    def process_image(self, image_path, prompt):
        """
        Abstract method for processing a single image.

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Processing results including analysis and recommendations
        """
        self.url = "http://127.0.0.1:7861/sdapi/v1/txt2img"
        self.payload = {
            "prompt": prompt,
            "steps": 30,
            "width": 512,
            "height": 512,
            "cfg_scale": 7.5
        }
        response = requests.post(self.url, json=self.payload)

        # 处理响应
        if response.status_code == 200:
            data = response.json()
            image_data = base64.b64decode(data["images"][0])  # 图片以 Base64 编码返回
            image = Image.open(BytesIO(image_data))
            image.save(image_path)
            print("图片已保存为 images/performance_chart.png")
        else:
            print(f"请求失败: {response.status_code}, {response.text}")

