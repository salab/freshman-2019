from __future__ import annotations
import cv2
import numpy
from .image import Image


class GrayImage(Image):
    """
    グレースケール画像

    SuperClass
    ----------
    Image
    """
    @classmethod
    def nChannel(cls) -> int:
        return 2

    def toGray(self) -> GrayImage:
        """
        グレースケール画像へ変換
        """
        return self

    def resize(self, scale: float) -> GrayImage:
        """
        拡大・縮小

        Parameters
        ----------
        scale : float
            拡大率
        """
        return super().resize(scale)

    def binarize(self) -> GrayImage:
        """
        ２値化
        """
        self.data = cv2.adaptiveThreshold(
            src=self.data,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=11,
            C=2
        )
        return self

    def morphology(self, method: int, kernelSize: int) -> GrayImage:
        """
        モルフォロジー変換
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        """
        shape = (kernelSize) * 2
        kernel = numpy.ones(shape,
                            dtype=numpy.uint8)
        self.data = cv2.morphologyEx(
            src=self.data,
            op=method,
            kernel=kernel
        )
        return self

    def morph_erode(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_ERODE, kernelSize)

    def morph_dilate(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_DILATE, kernelSize)

    def morph_open(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_OPEN, kernelSize)

    def morph_close(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_CLOSE, kernelSize)

    def blur_median(self, kernelSize: int) -> GrayImage:
        """
        中央値フィルタ
        kernelSizeは奇数とすること.
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_filtering/py_filtering.html#id6
        """

        assert (kernelSize % 2) == 1, """
        kernelSizeは奇数でなければなりません.(given= %d) """ % kernelSize

        self.data = cv2.medianBlur(self.data, kernelSize)
        return self

    def normalize_clahe(self, clipLimit: float, gridSize: int) -> GrayImage:
        """
        ヒストグラム平均化(CLAHE法)
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.html#clahe-contrast-limited-adaptive-histogram-equalization
        """
        tile = (gridSize) * 2
        normalizer = cv2.createCLAHE(clipLimit=clipLimit,
                                     tileGridSize=tile)
        self.data = normalizer.apply(self.data)
        return self