import json
from datetime import datetime

import pymysql
import requests
from lxml import html

# 设置请求头，模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    'cookie': '_ga=GA1.1.342778751.1732431879; _cc_id=cabfddef7122545c4daab98d4b1dce0f; _uetvid=5f258fe0aa3211efb68d896ddbe994ba|vsu47k|1732721312307|1|1|bat.bing.com/p/insights/c/s; _gcl_au=1.1.1135082404.1732431879.1557663333.1734147961.1734147960; _ga_MGM1G52C1P=GS1.1.1734147952.1.1.1734148003.9.0.0; _ym_uid=1736603030201215646; _ym_d=1736603030; FCNEC=%5B%5B%22AKsRol-OfdfHA96yc2U-zz7rmu15fs3-uhz_go78NkvyeEmeBTRwZCz0AgJvTO3vqxWekm5ZvoQoDN5xrmLwrof4X4KrAeeR_uGh9P6uFFlrwMJrTOykjeURcNVc2rIoPG1OSVJj0_7YAWkAq7eucPwh8FyzQzWBFw%3D%3D%22%5D%5D; panoramaId_expiry=1739157544866; panoramaId=b81d0dbda679b9898594904f86dc16d5393896f78fe69b21a96b379acb8db2ba; sharedid=4d6f7fbc-520e-4d46-9559-fd624a2c9206; sharedid_cst=zix7LPQsHA%3D%3D; __cf_bm=5WpUhULYW8UCujUjDol5uNf6uotk377flJYGpuP2t20-1738721980-1.0.1.1-978kzljOgLLaydLalDAV06bmlEnUm3Ru3w8j8lCCcWYi5hkFGBtIq4s4m3fRJA4hMQjRDJjIDRh5T4sGZZ8r_g; __gads=ID=cc2e303f7383e1f2:T=1732431887:RT=1738722693:S=ALNI_Ma8M8zay2adKNZ_pgtbmU9PSkf49g; __gpi=UID=00000f9d5724bcdb:T=1732431887:RT=1738722693:S=ALNI_MaWFMzacfsrxR9tyjU09W4tqRFtBA; __eoi=ID=654890f0e3ae85b4:T=1732431887:RT=1738722693:S=AA-AfjbhGH6ukHaggAUwfx24ZFRL; _ga_BB20KEMLCJ=GS1.1.1738721038.23.1.1738722711.30.0.0; cto_bundle=6Bo94V8wVkoyMWJ5VXVYJTJCaHJHREdoSG1GbVkxV1JQRjZSbWd3ek5lbUVMZEs1QldSZW9tR3Y4VVlzdnRtaUJyb3ZvTSUyQm8lMkJ6R3VxSmN4R0c5ZnpkaTlqQVFNQTJlJTJGakpNQmNENzhxJTJCdWNwbzhSa3VnSUN6N3hXd2xzRFFYODNNZ2JaVXFEb0JHcFlXYWpWR2V5ckt2VWUlMkJTemclM0QlM0Q; cto_bidid=mY374F9WSEg1eUJVSWhhR2tlZHlZNmE3ZzdpTlRZeEk3TUJKN3hPNCUyQlpDSjBVYzFCNTA5NlRkJTJCdUlnaTFNbFZJNFc4ZGVMallNJTJGOFdrYW4wRXM3OXBNaVZNekNreSUyQlU3YWtHQ3AlMkYlMkZxdFEycktRNHNEenRBY2FMJTJCeDRTODZkRGdtbzIlMkI; cto_dna_bundle=V2o8JV8wVkoyMWJ5VXVYJTJCaHJHREdoSG1GbWQlMkIlMkJsT3lEeVVCTjklMkJ6ZUlrMTE0eG1INmxIazdMR3BERURubCUyRmIlMkY3RzFPJTJCeGtUNUZTdGRWUUxidHJaNzdqRmZ3JTNEJTNE'
}
def get_game_links():
    list_pages = []
    game_links = []
    for i in range(1, 6):
        list_pages.append(
            "https://model.crazygames.com/modelRequest?table=model_featured_new_vs_returning_202502031513&locale=en_US&place=tagPage&tag=5315de90-56c4-4fe0-a8c2-8cecf24f0331&os=Windows&device=desktop&location=US&userType=returning&page=" + str(
                i) + "&size=70&cgClient=crazygames-portal%2F1.245.1")
    for list in list_pages:
        response = requests.get(list, headers=headers).text
        res_json = json.loads(response)['items']
        for item in res_json:
            game_link = 'https://www.crazygames.com/game/' + item['slug']
            game_links.append(game_link)
    return game_links

