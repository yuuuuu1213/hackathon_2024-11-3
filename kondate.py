from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)

# メニュー項目とそれぞれの価格を辞書で定義

# 朝食用メニュー (menu_items_1)
menu_items_1 = {
    "主食": [
        ("食パン2枚", 130, 210),
        ("食パン3枚", 195, 315),
        ("ツナマヨおにぎり", 120, 180),
        ("焼きおにぎり", 130, 200),
        ("もち", 100, 150),
        ("美味しいサンドイッチ", 180, 320)
    ],
    "汁物": [
        ("味噌汁", 70, 50),
        ("コーンスープ", 120, 100),
        ("豆腐スープ", 80, 40),
        ("ワカメスープ", 90, 40),
        ("甘～いかぼちゃスープ", 400, 110)
    ],
    "小鉢": [
        ("漬物", 100, 20),
        ("冷奴", 120, 100),
        ("ポテトサラダ", 130, 150),
        ("もやしナムル", 90, 30),
        ("枝豆", 80, 60)
    ],
    "おかず": [
        ("厚焼き玉子", 150, 200),
        ("熟成された焼き魚", 250, 300),
        ("野菜炒め", 200, 180),
        ("サラダ", 150, 200),
        ("唐揚げ", 300, 350)
    ],
    "飲み物": [
        ("烏龍茶", 100, 0),
        ("抹茶ラテ", 180, 90),
        ("アイスティー", 130, 30),
        ("ミルク", 120, 80),
        ("100%オレンジジュース", 150, 120)
    ]
}

# 昼食用メニュー (menu_items_2)
menu_items_2 = {
    "主食": [
        ("ごはん1杯", 110, 200),
        ("うどん大盛り", 220, 220),
        ("チャーハン", 450, 450),
        ("特製カレーライス", 300, 600),
        ("ペペロンチーノ", 400, 450)
    ],
    "汁物": [
        ("コンソメスープ", 130, 80),
        ("トマトスープ", 110, 70),
        ("中華スープ", 100, 60),
        ("にんじんスープ", 120, 80),
        ("ミネストローネ", 130, 90)
    ],
    "小鉢": [
        ("ひじきと大豆の煮物", 140, 120),
        ("きんぴらごぼう", 110, 80),
        ("ナスのお浸し", 120, 50),
        ("カボチャの煮物", 130, 110),
        ("ほうれん草の胡麻和え", 110, 70)
    ],
    "おかず": [
        ("エビフライ5本", 700, 350),
        ("みそ鶏の照り焼き", 320, 280),
        ("野菜たっぷりシチュー", 290, 320),
        ("肉じゃが", 250, 250),
        ("天ぷら盛り合わせ", 350, 400)
    ],
    "飲み物": [
        ("ブラックコーヒー", 200, 5),
        ("レモネード", 160, 100),
        ("グレープフルーツジュース", 140, 110),
        ("ジンジャーエール", 150, 100),
        ("レモン水", 90, 10)
    ]
}

# 晩飯用メニュー (menu_items_3)
menu_items_3 = {
    "主食": [
        ("山盛りそば", 300, 190),
        ("高級ラーメン", 1500, 900),
        ("旨味たっぷりピラフ", 250, 400),
        ("やみつきオムライス", 450, 600),
        ("塩焼きそば", 350, 500)
    ],
    "汁物": [
        ("豚汁", 140, 120),
        ("クリームスープ", 130, 120),
        ("オニオンスープ", 110, 70),
        ("かき玉スープ", 100, 50),
        ("野菜スープ", 90, 60)
    ],
    "小鉢": [
        ("漬物", 100, 20),
        ("おひたし", 90, 40),
        ("もずく酢", 70, 20),
        ("酢の物", 60, 15),
        ("しらすおろし", 100, 80)
    ],
    "おかず": [
        ("デミグラスソース付きハンバーグ", 400, 380),
        ("ロースカツ", 400, 450),
        ("チキンカツ", 600, 350),
        ("麻婆豆腐", 250, 300),
        ("茄子の炒め物", 800, 600),
        ("がっつり焼肉コース盛り合わせ【極】", 5000, 1000)
    ],
    "飲み物": [
        ("ほろよい", 200, 120),
        ("青汁", 110, 20),
        ("トマトジュース", 120, 60),
        ("カフェラテ", 160, 90),
        ("美味しい甘酒", 700, 90),
        ("ワイン", 1000, 100)
    ]
}



def select_menu(budget, meal_time):
    selected_menu = {}
    total_price = 0
    total_calories = 0
    error = None
    otsuri = 0

    if budget < 100:
        error = "予算内でメニューを選ぶことができませんでした。"
        return selected_menu, total_price, error, otsuri, total_calories

    # meal_time に基づいてメニューを選択
    if meal_time == "朝食":
        menu_items = menu_items_1
    elif meal_time == "昼食":
        menu_items = menu_items_2
    else:  # 晩飯
        menu_items = menu_items_3

    for category, items in menu_items.items():
        affordable_items = [item for item in items if item[1] <= budget - total_price]
        if affordable_items:
            item, price, calorie = random.choice(affordable_items)
            selected_menu[category] = (item, price, calorie)
            total_price += price
            total_calories += calorie
            
    otsuri = budget - total_price
    
    return selected_menu, total_price, error, otsuri, total_calories

@app.route('/')
def index():
    # 初回アクセス時はメニューとエラーメッセージを空で渡す
    return render_template('kon.html', menu=None, total=0, error=None)

@app.route('/set_budget', methods=['POST'])
def set_budget():
    budget = int(request.form['budget'])  # ユーザーが入力した予算を取得
    meal_time = request.form['meal_time']  # ユーザーが選んだ食事の時間を取得
    selected_menu, total_price, error, otsuri, total_calories = select_menu(budget, meal_time)
    
    return render_template('kon.html', menu=selected_menu, total=total_price, error=error, otsuri=otsuri, total_cal=total_calories)

if __name__ == '__main__':
    app.run(debug=True)
