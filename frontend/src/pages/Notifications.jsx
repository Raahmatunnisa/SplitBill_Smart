import { useEffect, useState } from 'react';
import { notificationAPI } from '../api/axios';

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    notificationAPI.list()
      .then((res) => setNotifications(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-slate-500">Memuat notifikasi...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Notifikasi</h2>
      <div className="card">
        {notifications.length === 0 ? (
          <p className="text-slate-500 text-sm">Belum ada notifikasi.</p>
        ) : (
          <div className="space-y-3">
            {notifications.map((n) => (
              <div key={n.id} className="p-4 bg-slate-50 rounded-lg border-l-4 border-primary-500">
                <p>{n.message}</p>
                <p className="text-xs text-slate-400 mt-1">
                  {new Date(n.created_at).toLocaleString('id-ID')}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
