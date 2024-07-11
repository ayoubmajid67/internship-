from app import mongo
import bcrypt


from flask import request


def get_user_json_structure(username, email, password, accountType):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Construct the full path to the default profile image
    server_ip = request.host.split(':')[0]
    server_port = request.host.split(':')[1] if ':' in request.host else '80'
    default_profile_image = f"http://{server_ip}:{server_port}/profiles/default_profile.png"
    print(default_profile_image)
    user = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'accountType': accountType,
        'status': 'active',
        "profileImg": default_profile_image,
        'canComment': True
    }
    return user

# User Functions


def add_user(username, email, password):
    user = get_user_json_structure(username, email, password, "normal")
    return mongo.db.users.insert_one(user)


def get_user_by_email(email):
    return mongo.db.users.find_one({'email': email, 'accountType': 'normal'}, {'_id': 0})


def get_user_by_username(username):
    return mongo.db.users.find_one({'username': username, 'accountType': 'normal'}, {'_id': 0})


def update_user_status(user_email, status):
    return mongo.db.users.update_one(
        {'email': user_email, 'accountType': 'normal'},
        {'$set': {'status': status}}
    )


def get_users():
    return list(mongo.db.users.find({'accountType': 'normal'}, {'password': 0, '_id': 0}))


def block_user_from_comment(user_email):
    return mongo.db.users.update_one(
        {'email': user_email, 'accountType': 'normal'},
        {'$set': {'canComment': False}}
    )


def delete_user(email):
    return mongo.db.users.delete_one({'email': email, 'accountType': 'normal'})

# Admin Functions


def add_admin(username, email, password):
    user = get_user_json_structure(username, email, password, "admin")
    return mongo.db.users.insert_one(user)


def remove_admin(email):
    return mongo.db.users.delete_one({'email': email, 'accountType': 'admin'})


def get_admins():
    return list(mongo.db.users.find({'accountType': 'admin'}, {'password': 0, '_id': 0}))


def get_admin_by_email(email):
    return mongo.db.users.find_one({'email': email, 'accountType': 'admin'}, {'_id': 0})


def get_admin_by_username(username):
    return mongo.db.users.find_one({'username': username, 'accountType': 'admin'}, {'_id': 0})


# Owner Functions
def get_users_and_admins():
    return list(mongo.db.users.find({'accountType': {'$in': ['normal', 'admin']}}, {'password': 0, '_id': 0}))


def add_owner(username, email, password):
    user = get_user_json_structure(username, email, password, "owner")
    return mongo.db.users.insert_one(user)


def remove_owner(email):
    return mongo.db.users.delete_one({'email': email, 'accountType': 'owner'})


def get_owner_by_email(email):
    return mongo.db.users.find_one({'email': email, 'accountType': 'owner'}, {'_id': 0})


def get_owner_by_username(username):
    return mongo.db.users.find_one({'username': username, 'accountType': 'owner'}, {'_id': 0})


def get_owners():
    return list(mongo.db.users.find({'accountType': 'owner'}, {'password': 0, '_id': 0}))


def delete_admin(email):
    return mongo.db.users.delete_one({'email': email, 'accountType': 'admin'})


def get_All_by_email(email):
    return mongo.db.users.find_one({'email': email}, {'_id': 0})


def get_All_by_username(username):
    return mongo.db.users.find_one({'email': username}, {'_id': 0})


# add_owner("youbista","ayoubmajjid@gmail.com","MajjidDev2024")
# add_owner("dnau","dnau@gmail.com","dnauDev2024")