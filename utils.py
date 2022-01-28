import os
import cv2
from torch.hub import download_url_to_file
from basicsr.utils import imwrite
from gfpgan import GFPGANer


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_face_model(path="model/face_model/GFPGANCleanv1-NoCE-C2.pth"):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        download_url_to_file("https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth",
                             path)


def restore_image(img_path: str,
                  output_dir: str = "static/restored",
                  bg_upsampler_model: str = "realesrgan",
                  model_path: str = "model/face_model/GFPGANCleanv1-NoCE-C2.pth",
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