from datetime import datetime
from diary import app, db  # 这个是从__init__.py中引入
from diary.models import Item
from flask import render_template, request
from pathlib import Path


@app.route('/')
def home_page():
    items = Item.query.with_entities(Item.title, Item.date_created, Item.date_last_commited).all()
    # print(items)
    return render_template('home.html', items=items)  # 渲染模板，从templates文件夹获取文件，可有传参可不传参


@app.route('/diary/<title>')
def show_page(title):
    item = Item.query.filter(Item.title == title).first()
    # print(item.content)
    content_url = str(Path(__file__).parent.joinpath('templates', 'data', title + '.html'))
    with open(content_url, "r", encoding='utf-8') as f:
        content = f.read()
    # print(content)
    return render_template('show.html', title=item.title, content=content)


@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_page(title):
    if request.method == 'POST':
        content = request.form.get('content')
        try:
            title_old = request.form.get('title')
            item = Item.query.filter(Item.title == title_old).first()
            content_url = str(Path(__file__).parent.joinpath('templates', 'data', title_old + '.html'))
            Path(content_url).unlink()
            item.title = title
            item.date_last_commited = datetime.utcnow()
            db.session.commit()
            content_url = str(Path(__file__).parent.joinpath('templates', 'data', title + '.html'))
            with open(content_url, "w", encoding='utf-8') as f:
                f.write(content)
            return 'success'
        except Exception as e:
            print(e)
            return 'fail'
    # print(title)
    item = Item.query.filter(Item.title == title).first()
    content_url = str(Path(__file__).parent.joinpath('templates', 'data', title + '.html'))
    with open(content_url, "r", encoding='utf-8') as f:
        content = f.read()
    return render_template('commit.html', title=item.title, content=content, URL='edit')


@app.route('/delete', methods=['GET', 'POST'])
def delete_page():
    if request.method == 'POST':
        title = request.form.get('title')
        try:
            item = Item.query.filter(Item.title == title).first()
            content_url = str(Path(__file__).parent.joinpath('templates', 'data', title + '.html'))
            Path(content_url).unlink()
            # print(item)
            db.session.delete(item)
            db.session.commit()
            return 'success'
        except Exception as e:
            print(e)
            return 'fail'


@app.route('/commit/<title>', methods=['GET', 'POST'])
def commit_page(title):
    if request.method == 'POST':
        content = request.form.get('content')
        try:
            content_url = str(Path(__file__).parent.joinpath('templates', 'data', title + '.html'))
            with open(content_url, "w", encoding='utf-8') as f:
                f.write(content)
            # print(content_url)
            item = Item(title=title)
            db.session.add(item)
            db.session.commit()
            return 'success'
        except Exception as e:
            print(e)
            return 'fail'
    else:
        return render_template('commit.html', title=datetime.now().strftime("%Y-%m-%d"), content='<p>你来啦！😋</p>',
                               URL='commit')
