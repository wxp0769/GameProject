import re
import os
from django.core.paginator import Paginator
from django.forms import inlineformset_factory, modelformset_factory
from game import models
from H5game import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from game.models import Game
from game.utils.pic_copy import copy_media_files

def siteinfo():
    site = models.Site.objects.first()
    return site
def menus():
    top_menus = models.Game.objects.filter(recommend=4, is_checked=1)[:8]
    return top_menus


def get_recommend_games():
    game_list_L = models.Game.objects.filter(recommend=1, is_checked=1)[:6]
    game_list_R = models.Game.objects.filter(recommend=2, is_checked=1)[:6]
    return game_list_L, game_list_R


def new_games():
    game_list = models.Game.objects.all().filter(is_checked=1, recommend=0).order_by('-create_time')[:18]
    return game_list
def generate_index_html(request):  # 生成静态html文件
    # 获取游戏对象
    game_obj = models.Game.objects.filter(recommend=3, is_checked=1).first()
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
    print(site.site_url)
    copy_media_files()
    # 生成首页静态文件路径
    # index_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    index_output_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://","").replace("http://","").replace("www.",""))
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
        f"首页静态 HTML 文件已生成：<a href='/index.html' target='_blank'>点击查看</a>")


def generate_game_html(request, game_id):  # 生成静态html文件
    # 获取游戏对象
    game_obj = Game.objects.filter(nid=game_id, is_checked=1).first()
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
    # game_output_dir = os.path.join(settings.BASE_DIR, "")  # 存储静态文件的目录，设置为空表示生成在根目录
    game_output_dir = os.path.join(settings.BASE_DIR,site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 存储静态文件的目录，设置为空表示生成在根目录
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
        f"游戏页静态 HTML 文件已生成：<a href='/{game_obj.slug}.html' target='_blank'>点击查看</a>")


def generate_allgame_html(request):
    all_games_obj = Game.objects.all()
    if all_games_obj:
        for game in all_games_obj:
            generate_game_html(request, game.nid)
    return HttpResponse(f"全部游戏静态 HTML 文件已生成")

def gameList_html(request):  # 分类页html
    """生成分页的静态 HTML 文件"""
    games = Game.objects.all().filter(is_checked=1).order_by('-create_time')  # 获取所有游戏并按创建时间降序排列
    paginator = Paginator(games, 30)  # 每页 10 条数据
    site = siteinfo()
    top_menus = menus()
    # static_dir = os.path.join(settings.BASE_DIR, '')  # 定义存储目录
    static_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 定义存储目录
    os.makedirs(static_dir, exist_ok=True)  # 确保目录存在

    for page_number in range(1, paginator.num_pages + 1):
        page_obj = paginator.get_page(page_number)  # 获取当前页对象
        context = {
            "page_obj": page_obj,  # 分完页的数据
            "site": site,
            "top_menus": top_menus,
            "index": 3,
        }
        html_content = render_to_string('static/list.html', context)  # 渲染模板

        file_path = os.path.join(static_dir, f'game_list_{page_number}.html')  # 静态文件路径

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)  # 写入 HTML 内容
    return HttpResponse(f"列表页静态 HTML 文件已生成，共 {paginator.num_pages} 页")


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
    game_output_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"about-us.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"AboutUs静态 HTML 文件已生成：<a href='/about-us.html' target='_blank'>点击查看</a>")

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
    game_output_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir,f"copyright.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"Copyright静态 HTML 文件已生成：<a href='./copyright.html' target='_blank'>点击查看</a>")


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
    game_output_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"contact-us.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"Contact Us静态 HTML 文件已生成：<a href='./copyright.html' target='_blank'>点击查看</a>")


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
    game_output_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"privacy-policy.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"Privacy Policy静态 HTML 文件已生成：<a href='./privacypolicy.html' target='_blank'>点击查看</a>")


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
    game_output_dir = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""))  # 存储静态文件的目录，设置为空表示生成在根目录
    if not os.path.exists(game_output_dir):
        os.makedirs(game_output_dir)  # 如果目录不存在，则创建
    output_file_path = os.path.join(game_output_dir, f"term-of-use.html")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
        f.close()
    return HttpResponse(
        f"Term Of Use静态 HTML 文件已生成：<a href='./termofuse.html' target='_blank'>点击查看</a>")


def generate_sitemap(request):
    # 获取动态内容（如数据库中的文章）
    games = Game.objects.filter(is_checked=True)
    site = siteinfo()
    # 获取静态页面 URL（如首页、关于页）
    static_urls = [
        reverse('aboutus'),
        reverse('copyright'),
    ]

    # 生成 XML 内容
    context = {
        'site': site,
        'games': games,
        'static_urls': static_urls,
        'current_date': timezone.now().date().isoformat(),
    }
    xml_content = render_to_string('sitemap.xml', context)  # 渲染模板
    file_path = os.path.join(settings.BASE_DIR, site.site_url.replace("https://", "").replace("http://", "").replace("www.", ""),f'sitemap.xml')  # 静态文件路径

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)  # 写入 HTML 内容
    return HttpResponse(f"sitemap.xml已生成")