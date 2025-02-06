import json
import os
import re

from django.core.paginator import Paginator
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from game.utils.opai import interact_with_openrouter
from H5game import settings
from game import models
from .models import Game, Questions
from game.utils.pagination import Pagination
from game.utils.myforms import SiteModelForm, GameModelForm, QuestionsModelForm
from django.http import HttpResponse, JsonResponse


# Create your views here.
def siteinfo():
    site = models.Site.objects.first()
    return site


def menus():
    top_menus = models.Game.objects.filter(recommend=4,is_checked=1)[:8]
    return top_menus


def get_recommend_games():
    game_list_L = models.Game.objects.filter(recommend=1,is_checked=1)[:6]
    game_list_R = models.Game.objects.filter(recommend=2,is_checked=1)[:6]
    return game_list_L, game_list_R


def new_games():
    game_list = models.Game.objects.all().filter(is_checked=1,recommend=0).order_by('-create_time')[:12]
    return game_list


def iframe_play(request, slug):
    # 可以通过 context 传递数据到模板
    game_obj = models.Game.objects.filter(slug=slug).first()
    context = {
        "game_obj": game_obj,
    }
    return render(request, 'play.html', context)


def index(request):
    game_obj = models.Game.objects.filter(recommend=3,is_checked=1).first()
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
    }
    return render(request, "game.html", context)


def generate_index_html(request):  # 生成静态html文件
    # 获取游戏对象
    game_obj = models.Game.objects.filter(recommend=3,is_checked=1).first()
    if not game_obj:
        return HttpResponse("游戏不存在", status=404)

    # 额外数据
    recommend_gamelist_L, recommend_gamelist_R = get_recommend_games()
    newgames = new_games()
    site = siteinfo()
    top_menus = menus()
    QandA = models.Questions.objects.filter(game_id=game_obj.nid).order_by('-nid')[:8]
    # 渲染模板为字符串
    context = {
        "game_obj": game_obj,
        "site": site,
        "recommend_gamelist_L": recommend_gamelist_L,
        "recommend_gamelist_R": recommend_gamelist_R,
        "newgames": newgames,
        "top_menus": top_menus,
        "QandA": QandA,
        "index": 1,
    }
    html_content = render_to_string("static/game.html", context).replace("/play/", "./play/").replace("/game/", "./")
    game_obj_play = models.Game.objects.filter(slug=game_obj.slug).first()
    context_play = {
        "game_obj_play": game_obj_play,
    }
    html_play = render_to_string("static/play.html", context_play).replace("/media/", "./../media/")

    # 生成首页静态文件路径
    index_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(index_output_dir):
        os.makedirs(index_output_dir)  # 如果目录不存在，则创建
    index_file_path = os.path.join(index_output_dir, f"index.html")

    # 生成首页主游戏静态文件路径
    play_output_dir = os.path.join(index_output_dir, "play/" + game_obj.slug)  # 存储静态文件的目录
    if not os.path.exists(play_output_dir):
        os.makedirs(play_output_dir)  # 如果目录不存在，则创建
    play_file_path = os.path.join(play_output_dir, "index.html")

    # 将渲染后的 HTML 写入文件
    with open(index_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        f.close()
    with open(play_file_path, "w", encoding="utf-8") as f:
        f.write(html_play)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='/index.html' target='_blank'>点击查看</a>")


def generate_game_html(request, game_id):  # 生成静态html文件
    # 获取游戏对象
    game_obj = Game.objects.filter(nid=game_id,is_checked=1).first()
    if not game_obj:
        return HttpResponse("游戏不存在", status=404)

    # 额外数据
    recommend_gamelist_L, recommend_gamelist_R = get_recommend_games()
    newgames = new_games()
    site = siteinfo()
    top_menus = menus()
    QandA = models.Questions.objects.filter(game_id=game_obj.nid).order_by('-nid')[:8]
    # 渲染模板为字符串
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
    html_content = render_to_string("static/game.html", context).replace("/play/", "./play/")
    game_obj_play = models.Game.objects.filter(slug=game_obj.slug).first()
    context_play = {
        "game_obj_play": game_obj_play,
    }
    html_play = render_to_string("static/play.html", context_play).replace("/media/", "./../media/")

    # 生成静态文件路径
    game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"{game_obj.slug}.html")

    # 生成游戏播放页静态文件路径
    play_output_dir = os.path.join(game_output_dir, "play/" + game_obj.slug)  # 存储静态文件的目录
    if not os.path.exists(play_output_dir):
        os.makedirs(play_output_dir)  # 如果目录不存在，则创建
    play_file_path = os.path.join(play_output_dir, "index.html")

    # 将渲染后的 HTML 写入文件
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        f.close()
    with open(play_file_path, "w", encoding="utf-8") as f:
        f.write(html_play)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='/{game_obj.slug}.html' target='_blank'>点击查看</a>")


def generate_allgame_html(request):
    all_games_obj = Game.objects.all()
    if all_games_obj:
        for game in all_games_obj:
            generate_game_html(request, game.nid)
    return HttpResponse(f"静态 HTML 文件已生成")


def gameList(request):
    game_list = models.Game.objects.all().filter(is_checked=1).order_by('-create_time')
    page_object = Pagination(request, game_list, page_size=48)
    site = siteinfo()
    top_menus = menus()
    context = {
        "game_list": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 页码
        "site": site,
        "top_menus": top_menus,
    }
    return render(request, "list.html", context)


