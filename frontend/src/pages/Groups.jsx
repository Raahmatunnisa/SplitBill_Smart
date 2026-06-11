import { useEffect, useState } from 'react';
import { groupAPI } from '../api/axios';

export default function Groups() {
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [members, setMembers] = useState([]);
  const [newGroupName, setNewGroupName] = useState('');
  const [newMember, setNewMember] = useState({ user_id: '', username: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadGroups = async () => {
    const res = await groupAPI.list();
    setGroups(res.data);
  };

  useEffect(() => {
    loadGroups();
  }, []);

  const loadMembers = async (groupId) => {
    setSelectedGroup(groupId);
    const res = await groupAPI.members(groupId);
    setMembers(res.data);
  };

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await groupAPI.create({ name: newGroupName });
      setNewGroupName('');
      setMessage('Grup berhasil dibuat');
      loadGroups();
    } catch (err) {
      setError(err.response?.data?.error || 'Gagal membuat grup');
    }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await groupAPI.addMember(selectedGroup, {
        user_id: parseInt(newMember.user_id, 10),
        username: newMember.username,
      });
      setNewMember({ user_id: '', username: '' });
      setMessage('Anggota berhasil ditambahkan');
      loadMembers(selectedGroup);
    } catch (err) {
      setError(err.response?.data?.error || 'Gagal menambah anggota');
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Manajemen Grup</h2>
      {message && <div className="bg-green-50 text-green-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}
      {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-4">Buat Grup Baru</h3>
          <form onSubmit={handleCreateGroup} className="flex gap-2">
            <input
              className="input"
              placeholder="Nama grup"
              value={newGroupName}
              onChange={(e) => setNewGroupName(e.target.value)}
              required
            />
            <button type="submit" className="btn-primary whitespace-nowrap">Buat</button>
          </form>

          <h3 className="font-semibold mt-6 mb-3">Daftar Grup</h3>
          <div className="space-y-2">
            {groups.map((g) => (
              <button
                key={g.id}
                onClick={() => loadMembers(g.id)}
                className={`w-full text-left p-3 rounded-lg border transition ${
                  selectedGroup === g.id ? 'border-primary-500 bg-primary-50' : 'border-slate-200 hover:bg-slate-50'
                }`}
              >
                <p className="font-medium">{g.name}</p>
                <p className="text-sm text-slate-500">{g.member_count} anggota</p>
              </button>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 className="font-semibold mb-4">Anggota Grup</h3>
          {!selectedGroup ? (
            <p className="text-slate-500 text-sm">Pilih grup untuk melihat anggota</p>
          ) : (
            <>
              <ul className="space-y-2 mb-4">
                {members.map((m) => (
                  <li key={m.id} className="p-2 bg-slate-50 rounded-lg flex justify-between">
                    <span>{m.username || `User #${m.user_id}`}</span>
                    <span className="text-sm text-slate-400">ID: {m.user_id}</span>
                  </li>
                ))}
              </ul>
              <form onSubmit={handleAddMember} className="space-y-2 border-t pt-4">
                <p className="text-sm font-medium">Tambah Anggota</p>
                <input
                  className="input"
                  placeholder="User ID"
                  type="number"
                  value={newMember.user_id}
                  onChange={(e) => setNewMember({ ...newMember, user_id: e.target.value })}
                  required
                />
                <input
                  className="input"
                  placeholder="Username (opsional)"
                  value={newMember.username}
                  onChange={(e) => setNewMember({ ...newMember, username: e.target.value })}
                />
                <button type="submit" className="btn-primary">Tambah</button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