def get_game_data(gamelink):
    game = gamelink
    response = requests.get(game, headers=headers)
    # 2. 解析HTML
    tree = html.fromstring(response.content)
    # 3. 使用XPath提取文本
    # --------------------------------------------------
    # 你的目标XPath（注意索引从1开始）
    t_xpath = '//*[@class="css-1tggrk3"]/h1[1]/text()'
    # d_xpath = '//*[@class="gameDescription_first css-zrsyhi" or @class="css-zrsyhi"]/p[1]/text()'
    d_xpath = '//*[@class="gameDescription_first css-zrsyhi" or @class="css-zrsyhi"]/text()'
    # 提取文本（会返回列表）
    title = tree.xpath(t_xpath)[0]
    print(tree.xpath(d_xpath))
    if tree.xpath(d_xpath):
        description = tree.xpath(d_xpath)[0]
        result = {'title': title, 'description': description}
        return result
    else:
        pass

def caiji_gamelink():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="xiaoyouxi",
            charset="utf8mb4"  # 设置字符集
        )
        cursor = conn.cursor()
        games_info = []
        game_links = get_game_links()
        for game_link in game_links:
            print(game_link)
            sql = "INSERT INTO game_pachong (source,is_caiji) VALUES (%s,%s)"
            values = (game_link,0)
            cursor.execute(sql, values)  # ✅ 安全
            conn.commit()
    except pymysql.MySQLError as err:
        print(f"数据库错误: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def caiji_gameinfo():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="xiaoyouxi",
            charset="utf8mb4"  # 设置字符集
        )
        cursor = conn.cursor()
        # 1️⃣ 查询所有数据
        query_sql = "SELECT * FROM game_pachong where is_caiji=0"  # 假设 'users' 表有 id、name、age 字段
        cursor.execute(query_sql)
        game_links = cursor.fetchall()  # 获取所有数据
        for game_obj in game_links:
            nid=game_obj[0]
            game_link=game_obj[3]
            data=get_game_data(game_link)
            print(data)
            if data is not None:
                if data["title"] and data["description"]:
                    update_sql = "UPDATE game_pachong SET title = %s,description = %s,is_caiji = 1 WHERE nid = %s"
                    values = (data["title"],data["description"],nid)
                    cursor.execute(update_sql,values)
                    print(nid,values)
                    conn.commit()  # 每次更新都提交
        cursor.close()
        conn.close()
        print("数据更新成功！")
    except pymysql.MySQLError as err:
        print(f"数据库错误: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            # 关闭连接
# caiji_gameinfo()
def game_publish():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="xiaoyouxi",
            charset="utf8mb4"  # 设置字符集
        )
        cursor = conn.cursor()
        # 1️⃣ 查询所有数据
        query_sql = "SELECT * FROM game_pachong where is_publish=0"  # 假设 'users' 表有 id、name、age 字段
        cursor.execute(query_sql)
        games = cursor.fetchall()  # 获取所有数据
        for game in games:
            title=game[1]
            description = game[2]
            if len(description)>1024:
                description = title
            source=game[3]
            thumbnail="/avatars/default.png"
            iframeUrl=source
            recommend=0
            if title and description:
                insert_sql = "insert into game_game SET title = %s,description = %s,source= %s,thumbnail=%s,iframeUrl=%s,recommend=%s,create_time=%s,update_time=%s,is_checked=%s"
                values = (title, description, source,thumbnail,iframeUrl,recommend,datetime.now(),datetime.now(),0)
                cursor.execute(insert_sql, values)
                update_sql = "UPDATE game_pachong SET is_publish = 1 WHERE nid = %s"
                values = (game[0])
                cursor.execute(update_sql, values)
                print(title)
                conn.commit()  # 每次更新都提交

        cursor.close()
        conn.close()
        print("数据更新成功！")
    except pymysql.MySQLError as err:
        print(f"数据库错误: {err}")
game_publish()