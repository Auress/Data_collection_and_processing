# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy



class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    variables_base = {'fetch_mutual': 'false', 'include_reel': 'true', 'first': 100}
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    following = {}

    def __init__(self, login, password, parse_user, *args, **kwargs):
        self.login = login
        self.password = password
        self.parse_user_name = parse_user
        # self.query_hash_followers = 'c76146de99bb02f6415203be841dd25a'
        self.query_hash_following = 'd04b0a864b4b54837c0d870b0e77e076'
        self.query_hash_comments = '97b41c52301f77ce508f55e66d17620e'
        self.query_hash_likes = 'd5d763b1e2acf209d62d22d184488e57'
        super().__init__(*args, **kwargs)


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'

        yield scrapy.FormRequest(
            insta_login_link,
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.password},
            headers={'X-CSRFToken': csrf_token}
        )

    # Обход пользователей
    def parse_users(self, response: HtmlResponse):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for user in self.parse_user_name:
                yield response.follow(urljoin(self.start_urls[0], user),
                                      callback=self.parse_user,
                                      cb_kwargs={'user': user})

    def parse_user(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars, self.query_hash_following),
                               callback=self.parse_following,
                               cb_kwargs={'user_vars': user_vars, 'user': user_id}
                              )

    # Обход на кого подписан
    def parse_following(self, response: HtmlResponse, user_vars, user):
        data = json.loads(response.body)

        self.following.update({user: {'edges': {}}})
        for i in range(len(data['data']['user']['edge_follow']['edges'])):
            self.following[user]['edges'].update({str(i): {
                'id': data['data']['user']['edge_follow']['edges'][i]['node']['id'],
                'username': data['data']['user']['edge_follow']['edges'][i]['node']['username'],
                'full_name': data['data']['user']['edge_follow']['edges'][i]['node']['full_name'],
            }})

        if data['data']['user']['edge_follow']['page_info']['has_next_page']:
            user_vars.update({'after': data['data']['user']['edge_follow']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars, self.query_hash_following)
            yield response.follow(next_page,
                                  callback=self.parse_following,
                                  cb_kwargs={'user_vars': user_vars, 'user': user}
                                  )
        else:
            for following_num in range(len(self.following[user]['edges'])):
                yield response.follow(
                    urljoin(
                        urljoin(self.start_urls[0], self.following[user]['edges'][str(following_num)]['username'])
                        , '?__a=1'),  # Получаем json с данныме о подписчике (там есть названия постов)
                    callback=self.parse_following_posts,
                    cb_kwargs={'user': user, 'following_num': str(following_num)}
                    )

    def parse_following_posts(self, response: HtmlResponse, user, following_num):
        data = json.loads(response.body)
        self.following[user]['edges'][following_num]['posts'] = {}

        for post_num in range(len(data['graphql']['user']['edge_owner_to_timeline_media']['edges'])):
            if post_num > 9:
                break
            self.following[user]['edges'][following_num]['posts'].update({str(post_num): {
                'post_id':
                    data['graphql']['user']['edge_owner_to_timeline_media']['edges'][post_num]['node']['id'],
                'shortcode':
                    data['graphql']['user']['edge_owner_to_timeline_media']['edges'][post_num]['node']['shortcode'],
            }})
            post = self.following[user]['edges'][following_num]['posts'][str(post_num)]['shortcode']
            f_user_id = self.following[user]['edges'][following_num]['id']
            yield response.follow(
                urljoin(urljoin(self.start_urls[0], 'p/'), post),  # Получаем json с комментами к посту
                callback=self.parse_post,
                cb_kwargs={'user': user, 'post': post, 'f_user_id': f_user_id,
                           'following_num': following_num, 'post_num': str(post_num)}
            )

    def parse_post(self, response: HtmlResponse, user, post, f_user_id, following_num, post_num):
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'shortcode': post, 'id': f_user_id})
        self.following[user]['edges'][following_num]['posts'][post_num]['comments'] = {}
        self.following[user]['edges'][following_num]['posts'][post_num]['likes'] = {}

        yield response.follow(self.make_graphql_url(user_vars, self.query_hash_comments),
                              callback=self.parse_comments,
                              cb_kwargs={'user_vars': user_vars, 'user': user,
                                         'following_num': following_num, 'post_num': post_num,
                                         'post': post, 'f_user_id': f_user_id}
                              )

    def parse_comments(self, response: HtmlResponse, user_vars, user, following_num, post_num, post, f_user_id):
        data = json.loads(response.body)
        total = len(self.following[user]['edges'][following_num]['posts'][post_num]['comments'])
        for i in range(len(data['data']['shortcode_media']['edge_media_to_parent_comment']['edges'])):
            self.following[user]['edges'][following_num]['posts'][post_num]['comments'].update({str(i + total): {
                'comment_id':
                    data['data']['shortcode_media']['edge_media_to_parent_comment']['edges'][i]['node']['id'],
                'comment_user_id':
                    data['data']['shortcode_media']['edge_media_to_parent_comment']['edges'][i]['node']['owner']['id'],
                'comment_username':
                    data['data']['shortcode_media']['edge_media_to_parent_comment']['edges'][i]['node']['owner']['username'],
            }})

        if data['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']:
            pass
            user_vars.update({'after': data['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars, self.query_hash_comments)
            yield response.follow(next_page,
                                  callback=self.parse_comments,
                                  cb_kwargs={'user_vars': user_vars, 'user': user,
                                             'following_num': following_num, 'post_num': post_num}
                                  )

        else:
            user_vars = deepcopy(self.variables_base)
            user_vars.update({'shortcode': post, 'id': f_user_id})

            yield response.follow(self.make_graphql_url(user_vars, self.query_hash_likes),
                                  callback=self.parse_likes,
                                  cb_kwargs={'user_vars': user_vars, 'user': user,
                                             'following_num': following_num, 'post_num': post_num}
                                  )

    def parse_likes(self, response: HtmlResponse, user_vars, user, following_num, post_num):
        data = json.loads(response.body)
        total = len(self.following[user]['edges'][following_num]['posts'][post_num]['likes'])
        for i in range(len(data['data']['shortcode_media']['edge_liked_by']['edges'])):
            self.following[user]['edges'][following_num]['posts'][post_num]['likes'].update({str(i + total): {
                'like_user_id':
                    data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['id'],
                'like_username':
                    data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['username'],
                'like_full_name':
                    data['data']['shortcode_media']['edge_liked_by']['edges'][i]['node']['full_name'],
            }})

        if data['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']:
            pass
            user_vars.update(
                {'after': data['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars, self.query_hash_likes)
            yield response.follow(next_page,
                                  callback=self.parse_likes,
                                  cb_kwargs={'user_vars': user_vars, 'user': user,
                                             'following_num': following_num, 'post_num': post_num}
                                  )
        else:
            item = deepcopy(self.following)
            yield item

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def make_graphql_url(self, user_vars, query_hash):
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=query_hash,
            variables=urlencode(user_vars)
        )
        return result
