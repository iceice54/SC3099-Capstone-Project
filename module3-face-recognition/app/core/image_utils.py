# Singleton MediaPipe FaceDetection & FaceMesh manager# Base64 decoding, RGB conversion, quality & blurriness scoring

import base64
from io.import BytesIO
from PIL import Image
import numpy as np

def decode_base64_image(base64_string: str) -> np.ndarray:
  """
  Decode a base64 encoded image to a numpy array.

  TODO: Implement using:
  - base64.b64decode()
  - PIL.Image.open(BytesIO(...))
  - numpy.array()

  Handle errors gracefully (invalid base64, corrupt image, etc.)
  """
  decoded = base64.b64decode(base64_string)
  image = Image.open(decoded)