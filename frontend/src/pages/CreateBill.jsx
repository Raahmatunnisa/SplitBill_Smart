import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { billAPI, groupAPI } from '../api/axios';

export default function CreateBill() {
  const [groups, setGroups] = useState([]);
  const [form, setForm] = useState({ group_id: '', title: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    groupAPI.list().then((res) => setGroups(res.data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await billAPI.create({
        group_id: parseInt(form.group_id, 10),
        title: form.title,
      });
      navigate(`/assign/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Gagal membuat tagihan');
    }
  };

  return (
    <div className="max-w-lg">
      <h2 className="text-2xl font-bold mb-6">Buat Tagihan Baru</h2>
      {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}
      <form onSubmit={handleSubmit} className="card space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Grup</label>
          <select
            className="input"
            value={form.group_id}
            onChange={(e) => setForm({ ...form, group_id: e.target.value })}
            required
          >
            <option value="">Pilih grup</option>
            {groups.map((g) => (
              <option key={g.id} value={g.id}>{g.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Judul Tagihan</label>
          <input
            className="input"
            placeholder="Makan siang restoran"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            required
          />
        </div>
        <button type="submit" className="btn-primary">Buat & Lanjut Assign Item</button>
      </form>
    </div>
  );
}
