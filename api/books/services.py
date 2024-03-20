import json

from flask import render_template, jsonify, session
from sqlalchemy import text
from sqlalchemy.orm import aliased

from api import db
from api.books.model import BooksCategories, Books


def fetch_all_books():
    # 编辑按钮时查询所有二级类目
    sql = "SELECT id,category_name FROM book_categories WHERE parent_id"
    r = db.session.execute(sql)
    type_list = [dict(row) for row in r]
    qsql = "SELECT b.*FROM books b LEFT JOIN (SELECT book_id FROM lending WHERE debtor_id=:debtor_id) l ON b.id=l.book_id WHERE l.book_id IS NULL ORDER BY RAND();"
    query = db.session.execute(qsql, {"debtor_id": session.get("user_info")['id']})
    results = [dict(row) for row in query]
    return render_template('books.html', results=results, type_list=type_list)


def classify_books():
    sql = "SELECT id,category_name AS title FROM book_categories WHERE id IN (SELECT DISTINCT bc.parent_id FROM books b INNER JOIN book_categories bc ON b.type=bc.id)"
    result = db.session.execute(sql)
    rows_list = [dict(row) for row in result]
    for row in rows_list:
        s = "SELECT id,category_name AS title FROM book_categories WHERE parent_id=" + str(row.get("id"))
        r = db.session.execute(s, {"parent_id": row.get("id")})
        rl = [dict(ro) for ro in r]
        row["children"] = rl
        for ch in rl:
            ss = "SELECT id,title,url AS href FROM books WHERE type=" + str(ch.get("id"))
            br = db.session.execute(ss, {"type": ch.get("id")})
            brw = [dict(o) for o in br]
            ch["children"] = brw
    return jsonify(rows_list), 200


def fetch_bk(book_id):
    query = text("""
    SELECT id, title, author, 
           DATE_FORMAT(publication_date, '%Y-%m-%d') as publication_date, 
           type, description 
    FROM Books 
    WHERE id = :book_id;
    """)
    result = db.session.execute(query, {'book_id': book_id})
    rl = [dict(ro) for ro in result]
    return jsonify(rl), 200


def insert_book(data):
    sql = "INSERT INTO books (title,type) VALUES ('" + str(data["title"]) + "','" + str(data["type"]) + "')"
    db.session.execute(sql)
    db.session.commit()
    return json.dumps(data)


def rec_bks():
    # 查出所借书籍的大类次数最多的大类
    sql = "SELECT bc.parent_id,COUNT(parent_id) AS count_value FROM lending l INNER JOIN books b ON l.book_id=b.id INNER JOIN book_categories bc ON b.type=bc.id WHERE l.debtor_id=:debtor_id GROUP BY bc.parent_id ORDER BY count_value DESC LIMIT 1"
    result = db.session.execute(sql, {"debtor_id": session.get("user_info")['id']}).fetchone()
    # 查询该大类下的所有二级类目,随机取10条二级类目
    parent_id = result["parent_id"] if result is not None else ""
    chd_bc = "SELECT id,category_name FROM book_categories WHERE parent_id=:parent_id ORDER BY RAND() LIMIT 10"
    r = db.session.execute(chd_bc, {"parent_id": parent_id})
    cld_cat = [dict(ro) for ro in r]
    arr = []
    for row in cld_cat:
        ss = "SELECT * FROM books WHERE type=:type AND id NOT IN (SELECT book_id FROM lending WHERE debtor_id=:debtor_id) ORDER BY RAND()"
        br = db.session.execute(ss, {"type": row.get("id"), "debtor_id": session.get("user_info")['id']})
        # 将每个list存入新的大的list
        arr.append([dict(o) for o in br])
    return render_template("rec_books.html", cld_cat=cld_cat, clg_bks=arr)


def synchrotron(file):
    json_data = file.read().decode('utf-8')
    data = json.loads(json_data)
    for supertype in data:
        bc_super = BooksCategories()
        bc_super.category_name = supertype["title"]
        db.session.add(bc_super)
        db.session.commit()
        for secondary in supertype["children"]:
            bc_second = BooksCategories()
            bc_second.category_name = secondary["title"]
            bc_second.parent_id = bc_super.id
            db.session.add(bc_second)
            db.session.commit()
            sec_child = secondary["children"] if "children" in secondary else []
            for bk in sec_child:
                book = Books()
                book.title = bk["title"] if "title" in bk else ""
                book.author = bk["author"] if "author" in bk else ""
                book.publication_date = bk["publication_date"] if "publication_date" in bk else ""
                book.type = bc_second.id
                book.description = bk["description"] if "description" in bk else ""
                book.url = bk["href"] if "href" in bk else ""
                db.session.add(book)
            db.session.commit()
    return jsonify(data)
