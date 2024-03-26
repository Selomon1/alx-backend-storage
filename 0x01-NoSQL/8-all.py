#!/usr/bin/env python3
"""
all module contains a function to list all documents in a collection
"""


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    Args:
        mongo_collection: pymongo object of collection.
    Returns:
        List containging all documents, else empty if not found
    """
    documents = mongo_collection.find()
    return list(documents) if mongo_collection.count_documents({}) > 0 else []