def gameList_html(request):  # 分类页html
    """生成分页的静态 HTML 文件"""
    games = Game.objects.all().filter(is_checked=1).order_by('-create_time')  # 获取所有游戏并按创建时间降序排列
    paginator = Paginator(games, 30)  # 每页 10 条数据
    site = siteinfo()
    top_menus = menus()
    static_dir = os.path.join(settings.BASE_DIR, '')  # 定义存储目录
    os.makedirs(static_dir, exist_ok=True)  # 确保目录存在

    for page_number in range(1, paginator.num_pages + 1):
        page_obj = paginator.get_page(page_number)  # 获取当前页对象
        context = {
            "page_obj": page_obj,  # 分完页的数据
            "site": site,
            "top_menus": top_menus,
        }
        html_content = render_to_string('static/list.html', context)  # 渲染模板

        file_path = os.path.join(static_dir, f'game_list_{page_number}.html')  # 静态文件路径

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)  # 写入 HTML 内容
    return HttpResponse(f"静态页面已生成，共 {paginator.num_pages} 页")


def generate_allpage_html(request):
    generate_index_html(request)
    generate_allgame_html(request)
    gameList_html(request)
    aboutus_html(request)
    copyright_html(request)
    contactus_html(request)
    privacypolicy_html(request)
    termofuse_html(request)
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


def aboutus_html(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "About Us"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus,
        "aboutpage": "a",
    }
    html_code = render_to_string("static/aboutus.html", context)
    # 生成静态文件路径
    game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"about-us.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='/about-us.html' target='_blank'>点击查看</a>")


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


def copyright_html(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Copyright"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus,
        "aboutpage": "cr",
    }
    html_code = render_to_string("static/aboutus.html", context)
    # 生成静态文件路径
    game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"copyright.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='./copyright.html' target='_blank'>点击查看</a>")


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


def contactus_html(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Contact Us"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus,
        "aboutpage": "cu",
    }
    html_code = render_to_string("static/aboutus.html", context)
    # 生成静态文件路径
    game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"contact-us.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='./copyright.html' target='_blank'>点击查看</a>")


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


def privacypolicy_html(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Privacy Policy"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus,
        "aboutpage": "p",
    }
    html_code = render_to_string("static/aboutus.html", context)
    # 生成静态文件路径
    game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"privacy-policy.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='./privacypolicy.html' target='_blank'>点击查看</a>")


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


def termofuse_html(request):
    site = siteinfo()
    top_menus = menus()
    about_title = "Term Of Use"
    context = {
        "site": site,
        "about_title": about_title,
        "top_menus": top_menus,
        "aboutpage": "t",
    }
    html_code = render_to_string("static/aboutus.html", context)
    # 生成静态文件路径
    game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"term-of-use.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"静态 HTML 文件已生成：<a href='./termofuse.html' target='_blank'>点击查看</a>")


def guanli(request):
    return render(request, 'admin/admin.html')


def create_Site(request):
    if request.method == 'POST':
        form = SiteModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 将表单数据保存到数据库
            return HttpResponse('OK')
    else:
        form = SiteModelForm()  # 初始化空表单

    return render(request, 'admin/edit_site.html', {'form': form})


def edit_Site(request):
    site = models.Site.objects.first()
    if request.method == 'POST':
        form = SiteModelForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()  # 保存数据到数据库
            return redirect('/editsite')  # 重定向到当前页面
    else:
        form = SiteModelForm(instance=site)  # 将站点信息加载到表单

    return render(request, 'admin/edit_site.html', {'site': site, 'form': form})


def game_list(request):
    game_list = models.Game.objects.all()
    page_object = Pagination(request, game_list, page_size=15)
    context = {
        "game_list": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 页码
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
    questions = Questions.objects.filter(game=game)  # 获取与游戏相关的问题

    if request.method == 'POST':
        game_form = GameModelForm(request.POST, request.FILES, instance=game)

        if game_form.is_valid():
            game_form.save()  # 保存游戏数据

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

    qas_str = interact_with_openrouter(prompts)
    print(type(qas_str["choices"][0]["message"]["content"].split('[')[1].split(']')[0]),qas_str["choices"][0]["message"]["content"].split('[')[1].split(']')[0])
    qas_str = '[' + qas_str["choices"][0]["message"]["content"].split('[')[1].split(']')[0] + ']'
    print(type(qas_str),qas_str)
    print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    qas_list = json.loads(qas_str)
    print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(qas_list)
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
    ai_res = interact_with_openrouter(prompts)["choices"][0]["message"]["content"]
    game_info = ai_res.replace("```json","[").replace("```","]")
    game_info=json.loads(game_info)
    if game_info:
        game = Game.objects.get(nid=game_id)
        game.whatis=game_info[0]["whatis"]
        game.HowPlay=game_info[0]["howtoplay"]
        game.save()
    return redirect('/game_list')  # 替换为成功后的重定向URL
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
                ai_res = interact_with_openrouter(prompts)["choices"][0]["message"]["content"]
                print(ai_res)
                game_info = ai_res.replace("```json", "[").replace("```", "]")
                game_info = json.loads(game_info)# 返回一个 JSON 响应
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
                    1)把下面的英文重新组织一下，使之更有利于google SEO:
                    {description}
                    2)把返回的答案赋值给description,然后组成一个json返回
                    """
                print("------------------------------------------------------------------------------------")
                ai_res = interact_with_openrouter(prompts)["choices"][0]["message"]["content"]
                print(ai_res)
                game_info = ai_res.replace("```json", "[").replace("```", "]")
                game_info = json.loads(game_info)# 返回一个 JSON 响应
                return JsonResponse(game_info[0])

            else:
                return JsonResponse({'error': 'No title provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
