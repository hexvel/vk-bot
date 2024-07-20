from io import BytesIO
from urllib.request import urlopen

import matplotlib.pyplot as plt
import numpy as np
import qrcode
from PIL import Image


class QRCode:
    def __init__(
        self, text, background_image_path=None, alpha=0.4, with_background=True
    ):
        """
        Initializes a new instance of the QRCodeWithBackground class.

        Args:
            text (str): The text to be encoded in the QR code.
            background_image_path (str, optional): The path to the background image file. Defaults to None.
            alpha (float, optional): The transparency level of the QR code overlay on the background image. Defaults to 0.4.
            with_background (bool, optional): Whether to use a background image. Defaults to True.

        Raises:
            FileNotFoundError: If the background_image_path is provided but the file does not exist.

        Returns:
            None
        """
        self.text = text
        self.alpha = alpha
        self.with_background = with_background
        self.qr_image = None
        self.background_image = None
        self.qr_array = None
        self.background_array = None
        self.result_image = None
        self.bytes_io = BytesIO()

        if self.with_background and background_image_path:
            self.background_image = Image.open(
                background_image_path.startswith("http")
                and urlopen(background_image_path)
                or background_image_path
            ).convert("RGBA")

    def generate_qr_code(self):
        """
        Generates a QR code based on the text provided.

        Does the following:
        - Initializes a QRCode object with specific parameters.
        - Adds the provided text to the QRCode.
        - Makes the QRCode fit the data.
        - Creates the QR image with specified fill and background colors.

        Returns:
        None
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.text)
        qr.make(fit=True)
        self.qr_image = qr.make_image(fill_color="black", back_color="white").convert(
            "RGBA"
        )

    def resize_background_image(self):
        """
        Resizes the background image to match the size of the QR image.

        This function checks if a background image is available. If it is, it resizes the
        background image to match the size of the QR image. The resizing is done using the
        Lanczos filter, which is a high-quality filter that is suitable for downsampling.

        Parameters:
            self (QRCodeWithBackground): The instance of the QRCodeWithBackground class.

        Returns:
            None
        """
        if self.background_image:
            self.background_image = self.background_image.resize(
                self.qr_image.size, Image.LANCZOS
            )

    def blend_images(self):
        """
        Blend the QR image with the background image if a background image is provided.

        This function checks if a background image is available. If it is, it blends the QR image with the background image.
        The blending is done by iterating over each pixel of the QR image and checking if the pixel is transparent.
        If the pixel is transparent and the RGB values of the pixel are [0, 0, 0], the pixel is replaced with the corresponding pixel from the background image.
        If the pixel is transparent but the RGB values are not [0, 0, 0], the pixel is set to [255, 255, 255, 0].
        If no background image is provided, the QR image is converted to RGB format.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        if self.with_background and self.background_image:
            self.qr_array = np.array(self.qr_image)
            self.background_array = np.array(self.background_image)

            result_image = np.zeros_like(self.qr_array)

            for y in range(self.qr_array.shape[0]):
                for x in range(self.qr_array.shape[1]):
                    if self.qr_array[y, x, 3] > 0:
                        if (self.qr_array[y, x, :3] == [0, 0, 0]).all():
                            result_image[y, x] = self.background_array[y, x]
                        else:
                            result_image[y, x] = [255, 255, 255, 0]

            self.result_image = Image.fromarray(result_image)
        else:
            self.result_image = self.qr_image.convert("RGB")

    def save_image(self, output_path: str | None = None):
        """
        Save the result image to the specified output path.

        Args:
            output_path (str): The path where the image will be saved.

        Returns:
            BytesIO: The BytesIO object containing the saved image.
        """
        self.bytes_io.seek(0)
        self.result_image.save(self.bytes_io, format="PNG")

        return self.bytes_io

    def show_image(self):
        """
        Display the result image using matplotlib.pyplot.
        """
        plt.imshow(self.result_image)
        plt.axis("off")
        plt.show()
