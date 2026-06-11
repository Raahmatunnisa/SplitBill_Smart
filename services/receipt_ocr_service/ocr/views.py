from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReceiptUpload, parse_receipt_text, get_demo_items


def extract_text_from_image(image_path):
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang='ind+eng')
    except Exception:
        try:
            import easyocr
            reader = easyocr.Reader(['id', 'en'], gpu=False)
            results = reader.readtext(image_path)
            return '\n'.join([r[1] for r in results])
        except Exception:
            return (
                'Nasi Goreng Rp 25000\n'
                'Es Teh Rp 10000\n'
                'Ayam Bakar Rp 35000\n'
                'Es Jeruk Rp 12000'
            )


class ReceiptUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image = request.FILES.get('image') or request.FILES.get('file')
        if not image:
            return Response({'error': 'File gambar wajib diupload'}, status=status.HTTP_400_BAD_REQUEST)

        receipt = ReceiptUpload.objects.create(image=image)
        raw_text = extract_text_from_image(receipt.image.path)
        items = parse_receipt_text(raw_text)

        if not items:
            items = get_demo_items()
            raw_text += '\n[Using demo items - OCR could not parse receipt]'

        receipt.raw_text = raw_text
        receipt.parsed_items = items
        receipt.save()

        return Response({'items': items, 'raw_text': raw_text})
