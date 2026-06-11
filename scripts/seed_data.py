"""
Seed sample data for SplitBill Smart demo.
Run after all migrations: python scripts/seed_data.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON = ROOT / 'venv' / 'Scripts' / 'python.exe'
if not PYTHON.exists():
    PYTHON = Path(sys.executable)


def run_shell(service_dir, code):
    result = subprocess.run(
        [str(PYTHON), 'manage.py', 'shell', '-c', code],
        cwd=ROOT / 'services' / service_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f'Seed failed in {service_dir}')
    if result.stdout.strip():
        print(result.stdout.strip())


print('Creating sample users...')
run_shell('user_service', """
from django.contrib.auth import get_user_model
User = get_user_model()
users = [
    ('andi', 'andi@splitbill.com', 'Andi', 'Pratama'),
    ('budi', 'budi@splitbill.com', 'Budi', 'Santoso'),
    ('citra', 'citra@splitbill.com', 'Citra', 'Wijaya'),
    ('dodi', 'dodi@splitbill.com', 'Dodi', 'Hakim'),
]
ids = {}
for u, e, fn, ln in users:
    user, created = User.objects.get_or_create(username=u, defaults={'email': e, 'first_name': fn, 'last_name': ln})
    if created:
        user.set_password('password123')
        user.save()
        print(f'  + {u} (id={user.id})')
    else:
        print(f'  = {u} (id={user.id}) exists')
    ids[u] = user.id
print('IDS', ids)
""")

print('\nCreating sample group...')
run_shell('group_service', """
from groups.models import Group, GroupMember
group, _ = Group.objects.get_or_create(name='Makan Siang Kantor', defaults={'created_by': 1})
for uid, name in [(1,'andi'),(2,'budi'),(3,'citra'),(4,'dodi')]:
    GroupMember.objects.get_or_create(group=group, user_id=uid, defaults={'username': name})
print(f'  Group "{group.name}" (id={group.id}) with 4 members')
""")

print('\nCreating sample bill...')
run_shell('bill_service', """
from bills.models import Bill, BillItem
bill, created = Bill.objects.get_or_create(
    title='Makan Siang Restoran', group_id=1,
    defaults={'created_by': 1, 'created_by_username': 'andi'}
)
if created:
    BillItem.objects.create(bill=bill, item_name='Menu Budi', price=30000, consumed_by_user_ids=[2])
    BillItem.objects.create(bill=bill, item_name='Menu Citra', price=40000, consumed_by_user_ids=[3])
    BillItem.objects.create(bill=bill, item_name='Menu Dodi', price=50000, consumed_by_user_ids=[4])
    bill.recalculate_total()
print(f'  Bill "{bill.title}" (id={bill.id}) total Rp{bill.total_amount}')
""")

print('\nCreating sample notifications...')
run_shell('notification_service', """
from notifications.models import Notification
for uid, name in [(2,'budi'),(3,'citra'),(4,'dodi')]:
    Notification.objects.get_or_create(
        user_id=uid,
        message='Tagihan baru "Makan Siang Restoran" - silakan cek settlement Anda.',
    )
    print(f'  Notification for user {name}')
""")

print('\nSample data seeding complete!')
print('Login: andi / password123 (or budi, citra, dodi)')
