from flask import Flask, request
from flask_restful import Api, Resource
import json
import os

app = Flask(__name__)
api = Api(app)

class UserList(Resource):
    filename = 'users.json'

    def get_users(self):
        users = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as fp:
                users = json.loads(fp.read())
        return users

    def get(self):
        if not os.path.exists(self.filename):
            return 'users.json is not exists'
        r = self.get_users()
        s = ''
        for d in r:
            email = d['email']
            password = d['password']
            s += '[email: {}, pw: {}]'.format(email, password)
        return s

    def post(self):
        r_json = request.get_json()
        email = r_json['email']
        password = r_json['password']
        r = self.get_users()
        for d in r:
            if email == d['email']:
                return '{} is aleady exists'.format(email)
        _id = 0
        for d in r:
            _id = max(_id, d['id'])
        _id = _id + 1
        r_json['id'] = _id
        r.append(r_json)
        with open(self.filename, 'w') as fp:
            fp.write(json.dumps(r))
        return 'email: {}, pw: {}'.format(email, password)

    def put(self):
        r_json = request.get_json()
        _id = r_json['id']
        password = r_json['password']
        users = self.get_users()
        found = False
        for idx, _ in enumerate(users):
            if users[idx]['id'] == _id:
                found = True
                users[idx]['password'] = password
        if not found:
            return '{} is not exists'.format(_id)
        with open(self.filename, 'w') as fp:
            fp.write(json.dumps(users))
        return 'update password successfully'

    def delete(self):
        r_json = request.get_json()
        _id = r_json['id']
        users = self.get_users()
        found = False
        for idx, _ in enumerate(users):
            if users[idx]['id'] == _id:
                found = True
                del users[idx]
        if not found:
            return '{} is not exists'.format(_id)
        with open(self.filename, 'w') as fp:
            fp.write(json.dumps(users))
        return '{} deleted successfully'.format(_id)


class ArticleList(Resource):
    filename = 'articles.json'

    def get_articles(self):
        articles = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as fp:
                articles = json.loads(fp.read())
        return articles

    def get(self):
        if not os.path.exists(self.filename):
            return 'articles.json is not exists'
        r = self.get_articles()
        s = ''
        for d in r:
            article_id = d['id']
            user_id = d['user_id']
            title = d['title']
            content = d['content']
            s += '[id: {}, user_id: {}, title: {}, content: {}]'.format(article_id, user_id, title, content)
        return s

    def post(self):
        r_json = request.get_json()
        user_id = r_json['user_id']
        title = r_json['title']
        content = r_json['content']
        r = self.get_articles()
        a_id = 0
        for d in r:
            a_id = max(a_id, d['id'])
        a_id = a_id + 1
        r_json['id'] = a_id
        r.append(r_json)
        with open(self.filename, 'w') as fp:
            fp.write(json.dumps(r))     
        return ' The content of user {} is posted successfully'.format(user_id)

    def put(self):
        
        return ""

    def delete(self):
        
        return '{} deleted successfully'.format(article_id)


class CommentList(Resource):
    def get(self):
        return ""

    def post(self):
        return ""

    def put(self):
        return ""

    def delete(self):
        return ""


class LikeList(Resource):
    def get(self):
        return ""

    def post(self):
        return ""

    def put(self):
        return ""

    def delete(self):
        return ""


api.add_resource(UserList, '/api/users')
api.add_resource(ArticleList, '/api/articles')
api.add_resource(CommentList, '/api/comments')
api.add_resource(LikeList, '/api/likes')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
