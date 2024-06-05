from PIL import Image
import piexif

def add_360_metadata(image_path):
    """
    Add 360-degree metadata to the given image.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        None
    """
    # Load the image
    image = Image.open(image_path)

    # Create a dictionary for the 360 metadata
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

    # Add the 360 metadata tags
    exif_dict["0th"][piexif.ImageIFD.Make] = "RICOH"
    exif_dict["0th"][piexif.ImageIFD.Model] = "RICOH THETA S"
    exif_dict["0th"][piexif.ImageIFD.Software] = "GIMP 2.10.22"
    exif_dict["0th"][piexif.ImageIFD.ImageWidth] = image.width
    exif_dict["0th"][piexif.ImageIFD.ImageLength] = image.height

    # Add the 360 metadata to the image
    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path, "jpeg", exif=exif_bytes)