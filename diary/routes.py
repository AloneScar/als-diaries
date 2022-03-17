from datetime import datetime
from diary import app, db # 这个是从__init__.py中引入
from diary.models import Item
from flask import render_template, request, url_for
from pathlib import Path


@app.route('/')
def home_page():
    items = Item.query.with_entities(Item.id, Item.title, Item.date_created, Item.date_last_commited).all()
    print(items)
    return render_template('home.html', items=items) # 渲染模板，从templates文件夹获取文件，可有传参可不传参

@app.route('/diary/<_id>')
def show_page(_id):
    item = Item.query.filter(Item.id == _id).first()
    # print(item.content)
    return render_template(f'data/{item.title}.html', title=item.title)

@app.route('/edit')
def edit_page():
    return 'Edit'

@app.route('/commit', methods=['GET', 'POST'])
def commit_page():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        content_html = "{% extends 'show.html' %}{% block title %}"+ title +"{% endblock %}{% block content %}"+ content +"{% endblock %}"
        content_url = str(Path(__file__).parent.joinpath('templates', 'data', title+'.html'))
        with open(content_url, "w", encoding='utf-8') as f:
            f.write(content_html)
        print(content_url)
        item = Item(title=title, content_url=content_url)
        db.session.add(item)
        db.session.commit()
        return 'success'
    else:
        return render_template('commit.html', timeNow=datetime.now().strftime("%Y-%m-%d"))
