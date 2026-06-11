import re
from django.db import models


class ReceiptUpload(models.Model):
    image = models.ImageField(upload_to='receipts/')
    raw_text = models.TextField(blank=True, default='')
    parsed_items = models.JSONField(default=list)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Receipt {self.id}'


def parse_receipt_text(text):
    """Parse OCR text into items with name and price."""
    items = []
    lines = text.strip().split('\n')

    price_patterns = [
        re.compile(r'^(.+?)\s+Rp\s*([\d.,]+)\s*$', re.IGNORECASE),
        re.compile(r'^(.+?)\s+([\d.,]+)\s*$'),
        re.compile(r'^(.+?)\s*[\-:]\s*Rp?\s*([\d.,]+)\s*$', re.IGNORECASE),
    ]

    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line.lower() for kw in ['total', 'subtotal', 'tax', 'pajak', 'bayar', 'tunai', 'kembali']):
            continue

        for pattern in price_patterns:
            match = pattern.match(line)
            if match:
                name = match.group(1).strip(' .-')
                price_str = match.group(2).replace('.', '').replace(',', '')
                try:
                    price = int(float(price_str))
                    if price > 0 and name:
                        items.append({'name': name, 'price': price})
                except ValueError:
                    pass
                break

    return items


def get_demo_items():
    return [
        {'name': 'Nasi Goreng', 'price': 25000},
        {'name': 'Es Teh', 'price': 10000},
        {'name': 'Ayam Bakar', 'price': 35000},
        {'name': 'Es Jeruk', 'price': 12000},
    ]
