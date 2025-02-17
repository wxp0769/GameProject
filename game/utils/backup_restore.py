import os
import datetime
from django.conf import settings

# 备份目录
BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backup')
os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_database():
    """
    备份 MySQL 数据库到 SQL 文件
    """
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']
    print(db_name, db_user, db_password, db_host,db_port)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'backup_{timestamp}.sql')

    # 执行 mysqldump 备份数据库
    command = f"mysql -h {db_host} -P {db_port} -u {db_user} -p {db_password} {db_name} > {backup_file}"
    print(os.system(command))

    if os.system(command) == 1:
        return f"数据库备份成功: {backup_file}"
    else:
        return "数据库备份失败"


def restore_database(backup_file):
    """
    从 SQL 文件恢复数据库
    """
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    backup_path = os.path.join(BACKUP_DIR, backup_file)
    print(backup_path, backup_file)

    if not os.path.exists(backup_path):
        return "Backup file not found"

    # 执行 mysql 进行数据库恢复
    command = f"mysql -h {db_host} -P {db_port} -u {db_user} -p'{db_password}' {db_name} < {backup_path}"

    if os.system(command) == 1:
        return f"数据库恢复成功: {backup_file}"
    else:
        return "数据库恢复失败"
