from app import mongo
from bson.objectid import ObjectId

def add_course(course_name, category_name, created_date, course_content):
    course = {
        'courseName': course_name,
        'categoryName': category_name,
        'createdDate': created_date,
        'courseContent': course_content,
        'comments': []
    }
    return mongo.db.courses.insert_one(course)

def get_courses():
    return list(mongo.db.courses.find())

def get_course(course_id):
    return mongo.db.courses.find_one({'_id': ObjectId(course_id)})

def update_course(course_id, data):
    return mongo.db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': data})

def delete_course(course_id):
    return mongo.db.courses.delete_one({'_id': ObjectId(course_id)})
