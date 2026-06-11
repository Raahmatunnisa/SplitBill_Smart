import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { billAPI, groupAPI, formatRupiah } from '../api/axios';

export default function AssignItems() {
  const { billId } = useParams();
  const navigate = useNavigate();
  const [bill, setBill] = useState(null);
  const [members, setMembers] = useState([]);
  const [ocrItems, setOcrItems] = useState([]);
  const [assignments, setAssignments] = useState({});
  const [manualItem, setManualItem] = useState({ item_name: '', price: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      const billRes = await billAPI.get(billId);
      setBill(billRes.data);
      const membersRes = await groupAPI.members(billRes.data.group_id);
      setMembers(membersRes.data);

      const stored = sessionStorage.getItem('ocr_items');
      if (stored) {
        const items = JSON.parse(stored);
        setOcrItems(items);
        const initial = {};
        items.forEach((_, i) => { initial[i] = []; });
        setAssignments(initial);
      }
    };
    load();
  }, [billId]);

  const toggleMember = (itemIndex, userId) => {
    setAssignments((prev) => {
      const current = prev[itemIndex] || [];
      const updated = current.includes(userId)
        ? current.filter((id) => id !== userId)
        : [...current, userId];
      return { ...prev, [itemIndex]: updated };
    });
  };

  const submitOcrItems = async () => {
    setError('');
    try {
      for (let i = 0; i < ocrItems.length; i++) {
        const item = ocrItems[i];
        await billAPI.addItem(billId, {
          item_name: item.name,
          price: item.price,
          consumed_by_user_ids: assignments[i] || [],
        });
      }
      sessionStorage.removeItem('ocr_items');
      navigate(`/settlement/${billId}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Gagal menambah item');
    }
  };

  const addManualItem = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await billAPI.addItem(billId, {
        item_name: manualItem.item_name,
        price: parseFloat(manualItem.price),
        consumed_by_user_ids: [],
      });
      const billRes = await billAPI.get(billId);
      setBill(billRes.data);
      setManualItem({ item_name: '', price: '' });
    } catch (err) {
      setError(err.response?.data?.error || 'Gagal menambah item');
    }
  };

  if (!bill) return <p>Memuat...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Assign Item ke Anggota</h2>
      <p className="text-slate-500 mb-6">Tagihan: {bill.title}</p>
      {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}

      {ocrItems.length > 0 && (
        <div className="card mb-6">
          <h3 className="font-semibold mb-4">Item dari OCR</h3>
          <div className="space-y-4">
            {ocrItems.map((item, index) => (
              <div key={index} className="p-4 bg-slate-50 rounded-lg">
                <div className="flex justify-between mb-3">
                  <span className="font-medium">{item.name}</span>
                  <span>{formatRupiah(item.price)}</span>
                </div>
                <p className="text-sm text-slate-500 mb-2">Pilih yang mengonsumsi:</p>
                <div className="flex flex-wrap gap-2">
                  {members.map((m) => (
                    <label key={m.user_id} className="flex items-center gap-1 text-sm bg-white px-2 py-1 rounded border">
                      <input
                        type="checkbox"
                        checked={(assignments[index] || []).includes(m.user_id)}
                        onChange={() => toggleMember(index, m.user_id)}
                      />
                      {m.username || `User ${m.user_id}`}
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <button onClick={submitOcrItems} className="btn-primary mt-4">
            Simpan & Hitung Settlement
          </button>
        </div>
      )}

      <div className="card mb-6">
        <h3 className="font-semibold mb-4">Tambah Item Manual</h3>
        <form onSubmit={addManualItem} className="flex flex-wrap gap-2">
          <input
            className="input flex-1 min-w-[150px]"
            placeholder="Nama item"
            value={manualItem.item_name}
            onChange={(e) => setManualItem({ ...manualItem, item_name: e.target.value })}
            required
          />
          <input
            className="input w-32"
            placeholder="Harga"
            type="number"
            value={manualItem.price}
            onChange={(e) => setManualItem({ ...manualItem, price: e.target.value })}
            required
          />
          <button type="submit" className="btn-secondary">Tambah</button>
        </form>
      </div>

      {bill.items?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold mb-4">Item Tagihan ({formatRupiah(bill.total_amount)})</h3>
          <ul className="space-y-2">
            {bill.items.map((item) => (
              <li key={item.id} className="flex justify-between p-2 bg-slate-50 rounded">
                <span>{item.item_name}</span>
                <span>{formatRupiah(item.price)}</span>
              </li>
            ))}
          </ul>
          <button onClick={() => navigate(`/settlement/${billId}`)} className="btn-primary mt-4">
            Lihat Settlement
          </button>
        </div>
      )}
    </div>
  );
}
