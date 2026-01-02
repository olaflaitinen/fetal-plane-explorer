from PIL import Image, ImageDraw
import numpy as np
import os

def create_synthetic_ultrasound():
    width, height = 224, 224
    
    # Perlin-like noise or just random noise
    noise = np.random.normal(0, 1, (height, width))
    
    # Create a shape (skull-like ellipse)
    y, x = np.ogrid[:height, :width]
    center = (int(width/2), int(height/2))
    mask = ((x - center[0])**2 / (0.4*width)**2 + (y - center[1])**2 / (0.3*height)**2) <= 1
    
    # Add structure to noise
    img_data = np.zeros((height, width))
    img_data[mask] = 0.5 # Mean intensity
    img_data += noise * 0.1 # Add speckle
    
    # Scale to 0-255
    img_data = np.clip(img_data * 255, 0, 255).astype(np.uint8)
    
    img = Image.fromarray(img_data, mode="L")
    
    os.makedirs("assets/synthetic", exist_ok=True)
    img.save("assets/synthetic/placeholder.png")
    print("Created assets/synthetic/placeholder.png")

if __name__ == "__main__":
    create_synthetic_ultrasound()
