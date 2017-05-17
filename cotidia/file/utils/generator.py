import io

from PIL import Image

from reportlab.pdfgen import canvas


def generate_pdf_file(content="Test PDF."):
    """Return a PDF file instance with given content."""

    # Create a file buffer to write the PDF to.
    _file = io.BytesIO()

    # Generate PDF
    pdf = canvas.Canvas(_file)
    pdf.drawString(100, 100, content)
    pdf.showPage()
    pdf.save()

    # Name the file
    _file.name = "test.pdf"
    _file.seek(0)

    return _file


def generate_image_file(file_type="PNG", size=(100, 100)):
    """Return an image file instance of given type and size.

    Accepted file types are: JPEG, PNG, BMP
    """

    if file_type not in ['JPEG', 'PNG', 'BMP']:
        raise Exception("File type {0} is not accepted.".format(file_type))

    _file = io.BytesIO()
    image = Image.new('RGBA', size=size, color=(155, 0, 0))
    image.save(_file, file_type)
    _file.name = 'test.{0}'.format(file_type)
    _file.seek(0)
    return _file


def generate_text_file(content="Test content."):
    """Return a text file instance with given content."""

    # Create a file buffer to write the text to.
    _file = io.StringIO()

    _file.write(content)

    # Name the file
    _file.name = "test.txt"
    _file.seek(0)

    return _file
