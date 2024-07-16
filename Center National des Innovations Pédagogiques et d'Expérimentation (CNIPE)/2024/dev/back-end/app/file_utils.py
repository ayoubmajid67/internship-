from werkzeug.utils import secure_filename
import shutil
import moviepy.editor as mp
import os
import re

CATEGORIES_DIR = os.path.join(os.getcwd(),'data', 'categories')


def sanitize_filename(filename):
    # Replace problematic characters with underscores
    return re.sub(r'[\/:*?"<>|]', '_', filename)


def create_category_dir(category_name):
    sanitized_category_name = sanitize_filename(category_name)
    dir_path = os.path.join(CATEGORIES_DIR, sanitized_category_name)
    
    # If the directory exists, clear its contents
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    
    # Create the directory (it will be empty if it already existed)
    os.makedirs(dir_path, exist_ok=True)

def save_category_thumbnail(category_name, thumbnail_file=None):
    sanitized_category_name = sanitize_filename(category_name)
    thumbnail_dir = os.path.join(CATEGORIES_DIR, sanitized_category_name)

    if thumbnail_file:
        thumbnail_filename = f"{sanitized_category_name}_thumbnail.jpg"
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)
        thumbnail_file.save(thumbnail_path)
    else:
        default_thumbnail_path = os.path.join(CATEGORIES_DIR, 'default_category_thumbnail.jpg')
        thumbnail_path = os.path.join(thumbnail_dir, f"{sanitized_category_name}_thumbnail.jpg")
        shutil.copy(default_thumbnail_path, thumbnail_path)

    


def update_category_dir(old_category_name, new_category_name):
    old_sanitized_name = sanitize_filename(old_category_name)
    new_sanitized_name = sanitize_filename(new_category_name)
    old_path = os.path.join(CATEGORIES_DIR, old_sanitized_name)
    new_path = os.path.join(CATEGORIES_DIR, new_sanitized_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)


def delete_category_dir(category_name):
    sanitized_category_name = sanitize_filename(category_name)
    dir_path = os.path.join(CATEGORIES_DIR, sanitized_category_name)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


def create_course_dir(category_name, course_name):
    sanitized_category_name = sanitize_filename(category_name)
    sanitized_course_name = sanitize_filename(course_name)
    course_dir_path = os.path.join(CATEGORIES_DIR, sanitized_category_name, sanitized_course_name)
    videos_dir_path = os.path.join(course_dir_path, "videos")

    # If the course directory exists, clear its contents
    if os.path.exists(course_dir_path):
        shutil.rmtree(course_dir_path)

    # Create the course and videos directories
    os.makedirs(course_dir_path, exist_ok=True)
    os.makedirs(videos_dir_path, exist_ok=True)
    

def save_course_thumbnail(category_name,course_name, thumbnail_file=None):
    sanitized_category_name = sanitize_filename(category_name)
    sanitized_course_name = sanitize_filename(course_name)
    thumbnail_dir = os.path.join(CATEGORIES_DIR,sanitized_category_name,sanitized_course_name)

    if thumbnail_file:
        thumbnail_filename = f"{sanitized_category_name}_thumbnail.jpg"
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)
        thumbnail_file.save(thumbnail_path)
    else:
        default_thumbnail_path = os.path.join(CATEGORIES_DIR, 'default_category_thumbnail.jpg')
        thumbnail_path = os.path.join(thumbnail_dir, f"{sanitized_course_name}_thumbnail.jpg")
        shutil.copy(default_thumbnail_path, thumbnail_path)
 


def update_course_dir(category_name, old_course_name, new_course_name):
    sanitized_category_name = sanitize_filename(category_name)
    old_sanitized_course_name = sanitize_filename(old_course_name)
    new_sanitized_course_name = sanitize_filename(new_course_name)
    old_path = os.path.join(CATEGORIES_DIR, sanitized_category_name, old_sanitized_course_name)
    new_path = os.path.join(CATEGORIES_DIR, sanitized_category_name, new_sanitized_course_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        
        # Update the thumbnail
        old_thumbnail_path = os.path.join(old_path, f'{old_sanitized_course_name}_thumbnail.png')
        new_thumbnail_path = os.path.join(new_path, f'{new_sanitized_course_name}_thumbnail.png')
        
        if os.path.exists(old_thumbnail_path):
            os.rename(old_thumbnail_path, new_thumbnail_path)


def delete_course_dir(category_name, course_name):
    sanitized_category_name = sanitize_filename(category_name)
    sanitized_course_name = sanitize_filename(course_name)
    dir_path = os.path.join(
        CATEGORIES_DIR, sanitized_category_name, sanitized_course_name)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

def save_video(category_name, course_name, title, video_file):
    sanitized_title = sanitize_filename(title)
    course_dir = os.path.join(
        CATEGORIES_DIR, category_name, course_name, 'videos', sanitized_title)
    os.makedirs(course_dir, exist_ok=True)

    video_filename = f"{sanitized_title}_video.mp4"
    video_path = os.path.join(course_dir, video_filename)
    video_file.save(video_path)

    # Calculate video duration
    video = mp.VideoFileClip(video_path)
    duration = int(video.duration)  # Duration in seconds

    return duration


def save_thumbnail(category_name, course_name, title, thumbnail_file=None):
    sanitized_title = sanitize_filename(title)
    thumbnail_dir = os.path.join(CATEGORIES_DIR, category_name, course_name, 'videos',sanitized_title)
   
    
    if thumbnail_file:
        thumbnail_filename = f"{sanitized_title}_thumbnail.jpg"
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)
        thumbnail_file.save(thumbnail_path)
    else:
        default_thumbnail_path = os.path.join(CATEGORIES_DIR, 'default_thumbnail.jpg')
        thumbnail_path = os.path.join(thumbnail_dir, f"{sanitized_title}_thumbnail.jpg")
        shutil.copy(default_thumbnail_path, thumbnail_path)
    


def save_video_and_thumbnail(category_name, course_name, title, video_file, thumbnail_file=None):
    duration = save_video(category_name, course_name, title, video_file)
    save_thumbnail(category_name, course_name, title, thumbnail_file)

    return {
        'duration': duration,
    }


# def save_video_and_thumbnail(category_name, course_name, title, video_file, thumbnail_file=None):
#     sanitized_title = sanitize_filename(title)
#     course_dir = os.path.join(
#         CATEGORIES_DIR, category_name, course_name, 'videos', sanitized_title)
#     os.makedirs(course_dir, exist_ok=True)

#     video_filename = f"{sanitized_title}_video.mp4"
#     video_path = os.path.join(course_dir, video_filename)
#     video_file.save(video_path)

#     # Calculate video duration
#     video = mp.VideoFileClip(video_path)
#     duration = int(video.duration)  # Duration in seconds

#     # Handle thumbnail
#     if thumbnail_file:
#         thumbnail_filename = f"{sanitized_title}_thumbnail.jpg"
#         thumbnail_path = os.path.join(course_dir, thumbnail_filename)
#         thumbnail_file.save(thumbnail_path)
#     else:
#         default_thumbnail_path = os.path.join(
#             CATEGORIES_DIR, 'default_thumbnail.jpg')
#         thumbnail_path = os.path.join(
#             course_dir, f"{sanitized_title}_thumbnail.jpg")
#         shutil.copy(default_thumbnail_path, thumbnail_path)

#     return {
#         'duration': duration
#     }
