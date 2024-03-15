import json

from flask import render_template, jsonify, session
from sqlalchemy import text

from api import db


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
            ss = "SELECT id,title FROM books WHERE type=" + str(ch.get("id"))
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
    parent_id, count_value = db.session.execute(sql, {"debtor_id": session.get("user_info")['id']}).fetchone()
    # 查询该大类下的所有二级类目,随机取10条二级类目
    chd_bc = "SELECT id,category_name FROM book_categories WHERE parent_id=:parent_id ORDER BY RAND() LIMIT 10"
    r = db.session.execute(chd_bc, {"parent_id": parent_id})
    cld_cat = [dict(ro) for ro in r]
    arr = []
    for row in cld_cat:
        ss = "SELECT * FROM books WHERE type=:type"
        br = db.session.execute(ss, {"type": row.get("id")})
        # 将每个list存入新的大的list
        arr.append([dict(o) for o in br])
    return render_template("rec_books.html", cld_cat=cld_cat, clg_bks=arr)
