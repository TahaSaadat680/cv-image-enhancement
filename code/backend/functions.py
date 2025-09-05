# code/functions.py
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Avoid Tkinter issues
import matplotlib.pyplot as plt

# ---------- Paths & IO helpers ----------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def load_grayscale(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img

def save_image(path: str, img: np.ndarray):
    ensure_dir(os.path.dirname(path))
    ok = cv2.imwrite(path, img)
    if not ok:
        raise IOError(f"Failed to save image: {path}")

def save_histogram(img: np.ndarray, title: str, out_path: str, yscale: float = 0.025):
    """
    Save histogram of the image with limited y-axis for better visualization.
    yscale: fraction of max frequency to display (e.g., 0.4 = 40% of max count).
    """
    ensure_dir(os.path.dirname(out_path))
    hist, bins = np.histogram(img.ravel(), bins=256, range=(0, 255))
    max_freq = hist.max()
    
    plt.figure(figsize=(5, 3))
    plt.title(title)
    plt.xlabel("Intensity (0-255)")
    plt.ylabel("Frequency")
    plt.xlim([0, 255])
    plt.ylim([0, int(max_freq * yscale)])  # Scale down Y-axis
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.bar(bins[:-1], hist, width=1, color="black", alpha=0.7)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


# ---------- Enhancement techniques ----------
def gamma_correction(img: np.ndarray, gamma: float = 0.5, c: float = 1.0) -> np.ndarray:
    """Gamma correction: s = c * r^gamma where r in [0,1]."""
    r = img.astype(np.float32) / 255.0
    s = c * np.power(r, gamma)
    out = np.clip(s * 255.0, 0, 255).astype(np.uint8)
    return out

def piecewise_contrast_stretch(img: np.ndarray, r1=70, s1=0, r2=140, s2=255) -> np.ndarray:
    """Piecewise linear contrast stretching"""
    lut = np.zeros(256, dtype=np.uint8)
    for r in range(256):
        if r < r1:
            lut[r] = int((s1 / r1) * r) if r1 != 0 else 0
        elif r < r2:
            lut[r] = int(((s2 - s1) / (r2 - r1)) * (r - r1) + s1)
        else:
            lut[r] = int(((255 - s2) / (255 - r2)) * (r - r2) + s2)
    return cv2.LUT(img, lut)

def combined_contrast_gamma(img: np.ndarray, gamma: float = 0.5, r1=70, s1=0, r2=140, s2=255) -> np.ndarray:
    contrast = piecewise_contrast_stretch(img, r1, s1, r2, s2)
    return gamma_correction(contrast, gamma=gamma)


# ---------- Full pipeline utility ----------
def process_and_save_all(
    input_path: str,
    images_dir: str,
    hist_dir: str,
    gamma: float = 0.5,
    r1: int = 70, s1: int = 0, r2: int = 140, s2: int = 255,
) -> dict:
    """
    Loads input image (grayscale), computes:
      - gamma correction
      - contrast stretching
      - combined (contrast -> gamma)
    Saves all images + histograms.
    Returns dict of output paths.
    """
    ensure_dir(images_dir)
    ensure_dir(hist_dir)

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # Load
    original = load_grayscale(input_path)

    # Save original histogram
    original_hist_path = os.path.join(hist_dir, f"{base_name}_original_hist.png")
    save_histogram(original, "Original Histogram", original_hist_path)

    # 1) Gamma Correction
    gamma_img = gamma_correction(original, gamma=gamma, c=1.0)
    gamma_path = os.path.join(images_dir, f"{base_name}_gamma.jpg")
    save_image(gamma_path, gamma_img)
    gamma_hist_path = os.path.join(hist_dir, f"{base_name}_gamma_hist.png")
    save_histogram(gamma_img, f"Histogram After Gamma (γ={gamma})", gamma_hist_path)

    # 2) Contrast Stretching
    contrast_img = piecewise_contrast_stretch(original, r1, s1, r2, s2)
    contrast_path = os.path.join(images_dir, f"{base_name}_contrast.jpg")
    save_image(contrast_path, contrast_img)
    contrast_hist_path = os.path.join(hist_dir, f"{base_name}_contrast_hist.png")
    save_histogram(contrast_img, "Histogram After Contrast Stretching", contrast_hist_path)

    # 3) Combined (Contrast → Gamma)
    combined_img = combined_contrast_gamma(original, gamma=gamma, r1=r1, s1=s1, r2=r2, s2=s2)
    combined_path = os.path.join(images_dir, f"{base_name}_combined.jpg")
    save_image(combined_path, combined_img)
    combined_hist_path = os.path.join(hist_dir, f"{base_name}_combined_hist.png")
    save_histogram(combined_img, f"Histogram After Contrast→Gamma (γ={gamma})", combined_hist_path)

    return {
        "original_hist": original_hist_path,
        "gamma_img": gamma_path,
        "gamma_hist": gamma_hist_path,
        "contrast_img": contrast_path,
        "contrast_hist": contrast_hist_path,
        "combined_img": combined_path,
        "combined_hist": combined_hist_path,
    }
