import json
import os
from django.views.decorators.csrf import csrf_exempt
from .utils.backup_restore import backup_database, restore_database
from django.shortcuts import render, redirect, get_object_or_404
from game.utils.opai import interact_with_openrouter, interact_with_openai
from H5game import settings
from game import models
from .models import Game, Questions
from game.utils.pagination import Pagination
from game.utils.myforms import SiteModelForm, GameModelForm, QuestionsModelForm
from django.http import HttpResponse, JsonResponse
from game.utils.generate_html_page import *

# Create your views here.

def iframe_play(request, slug):
    # 可以通过 context 传递数据到模板
    game_obj = models.Game.objects.filter(slug=slug).first()
    context = {
        "game_obj": game_obj,
    }
    return render(request, 'play.html', context)


def index(request):
    game_obj = models.Game.objects.filter(recommend=3, is_checked=1).first()
    if game_obj is None:
        game_obj = models.Game.objects.all().first()
    recommend_gamelist_L, recommend_gamelist_R = get_recommend_games()
    newgames = new_games()
    site = siteinfo()
    top_menus = menus()
    QandA = models.Questions.objects.filter(game_id=game_obj.nid).order_by('-nid')[:8]
    context = {
        "game_obj": game_obj,
        "recommend_gamelist_L": recommend_gamelist_L,
        "recommend_gamelist_R": recommend_gamelist_R,
        "newgames": newgames,
        "top_menus": top_menus,
        "site": site,
        "QandA": QandA,
        "index": 1,
    }
    return render(request, "game.html", context)


def game(request, slug):
    game_obj = models.Game.objects.filter(slug=slug).first()
    recommend_gamelist_L, recommend_gamelist_R = get_recommend_games()
    newgames = new_games()
    site = siteinfo()
    top_menus = menus()
    QandA = models.Questions.objects.filter(game_id=game_obj.nid).order_by('-nid')[:8]
    context = {
        "game_obj": game_obj,
        "site": site,
        "recommend_gamelist_L": recommend_gamelist_L,
        "recommend_gamelist_R": recommend_gamelist_R,
        "newgames": newgames,
        "top_menus": top_menus,
        "QandA": QandA,
        "index": 2,
    }
    return render(request, "game.html", context)

def gameList(request):
    game_list = models.Game.objects.all().filter(is_checked=1).order_by('-update_time')
    page_object = Pagination(request, game_list, page_size=48)
    site = siteinfo()
    top_menus = menus()
    context = {
        "game_list": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 页码
        "site": site,
        "top_menus": top_menus,
        "index": 3,
    }
    return render(request, "list.html", context)

def generate_allpage_html(request):
    generate_index_html(request)
    generate_allgame_html(request)
    gameList_html(request)
    aboutus_html(request)
    copyright_html(request)
    contactus_html(request)
    privacypolicy_html(request)
    termofuse_html(request)
    generate_sitemap(request)
    return HttpResponse(f"全站静态 HTML 文件已生成")


def aboutus(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "About Us"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus
    }
    return render(request, "aboutus.html", context)

def copyright(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Copyright"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus
    }
    return render(request, "aboutus.html", context)
def contactus(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Contact Us"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus
    }
    return render(request, "aboutus.html", context)




def privacypolicy(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Privacy Policy"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus
    }
    return render(request, "aboutus.html", context)

def termofuse(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Term Of Use"
    top_menus = menus()
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus,
    }
    return render(request, "aboutus.html", context)

def guanli(request):
    return render(request, 'admin/admin.html')

def site_manage(request,site_id):
    return render(request, 'admin/site_manage.html')


def create_Site(request):
    if request.method == 'POST':
        form = SiteModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 将表单数据保存到数据库
            return HttpResponse('OK')
    else:
        form = SiteModelForm()  # 初始化空表单

    return render(request, 'admin/edit_site.html', {'form': form})

def site_list(request):
    sites = models.Site.objects.all()
    return render(request, 'admin/site_list.html', {'sites': sites})

