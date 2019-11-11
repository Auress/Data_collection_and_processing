from pymongo import MongoClient

mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
instagram_data_base = client.instagram
instagram_likes_collection = instagram_data_base.instagram_likes


for x in instagram_likes_collection.find()[0]:
    if x != '_id':
        for following in range(len(instagram_likes_collection.find_one()[x]['edges'])):
            try:
                following_id = instagram_likes_collection.find_one()[str(x)]['edges'][str(following)]['id']
                for posts in range(len(
                        instagram_likes_collection.find_one()[str(x)]['edges'][str(following)]['posts'])):
                    try:
                        for comments in range(len(instagram_likes_collection.find_one()
                                                  [str(x)]['edges'][str(following)]['posts'][str(posts)]['comments'])):
                            u_id = instagram_likes_collection.find_one()[str(x)]['edges'][str(following)]['posts'][str(
                                posts)]['comments'][str(comments)]['comment_user_id']
                            if u_id == x:
                                print(f'user (id: {x}) commented followings (f_id: {following_id}) post')
                    except Exception as e:
                        pass
                    try:
                        for likes in range(len(instagram_likes_collection.find_one()
                                               [str(x)]['edges'][str(following)]['posts'][str(posts)]['likes'])):
                            u_id = instagram_likes_collection.find_one()[str(x)]['edges'][str(following)]['posts'][str(
                                posts)]['likes'][str(likes)]['like_user_id']
                            if u_id == x:
                                print(f'user (id: {x}) liked followings (f_id: {following_id}) post')
                    except Exception as e:
                        pass
            except Exception as e:
                pass
