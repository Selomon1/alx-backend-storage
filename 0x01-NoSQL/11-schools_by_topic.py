#!/usr/bin/env python3
"""
schools by topic module
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
