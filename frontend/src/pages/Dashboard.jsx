import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { billAPI, groupAPI, settlementAPI, formatRupiah } from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({ groups: 0, bills: 0, totalDebt: 0 });
  const [recentBills, setRecentBills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [groupsRes, billsRes] = await Promise.all([groupAPI.list(), billAPI.list()]);
        const groups = groupsRes.data;
        const bills = billsRes.data;

        let totalDebt = 0;
        for (const bill of bills.slice(0, 5)) {
          try {
            const settlement = await settlementAPI.get(bill.id);
            const myDebt = settlement.data.per_user_debt?.find((d) => d.user_id === user.id);
            if (myDebt) totalDebt += myDebt.debt;
          } catch {
            /* ignore */
          }
        }

        setStats({ groups: groups.length, bills: bills.length, totalDebt });
        setRecentBills(bills.slice(0, 5));
      } catch {
        /* ignore */
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user.id]);

  if (loading) return <p className="text-slate-500">Memuat dashboard...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="card bg-primary-50 border-primary-200">
          <p className="text-sm text-primary-600 font-medium">Total Grup</p>
          <p className="text-3xl font-bold text-primary-900">{stats.groups}</p>
        </div>
        <div className="card bg-emerald-50 border-emerald-200">
          <p className="text-sm text-emerald-600 font-medium">Total Tagihan</p>
          <p className="text-3xl font-bold text-emerald-900">{stats.bills}</p>
        </div>
        <div className="card bg-amber-50 border-amber-200">
          <p className="text-sm text-amber-600 font-medium">Total Hutang Anda</p>
          <p className="text-2xl font-bold text-amber-900">{formatRupiah(stats.totalDebt)}</p>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Tagihan Terbaru</h3>
          <Link to="/bills/create" className="btn-primary text-sm">Buat Tagihan</Link>
        </div>
        {recentBills.length === 0 ? (
          <p className="text-slate-500 text-sm">Belum ada tagihan.</p>
        ) : (
          <div className="space-y-3">
            {recentBills.map((bill) => (
              <div key={bill.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                <div>
                  <p className="font-medium">{bill.title}</p>
                  <p className="text-sm text-slate-500">Grup #{bill.group_id}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold">{formatRupiah(bill.total_amount)}</p>
                  <Link to={`/settlement/${bill.id}`} className="text-sm text-primary-600 hover:underline">
                    Lihat Settlement
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
