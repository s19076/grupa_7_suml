"""This module has some functions related to machine learning model"""
# pylint: disable=no-member, line-too-long
from typing import NoReturn
import argparse
import os
import cv2
import facexlib.utils
import torch.cuda
from realesrgan import RealESRGANer
from torch.hub import download_url_to_file
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils import imwrite
from gfpgan import GFPGANer
from config import RESTORE_FOLDER, UPSCALE, ARCH, CHANNEL, ALIGNED, ONLY_CENTER_FACE, PASTE_BACK, \
    EXTENSION

FACEXLIB_DETECTION_MODEL_URL = "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"
GFPGAN_MODEL_URL = "https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth"
REALESREGANER_MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"
GFPGAN_MODEL_PATH = "model/face_model/GFPGANCleanv1-NoCE-C2.pth"
REALESRGANER_MODEL_PATH = "model/background_model/RealEsrGAN_x2plus.pth"


def download_models() -> NoReturn:
    """Download model files if not present."""
    if not os.path.exists(GFPGAN_MODEL_PATH):
        os.makedirs(os.path.dirname(GFPGAN_MODEL_PATH), exist_ok=True)
        download_url_to_file(GFPGAN_MODEL_URL, GFPGAN_MODEL_PATH)

    if not os.path.exists(REALESRGANER_MODEL_PATH):
        os.makedirs(os.path.dirname(REALESRGANER_MODEL_PATH), exist_ok=True)
        download_url_to_file(REALESREGANER_MODEL_URL, REALESRGANER_MODEL_PATH)

    facexlib.utils.load_file_from_url(FACEXLIB_DETECTION_MODEL_URL, model_dir="facexlib/weights")


# pylint: disable=unused-argument, too-many-arguments, too-many-locals
def restore_image(img_path: str,
                  output_dir: str = RESTORE_FOLDER,
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

    if torch.cuda.is_available():
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        bg_upsampler = RealESRGANer(
            scale=2,
            model_path=REALESRGANER_MODEL_PATH,
            model=model,
            tile=400,
            tile_pad=10,
            pre_pad=0,
            half=True)
    else:
        # bg_upsampler = RealESRGANer(
        #   scale=2,
        #  model_path=REALESRGANER_MODEL_PATH,
        # model=model,
        # tile=400,
        # tile_pad=10,
        # pre_pad=0,
        # half=False) # need to set False in CPU mode
        bg_upsampler = None

    restorer = GFPGANer(
        model_path=GFPGAN_MODEL_PATH,
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