def edit_Site(request,site_id):
    site = models.Site.objects.filter(nid=site_id).first()
    if request.method == 'POST':
        form = SiteModelForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()  # 保存数据到数据库
            return redirect('/site_list')  # 重定向到当前页面
    else:
        form = SiteModelForm(instance=site)  # 将站点信息加载到表单

    return render(request, 'admin/edit_site.html', {'site': site, 'form': form})


def game_list(request):  # 管理未审核的游戏
    """按标题搜索游戏（模糊匹配）"""
    query = request.GET.get("query", "").strip()  # 获取搜索关键字
    if query:
        game_list = Game.objects.filter(title__icontains=query)  # 模糊搜索
        page_object = Pagination(request, game_list, page_size=15)
    else:
        game_list = Game.objects.filter(is_checked=False).order_by('-update_time')  # 显示所有游戏
        page_object = Pagination(request, game_list, page_size=15)
    qty = Game.objects.filter(is_checked=False).count()  # 未审核数量
    qty_ok = Game.objects.filter(is_checked=True).count()  # 已审核数量
    context = {
        "game_list": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 页码
        "query": query,  # 让搜索框回显
        "qty": qty,
        "qty_ok": qty_ok
    }

    return render(request, 'admin/game_list.html', context)

def game_list_checked(request):  # 管理已审核的游戏
    game_list = models.Game.objects.filter(is_checked=True).order_by('-update_time')
    page_object = Pagination(request, game_list, page_size=15)
    qty = Game.objects.filter(is_checked=False).count()  # 未审核数量
    qty_ok = len(game_list)
    context = {
        "game_list": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 页码
        "qty": qty,
        'qty_ok': qty_ok,  # 页码已审核的游戏数量
    }

    return render(request, 'admin/game_list.html', context)

def add_game(request):
    if request.method == 'POST':
        game_form = GameModelForm(request.POST, request.FILES)
        question_form = QuestionsModelForm(request.POST)
        if game_form.is_valid() and question_form.is_valid():
            # 保存游戏
            game = game_form.save()
            # 保存问题并关联到游戏
            question = question_form.save(commit=False)
            question.game = game  # 关联游戏
            question.save()
            return redirect('/game_list')  # 替换为成功后的重定向URL
    else:
        game_form = GameModelForm()
        question_form = QuestionsModelForm()

    return render(request, 'admin/add_game.html', {'game_form': game_form, 'question_form': question_form})


def del_game(request, game_id):
    try:
        game = models.Game.objects.get(nid=game_id)
        game.delete()
        return redirect('/game_list')
    except models.Game.DoesNotExist:
        return HttpResponse("游戏不存在")


def edit_game(request, game_id):
    game = get_object_or_404(Game, nid=game_id)  # 获取要编辑的游戏
    game.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    questions = Questions.objects.filter(game=game)  # 获取与游戏相关的问题

    if request.method == 'POST':
        game_form = GameModelForm(request.POST, request.FILES, instance=game)

        if game_form.is_valid():
            game_form.save()  # 保存游戏数据
            generate_game_html(request, game_id)  # 生成html
            # 更新问题
            for question in questions:
                question_text = request.POST.get(f'question_{question.nid}')
                answer_text = request.POST.get(f'answer_{question.nid}')

                # 只更新非空的问题
                if question_text and answer_text:
                    question.question = question_text
                    question.answer = answer_text
                    question.save()
                else:
                    # 如果问题为空，可以选择删除或忽略
                    question.delete()  # 删除空白问题记录

            return redirect('game_list')  # 跳转到游戏列表页
    else:
        game_form = GameModelForm(instance=game)  # 加载游戏数据到表单

    return render(request, 'admin/edit_game.html', {
        'game_form': game_form,
        'questions': questions,  # 传递问题列表到模板
    })


