"""
URL configuration for H5game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from game import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    path('htgl/', views.guanli),
    path('game/<slug:slug>/', views.game, name='singleGame'),
    path('play/<slug:slug>/', views.iframe_play, name='gamePlay'),
    path('games/', views.gameList, name='gameList'),

    # <表单页面路由开始
    path('guanli/', views.guanli, name='guanli'),
    path('createsite/', views.create_Site, name='create_Site'),
    path('editsite/', views.edit_Site, name='edit_Site'),
    path('game_list/', views.game_list, name='game_list'),
    path('game_list_ok/', views.game_list_checked, name='game_list_checked'),
    path('delete/<int:game_id>', views.del_game, name='del_game'),
    path('addgame/', views.add_game, name='add_game'),
    path('editgame/<int:game_id>', views.edit_game, name='edit_game'),
    # >表单页面路由结束

    # <静态页路由开始
    path("generate_index/", views.generate_index_html, name="generate_index"),  # 生成首页静态html文件
    path("generate_game/<int:game_id>/", views.generate_game_html, name="generate_game"),  # 生成单个游戏页静态html文件
    path("generate_allgame/", views.generate_allgame_html, name="generate_allgame"),  # 生成所有游戏页静态html文件
    path("generate_list/", views.gameList_html, name="generate_list"),  # 生成所有游戏页静态html文件
    path("generate_allpage_html/", views.generate_allpage_html, name="generate_allpage_html"),  # 生成所有游戏页静态html文件
    # >静态页路由结束

    # 生成问题及答案开始
    path("generate_QandA/<int:game_id>/", views.generate_QandA, name="generate_QandA"),
    path("generate_whathow/<int:game_id>/", views.generate_whathow, name="generate_whathow"),
    path("generate_whathow2/", views.generate_whathow2, name="generate_whathow2"),
    path("generate_description/", views.generate_description, name="generate_description"),
    # 生成问题及答案结束

    # 生成About开始
    path("generate_aboutus/", views.aboutus_html, name="aboutus_html"),
    # 生成About结束

    # 生成sitemap开始
    path("generate_sitemap/", views.generate_sitemap, name="generate_sitemap"),
    # 生成sitemap结束

    # <footer路由
    path('about-us/', views.aboutus, name='aboutus'),
    path('copyright/', views.copyright, name='copyright'),
    path('contact-us/', views.contactus, name='contactus'),
    path('privacy-policy/', views.privacypolicy, name='privacypolicy'),
    path('term-of-use/', views.termofuse, name='termofuse'),
    # footer路由>
    path("push/", views.pushByGit, name="pushByGit"),
    # 其他路由
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('backup/', views.backup_view, name='backup'),
    path('restore/', views.restore_view, name='restore'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
