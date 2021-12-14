import json
import os
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="project"
)

# print(mydb)

input_dir = 'raw_data/For Merge Disqus/'
all_files = os.listdir(input_dir)

mycursor = mydb.cursor()


for fname in all_files:
    if '.txt' in fname:
        file_name = fname.split('.')[0]
        article_id = file_name.split('_')[0]
        date = file_name.split('_')[1]

        sql = "INSERT IGNORE INTO articles (article_id, article_name) VALUES (%s, %s)"
        val = (article_id, "")
        mycursor.execute(sql, val)

        with open(input_dir + fname, 'r') as f:
            try:
                data = json.loads("[" + f.read().replace("}\n{", "},\n{") + "]")
                for d in data:
                    c = d['cursor']

                    sql = "INSERT IGNORE INTO cursors (cursor_id, has_next, has_prev, cursor_more, " \
                          "next_cursor_id, prev_cursor_id, article_id, datetime) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (c['id'], c['hasNext'], c['hasPrev'], c['more'], c['next'], c['prev'], article_id, date)
                    mycursor.execute(sql, val)

                    for com in d['response']:

                        if com['author']["isAnonymous"] is False:

                            sql = "INSERT IGNORE INTO comments (comment_id, comment_likes, comment_dislikes, num_reports, " \
                                  "created_at, editable_until, message, is_spam," \
                                  "is_deleted, is_deleted_by_author, is_approved, is_flagged," \
                                  "raw_message, is_highlighted, can_vote, points, is_edited, " \
                                  "sb, forum, thread, cursor_id, author_id, parent_comment_id) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (
                                com['id'], com['likes'], com['dislikes'], com['numReports'],
                                com['createdAt'], com['editableUntil'], com['message'], com['isSpam'],
                                com['isDeleted'], com['isDeletedByAuthor'], com['isApproved'], com['isFlagged'],
                                com['raw_message'], com['isHighlighted'], com['canVote'], com['points'],
                                com['isEdited'], com['sb'], com['forum'], com['thread'], d['cursor']['id'],
                                com['author']['id'], com['parent'])

                            mycursor.execute(sql, val)

                            bio = com['author']

                            sql = "INSERT IGNORE INTO authors (author_id, username, about, author_name, " \
                                  "disable_trackers, is_power_contributor, joined_at, profile_url, " \
                                  "is_private, is_primary, is_anonymous, url, location) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (
                                bio['id'], bio['username'], bio['about'], bio['name'], bio['disable3rdPartyTrackers'],
                                bio['isPowerContributor'], bio['joinedAt'], bio['profileUrl'], bio['isPrivate'],
                                bio['isPrimary'], bio['isAnonymous'], bio['url'], bio['location'])
                            mycursor.execute(sql, val)

                            ava = bio['avatar']
                            avatar = {
                                'author_id': bio['id'],
                                'permalink': ava['permalink'],
                                'small_permalink': ava['small']['permalink'],
                                'small_cache': ava['small']['cache'],
                                'large_permalink': ava['large']['permalink'],
                                'large_cache': ava['large']['cache']
                            }

                            sql = "INSERT IGNORE INTO avatars (author_id, permalink, small_permalink, small_cache, " \
                                  "large_permalink, large_cache) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s)"
                            val = (
                                bio['id'], ava['permalink'], ava['small']['permalink'], ava['small']['cache'],
                                ava['large']['permalink'], ava['large']['cache'])
                            mycursor.execute(sql, val)

                        else:

                            sql = "INSERT IGNORE INTO comments (comment_id, comment_likes, comment_dislikes, num_reports, " \
                                  "created_at, editable_until, message, is_spam," \
                                  "is_deleted, is_deleted_by_author, is_approved, is_flagged," \
                                  "raw_message, is_highlighted, can_vote, points, is_edited, " \
                                  "sb, forum, thread, cursor_id, author_id, parent_comment_id) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (
                                com['id'], com['likes'], com['dislikes'], com['numReports'],
                                com['createdAt'], com['editableUntil'], com['message'], com['isSpam'],
                                com['isDeleted'], com['isDeletedByAuthor'], com['isApproved'], com['isFlagged'],
                                com['raw_message'], com['isHighlighted'], com['canVote'], com['points'],
                                com['isEdited'], com['sb'], com['forum'], com['thread'], d['cursor']['id'],
                                "Unknown", com['parent'])

                            mycursor.execute(sql, val)



            except Exception as e:
                print(fname)
                print(str(e))
                break

mydb.commit()