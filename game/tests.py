import git,os
import os

current_path = os.getcwd()  # 获取当前工作目录
project_path = os.path.dirname(current_path)  # 获取上一级目录

# 获取当前仓库
repo = git.Repo(project_path)

# 检查是否有未提交的更改
if repo.is_dirty(untracked_files=True):
    # # 获取已修改的文件
    # modified_files = [item.a_path for item in repo.index.diff(None)]
    #
    # # 获取未跟踪的文件（新文件）
    # untracked_files = repo.untracked_files
    #
    # # 获取已删除的文件
    # deleted_files = [item.a_path for item in repo.index.diff(None) if item.deleted_file]
    #
    # print("已修改文件:", modified_files)
    # print("未跟踪文件:", untracked_files)
    # print("已删除文件:", deleted_files)

    # 添加所有更改（包括新文件和删除的文件）
    repo.git.add(A=True)  # 等同于 `git add .`

    # 提交更改
    commit_message = "Auto-commit: 更新了文件"
    repo.index.commit(commit_message)
    print("✅ 提交成功:", commit_message)
    # 推送更改到远程仓库
    repo.git.push("origin", "main")  # 或 "main"
    print("🚀 已推送到远程仓库")
else:
    print("✅ 没有需要提交的更改")