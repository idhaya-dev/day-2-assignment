COURSE_DATA = {
    "CS101": {
        "name": "Computer Science Fundamentals",
        "fee": 30000
    },
    "AI202": {
        "name": "Artificial Intelligence",
        "fee": 40000
    },
    "DS303": {
        "name": "Data Science",
        "fee": 35000
    }
}


def get_course_fee(course_code):
    course = COURSE_DATA.get(course_code)

    if not course:
        return {
            "error": "Course not found"
        }

    return {
        "course_code": course_code,
        "course_name": course["name"],
        "fee": course["fee"]
    }


def calculate_discounted_fee(course_code, scholarship_percent):
    course = COURSE_DATA.get(course_code)

    if not course:
        return {
            "error": "Course not found"
        }

    original_fee = course["fee"]

    discount = original_fee * scholarship_percent / 100

    final_fee = original_fee - discount

    return {
        "course_code": course_code,
        "course_name": course["name"],
        "original_fee": original_fee,
        "scholarship_percent": scholarship_percent,
        "discount": discount,
        "final_fee": final_fee
    }