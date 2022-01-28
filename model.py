import argparse
import os
import cv2
import facexlib.utils
from torch.hub import download_url_to_file
from basicsr.utils import imwrite
from gfpgan import GFPGANer

FACEXLIB_DETECTION_MODEL_URL = "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"
GFPGAN_MODEL_URL = "https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth"
GFPGAN_MODEL_PATH = "model/face_model/GFPGANCleanv1-NoCE-C2.pth"


def download_models():
    """Download model files if not present."""
    if not os.path.exists(GFPGAN_MODEL_PATH):
        os.makedirs(os.path.dirname(GFPGAN_MODEL_PATH), exist_ok=True)
        download_url_to_file(GFPGAN_MODEL_URL, GFPGAN_MODEL_PATH)
    facexlib.utils.load_file_from_url(FACEXLIB_DETECTION_MODEL_URL, model_dir="facexlib/weights")


def restore_image(img_path: str,
                  output_dir: str = "static/restored",
                  bg_upsampler_model: str = "realesrgan",
                  model_path: str = GFPGAN_MODEL_PATH,
                  upscale: int = 2,
                  arch: str = "clean",
                  channel: int = 2,
                  aligned: bool = False,
                  only_center_face: bool = False,
                  paste_back: bool = True,
                  ext: str = "auto"):
    if output_dir.endswith('/'):
        output_dir = output_dir[:-1]
    os.makedirs(output_dir, exist_ok=True)

    bg_upsampler = None

    restorer = GFPGANer(
        model_path=model_path,
        upscale=upscale,
        arch=arch,
        channel_multiplier=channel,
        bg_upsampler=bg_upsampler)

    # read image
    img_name = os.path.basename(img_path)
    print(f'Processing {img_name} ...')
    basename = os.path.splitext(img_name)[0]
    input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # restore faces and background if necessary

    cropped_faces, restored_faces, restored_img = restorer.enhance(
        input_img, has_aligned=aligned, only_center_face=only_center_face, paste_back=paste_back)

    # save restored img
    if restored_img is not None:
        if ext == 'auto':
            extension = img_name.split('.')[1]

        else:
            extension = ext

        save_restore_path = os.path.join(output_dir, f'{basename}_restored.{extension}')
        imwrite(restored_img, save_restore_path)

    print("DONE, ", save_restore_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    subparsers = ap.add_subparsers(dest="cmd")
    subparsers.required = True
    download_ap = subparsers.add_parser("download-models", help="download model files required for restoration")
    restore_ap = subparsers.add_parser("restore-image", help="restore an image")
    restore_ap.add_argument("image_path", help="path to the image you want to restore")

    args = ap.parse_args()
    {
        "download-models": download_models,
        "restore-image": lambda: restore_image(args.image_path),
    }[args.cmd]()
