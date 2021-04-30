from PIL import Image
import numpy as np
import sys
import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()

def crop(img, i, j, h, w):
    """Crop the given PIL Image.

    Args:
        img (PIL Image): Image to be cropped.
        i: Upper pixel coordinate.
        j: Left pixel coordinate.
        h: Height of the cropped image.
        w: Width of the cropped image.

    Returns:
        PIL Image: Cropped image.
    """
    return img.crop((j, i, j + w, i + h))

def resize(img, size, interpolation=Image.BILINEAR):
    """Resize the input PIL Image to the given size.

    Args:
        img (PIL Image): Image to be resized.
        size (sequence or int): Desired output size. If size is a sequence like
            (h, w), the output size will be matched to this. If size is an int,
            the smaller edge of the image will be matched to this number maintaing
            the aspect ratio. i.e, if height > width, then image will be rescaled to
            (size * height / width, size)
        interpolation (int, optional): Desired interpolation. Default is
            ``PIL.Image.BILINEAR``

    Returns:
        PIL Image: Resized image.
    """
    w, h = img.size
    if (w <= h and w == size) or (h <= w and h == size):
        return img
    if w < h:
        ow = size
        oh = int(size * h / w)
        return img.resize((ow, oh), interpolation)
    oh = size
    ow = int(size * w / h)
    return img.resize((ow, oh), interpolation)


def center_crop(img, output_size):
  w, h = img.size
  th, tw = output_size, output_size
  i = int(round((h - th) / 2.))
  j = int(round((w - tw) / 2.))
  PIL_img = crop(img, i, j, th, tw)
  return PIL_img

def normalize(image, mean, std):
  """Normalize a float tensor image with mean and standard deviation.
    This transform does not support PIL Image.
    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.
    Args:
        image (Tensor): Float tensor image of size (C, H, W) to be normalized.
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
    Returns:
        Tensor: Normalized Tensor image.
    """
  image = tf.transpose(image, [1, 2, 0])
  result = tf.divide(tf.subtract(image, mean), std)
  return tf.transpose(result, [2, 0, 1])
  

def to_tensor(image):
  """Convert a `numpy.ndarray`` to tensor.
    This function does not support torchscript.
    See :class:`~torchvision.transforms.ToTensor` for more details.
    Args:
        pic (numpy.ndarray): Image to be converted to tensor.
    Returns:
        Tensor: Converted image.
    """
  # put it from HWC to CHW format
  image = tf.convert_to_tensor(np.transpose(image, [2, 0, 1]), dtype=float)
  image = tf.divide(image, 255.0)
  return image


  
def transform_custom(image):
  image = resize(image, 320)
  image = center_crop(image, 320)
  image = to_tensor(image)
  image = normalize(image, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  return image




def pre_process(image_name, output_name):
  image = Image.open(image_name).convert('RGB')
  print("Resize starting")
  np_img = transform_custom(image)
  np_img = tf.expand_dims(np_img, axis=0)
  np.save(output_name, tf.keras.backend.get_value(np_img))
  print("Resizing done. Image dumped in {}.npy".format(output_name))

if __name__ == "__main__":
  image_name = sys.argv[1]
  output_name = "xray"
  pre_process(image_name, output_name)