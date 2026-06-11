import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { receiptAPI } from '../api/axios';

export default function UploadReceipt() {
  const [file, setFile] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      const res = await receiptAPI.upload(file);
      setItems(res.data.items);
      sessionStorage.setItem('ocr_items', JSON.stringify(res.data.items));
    } catch (err) {
      setError(err.response?.data?.error || 'Upload gagal');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Upload Foto Struk</h2>
      {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}

      <div className="card max-w-lg mb-6">
        <form onSubmit={handleUpload} className="space-y-4">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm"
          />
          <button type="submit" disabled={!file || loading} className="btn-primary">
            {loading ? 'Memproses OCR...' : 'Upload & Scan'}
          </button>
        </form>
        <p className="text-xs text-slate-500 mt-3">
          OCR menggunakan pytesseract/easyocr. Jika tidak terinstall, sistem akan menggunakan data demo.
        </p>
      </div>

      {items.length > 0 && (
        <div className="card">
          <h3 className="font-semibold mb-4">Hasil OCR</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2">Item</th>
                <th className="text-right py-2">Harga</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, i) => (
                <tr key={i} className="border-b border-slate-100">
                  <td className="py-2">{item.name}</td>
                  <td className="py-2 text-right">Rp {item.price.toLocaleString('id-ID')}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button
            onClick={() => navigate('/bills/create')}
            className="btn-primary mt-4"
          >
            Lanjut Buat Tagihan
          </button>
        </div>
      )}
    </div>
  );
}