def generate_QandA(request, game_id):
    game = Game.objects.get(nid=game_id)
    print(game.title)
    prompts = """
    编程语言：python
    用英文生成8个关于Racing Limits游戏的问题及答案，把每个问题及其答案组成一个字典,字典的键是question和answer，最后再把所有字典作为元素放到一个json中,
    格式如下：
    [
    {'question':'','answer':''},
    {'question':'','answer':''},
    {'question':'','answer':''},
    ......
    ]
        """
    # "用英文生成8个关于" + game.title + "游戏的问题及答案，把每个问题赋值给Question,把每个答案赋值给Answer，把每个Question和对应的Answer组成一个字典，再把字典作为元素放到一个list中")

    # qas_str = interact_with_openrouter(prompts)
    # print(qas_str)
    # print(type(qas_str["choices"][0]["message"]["content"].split('[')[1].split(']')[0]),qas_str["choices"][0]["message"]["content"].split('[')[1].split(']')[0])
    # qas_str = '[' + qas_str["choices"][0]["message"]["content"].split('[')[1].split(']')[0] + ']'
    # print(type(qas_str),qas_str)
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # qas_list = json.loads(qas_str)
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # print(qas_list)
    resp = interact_with_openai(prompts)
    resp = json.loads(resp)
    qas_list = resp["choices"][0]["message"]["content"]
    qas_list = json.loads(qas_list)  # 返回一个 JSON 响应
    print(qas_list)
    print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    if qas_list:
        Questions.objects.filter(game_id=game.nid).delete()
        for qa in qas_list:
            Questions.objects.create(game_id=game.nid, question=qa["question"], answer=qa["answer"])
    return redirect('/game_list')  # 替换为成功后的重定向URL

def generate_whathow(request, game_id):
    game = Game.objects.get(nid=game_id)
    title = game.title
    prompts = f"""    
    1）用英文回答What is {title} game?字数限制在100words以内
    2)用英文回答how to play {title} game?字数限制在100words以内
    3)把第一个答案赋值给whatis,第二个答案赋值给howtoplay,然后组成一个json返回
    """
    # ai_res = interact_with_openrouter(prompts)["choices"][0]["message"]["content"]
    # game_info = ai_res.replace("```json","[").replace("```","]")
    # game_info=json.loads(game_info)
    resp = interact_with_openai(prompts)
    resp = json.loads(resp)
    ai_res = resp["choices"][0]["message"]["content"]
    game_info = "[" + ai_res + "]"
    print(type(ai_res), ai_res)
    game_info = json.loads(game_info)  # 返回一个 JSON 响应
    print(type(game_info), game_info)
    if game_info:
        game = Game.objects.get(nid=game_id)
        print(game_info)
        game.whatis = game_info[0]["whatis"]
        game.HowtoPlay = game_info[0]["howtoplay"]
        game.save()
    return redirect('/game_list')  # 替换为成功后的重定向URL


