from setuptools import setup

long_description = """
This is a tool for Nanyang Technological University students to plan their timetable.
After you supply with the tool the courses that you intent to take in a semester, it
can automatically generate all the possible combinations of indexes for the courses
that you picked. It's guaranteed that there will be no timetable clash.
"""

setup(
    name = "ntu-course-planner",
    version = "1.0.0",
    description = "A course planner for Nanyang Technological University students",
    long_description = long_description,
    url = "https://github.com/koallen/ntu-course-planner-cli",
    author = "Liu Siyuan",
    author_email = "weifengzi2009@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities"
    ],
    keywords = ["course", "planner", "Nanyang Technological University"],
    packages = ["ntu_course_planner"],
    install_requires = ['requests', 'beautifulsoup4'],
    entry_points = {
        "console_scripts": [
            'ntu-course-planner = ntu_course_planner.main:main'
        ]
    }
)
