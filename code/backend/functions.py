# code/functions.py
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Fix: avoid Tkinter dependency
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

def save_histogram(img: np.ndarray, title: str, out_path: str):
    ensure_dir(os.path.dirname(out_path))
    plt.figure()
    plt.title(title)
    plt.xlabel("Intensity (0-255)")
    plt.ylabel("Frequency")
    plt.xlim([0, 255])
    plt.hist(img.ravel(), bins=256, range=(0, 255))
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

# ---------- Enhancement techniques ----------
def histogram_equalization(img: np.ndarray) -> np.ndarray:
    # expects uint8 grayscale
    return cv2.equalizeHist(img)

def gamma_correction(img: np.ndarray, gamma: float = 0.5, c: float = 1.0) -> np.ndarray:
    # s = c * r^gamma  where r in [0,1]
    r = img.astype(np.float32) / 255.0
    s = c * np.power(r, gamma)
    out = np.clip(s * 255.0, 0, 255).astype(np.uint8)
    return out

def combined_eq_then_gamma(img: np.ndarray, gamma: float = 0.5) -> np.ndarray:
    eq = histogram_equalization(img)
    return gamma_correction(eq, gamma=gamma, c=1.0)

# ---------- Full pipeline utility (used by GUI & CLI) ----------
def process_and_save_all(
    input_path: str,
    images_dir: str,
    hist_dir: str,
    gamma: float = 0.5,
) -> dict:
    """
    Loads input image (grayscale), computes:
      - histogram equalization
      - gamma correction
      - combined (eq -> gamma)
    Saves all images + histograms using the original image name as prefix.
    Returns dict of output paths.
    """
    ensure_dir(images_dir)
    ensure_dir(hist_dir)

    # --- Extract base name without extension ---
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # Load
    original = load_grayscale(input_path)

    # Save original histogram
    original_hist_path = os.path.join(hist_dir, f"{base_name}_original_hist.png")
    save_histogram(original, "Original Histogram", original_hist_path)

    # 1) Histogram Equalization
    hist_eq_img = histogram_equalization(original)
    hist_eq_path = os.path.join(images_dir, f"{base_name}_hist_eq.jpg")
    save_image(hist_eq_path, hist_eq_img)
    hist_eq_hist_path = os.path.join(hist_dir, f"{base_name}_hist_eq_hist.png")
    save_histogram(hist_eq_img, "Histogram After Equalization", hist_eq_hist_path)

    # 2) Gamma Correction
    gamma_img = gamma_correction(original, gamma=gamma, c=1.0)
    gamma_path = os.path.join(images_dir, f"{base_name}_gamma.jpg")
    save_image(gamma_path, gamma_img)
    gamma_hist_path = os.path.join(hist_dir, f"{base_name}_gamma_hist.png")
    save_histogram(gamma_img, f"Histogram After Gamma (γ={gamma})", gamma_hist_path)

    # 3) Combined (EQ -> Gamma)
    combined_img = combined_eq_then_gamma(original, gamma=gamma)
    combined_path = os.path.join(images_dir, f"{base_name}_combined.jpg")
    save_image(combined_path, combined_img)
    combined_hist_path = os.path.join(hist_dir, f"{base_name}_combined_hist.png")
    save_histogram(combined_img, f"Histogram After EQ→Gamma (γ={gamma})", combined_hist_path)

    return {
        "original_hist": original_hist_path,
        "hist_eq_img": hist_eq_path,
        "hist_eq_hist": hist_eq_hist_path,
        "gamma_img": gamma_path,
        "gamma_hist": gamma_hist_path,
        "combined_img": combined_path,
        "combined_hist": combined_hist_path,
    }
