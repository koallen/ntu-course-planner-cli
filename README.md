# NTU Course Planner

A Python program for NTU students to plan courses.

## Newest Course Schedule Updates

Updated for academic year 2016-17 semester 1 (*22/05/2016*)

## Development Dependencies

* requests
* beautifulsoup4

If you know how to use *requirements.txt*, you can use that to help you install these dependencies.

## Installation

To use this program, just install the package via `pip` by typing the following command in your terminal
```bash
$ pip install ntu-course-planner
```

## Usage

After you installed the package, run the program by typing the following in your terminal
```bash
$ ntu-course-planner
```

You are required to type in the number of courses you are taking and their course codes. Then the planner will plan your timetable.

The result which has all the possible combination of indexes is saved as a text file called *result.txt*. The file is inside the folder which you run the command.

## Contribution
If you would like to contribute to this project, please contact me via the email in my profile page. Here are some improvements that I would like to implement in the future if I have time:
- ~~Make it a Python package~~ (done)
- Develop a front-end website as well as a back-end API for it
