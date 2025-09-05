# code/enhancement.py
import os
import argparse
from functions import (
    ensure_dir,
    load_grayscale,
    gamma_correction,
    piecewise_contrast_stretch,
    combined_contrast_gamma,
    save_image,
    save_histogram,
)

def main():
    parser = argparse.ArgumentParser(description="Image enhancement CLI for medical MRI/X-rays.")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path to save enhanced image")
    parser.add_argument("--method", choices=["gamma", "contrast", "combined"], default="combined",
                        help="Enhancement method to apply (default: combined)")
    parser.add_argument("--gamma", type=float, default=0.5, help="Gamma value (default: 0.5)")
    parser.add_argument("--r1", type=int, default=70, help="Contrast stretch input low breakpoint (default: 70)")
    parser.add_argument("--s1", type=int, default=0, help="Contrast stretch output low value (default: 0)")
    parser.add_argument("--r2", type=int, default=140, help="Contrast stretch input high breakpoint (default: 140)")
    parser.add_argument("--s2", type=int, default=255, help="Contrast stretch output high value (default: 255)")
    parser.add_argument("--images_dir", default=os.path.join("images"), help="Where to save intermediate images")
    parser.add_argument("--hist_dir", default=os.path.join("images", "histograms"), help="Where to save histograms")
    args = parser.parse_args()

    ensure_dir(args.images_dir)
    ensure_dir(args.hist_dir)
    ensure_dir(os.path.dirname(os.path.abspath(args.output)))

    # Load input image
    img = load_grayscale(args.input)

    # Save original histogram
    save_histogram(img, "Original Histogram", os.path.join(args.hist_dir, "original_hist.png"))

    if args.method == "gamma":
        out = gamma_correction(img, gamma=args.gamma)
        save_image(os.path.join(args.images_dir, "gamma_result.jpg"), out)
        save_histogram(out, f"Histogram After Gamma (γ={args.gamma})", os.path.join(args.hist_dir, "gamma_hist.png"))

    elif args.method == "contrast":
        out = piecewise_contrast_stretch(img, r1=args.r1, s1=args.s1, r2=args.r2, s2=args.s2)
        save_image(os.path.join(args.images_dir, "contrast_result.jpg"), out)
        save_histogram(out, "Histogram After Contrast Stretching", os.path.join(args.hist_dir, "contrast_hist.png"))

    else:  # combined
        out = combined_contrast_gamma(img, gamma=args.gamma, r1=args.r1, s1=args.s1, r2=args.r2, s2=args.s2)
        save_image(os.path.join(args.images_dir, "combined_result.jpg"), out)
        save_histogram(out, f"Histogram After Contrast→Gamma (γ={args.gamma})", os.path.join(args.hist_dir, "combined_hist.png"))

    # Save final enhanced image to user-specified path
    save_image(args.output, out)
    print(f"Enhanced image saved to: {args.output}")

if __name__ == "__main__":
    main()
