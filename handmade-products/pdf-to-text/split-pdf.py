import os
import cv2
from pdf2image import convert_from_path

def split_pdf(pdf_path, directory):
    images = convert_from_path(pdf_path, output_folder=directory)
    return images

split_pdf('pdf_file.pdf', 'dataset/algorithm-to-live-by')
