import git, os
from datetime import datetime
def pushByGit():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    current_path = os.getcwd()  # 获取当前工作目录
    project_path = os.path.dirname(current_path)  # 获取上一级目录
    # 获取当前仓库
    repo = git.Repo(project_path)

    # 检查是否有未提交的更改
    if repo.is_dirty(untracked_files=True):
        modified_files = [item.a_path for item in repo.index.diff(None)]  # 获取已修改的文件
        untracked_files = repo.untracked_files  # 获取未跟踪的文件（新文件）
        deleted_files = [item.a_path for item in repo.index.diff(None) if item.deleted_file]  # 获取已删除的文件
        original_list = modified_files + deleted_files
        list = list(dict.fromkeys(original_list))
        print("已修改文件:", list)
        # 添加所有更改（包括新文件和删除的文件）
        repo.git.add(A=True)  # 等同于 `git add .`
        # 提交更改
        commit_message = now+"使用python脚本更新"
        repo.index.commit(commit_message)
        # 推送更改到远程仓库
        repo.git.push("origin", "main")  # 或 "main"
        print("🚀 已推送到远程仓库")
        return list
    else:
        print("✅ 没有需要提交的更改")
