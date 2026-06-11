import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { settlementAPI, formatRupiah } from '../api/axios';

export default function SettlementResult() {
  const { billId } = useParams();
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    settlementAPI.get(billId)
      .then((res) => setResult(res.data))
      .catch((err) => setError(err.response?.data?.error || 'Gagal menghitung settlement'))
      .finally(() => setLoading(false));
  }, [billId]);

  if (loading) return <p className="text-slate-500">Menghitung settlement...</p>;
  if (error) return <div className="bg-red-50 text-red-600 p-4 rounded-lg">{error}</div>;
  if (!result) return null;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Hasil Settlement</h2>
      <p className="text-slate-500 mb-6">{result.bill_title}</p>

      <div className="grid md:grid-cols-3 gap-4 mb-6">
        <div className="card">
          <p className="text-sm text-slate-500">Total Tagihan</p>
          <p className="text-xl font-bold">{formatRupiah(result.total_amount)}</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Yang Membayar</p>
          <p className="text-xl font-bold">{result.payer_username}</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Total Hutang</p>
          <p className="text-xl font-bold">{formatRupiah(result.total_debt)}</p>
        </div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-4">Rincian Pembayaran</h3>
        {result.settlements.length === 0 ? (
          <p className="text-slate-500 text-sm">Tidak ada hutang antar anggota.</p>
        ) : (
          <div className="space-y-3">
            {result.settlements.map((s, i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
                <div>
                  <p className="font-medium">{s.from_username}</p>
                  <p className="text-sm text-slate-500">bayar ke {s.to_username}</p>
                </div>
                <p className="text-lg font-bold text-emerald-700">{formatRupiah(s.amount)}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mt-6">
        <Link to="/dashboard" className="btn-secondary">Kembali ke Dashboard</Link>
      </div>
    </div>
  );
}
