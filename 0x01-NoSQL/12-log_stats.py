#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats():
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})

    # Count of each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {
        method: collection.count_documents({"method": method})
        for method in methods
    }

    # Number of logs with mehod=GET and path=/status
    status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    # Print stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}:", method_counts[method])
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
