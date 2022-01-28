"""This module has some functions related to machine learning model"""
# pylint: disable=no-member, line-too-long
import argparse
import os
from typing import NoReturn

import cv2
import facexlib.utils
from basicsr.utils import imwrite
from gfpgan import GFPGANer
from torch.hub import download_url_to_file

from config import (ALIGNED, ARCH, BACKGROUND_MODEL_NAME, CHANNEL, EXTENSION,
                    ONLY_CENTER_FACE, PASTE_BACK, RESTORE_FOLDER, UPSCALE)

FACEXLIB_DETECTION_MODEL_URL = "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"
GFPGAN_MODEL_URL = "https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth"
GFPGAN_MODEL_PATH = "model/face_model/GFPGANCleanv1-NoCE-C2.pth"


def download_models() -> NoReturn:
    """Download model files if not present."""
    if not os.path.exists(GFPGAN_MODEL_PATH):
        os.makedirs(os.path.dirname(GFPGAN_MODEL_PATH), exist_ok=True)
        download_url_to_file(GFPGAN_MODEL_URL, GFPGAN_MODEL_PATH)
    facexlib.utils.load_file_from_url(FACEXLIB_DETECTION_MODEL_URL, model_dir="facexlib/weights")


# pylint: disable=unused-argument, too-many-arguments, too-many-locals
def restore_image(img_path: str,
                  output_dir: str = RESTORE_FOLDER,
                  bg_upsampler_model: str = BACKGROUND_MODEL_NAME,
                  model_path: str = GFPGAN_MODEL_PATH,
                  upscale: int = UPSCALE,
                  arch: str = ARCH,
                  channel: int = CHANNEL,
                  aligned: bool = ALIGNED,
                  only_center_face: bool = ONLY_CENTER_FACE,
                  paste_back: bool = PASTE_BACK,
                  ext: str = EXTENSION) -> NoReturn:
    """
    Function restores provided image and saves it in `RESTORE_FOLDER`

    Parameters
    ----------
    img_path: str
        Path to image for restoration
    output_dir: str
        Directory, where restored image should be saved
        default = `RESTORE_FOLDER` from `config.py`
    bg_upsampler_model: str
        Name of a model for background restoration
        default = `BACKGROUND_MODEL_NAME` from `config.py`
    model_path: str
        Path for GFPGAN model for face restoration
        default = `GFPGAN_MODEL_PATH` from `config.py`
    upscale: int
        Final upsampling scale of the image
        default = `UPSCALE` from `config.py`
    arch: str,
        GFPGAN architecture. Options: clear | original
        default = `ARCH` from `config.py`
    channel: int
        Channel multiplier for large networks of StyleGAN2
        default = `CHANNEL` from `config.py`
    aligned: bool
        Input image has aligned faces
        default = `ALIGNED` from `config.py`
    only_center_face: bool
        If only center face should be restored
        default = `ONLY_CENTER_FACE` from `config.py`
    paste_back: bool
        Paste restored faces back to images
        default = `PASTE_BACK` from `config.py`
    ext: str
        Image extension. Options: auto | jpg | png, auto means using the same extension as inputs
        default = `EXTENSION` from `config.py`

    Raises
    ------
    SystemError
        If model did not restore image properly
    """
    # Create output directory if needed
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
    basename = os.path.splitext(img_name)[0]
    input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # restore faces and background if necessary
    restored_img = restorer.enhance(
        input_img, has_aligned=aligned, only_center_face=only_center_face, paste_back=paste_back)[2]

    # save restored img
    if restored_img is not None:
        # get image extension
        if ext == "auto":
            extension = img_name.split('.')[1]

        else:
            extension = ext

        save_restore_path = os.path.join(output_dir, f'{basename}_restored.{extension}')
        imwrite(restored_img, save_restore_path)
    else:
        raise SystemError("File was not restored properly!")


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
