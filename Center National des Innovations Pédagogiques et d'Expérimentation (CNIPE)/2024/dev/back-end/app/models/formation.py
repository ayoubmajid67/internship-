from flask import request
from app import mongo
from bson.objectid import ObjectId
import datetime


def add_formation(category_name, description):
    formation = {
        'categoryName': category_name,
        'createdDate': datetime.datetime.utcnow(),
        "description": description,
        'courses': []
    }
    mongo.db.formations.insert_one(formation)

# def get_formations():
#     return list(mongo.db.formations.find())


def get_formations():
    pipeline = [
        {
            '$project': {
                '_id': 0,
                'categoryName': 1,
                'createdDate': 1,
                'coursesSize': {
                    '$size': '$courses'
                },
                'totalLikes': {
                    '$sum': {
                        '$map': {
                            'input': '$courses',
                            'as': 'course',
                            'in': {
                                '$sum': {
                                    '$ifNull': [
                                        {
                                            '$sum': {
                                                '$map': {
                                                    'input': '$course.courseContent',
                                                    'as': 'content',
                                                    'in': '$content.nbrOfLikes'
                                                }
                                            }
                                        },
                                        0
                                    ]
                                }
                            }
                        }
                    }
                },
                'averageReview': {
                    '$avg': {
                        '$map': {
                            'input': '$courses',
                            'as': 'course',
                            'in': {
                                '$ifNull': [
                                    {
                                        '$convert': {
                                            'input': '$course.review',
                                            'to': 'double',
                                            'onError': 0
                                        }
                                    },
                                    0
                                ]
                            }
                        }
                    }
                }
            }
        },
        {
            '$project': {
                'categoryName': 1,
                'createdDate': 1,
                'courses': {
                    'size': '$coursesSize',
                    'totalLikes': '$totalLikes',
                    'averageReview': {
                        '$cond': {
                            'if': {'$eq': ['$coursesSize', 0]},
                            'then': 0,
                            'else': {
                                '$ifNull': ['$averageReview', 0]
                            }
                        }
                    }
                }
            }
        }
    ]
    return list(mongo.db.formations.aggregate(pipeline))


def get_formation_by_category(category_name):
    return mongo.db.formations.find_one({'categoryName': category_name}, {'_id': 0, 'courses.courseContent': 0})


def update_formation_by_category(old_category_name, update_fields):
    return mongo.db.formations.update_one(
        {'categoryName': old_category_name},
        {'$set': update_fields}
    )


def delete_formation_by_category(category_name):
    return mongo.db.formations.delete_one({'categoryName': category_name})


def get_course_json_Structure(course_name, description):
    return {
        "courseName": course_name,
        "createdDate": datetime.datetime.utcnow(),
        "description": description,
        "review": "",
        "comments": "",
        "courseContent": []
    }


def add_course_to_formation(category_name, course_name, course_description):
    course = get_course_json_Structure(course_name, course_description)
    mongo.db.formations.update_one(
        {'categoryName': category_name},
        {'$addToSet': {'courses': course}}
    )


def update_course_in_formation(category_name, course_name, data):
    # Normalize inputs
    new_course_name = data.get('courseName', '')
    new_description = data.get('description', '')

    # Build update document dynamically
    update_doc = {}
    if new_course_name:
        update_doc['courses.$.courseName'] = new_course_name
    if new_description:
        update_doc['courses.$.description'] = new_description

    # Perform the update operation
    mongo.db.formations.update_one(
        {'categoryName': category_name, 'courses.courseName': course_name},
        {'$set': update_doc}
    )


def remove_course_from_formation(category_name, course_name):
    return mongo.db.formations.update_one(
        {'categoryName': category_name},
        {'$pull': {'courses': {'courseName': course_name}}}
    )


def get_course_from_formation_by_name(category_name, course_name):
    formation = mongo.db.formations.find_one(
        {'categoryName': category_name, 'courses.courseName': course_name})
    if formation:
        course = next((c for c in formation.get('courses', [])
                      if c['courseName'] == course_name), None)
        if course:
            return course
    return None
# comments :


def get_comment_json(message, category_name, course_name, current_user):
    # Create the JSON structure for the comment
    return {
        '_id': str(ObjectId()),  # Generate a unique ID for the comment
        'email': current_user['email'],
        'username': current_user['username'],
        'message': message,
        'formationCategory': category_name,
        'courseName': course_name,
        'createdDate':  datetime.datetime.utcnow()
    }


def add_comment_to_course_by_name(category_name, course_name, comment_message, current_user):
    # Generate the JSON structure for the comment
    comment_json = get_comment_json(
        comment_message, category_name, course_name, current_user)

    # Update the formation with the JSON comment
    return mongo.db.formations.update_one({'categoryName': category_name, 'courses.courseName': course_name}, {'$addToSet': {'courses.$.comments': comment_json}})


def update_comment_message(category_name, course_name, comment_id, new_message):
    return mongo.db.formations.update_one(
        {'categoryName': category_name, 'courses.courseName': course_name,
            'courses.comments._id': comment_id},
        {'$set': {
            'courses.$[course].comments.$[comment].message': new_message}},
        array_filters=[{'course.courseName': course_name},
                       {'comment._id': comment_id}]
    )


def delete_comment_from_course_by_name(category_name, course_name, comment_id):
    return mongo.db.formations.update_one(
        {'categoryName': category_name, 'courses.courseName': course_name},
        {'$pull': {'courses.$.comments': {'_id': comment_id}}}
    )


def get_course_content_by_title(category_name, course_name, title):
    formation = mongo.db.formations.find_one(
        {'categoryName': category_name, 'courses.courseName': course_name})
    if formation:
        course = next((c for c in formation.get('courses', [])
                      if c['courseName'] == course_name), None)
        if course:
            return next((content for content in course.get('courseContent', []) if content['title'] == title), None)
    return None


def create_course_content_object(category_name, course_name, title, video_info, description):
    server_ip = request.host.split(':')[0]
    server_port = request.host.split(':')[1] if ':' in request.host else '80'
    video_link = f"http://{server_ip}:{server_port}/formations/{
        category_name}/courses/{course_name}/videos/{title}"
    thumbnail_link = f"http://{server_ip}:{server_port}/formations/{
        category_name}/courses/{course_name}/thumbnails/{title}"

    course_content = {
        'videoLink': video_link,
        'thumbnail': thumbnail_link,
        'addedDate': datetime.datetime.utcnow().isoformat(),
        'duration': video_info['duration'],
        'nbrOfLikes': 0,
        'title': title,
        'description': description
    }
    return course_content


def update_course_content_in_db(category_name, course_name, course_content):
    result = mongo.db.formations.update_one(
        {'categoryName': category_name, 'courses.courseName': course_name},
        {'$addToSet': {'courses.$.courseContent': course_content}}
    )
    return result


def delete_course_content_in_db(category_name, course_name, title):
    result = mongo.db.formations.update_one(
        {'categoryName': category_name, 'courses.courseName': course_name},
        {'$pull': {'courses.$.courseContent': {'title': title}}}
    )
    return result
