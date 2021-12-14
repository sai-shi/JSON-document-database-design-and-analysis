from pymongo import MongoClient
import json
import os
from pprint import pprint

input_dir = 'raw_data/For Merge Disqus/'
all_files = os.listdir(input_dir)

# Step 1: Connect to MongoDB - Note: Change connection string as needed

client = MongoClient(port=27017)
db = client.admin

serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)


db.articles.drop()
db.cursors.drop()
db.comments.drop()
db.authors.drop()
db.avatars.drop()
print(db.cursors.count_documents({}))
print(db.authors.count_documents({}))
print(db.comments.count_documents({}))
print(db.avatars.count_documents({}))

# Step 2: Create databases

for fname in all_files:
    if '.txt' in fname:
        file_name = fname.split('.')[0]
        # print(file_name.split('_'))
        article_id = file_name.split('_')[0]
        date = file_name.split('_')[1]
        article = {'article_id': article_id}
        db.articles.insert_one(article)
        with open(input_dir + fname, 'r') as f:
            try:
                data = json.loads("[" + f.read().replace("}\n{", "},\n{") + "]")
                for d in data:
                    c = d['cursor']
                    cursor = {
                        'cursor_id': c['id'],
                        'has_next': c['hasNext'],
                        'has_prev': c['hasPrev'],
                        'cursor_more': c['more'],
                        'next_cursor_id': c['next'],
                        'prev_cursor_id': c['prev'],
                        'article_id': article_id,
                        'datetime': date
                    }

                    db.cursors.insert_one(cursor)

                    for com in d['response']:

                        if com['author']["isAnonymous"] is False:

                            response = {
                                'comment_id': com['id'],
                                'comment_likes': com['likes'],
                                'comment_dislikes': com['dislikes'],
                                'num_reports': com['numReports'],
                                'created_at': com['createdAt'],
                                'editable_until': com['editableUntil'],
                                'message': com['message'],
                                'is_spam': com['isSpam'],
                                'is_deleted': com['isDeleted'],
                                'is_deleted_by_author': com['isDeletedByAuthor'],
                                'is_approved': com['isApproved'],
                                'is_flagged': com['isFlagged'],
                                'raw_message': com['raw_message'],
                                'is_highlighted': com['isHighlighted'],
                                'can_vote': com['canVote'],
                                'points': com['points'],
                                'is_edited': com['isEdited'],
                                'sb': com['sb'],
                                'forum': com['forum'],
                                'thread': com['thread'],
                                'cursor_id': d['cursor']['id'],
                                'author_id': com['author']['id'],
                                'parent_comment_id': com['parent'],
                            }

                            db.comments.insert_one(response)
                            bio = com['author']

                            # print(bio.keys())
                            # print(db.authors.count_documents({'author_id': bio['id']}))

                            if db.authors.count_documents({'author_id': bio['id']}) == 0:
                                author = {
                                    'author_id': bio['id'],
                                    'username': bio['username'],
                                    'about': bio['about'],
                                    'author_name': bio['name'],
                                    'disable_trackers': bio['disable3rdPartyTrackers'],
                                    'is_power_contributor': bio['isPowerContributor'],
                                    'joined_at': bio['joinedAt'],
                                    'profile_url': bio['profileUrl'],
                                    'is_private': bio['isPrivate'],
                                    'is_primary': bio['isPrimary'],
                                    'is_anonymous': bio['isAnonymous'],
                                    'url': bio['url'],
                                    'location': bio['location']
                                }
                                db.authors.insert_one(author)

                                ava = bio['avatar']
                                avatar = {
                                    'author_id': bio['id'],
                                    'permalink': ava['permalink'],
                                    'small_permalink': ava['small']['permalink'],
                                    'small_cache': ava['small']['cache'],
                                    'large_permalink': ava['large']['permalink'],
                                    'large_cache': ava['large']['cache']
                                }

                                db.avatars.insert_one(avatar)

                            else:
                                response = {
                                    'comment_id': com['id'],
                                    'comment_likes': com['likes'],
                                    'comment_dislikes': com['dislikes'],
                                    'num_reports': com['numReports'],
                                    'created_at': com['createdAt'],
                                    'editable_until': com['editableUntil'],
                                    'message': com['message'],
                                    'is_spam': com['isSpam'],
                                    'is_deleted': com['isDeleted'],
                                    'is_deleted_by_author': com['isDeletedByAuthor'],
                                    'is_approved': com['isApproved'],
                                    'is_flagged': com['isFlagged'],
                                    'raw_message': com['raw_message'],
                                    'is_highlighted': com['isHighlighted'],
                                    'can_vote': com['canVote'],
                                    'points': com['points'],
                                    'is_edited': com['isEdited'],
                                    'sb': com['sb'],
                                    'forum': com['forum'],
                                    'thread': com['thread'],
                                    'cursor_id': d['cursor']['id'],
                                    'author_id': "Unknown",
                                    'parent_comment_id': com['parent'],
                                }

                                db.comments.insert_one(response)


            except Exception as e:
                print(fname)
                print(str(e))
                break

print(db.cursors.count_documents({}))
print(db.comments.count_documents({}))
print(db.authors.count_documents({}))
print(db.avatars.count_documents({}))