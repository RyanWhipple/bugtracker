from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User

class Thought:
    def __init__(self, data):
        self.id                 = data['id']
        self.content            = data['content']
        self.user_id            = data['user_id']
        self.thinker            = None
        self.users_who_liked    = []


    # Validate Thought
    @staticmethod
    def validate_thought(thought, methods=['POST']):
        is_valid = True # we assume this is true
        if len(thought['content']) < 5:
            flash("Thought must be at least 5 characters.")
            is_valid = False
        return is_valid


    # Add/Save a Thought
    @classmethod
    def add_thought(cls, data):
        query = "INSERT INTO thoughts (content, user_id) VALUES ( %(content)s, %(user_id)s ) "
        return connectToMySQL().query_db(query, data)


    # Delete a Thought
    @classmethod
    def delete(cls, data):
        query="DELETE FROM thoughts WHERE id = %(id)s"
        return connectToMySQL().query_db(query, data)


    # Get All Liked Thoughts for a User
    @classmethod
    def get_all_users_liked_thoughts(cls, data):
        thoughts_liked = []
        query = "SELECT thought_id FROM likes JOIN users ON users.id = user_id WHERE user_id = %(id)s"
        results = connectToMySQL().query_db(query, data)
        for result in results:
            thoughts_liked.append(result['thought_id'])
        return thoughts_liked


    # Like a Thought
    @classmethod
    def like_thought(cls, data):
        query = "INSERT INTO likes(thought_id, user_id) VALUES(%(thought_id)s, %(user_id)s)"
        return connectToMySQL().query_db(query, data)


    # Dislike a Thought
    @classmethod
    def dislike_thought(cls, data):
        query = "DELETE FROM likes WHERE thought_id=%(thought_id)s AND user_id=%(user_id)s "
        return connectToMySQL().query_db(query, data)


    # Get All Thoughts
    # Attach a List of Users who liked the Thought to each Thought
    @classmethod
    def get_all_thoughts(cls):
        query = "SELECT * FROM thoughts "\
                "LEFT JOIN users ON users.id = thoughts.user_id "\
                "LEFT JOIN likes ON thoughts.id = likes.thought_id "\
                "LEFT JOIN users AS users2 ON users2.id = likes.user_id "\
                "ORDER BY thoughts.id DESC"
        
        results = connectToMySQL().query_db(query)
        all_thoughts = []

        
        for result in results:      #   Iterate through all results
            new_thought = True      #   Assume the thought is new
            like_user_data = {      #   Populate dict "like_user"data" with the data of the user who liked the thought
                'id'            :   result['users2.id'],
                'first_name'    :   result['users2.first_name'],
                'last_name'     :   result['users2.last_name'],
                'email'         :   result['users2.email'],
                'password'      :   result['users2.password'],
            }

            if len(all_thoughts) > 0 and all_thoughts[len(all_thoughts) -1].id == result['id']:     #   If the last thought in all_thoughts has the same id as the thought held by "result"...  (Check that there are any thoughts at all in all_thoughts first)
                all_thoughts[len(all_thoughts)-1].users_who_liked.append(User(like_user_data))      #   ...append the User who liked the thought to that thought's users_who_liked list...
                new_thought = False                                                                 #   ...and set new_thought to False

            if new_thought:                                                                         #   Otherwise...
                thought = cls(result)                                                               #   Construct a new thought from "result"
                thinker_data = {                                                                    #   Construct the thinker from "result"
                    'id'            :   result['users.id'],
                    'first_name'    :   result['first_name'],
                    'last_name'     :   result['last_name'],
                    'email'         :   result['email'],
                    'password'      :   result['password'],
                }
                thought.thinker = User(thinker_data)                                                #   Set thought's thinker to the constructed thinker
                if result['users2.id'] is not None:                                                 #   If the thinker liked their ouwn post...
                    thought.users_who_liked.append(User(like_user_data))                            #   ...append them to the users_who_liked list
                all_thoughts.append(thought)                                                        #   Append thought to all_thoughts

        return all_thoughts

    
    # Get Thoughts for a given User ID
    # This powers route "/users/<int:id>"
    @classmethod
    def get_user_thoughts(cls, data):

        query = "SELECT * FROM thoughts WHERE user_id = %(user_id)s"
        thoughts = connectToMySQL().query_db(query, data)
        results = []
        for thought in thoughts:
            results.append(cls(thought))
        return results


    # Get a Thought by ID
    @classmethod
    def get_thought(cls, data):
        query="SELECT * FROM thoughts WHERE id = %(id)s"
        results=connectToMySQL().query_db(query, data)
        if len(results) < 1:
            return False
        return results[0]


    
#   UNUSED
    




    # Update a Thought by ID
    @classmethod
    def update(cls, data):
        query = "UPDATE thoughts SET content = %(content)s, user_id = %(user_id)s WHERE id=%(id)s"
        return connectToMySQL().query_db(query, data)


    # Get All Thoughts
    # Simple
    @classmethod
    def get_all(cls):
        query="SELECT * FROM thoughts ORDER BY users.id DESC"
        results=connectToMySQL().query_db(query)
        return results


    # Get all Thoughts with User attached
    @classmethod
    def get_all_with_user(cls):
        query="SELECT * FROM thoughts JOIN users on user_id = users.id ORDER BY users.id DESC"
        results=connectToMySQL().query_db(query)
        return results