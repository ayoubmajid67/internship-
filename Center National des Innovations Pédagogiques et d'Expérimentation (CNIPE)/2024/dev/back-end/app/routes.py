from flask import Blueprint, jsonify, request, current_app, send_from_directory, abort
from functools import wraps
import jwt
import datetime
import os


# from bson.objectid import ObjectId
# from app import mongo
import app.models.user as user_model
import app.models.formation as formation_model
import app.utile as utile
import bcrypt
import app.file_utils as file_utils

bp = Blueprint('api', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user_model.get_All_by_email(data['email'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['accountType'] not in ['admin', 'owner']:
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


def owner_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['accountType'] != 'owner':
            return jsonify({'message': 'Owner access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


# User routes

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    required_fields = ['username', 'email', 'password']
    missing_fields = [
        field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    username = str(data['username']).strip()

    if not utile.validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not utile.validate_password(password):
        return jsonify({'error': 'Invalid password format'}), 400

    if user_model.get_user_by_email(email):
        return jsonify({'error': 'User already exists'}), 400

    if user_model.get_user_by_username(username):
        return jsonify({'error': 'User already exists'}), 400

    result = user_model.add_user(username, email, password)

    return jsonify({'message': 'User registered successfully'}), 201


@bp.route('/registerAdmin', methods=['POST'])
@token_required
@owner_required
def register_Admin(current_user):
    data = request.get_json() or {}
    required_fields = ['username', 'email', 'password']
    missing_fields = [
        field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    username = str(data['username']).strip()

    if not utile.validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not utile.validate_password(password):
        return jsonify({'error': 'Invalid password format'}), 400

    if user_model.get_admin_by_email(email):
        return jsonify({'error': 'Admin already exists'}), 400

    if user_model.get_admin_by_username(username):
        return jsonify({'error': 'Admin already exists'}), 400

    result = user_model.add_admin(username, email, password)

    return jsonify({'message': 'Admin registered successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    required_fields = ['email', 'password']
    missing_fields = [
        field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    email = str(data.get('email')).strip().lower()
    password = str(data.get('password')).strip()

    user = user_model.get_All_by_email(email)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = utile.generate_token(email)
    username = user["username"]
    profileImg = user["profileImg"]
    return jsonify({'message': "User login successfully", 'token': token, 'username': username, 'profileImg': profileImg})


@bp.route('/dropUser', methods=['DELETE'])
@token_required
@admin_required
def drop_user(current_user):
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required to drop a user'}), 400

    user = user_model.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_model.delete_user(email)
    return jsonify({'message': 'User deleted successfully'}), 200


@bp.route('/dropAdmin', methods=['DELETE'])
@token_required
@owner_required
def drop_admin(current_user):
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required to drop an admin'}), 400

    admin = user_model.get_admin_by_email(email)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    user_model.delete_admin(email)
    return jsonify({'message': 'Admin deleted successfully'}), 200


@bp.route('/getUsers', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    users = user_model.get_users()
    return jsonify(users), 200


@bp.route('/getAdmins', methods=['GET'])
@token_required
@owner_required
def get_admins(current_user):
    users_and_admins = user_model.get_admins()
    return jsonify(users_and_admins), 200


@bp.route('/getUsersAndAdmins', methods=['GET'])
@token_required
@owner_required
def get_users_and_admins(current_user):
    users_and_admins = user_model.get_users_and_admins()
    return jsonify(users_and_admins), 200


@bp.route('/stats', methods=['GET'])
def get_stats():
    # Get the count of users
    user_count =user_model.get_number_of_users()

    # Get the count of courses
    formation_count = formation_model.get_number_of_formations()
    course_count = 0
    video_count = 0

    # Count courses and videos
    formations = formation_model.get_simple_formations()
    for formation in formations:
        courses = formation.get('courses', [])
        course_count += len(courses)
        for course in courses:
            videos = course.get('courseContent', [])
            video_count += len(videos)

    stats = {
        "numberOfUsers": user_count,
        "numberOfCategories":formation_count,
        "numberOfCourses": course_count,
        "numberOfVideos": video_count
    }

    return jsonify(stats), 200

@bp.route('/userRole', methods=['GET'])
@token_required
def get_user_role(current_user):
    user_role = current_user.get('accountType')
    if not user_role : 
        return jsonify({"error":"invalid user type"})
    return jsonify({"role": user_role}), 200


# Formation routes
@bp.route('/formations', methods=['GET'])
def get_all_formations():
    formations = formation_model.get_formations()
    return jsonify(formations)


@bp.route('/profiles/<filename>', methods=['GET'])
def uploaded_file(filename):
    try:
        # Ensure filename is safe and properly sanitized
        safe_filename = os.path.basename(filename)

        # Construct the path to the directory where profiles are stored
        profile_directory = os.path.abspath(os.path.join(
            current_app.root_path, '..', 'data', 'profiles'))

        # Check if file exists
        file_path = os.path.join(profile_directory, safe_filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Serve the file from the specified directory
        return send_from_directory(profile_directory, safe_filename)
    except Exception as e:
        return jsonify({'error': 'Error serving file', 'details': str(e)}), 500


# @bp.route('/test', methods=['GET'])
# def test():
#     file_utils.create_category_dir("cours sur l'images")
#     file_utils.create_category_dir("cours sur le son")
#     file_utils.create_category_dir("cours sur le montage")
#     file_utils.create_category_dir("cours sur l'éclairage")


# formations :
@bp.route('/formations', methods=['POST'])
@token_required
@admin_required
def create_formation(current_user):
    data = request.form
    missing_fields = utile.validate_fields(
        data, ['categoryName', "description"])
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    categoryName = str(data["categoryName"]).strip().lower()

    sanitized_categoryName = file_utils.sanitize_filename(categoryName)
    description = str(data["description"]).strip()
    thumbnail_file = request.files.get('thumbnail')

    if formation_model.get_formation_by_category(sanitized_categoryName):
        return jsonify({'error': 'Formation with this category already exists'}), 400

    file_utils.create_category_dir(sanitized_categoryName)
    file_utils.save_category_thumbnail(sanitized_categoryName, thumbnail_file)
    formation_model.add_formation(sanitized_categoryName, description)

    return jsonify({'message': f'Formation created successfully :{sanitized_categoryName} / {categoryName}'}), 201


@bp.route('/formations/<category_name>/thumbnails/', methods=['GET'])
def get_category_thumbnail(category_name):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    category_dir = os.path.join(file_utils.CATEGORIES_DIR, category_name)
    return send_from_directory(category_dir, f"{category_name}_thumbnail.jpg")


@bp.route('/formations', methods=['POST'])
def get_formations():
    formations = formation_model.get_formations()

    return jsonify(formations), 201


@bp.route('/formations/<category_name>', methods=['GET'])
def get_single_formation_by_category(category_name):
    sanitized_category_name = file_utils.sanitize_filename(
        category_name.strip().lower())
    formation = formation_model.get_formation_by_category(
        sanitized_category_name)
    if formation:
        return jsonify(formation)
    return jsonify({'error': 'Formation not found'}), 404


@bp.route('/formations/<category_name>', methods=['PUT'])
@token_required
@admin_required
def update_single_formation_category(current_user, category_name):
    data = request.form 
    sanitized_category_name = file_utils.sanitize_filename(
        category_name.strip().lower())

    formation = formation_model.get_formation_by_category(
        sanitized_category_name)
    if not formation:
        return jsonify({'error': 'Formation not found'}), 404

    new_category_name = str(data.get('newCategoryName', '')).strip().lower()
    sanitized_new_category_name = file_utils.sanitize_filename(
        new_category_name)
    new_description = str(data.get('newDescription', '')).strip()
    thumbnail_file = request.files.get('thumbnail')

    if not new_category_name and not new_description and not thumbnail_file:
        return jsonify({'error': 'Either newCategoryName or newDescription  or thumbnail must be provided'}), 400

    if new_category_name and formation_model.get_formation_by_category(sanitized_new_category_name):
        return jsonify({'error': 'Category name already exists'}), 400

    if thumbnail_file :
       file_utils.save_category_thumbnail(sanitized_category_name, thumbnail_file)
    update_fields = {}
    if new_category_name:
        update_fields['categoryName'] = sanitized_new_category_name
        file_utils.update_category_dir(
            sanitized_category_name, sanitized_new_category_name)

    if new_description:
        update_fields['description'] = new_description

    formation_model.update_formation_by_category(
        sanitized_category_name, update_fields)

    return jsonify({'message': 'Formation updated successfully'})


@bp.route('/formations/<category_name>', methods=['DELETE'])
@token_required
@admin_required
def delete_single_formation_by_category(current_user, category_name):
    sanitized_category_name = file_utils.sanitize_filename(
        category_name.strip().lower())
    result = formation_model.delete_formation_by_category(
        sanitized_category_name)
    if result.deleted_count:
        file_utils.delete_category_dir(sanitized_category_name)
        return jsonify({'message': 'Formation deleted successfully'})
    return jsonify({'error': 'Formation not found'}), 404


# Course routes
@bp.route('/formations/<category_name>/courses', methods=['POST'])
@token_required
@admin_required
def create_course(current_user, category_name):
    data = request.form
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(
        str(data.get('courseName', '')).strip().lower())

    if formation_model.get_course_from_formation_by_name(category_name, course_name):
        return jsonify({'error': f'Formation with {category_name} category already contains {course_name} course'}), 404

    missing_fields = utile.validate_fields(data, ['courseName', 'description'])
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    course_description = str(data.get('description', '')).strip().lower()

    if not formation_model.get_formation_by_category(category_name):
        return jsonify({'error': 'Formation with this category does not exist'}), 404
    thumbnail_file = request.files.get('thumbnail')

    file_utils.create_course_dir(category_name, course_name)
    file_utils.save_course_thumbnail(category_name,course_name ,thumbnail_file)
    formation_model.add_course_to_formation(
        category_name, course_name, course_description)

    return jsonify({'message': 'Course created successfully'}), 201

@bp.route('/formations/<category_name>/courses/<course_name>/thumbnails/', methods=['GET'])
def get_course_thumbnail(category_name,course_name):

    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())
    course_dir = os.path.join(file_utils.CATEGORIES_DIR, category_name,course_name)
    print(course_dir,f"\{course_name}_thumbnail.jpg")
    return send_from_directory(course_dir, f"{course_name}_thumbnail.jpg")


@bp.route('/formations/<category_name>/courses/<course_name>', methods=['GET'])
@token_required
def get_course_by_name(current_user, category_name, course_name):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())

    course = formation_model.get_course_from_formation_by_name(
        category_name, course_name)
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404


@bp.route('/formations/<category_name>/courses/<course_name>', methods=['PUT'])
@token_required
@admin_required
def update_course_route(current_user, category_name, course_name):
    category_name = file_utils.sanitize_filename(category_name.lower().strip())
    course_name = file_utils.sanitize_filename(course_name.lower().strip())

    if not formation_model.get_course_from_formation_by_name(category_name, course_name):
        return jsonify({'error': f'Formation with {category_name} category does not contain {course_name} course'}), 404

    data = request.form

    if not (data.get('courseName') or data.get('description') or data.get('thumbnail')):
        return jsonify({'error': 'At least one field (courseName or description or thumbnail) is required'}), 400

    new_course_name = file_utils.sanitize_filename(str(data.get('courseName', '')).strip().lower())
    new_course_description = str(data.get('description', '')).strip().lower()

    if new_course_name:
        existing_course = formation_model.get_course_from_formation_by_name(
            category_name, new_course_name)
        if existing_course:
            return jsonify({'error': 'Course name already exists'}), 400


    thumbnail_file = request.files.get('thumbnail')
    if thumbnail_file :
        file_utils.save_course_thumbnail(category_name,course_name ,thumbnail_file)


    update_fields = {}
    if new_course_name:
        update_fields['courseName'] = new_course_name
        file_utils.update_course_dir(category_name, course_name, new_course_name)
    if new_course_description:
        update_fields['description'] = new_course_description

    formation_model.update_course_in_formation(
        category_name, course_name, update_fields)
    



    return jsonify({'message': 'Course updated successfully'})


@bp.route('/formations/<category_name>/courses/<course_name>', methods=['DELETE'])
@token_required
@admin_required
def delete_course_route(current_user, category_name, course_name):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())

    result = formation_model.remove_course_from_formation(
        category_name, course_name)
    if result.modified_count:
        file_utils.delete_course_dir(category_name, course_name)
        return jsonify({'message': 'Course deleted successfully'})
    return jsonify({'error': 'Course not found'}), 404


# Comment routes
@bp.route('/formations/<category_name>/courses/<course_name>/comments', methods=['POST'])
@token_required
def create_comment(current_user, category_name, course_name):
    data = request.get_json() or {}
    missing_fields = utile.validate_fields(data, ['message'])
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())
    
    if not formation_model.get_course_from_formation_by_name(category_name, course_name):
        return jsonify({'error': 'Course not found'}), 404

    message = str(data['message']).strip()

    result = formation_model.add_comment_to_course_by_name(
        category_name, course_name, message, current_user)
    if result.modified_count:
        return jsonify({'message': 'Comment added successfully'})
    return jsonify({'error': 'Course not found'}), 404


@bp.route('/formations/<category_name>/courses/<course_name>/comments/<comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, category_name, course_name, comment_id):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())
    data = request.get_json() or {}
    message = str(data['message']).strip()
    if 'message' not in data or not message:
        return jsonify({'error': 'Message field is required'}), 400

    course = formation_model.get_course_from_formation_by_name(
        category_name, course_name)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    comment = next((c for c in course.get('comments', [])
                   if str(c['_id']) == comment_id), None)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if comment['email'] == current_user['email']:
        result = formation_model.update_comment_message(
            category_name, course_name, comment_id, message)
        if result.modified_count == 1:
            return jsonify({'message': 'Comment updated successfully'})
        else:
            return jsonify({'error': 'Failed to update comment'}), 500
    else:
        return jsonify({'error': 'Permission denied'}), 403


@bp.route('/formations/<category_name>/courses/<course_name>/comments/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, category_name, course_name, comment_id):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())

    course = formation_model.get_course_from_formation_by_name(
        category_name, course_name)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    comment = next((c for c in course.get('comments', [])
                   if str(c['_id']) == comment_id), None)
    print("the comment :", comment)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if current_user['accountType'] in ['admin', 'owner'] or comment['email'] == current_user['email']:
        result = formation_model.delete_comment_from_course_by_name(
            category_name, course_name, comment_id)
        if result.modified_count == 1:
            return jsonify({'message': 'Comment deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete comment'}), 500
    else:
        return jsonify({'error': 'Permission denied'}), 403


def add_course_content(category_name, course_name):
    category_name = category_name.strip().lower()
    course_name = course_name.strip().lower()

    if 'video' not in request.files:
        return jsonify({'error': 'Video file is required'}), 400

    video_file = request.files['video']
    title = file_utils.sanitize_filename(
        str(request.form.get('title', '')).strip().lower())
    description = str(request.form.get('description', '')).strip()
    thumbnail = request.files.get('thumbnail')

    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    if not formation_model.get_course_from_formation_by_name(category_name, course_name):
        return jsonify({'error': 'Course not found'}), 404

    existing_content = formation_model.get_course_content_by_title(
        category_name, course_name, title)
    if existing_content:
        return jsonify({'error': 'Course content with the same title already exists'}), 400

    video_info = file_utils.save_video_and_thumbnail(
        category_name, course_name, title, video_file, thumbnail)

    course_content = formation_model.create_course_content_object(
        category_name, course_name, title, video_info, description)

    result = formation_model.create_course_content(category_name, course_name, course_content)

    if result.modified_count:
        return jsonify({'message': 'Course content added successfully'}), 201
    return jsonify({'error': 'Failed to add course content'}), 500


@bp.route('/formations/<category_name>/courses/<course_name>/content', methods=['POST'])
@token_required
@admin_required
def add_course_content_route(current_user, category_name, course_name):
    return add_course_content(category_name, course_name)


@bp.route('/formations/<category_name>/courses/<course_name>/videos/<filename>', methods=['GET'])
def get_video(category_name, course_name, filename):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())
    filename = file_utils.sanitize_filename(filename)

    video_dir = os.path.join(file_utils.CATEGORIES_DIR,
                             category_name, course_name, 'videos', filename)
    return send_from_directory(video_dir, f"{filename}_video.mp4")


@bp.route('/formations/<category_name>/courses/<course_name>/thumbnails/<filename>', methods=['GET'])
def get_thumbnail(category_name, course_name, filename):
    category_name = file_utils.sanitize_filename(category_name.strip().lower())
    course_name = file_utils.sanitize_filename(course_name.strip().lower())
    thumbnail_dir = os.path.join(
        file_utils.CATEGORIES_DIR, category_name, course_name, 'videos', filename)
    return send_from_directory(thumbnail_dir, f"{filename}_thumbnail.jpg")


@bp.route('/formations/<category_name>/courses/<course_name>/content/<title>', methods=['PUT'])
@token_required
@admin_required
def update_course_content(current_user, category_name, course_name, title):


    if 'video' not in request.files and 'thumbnail' not in request.files and 'title' not in request.form:
      return jsonify({"error": "No video, thumbnail, or title provided"}), 400

    # Find the course content to be deleted
    title = file_utils.sanitize_filename(title.lower().strip())
    course_content = formation_model.get_course_content_by_title(
        category_name, course_name, title)

    if not course_content:
        return  jsonify({ "error" :'Course content not found'}),404

    video_file = request.files.get('video')
    thumbnail_file = request.files.get('thumbnail')
    new_title=str(request.form.get("title")).lower().strip()

 
    new_title =file_utils.sanitize_filename(new_title)
    print(new_title)


    if new_title  and formation_model.get_course_content_by_title(category_name, course_name, new_title):
                return jsonify({'error': ' video Title already exists'}), 400
    

    
    update_data = {}
    if new_title : 
        update_data['title']=new_title
        file_utils. update_course_content_dir(category_name,course_name,title,new_title)

    if video_file:
        video_info = file_utils.save_video(
            category_name, course_name, new_title, video_file)
        update_data['duration'] = video_info['duration']

    if thumbnail_file:
        file_utils.save_thumbnail(
            category_name, course_name, new_title, thumbnail_file)

    # Update the course content in the database
    result = formation_model.update_course_content_in_db(category_name, course_name, title, update_data)

    if result.matched_count == 0:
        return jsonify({"error":"Course content not found"}), 404

    return  jsonify({"message":'Course content updated successfully'}), 200


import shutil
@bp.route('/formations/<category_name>/courses/<course_name>/content/<title>', methods=['DELETE'])
@token_required
@admin_required
def delete_course_content(current_user, category_name, course_name, title):
    # Find the course content to be deleted
    title = file_utils.sanitize_filename(title.lower().strip())
    course_content = formation_model.get_course_content_by_title(
        category_name, course_name, title)

    if not course_content:
        return 'Course content not found', 404

    contentPath = os.path.join(file_utils.CATEGORIES_DIR, category_name, course_name, 'videos', title)

    if os.path.exists(contentPath):
        shutil.rmtree(contentPath)
  

    # Remove the course content from the database
    result = formation_model.delete_course_content_in_db(
        category_name, course_name, title)
    if result.modified_count == 0:
        return jsonify({"error" :"Failed to delete course content"}), 500

    return   jsonify({"message"'Course content deleted successfully'}), 200


