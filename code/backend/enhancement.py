# code/enhancement.py
import os
import argparse
from functions import (
    ensure_dir,
    load_grayscale,
    histogram_equalization,
    gamma_correction,
    combined_eq_then_gamma,
    save_image,
    save_histogram,
)

def main():
    parser = argparse.ArgumentParser(description="Image enhancement CLI for medical X-rays.")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path to save enhanced image")
    parser.add_argument("--method", choices=["hist_eq", "gamma", "combined"], default="combined",
                        help="Enhancement method to apply (default: combined)")
    parser.add_argument("--gamma", type=float, default=0.5, help="Gamma value when using gamma/combined (default: 0.5)")
    parser.add_argument("--images_dir", default=os.path.join("images"), help="Where to save intermediate images")
    parser.add_argument("--hist_dir", default=os.path.join("images", "histograms"), help="Where to save histograms")
    args = parser.parse_args()

    ensure_dir(args.images_dir)
    ensure_dir(args.hist_dir)
    ensure_dir(os.path.dirname(os.path.abspath(args.output)))

    img = load_grayscale(args.input)
    save_histogram(img, "Original Histogram", os.path.join(args.hist_dir, "original_hist.png"))

    if args.method == "hist_eq":
        out = histogram_equalization(img)
        save_image(os.path.join(args.images_dir, "hist_eq_result.jpg"), out)
        save_histogram(out, "Histogram After Equalization", os.path.join(args.hist_dir, "hist_eq_hist.png"))

    elif args.method == "gamma":
        out = gamma_correction(img, gamma=args.gamma, c=1.0)
        save_image(os.path.join(args.images_dir, "gamma_result.jpg"), out)
        save_histogram(out, f"Histogram After Gamma (γ={args.gamma})", os.path.join(args.hist_dir, "gamma_hist.png"))

    else:  # combined
        out = combined_eq_then_gamma(img, gamma=args.gamma)
        save_image(os.path.join(args.images_dir, "combined_result.jpg"), out)
        save_histogram(out, f"Histogram After EQ→Gamma (γ={args.gamma})", os.path.join(args.hist_dir, "combined_hist.png"))

    save_image(args.output, out)
    print(f"Enhanced image saved to: {args.output}")

if __name__ == "__main__":
    main()
