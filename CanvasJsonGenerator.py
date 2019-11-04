import json
import random as r
import datetime as dt

r.seed();


def randEnrollment(nameset, **settings):
    
    '''
            Settings variables
    '''

    # subdomain
    # the subdomain for your institute
    # If left blank, URLs generated will be for instructure.com with no prefix
    if 'subdomain' in settings: subdomain = settings['subdomain']+"." if settings['subdomain']!="" else ""
    else: subdomain  = ""

    # courseId
    # set the course Id if included
    # If not included, a course Id will be randomly generated
    if 'courseId' in settings: courseId = settings['courseId']
    else: courseId  = ""

    # teacherView
    # enables the viewing of some variables if the current user is the teacher
    # set to True by default
    if 'teacherView' in settings: teacherView = settings['teacherView']
    else: teacherView = True

    # selfView
    # enables the viewing of some variables if the record belongs to the current user
    # set to False by default
    if 'selfView' in settings: selfView = settings['selfView']
    else: selfView = False
    
    # customRoles
    # Adds a list of customRoles to replace established roles
    # Set to false as default
    if 'customeRoles' in settings:
        enableCustomRoles = True
        customRoles = ["foo", "bar"] # add later if necessary 
    else: enableCustomRoles = False


    # limitPrivilages
    # Enrolled persons can only interact with those of their section of the class
    # Set to false as default
    if 'limitPrivilages' in settings: limitPrivilages = bool(settings['limitPrivilages'])
    else: limitPrivilages = False

    # finalScoreSameAsCurrent
    # set the final score to be the same as the current one
    # set to true as defalt.
    if 'finalScoreSameAsCurrent' in settings: finalScoreSameAsCurrent = settings['finalScoreSameAsCurrent']
    else: finalScoreSameAsCurrent = True

    # shortNameSameAsName
    # set shortname to be the same as the regular name var
    # set to true as defalt.
    if 'shortNameSameAsName' in settings: shortNameSameAsName = settings['shortNameSameAsName']
    else: shortNameSameAsName = True


    # includeLetterGrade
    # Add in an A,B,C,D, or F grade to match the final and current score
    # set to true by default
    if 'includeLetterGrade' in settings: includeLetterGrade = settings['includeLetterGrade']
    else: includeLetterGrade = True

    # includeLetterGrade
    # Add in an A,B,C,D, or F grade to match the final and current score
    # set to true by default
    if 'hasUnpostedGrades' in settings: hasUnpostedGrades = settings['hasUnpostedGrades']
    else: hasUnpostedGrades = True

    # viewGrades
    # Allows certain persons to see grades
    # Set to allow teachers and current users
    viewGrades = teacherView or selfView

    # viewUnposted
    # Allows only certain users to see unposted grades
    # Set to allow teachers and admins to view
    viewUnposted = teacherView

    # enableSIS
    # Allows viewing of all SIS-only variables
    # Set to allow teachers and admin to view
    enableSIS = teacherView


    # System variable, Suppress Print warnings
    # Set to disable print warnings
    if 'disableWarnings' in settings: disableWarnings = settings['disableWarnings']
    else: disableWarnings = False 
    


    '''
            JSON Building
    '''

    # Create the enrollment dictionary
    enrollment = {}


    # id
    # The ID of the enrollment.
    enrollment['id'] = generateId()

    # course_id
    # The unique id of the course.
    enrollment['course_id'] = courseId if courseId != "" else generateId()

    # institute system admin only, disabled by default
    if enableSIS:
        enrollment['sis_course_id'] = generateId()
        enrollment['course_integration_id'] = generateId()
        enrollment['course_section_id'] = generateId()
        enrollment['section_integration_id'] = generateId()
        enrollment['sis_account_id'] = generateId()
        enrollment['sis_section_id'] = generateId()
        enrollment['sis_user_id'] = generateId()
        enrollment['enrollment_state'] = r.choices(population=['Active','Inactive'], weights=[0.9, 0.1])[0]
        enrollment['sis_import_id'] = generateId()

    # limit_privileges_to_course_section
    # User can only access his or her own course section.
    # If set, enrollment will only allow the user to see and interact with users enrolled ((in the section given by course_section_id)).
    enrollment['limit_privileges_to_course_section'] = limitPrivilages

    # root_account_id
    # The unique id of the user's account.
    enrollment['root_account_id'] = generateId()

    # type
    # The enrollment type. One of 'StudentEnrollment', 'TeacherEnrollment','TaEnrollment', 'DesignerEnrollment', 'ObserverEnrollment'.

    '''''''''''''''''''''
    NOTE:
    This simulation is set only to generate students
    '''''''''''''''''''''
    warning("WARNING: This simulation is set only to generate student enrollments.", disableWarnings)
    enrollment['type'] = "StudentEnrollment"

    # user_id
    # unique id of the user
    enrollment['user_id'] = generateId()

    # associated_user_id
    # The unique id of the associated user. Will be null unless type is ObserverEnrollment.

    '''''''''''''''''''''
    NOTE:
    associated_user_id set only to output null due to this simulation exclusivly
    outputting student enrollment
    '''''''''''''''''''''
    warning("Due to only generating student enrollments, all associated_user_id will be set to null.", disableWarnings)
    enrollment['associated_user_id'] = None

    # role
    # Will match type unless the enrollment role has been customized.
    if enableCustomRoles:
        # Add the ability to create custom roles later if need-be
        foo = "bar"

    else:
        enrollment['role'] = enrollment['type']
        enrollment['role_id'] = "1"
    
    '''
    NOTE: For the purposes of this simulation,
    all datatime variables will be set to the time of execution
    '''
    warning("WARNING: All DateTime variables will be set to time of execution.", disableWarnings)


    # created_at
    # The created time of the enrollment, in ISO8601 format.
    enrollment['created_at'] = dt.datetime.now().replace(microsecond=0).isoformat();

    # updated_at
    # The updated time of the enrollment, in ISO8601 format.
    enrollment['updated_at'] = dt.datetime.now().replace(microsecond=0).isoformat();

    # start_at
    # The start time of the enrollment, in ISO8601 format
    enrollment['start_at'] = dt.datetime.now().replace(microsecond=0).isoformat();

    # end_at
    # The end time of the enrollment, in ISO8601 format.
    enrollment['end_at'] = dt.datetime.now().replace(microsecond=0).isoformat();

    # last_activity_at
    # The last activity time of the user for the enrollment, in ISO8601 format
    enrollment['last_activity_at'] = dt.datetime.now().replace(microsecond=0).isoformat();

    # last_attended_at
    # The last attended date of the user for the enrollment in a course, in ISO860
    enrollment['last_attended_at'] = dt.datetime.now().replace(microsecond=0).isoformat();

    # total_activity_time
    # The total activity time of the user for the enrollment, in seconds.
    # Current range is hardcoded between 10 minutes and 48 hours
    enrollment['total_activity_time'] = r.randrange(600,172800)

    # html_url
    # The URL to the Canvas web UI page for this enrollment's user.
    enrollment['html_url'] = subdomain+"instructure.com/courses/"+enrollment['course_id']+"/users/"+enrollment['user_id']
    
    # Create Grades Object
    grades = {}

    # grade.html_url
    # The URL to the Canvas UI page for user grades
    grades['html_url'] = subdomain+"instructure.com/courses/"+enrollment['course_id']+"/grades/"+enrollment['user_id']

    # Generate random scores
    currentScore = r.randrange(0,10000)
    finalScore = currentScore if finalScoreSameAsCurrent else r.randrange(0,currentScore)
        
    # Build hidden grades object
    # Only visible to those with permission
    if(viewGrades):
        
            
        # grade.current_score
        # The current numeric score in class.
        grades['current_score'] = currentScore/100

        # grade.final_score
        # The final numeric score in class 
        grades['final_score'] = finalScore/100

        # grade.current_grade
        # The current letter grade in class
        # Set to None if includeLetterGrade is false
        grades['current_grade'] = getLetterGrade(grades['current_score']) if includeLetterGrade else None

        # grade.final_grade
        # The current letter grade in class
        # Set to None if includeLetterGrade is false
        grades['final_grade'] = getLetterGrade(grades['final_score']) if includeLetterGrade else None


    # Build unposted grades object
    # Onlyvisible to those with permissions
    if(viewUnposted):

        #grades.unposted_current_score
        grades['unposted_current_score'] = r.randrange(0,10000)/100 if hasUnpostedGrades else None

        # grades.unposted_final_score
        if(not viewUnposted):
            grades['unposted_final_score'] = None
        elif(finalScoreSameAsCurrent):
            grades['unposted_final_score'] = grades['unposted_current_score']
        else:
            grades['unposted_final_score'] = r.randrange(0,grades['unposted_current_score'])

        # grades.unposted_current_grade
        grades['unposted_current_grade'] = getLetterGrade(grades['unposted_current_score']) if includeLetterGrade else None

        # grades.unposted_final_grade
        grades['unposted_final_grade'] = getLetterGrade(grades['unposted_final_score']) if includeLetterGrade else None

                   
                                                    
                                                    

            
    # grades (object)
    # the grades object of the enrollment
    enrollment['grades'] = grades

    # Create user object
    user = {}
    
    # user.id
    # Id of enrollment's user. Same as enrollment.user_id
    user['id'] = enrollment['user_id']

    # generate names
    fname = randomName(nameset)
    lname = randomName(nameset)

    # user.name
    # full name of student (first, last)
    user['name'] = fname+" "+lname

    # user.short_name
    # alternate name of student
    user['short_name'] = user['name'] if shortNameSameAsName else fname

    # user.sortable_name
    # full name of student (last, first)
    user['sortable_name'] = lname+", "+fname

    # user
    # user object of the student assigned to the enrollment 
    enrollment['user'] = user
    return enrollment


'''functions'''

def warning(string, disableWarnings):
    if(not disableWarnings):
        print(string)

def generateId(start = 100, end = 100000):
    return str(r.randrange(100, 99999))

def getLetterGrade(score):
    if(score<60):
        return "F"
    if(score<70):
        return "D"
    if(score<80):
        return "C"
    if(score<90):
        return "B"
    return "A"

def randomName(namesList):
    return r.choice(namesList).strip();

def openNamesFile(nameset):
    # Set up random-name generator 
    # Open a list of names from file for random name assignment

    namesList = [];
    with open(nameset) as file:
        namesList = file.readlines()
    return namesList

def beautify(data):
    return json.dumps(data, indent=4, separators=(',', ': '))

def saveJSON(filepath, data):
    with open(filepath, 'w') as jsonFile:
        jsonFile.write(beautify(data))























