#!/usr/bin/env python3
"""
list all students sorted by avareage score module
"""


def top_students(mongo_collection):
    """
    Retrieves all students document from MongoDB collection
    calculate their average score and sorts the student based
    on their average scores.
    Args:
        mongo collection: pymongo collection object
    """
    students = list(mongo_collection.find())

    for student in students:
        scores = [topic['score'] for topic in student['topics']]
        average_score = sum(scores) / len(scores)
        student['averageScore'] = average_score

    sorted_students = sorted(
        students, key=lambda x: x['averageScore'], reverse=True)
    return sorted_students
