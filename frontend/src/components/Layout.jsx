import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/groups', label: 'Grup' },
  { to: '/bills/create', label: 'Buat Tagihan' },
  { to: '/receipt', label: 'Upload Struk' },
  { to: '/notifications', label: 'Notifikasi' },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-primary-700 text-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">SplitBill Smart</h1>
            <p className="text-primary-100 text-sm">Bagi tagihan dengan mudah</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm hidden sm:block">Halo, {user?.username}</span>
            <button onClick={handleLogout} className="text-sm bg-white/20 hover:bg-white/30 px-3 py-1 rounded-lg">
              Logout
            </button>
          </div>
        </div>
        <nav className="bg-primary-800">
          <div className="max-w-6xl mx-auto px-4 flex gap-1 overflow-x-auto">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `px-4 py-2 text-sm whitespace-nowrap ${isActive ? 'bg-primary-900 text-white' : 'text-primary-100 hover:bg-primary-900/50'}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </nav>
      </header>
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
