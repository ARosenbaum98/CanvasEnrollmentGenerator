#Open Tkinter
import random as r
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter import filedialog

# Open CavasJsonGenerator
import CanvasJsonGenerator as jsonGen
nameset = jsonGen.openNamesFile("names.txt")

# Create Window
root = Tk()
root.title("LTI JSON Generator")



#TK class
class Window:
    def __init__(self, root):

        # Set root
        self.root = root

        '''
        Frames
        '''

        # Options frame
        self.optFrameWidth = 200
        self.optFrameHeight = 350
        self.optFrame = Frame(root,
                              width = self.optFrameWidth,
                              height = self.optFrameHeight)
        self.optFrame.pack_propagate(False)
        self.optFrame.pack(side = "left")


        # Hidden Teacher Frames (REMOVED)
        self.teacherHiddenFrame = Frame(self.optFrame)
        self.teacherHiddenFrame.pack()

        '''
        Scrollbars
        '''
        
        # Sample json scroll bar
        self.sampleScroll = Scrollbar(root)
        self.sampleScroll.pack(side=RIGHT, fill=Y)
        

        '''
        Options Buttons
        '''

        # TeacherView Button
        self.teacherView = IntVar()
        self.teacherViewBox = Checkbutton(
                                    self.optFrame,\
                                    text = "Enable Teacher View",\
                                    variable = self.teacherView,\
                                    width = self.optFrameWidth,\
                                    anchor = 'w',\
                                    command = self.setTeacherView)
        self.teacherViewBox.pack()

        # Limit Privilages Button
        self.limitPrivilages = IntVar()
        self.limitPrivilagesBox = Checkbutton(\
                                    self.teacherHiddenFrame,\
                                    text = "Set limit_privileges to true",\
                                    width = self.optFrameWidth,\
                                    anchor = 'w',\
                                    variable = self.limitPrivilages,\
                                    command = self.setLimitPrivilages)
        self.limitPrivilagesBox.pack()

        # Include Letter Grade Button
        self.includeGrade = IntVar()
        self.includeGradeBox = Checkbutton(
                                    self.teacherHiddenFrame,\
                                    text = "Include Letter Grade",\
                                    width = self.optFrameWidth,\
                                    anchor = 'w',\
                                    variable = self.includeGrade,\
                                    command = self.setIncludeGrade)
        self.includeGradeBox.pack()

        # Short Name Same As Name
        self.shortName = IntVar()
        self.shortNameBox = Checkbutton(
                                    self.optFrame,\
                                    text = "Set short_name to name",\
                                    width = self.optFrameWidth,\
                                    anchor = 'w',\
                                    variable = self.shortName,\
                                    command = self.setShortName)
        self.shortNameBox.pack()

        # subdomain
        Label(self.optFrame, text = "subdomain:", anchor = 'w').pack()
        self.subdomain = Entry(self.optFrame, width = 20)
        self.subdomainButton = Button(
                        self.optFrame,\
                        text = "set",\
                        command = self.setSubDomain)
        
        self.subdomain.pack()
        self.subdomainButton.pack()

        # Number of Students
        Label(self.optFrame, text = "Number of students:").pack()
        self.nstudents = Entry(self.optFrame, width = 20)
        
        self.nstudents.pack()

        # Submit
        self.submitButton = Button(
                                self.optFrame,
                                text = "Create File",
                                command = self.submit)
        self.submitButton.pack(side = "bottom")
        
                                

        '''
        Generate Sample JSON data
        '''
        
        # Create Sample JSON Data
        self.sampleDisplay = Text(root, wrap = NONE, yscrollcommand = self.sampleScroll.set)
        self.loadSample()

        # Set default file location
        self.saveFileDir = "/"

    '''
    Param settings
    '''

    def submit(self):
        filename =  filedialog.asksaveasfilename(
                                    initialdir = self.saveFileDir,
                                    title = "Select file",
                                    filetypes = (("JSON files","*.json"),
                                                 ("all files","*.*")),
                                    defaultextension = ".json")
        if(filename):
            self.saveJSONfile(filename)
            self.saveFileDir = filename

    def setTeacherView(self):
        self.loadSample()

    def setIncludeGrade(self):
        self.loadSample()

    def setLimitPrivilages(self):
        self.loadSample()

    def setShortName(self):
        self.loadSample()

    def setSubDomain(self):
        self.loadSample()

    def loadSample(self):
        self.sample = self.loadFullJSONParams()
        self.sampleDisplay.delete("1.0",END)
        self.sampleDisplay.insert("1.0",jsonGen.beautify(self.sample))
        self.sampleDisplay.pack(side = "right")


    def saveJSONfile(self, path):

        # Get the number of entries to generate (auto set to 10 if none provided)
        if(not self.nstudents.get() == ''):
            n = int(self.nstudents.get())
        else:
            n = 10
        
        # Set a random student to be the current user's record
        selfStudent = r.randrange(0,n-1)

        # Set a random CourseID for all records
        randId = str(r.randrange(100, 999999))

        # Generate Json
        i = 0
        returnJson = {}
        while(i<n):
            returnJson[i] = self.loadFullJSONParams(randId, selfStudent==i,)
            i+=1
        jsonGen.saveJSON(path, returnJson)

    def loadFullJSONParams(self, randId = "", isSelfStudent = False):
        return jsonGen.randEnrollment(\
                                        nameset,\
                                        limitPrivilages = self.limitPrivilages.get(),
                                        includeLetterGrade = self.includeGrade.get(),
                                        teacherView = self.teacherView.get(),
                                        shortNameSameAsName = self.shortName.get(),
                                        subdomain = self.subdomain.get(),
                                        selfView = isSelfStudent,
                                        disableWarnings = True,
                                        courseId = randId
                                        )
        
    



# Start TK
win = Window(root)
# Main Loop
win.root.mainloop()


