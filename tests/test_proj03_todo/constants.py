"""
Variables used across the test
"""


from fastapi_udemy_course.proj03_todo.hashing import Hasher

TEST_PWD = 'test123'
HASHED_PASSWORD = Hasher.hash_password(TEST_PWD)

USER_DATA = [{"email_address": "praveen@gmail.com", "first_name": "praveen", "last_name": "ilangovan", "hashed_password": HASHED_PASSWORD, "role": "admin"},
        {"email_address": "praveen1@gmail.com", "first_name": "praveen", "last_name": "kumar", "hashed_password": HASHED_PASSWORD, "role": "user"}]

TODO_ITEMS = [{"title":"Test", "description":"Test item 1", "priority":5, "complete":False, "owner_id" : 1},
              {"title":"Test", "description":"Test item 2", "priority":5, "complete":True, "owner_id" : 1},
              {"title":"Test", "description":"Test item 3", "priority":4, "complete":False, "owner_id" : 1},
              {"title":"Test", "description":"Test item 4", "priority":2, "complete":False, "owner_id" : 1},
              {"title":"Test", "description":"Test item 5", "priority":1, "complete":True, "owner_id" : 1},
              {"title":"Test", "description":"Test item 21", "priority":5, "complete":False, "owner_id" : 2},
              {"title":"Test", "description":"Test item 22", "priority":1, "complete":False, "owner_id" : 2},
              {"title":"Test", "description":"Test item 22", "priority":1, "complete":False, "owner_id" : 3}
             ]

NUMBER_OF_OWNER_ID_1_ITEMS = 5
NUMBER_OF_TODO_ITEMS = len(TODO_ITEMS)