# ajax调用AI
def generate_whathow2(request):
    if request.method == 'POST':
        try:
            # 获取传递的参数
            title = request.POST.get('title', '')  # 获取 title 参数
            print(title)
            if title:
                # 这里可以根据传递的 title 值进行处理
                # 假设你处理了 title 并生成了 whathow 内容
                prompts = f"""    
                    1）用英文回答What is {title} game?字数限制在100words以内
                    2)用英文回答how to play {title} game?字数限制在100words以内
                    3)把第一个答案赋值给whatis,第二个答案赋值给howtoplay,然后组成一个json返回
                    """
                # ai_res = interact_with_openrouter(prompts)["choices"][0]["message"]["content"]
                # print(ai_res)
                # game_info = ai_res.replace("```json", "[").replace("```", "]")
                # game_info = json.loads(game_info)# 返回一个 JSON 响应
                resp = interact_with_openai(prompts)
                resp = json.loads(resp)
                ai_res = resp["choices"][0]["message"]["content"]
                game_info = "[" + ai_res + "]"
                print(type(ai_res), ai_res)
                game_info = json.loads(game_info)  # 返回一个 JSON 响应
                print(type(game_info), game_info)
                return JsonResponse(game_info[0])

            else:
                return JsonResponse({'error': 'No title provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


def generate_description(request):
    if request.method == 'POST':
        try:
            # 获取传递的参数
            description = request.POST.get('description', '')  # 获取 title 参数
            if description:
                # 这里可以根据传递的 title 值进行处理
                # 假设你处理了 title 并生成了 whathow 内容
                prompts = f"""    
                    1)把下面的英文重新组织一下，字符数控制在300以内，使之更有利于google SEO:
                    {description}
                    2)把返回的答案赋值给description,然后组成一个json返回
                    """
                print("------------------------------------------------------------------------------------")
                # ai_res = interact_with_openrouter(prompts)["choices"][0]["message"]["content"]
                # game_info = ai_res.replace("```json", "[").replace("```", "]")
                # game_info = json.loads(game_info)# 返回一个 JSON 响应
                resp = interact_with_openai(prompts)
                resp = json.loads(resp)
                ai_res = resp["choices"][0]["message"]["content"]
                game_info = "[" + ai_res + "]"
                print(type(ai_res), ai_res)
                game_info = json.loads(game_info)  # 返回一个 JSON 响应
                print(type(game_info), game_info)
                return JsonResponse(game_info[0])

            else:
                return JsonResponse({'error': 'No title provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


# ajax调用AI

import git
from datetime import datetime
from git import Repo


def pushByGit(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_path = os.getcwd()  # 获取当前工作目录
    # 获取当前仓库
    repo = git.Repo(project_path)
    # 检查是否有未提交的更改
    if repo.is_dirty(untracked_files=True):
        modified_files = [item.a_path for item in repo.index.diff(None)]  # 获取已修改的文件
        untracked_files = repo.untracked_files  # 获取未跟踪的文件（新文件）
        deleted_files = [item.a_path for item in repo.index.diff(None) if item.deleted_file]  # 获取已删除的文件
        list = modified_files + deleted_files
        print("已修改文件:", list)
        # 添加所有更改（包括新文件和删除的文件）
        repo.git.add(A=True)  # 等同于 `git add .`
        # 提交更改
        commit_message = now + "使用python脚本更新"
        repo.index.commit(commit_message)
        # 推送更改到远程仓库
        repo.git.push("origin", "main")  # 或 "main"
        responsetext = f"""
        下列文件已推送到远程仓库：
        """
        context = {
            "list": list,
            "responsetext": responsetext
        }
        return render(request, 'admin/push.html', context)

    else:
        return render(request, 'admin/push.html', {"responsetext": "✅ 没有需要提交的更改"})

def backup_view(request):
    """ 触发数据库备份 """
    result = backup_database()
    return HttpResponse(result)

def restore_view(request):
    """ 触发数据库恢复 """
    if request.method == "POST":
        backup_file = request.POST.get("backup_file")
        result = restore_database(backup_file)
        return HttpResponse(result)

    # 获取所有备份文件列表
    backup_dir = os.path.join(settings.BASE_DIR, 'backup')
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".sql")]
    return render(request, "admin/restore.html", {"backup_files": backup_files})


def delete_backup(request):
    """ 触发数据库备份 """
    file_name = request.GET.get("backup_file")

    if file_name:
        backup_dir = os.path.join(settings.BASE_DIR, "backup")
        file_path = os.path.join(backup_dir, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            return redirect('/restore')  # 重定向到其他页面
        else:
            return HttpResponse("文件不存在", status=404)
    else:
        return HttpResponse("无效的请求", status=400)


def savepic(request):
    from game.utils.crazypic import get_pic
    if request.method == "POST":
        myurl = request.POST.get("iframeValue")
        get_pic(myurl)
        return JsonResponse({"status": "success", "message": "处理成功"})

@csrf_exempt
def update_status(request, item_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            is_checked = data.get("is_checked", False)  # 获取前端传来的状态
            game = Game.objects.get(nid=item_id)
            game.is_checked = is_checked  # 更新状态
            game.save()

            return JsonResponse({"success": True})
        except Game.DoesNotExist:
            return JsonResponse({"success": False, "error": "游戏不存在"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "无效请求"}, status=400)