import sqlite3  # imports the SQL library.
from appJar import gui  # import gui from the self.app.ar library
from datetime import datetime, timedelta


def dates(todayDate):
    date = datetime.strptime(todayDate, "%Y - %m - %d %H:%M:%S")  # strips the original format of the datetime object and assigns it to a variable
    convertedDate = date.strftime("%d/%m/%y")  # formats the date into the DD/MM/YYYY format
    return convertedDate  # returns the convertedDate


def times(time):
    if len(time) <= 5:  # checks if the time variable is not in the correct format for example "09:30"
        time += ":00"  # adds a ":00" to the end of the string converting it to "9:30:00"
    timeObj = datetime.strptime(time, "%H:%M:%S")  # strips the time of the HH/MM/SS format
    formattedTime = timeObj.strftime("%I:%M:%S %p")  # formats the time into 12-hour format with AM/PM
    return formattedTime


class BookingSoftware:
    def __init__(self):
        self.username = None
        self.pitchNum = None
        self.pitchPrice = None
        self.app = gui("PlayingFields booking system")
        self.con = sqlite3.connect("pfDatabase.db")  # create my database and store it in the variable con.
        self.cur = self.con.cursor()  # set up the cursor value in my database and store it in the variable self.cur.
        self.attempts = 0
        self.seconds = 10
        self.running = False
        self.createInterface()
        self.app.go(startWindow="window_CreateAnAccount")

    def createInterface(self):
        # LOGIN PAGE: this is the initial starting page of the software,
        #             where users will be able to log into their account to access the main menu,
        #             go to the create an account page or the forgot password page
        self.app.setSize("600x300")  # Sets the size of the window to 600x300
        self.app.setSticky("W")
        self.app.setBg("#353332")  # changes the background colour of the whole page to the colour selected
        self.app.addImage("loginLogo", "Logo.gif", 0, 3)  # adds the image from the gif file added to the top right of the page
        self.app.setImageSize("loginLogo", 75, 75)  # sets the size of the image to 75x75
        self.app.addLabel("lb_Login", "Log In", 0, 0).config(font="bold 15 underline")  # makes the Log In text bold, underlined and have a font size of 15
        self.app.setLabelFg("lb_Login", "white")  # Set text color to white
        self.app.addLabel("timer", "", 1, 3)
        self.app.addLabelEntry("UsernameCheck", 1, 0)
        self.app.setLabel("UsernameCheck", "Username *:")
        self.app.setLabelFg("UsernameCheck", "white")  # Set text color to white
        # Creates an entry box where the entered values are displayed as "*"
        self.app.addSecretLabelEntry("PasswordCheck", 2, 0)
        self.app.setLabel("PasswordCheck", "Password *:")
        self.app.setLabelFg("PasswordCheck", "white")  # Set text color to white
        self.app.addButton("SignIn", self.doSignin, 3, 0)
        self.app.setButton("SignIn", "Sign In")
        self.app.link("Forgot Password", self.doForgotPassword, 3, 1)  # Creates a hyperlink that acts as a button
        self.app.setLinkFg("Forgot Password", "#759fb9")  # Change link text color to light blue
        self.app.addLabel("lb_createAnAccount", "Dont have an account?", 5, 0)
        self.app.setLabelFg("lb_createAnAccount", "#c5c8c9")  # Set text color to grey
        self.app.addButton("Sign Up", self.doSignUp, 6, 0)
        self.app.addLabel("lb_requiredFields", "Required Fields: *", 9, 0)
        self.app.setLabelFg("lb_requiredFields", "#c5c8c9")  # Set text color to grey

        # CREATE AN ACCOUNT PAGE: this is the page where users will enter all the required
        #                         information for them to create an account which will then
        #                         be added to the tbl_users table
        self.app.startSubWindow("window_CreateAnAccount")
        self.app.setBg("#353332")  # changes the background colour of the whole page to the colour selected
        self.app.addImage("CreateAccLogo", "Logo.gif", 0, 3)  # adds the image from the gif file added to the top right of the page
        self.app.setImageSize("CreateAccLogo", 75, 75)  # sets the size of the image to 75x75
        # makes the Log In text bold, underlined and have a font size of 15
        self.app.addLabel("lb_CreateAnAccount", "Create An Account", 0, 0).config(font="bold 15 underline")
        self.app.setLabelFg("lb_CreateAnAccount", "white")  # Set text color to white
        self.app.setSize("600x300")  # Sets the size of the window to 600x300
        self.app.setSticky("W")  # move everything to the west of the page
        self.app.addLabelEntry("FirstnameEntry", 1, 0)  # add a label entry to the 1st row and 0th column
        self.app.setLabel("FirstnameEntry", "Firstname *:")  # change the value of the label entry to Firstname :*
        self.app.setLabelFg("FirstnameEntry", "white")  # Set text color to white
        self.app.addLabelEntry("SurnameEntry", 2, 0)  # add a label entry to the 2nd row and 0th column
        self.app.setLabel("SurnameEntry", "Surname *:")  # change the value of the label entry to Surname :*
        self.app.setLabelFg("SurnameEntry", "white")  # Set text color to white
        self.app.addLabelEntry("UsernameEntry", 3, 0)  # add a label entry to the 3rd row and 0th column
        self.app.setLabel("UsernameEntry", "Username *:")  # change the value of the label entry to Username :*
        self.app.setLabelFg("UsernameEntry", "white")  # Set text color to white
        # Creates an entry box where the entered values are displayed as "*"
        self.app.addSecretLabelEntry("PasswordEntry", 4, 0)  # add a secret label entry to the 4th row and 0th column
        self.app.setLabel("PasswordEntry", "Password *:")  # change the value of the secret label entry to Password :*
        self.app.setLabelFg("PasswordEntry", "white")  # Set text color to white
        # Creates an entry box where the entered values are displayed as "*"
        self.app.addSecretLabelEntry("RepeatPasswordEntry", 5, 0)  # add a secret label entry to the 5th row and 0th column
        self.app.setLabel("RepeatPasswordEntry", "Repeat Password *:")  # change the value of the secret label entry to Repeat Password :*
        self.app.setLabelFg("RepeatPasswordEntry", "white")  # Set text color to white
        self.app.addLabelEntry("PhoneNumberEntry", 6, 0)  # add a label entry to the 6th row and 0th column
        self.app.setLabel("PhoneNumberEntry", "Phone Number :")  # change the value of the label entry to Phone Number :
        self.app.setLabelFg("PhoneNumberEntry", "white")  # Set text color to white
        self.app.addLabelEntry("MemorableWordEntry", 7, 0)  # add a label entry to the 7th row and 0th column
        self.app.setLabel("MemorableWordEntry", "Memorable Word *:")  # change the value of the label entry to Memorable Word :*
        self.app.setLabelFg("MemorableWordEntry", "white")  # Set text color to white
        self.app.addButton("CreateAccountSubmit", self.doCreateAnAccountSubmit, 8, 0)  # add a button to the 8th row and 0th column
        self.app.setButton("CreateAccountSubmit", "Submit")  # change the value of the button to Submit
        self.app.addButton("CreateAccountToLogIn", self.doCreateAccountToLogIn, 9, 2)  # add a button to the 9th row and 2nd column
        self.app.setButton("CreateAccountToLogIn", "Log In")  # change the value of the button to Log In
        self.app.addLabel("lb_requiredFields2", "Required Fields: *", 9, 0)  # add a label to the 9th row and 0th column that says Required Fields: *
        self.app.setLabelFg("lb_requiredFields2", "white")  # Set text color to white
        self.app.stopSubWindow()

        # FORGOT PASSWORD PAGE: this is the page where users will use their memorable word to
        #                       retrieve their password if they have forgotten it
        self.app.startSubWindow("window_ForgotPassword")
        self.app.setSize("600x300")  # Sets the size of the window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        self.app.addLabel("lb_ForgotPassword", "ForgotPassword")  # adds a label with the text Forgot Password
        self.app.addLabelEntry("UsernameChecker", 1, 0)  # adds a label entry in the 1st row and 0th column
        self.app.setLabel("UsernameChecker", "Username *:")  # sets the label entry to Username *:
        self.app.addLabelEntry("MemorableWordChecker", 2, 0)  # adds a label entry to the 2nd row and 0th column
        self.app.setLabel("MemorableWordChecker", "Memorable Word *:")  # sets the label entry to Memorable Word *:
        self.app.addButton("GetPassword", self.doGetPassword, 3, 0)  # adds a button to the 3rd row and 0th column
        self.app.setButton("GetPassword", "Get Password")  # sets the button to Get Password
        self.app.addLabel("lb_requiredFields3", "Required Fields: *", 9, 0)  # adds a label with the text Required Fields:* to the 9th row and 0th column
        self.app.addButton("BackToLogIn", self.doBackToLogIn, 9, 2)  # adds a button to the 9th row and 2nd column
        self.app.setButton("BackToLogIn", "Log In")  # sets the button to Log In
        self.app.stopSubWindow()

        # MAIN MENU PAGE: this is the page that will allow users to access the Book a pitch page,
        #                 the Cancel booking page and the View bookings page,
        #                 they will also be able to log out of their account taking them back to the Log-in page,
        #                 this page is acting as a linking page between all the other pages in my software.
        self.app.startSubWindow("window_MainMenu")
        self.app.setSize("600x300")  # sets the size of the window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        self.app.addLabel("lb_MainMenu", "Main Menu", 0, 1)  # adds a label with the text Main Menu to the 0th row and 1st column
        self.app.addButton("BookAPitch", self.doBookAPitch, 1, 1)  # adds a button to the 1st row and 1st column
        self.app.setButton("BookAPitch", "Book A Pitch")  # sets the button to Book A Pitch
        self.app.addButton("CancelABooking", self.doCancelABooking, 2, 1)  # adds a button to the 2nd row and 1st column
        self.app.setButton("CancelABooking", "Cancel A Booking")  # sets the button to Cancel A Booking
        self.app.addButton("ViewBookings", self.doViewBookings, 3, 1)  # adds a button to the 3rd row and 1st column
        self.app.setButton("ViewBookings", "View Bookings")  # sets the button to View Bookings
        self.app.addButton("MainMenuLogOut", self.doMainMenuLogOut, 0, 0)  # adds a button to the 0th row and 0th column
        self.app.setButton("MainMenuLogOut", "Log Out")  # sets the button to Log Out
        self.app.stopSubWindow()

        # PITCH SIZE SELECTION: this is the page that will start the booking process,
        #                       by allowing users to select the pitch size that they want,
        #                       so that the correct buttons can be disabled depending on the
        #                       pitch size selected
        self.app.startSubWindow("window_PitchSizeSelection")
        self.app.setSize("600x300")  # sets the size of the sub-window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        # adds a label with the text Pitch Size Selection to the 0th row and 1st column
        self.app.addLabel("lb_PitchSizeSelection", "Pitch Size Selection", 0, 1)
        self.app.addButton("PitchSelectionToMainMenu", self.doPitchSelectionToMainMenu, 9, 2)  # adds a button to the 9th row and 2nd column
        self.app.setButton("PitchSelectionToMainMenu", "Main Menu")  # sets the button to Main Menu
        self.app.addButton("7asideSelection", self.doPitchSelection, 1, 0)  # adds a button the 1st row and 0th column
        self.app.setButton("7asideSelection", "7-aside")  # sets the button to 7-aside
        self.app.addButton("9asideSelection", self.doPitchSelection, 2, 0)  # adds a button the 2bd row and 0th column
        self.app.setButton("9asideSelection", "9-aside")  # sets the button to 9-aside
        self.app.addButton("11asideSelection", self.doPitchSelection, 3, 0)  # adds a button the 3rd row and 0th column
        self.app.setButton("11asideSelection", "11-aside")  # sets the button to 11-aside
        self.app.stopSubWindow()

        # CANCEL BOOKING : this is the page that will allow users to cancel a booking that they have made
        #                  if they wish to do so, by selecting a bookingID from the labelOptionBox
        self.app.startSubWindow("window_CancelBooking")
        self.app.setSize("600x300")  # sets the size of the sub-window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        self.app.addLabel("lb_CancelBooking", "Cancel Booking")  # adds a label with the text Cancel Booking to the page
        self.app.addButton("CancelBookingToMainMenu", self.doCancelBookingToMainMenu, 9, 2)  # adds a button to the 9th row and 2nd column
        self.app.setButton("CancelBookingToMainMenu", "Main Menu")  # sets the button to text Main Menu
        self.app.addLabelOptionBox("Select booking you'd like to cancel :", [""], 3, 2)  # adds an empty label option box to the 3rd row and 2nd column
        self.app.addButton("CancelBooking", self.doCancelBooking, 6, 2)  # adds a button to the 6th row and 2nd column
        self.app.setButton("CancelBooking", "Cancel Booking")  # sets the button to Cancel Booking
        self.app.stopSubWindow()

        # VIEW BOOKING: this is the page where users will be able to view all their previous and
        #              upcoming bookings by selecting the bookingID from the labelOptionBox, to see
        #              that bookings information in an info box
        self.app.startSubWindow("window_ViewBooking")
        self.app.setSize("600x300")  # sets the size of the sub-window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        self.app.addLabel("lb_ViewBooking", "View Booking", 0, 2)  # adds a label with the text View Booking to the 0th row and 2nd column
        self.app.addButton("ViewBookingToMainMenu", self.doViewBookingToMainMenu, 9, 2)  # adds a button to the 9th row and 2nd column
        self.app.setButton("ViewBookingToMainMenu", "Main Menu")  # sets the button to Main Menu
        self.app.addLabelOptionBox("Select a Booking ID :", [""], 3, 2)  # adds an empty label option box to the 3rd row and 2nd column
        self.app.addButton("GetBookingInfo", self.doGetBookingInfo, 6, 2)  # adds a button to the 6th rpw and 2nd column
        self.app.setButton("GetBookingInfo", "View Booking")  # sets the button to View Booking
        self.app.stopSubWindow()

        # Booking: this is the page where users will be able to put all the details of the pitch they want to book
        #          as well as the date and time, allowing them to make a booking, they are then automatically
        #          taken to the bookingSummary page
        todayDate = datetime.now()  # stores the date the user is using the software in the todayDate variable
        # iterates through the next 14 days storing it in the nextTwoWeeks variable
        nextTwoWeeks = [dates((todayDate + timedelta(days=i)).strftime("%Y - %m - %d %H:%M:%S")) for i in range(14)]
        self.app.startSubWindow("window_Booking")
        self.app.setSize("600x300")  # sets the size of the window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        self.app.addLabel("lb_Booking", "Booking", 0, 1)  # adds a label with the text Booking to the 0th row and 1st column
        # add a label option box to the 1st row and 1st column storing the values in the nextTwoWeeks variable
        self.app.addLabelOptionBox("Date: ", nextTwoWeeks, 1, 1)
        # stores the times from 8:00 to 20:00 in a label spin box in the 9th row and 1st column
        self.app.addLabelSpinBox("Time: ",
                                 ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00",
                                  "13:30",
                                  "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00",
                                  "18:30", "19:00",
                                  "19:30", "20:00"], 9, 1)
        self.app.addButton("BookingToPitchSizeSelection", self.doBookingToPitchSizeSelection, 9, 3)  # adds a button to the 9th row and 3rd column of the page
        self.app.setButton("BookingToPitchSizeSelection", "Back")  # sets the button to Back
        self.app.addButton("BookPitch1", self.doSelectPitch, 4, 1)  # adds a button to the 4th row and 1st column
        self.app.setButton("BookPitch1", "Pitch 1 ")  # set the button to Pitch 1
        self.app.addButton("BookPitch2", self.doSelectPitch, 4, 2)  # adds a button to the 4th row and 2nd column
        self.app.setButton("BookPitch2", "Pitch 2")  # set the button to Pitch 2
        self.app.addButton("BookPitch3", self.doSelectPitch, 5, 1)  # adds a button to the 5th row and 1st column
        self.app.setButton("BookPitch3", "Pitch 3")  # set the button to Pitch 3
        self.app.addButton("BookPitch4", self.doSelectPitch, 5, 2)  # adds a button to the 5th row and 2nd column
        self.app.setButton("BookPitch4", "Pitch 4")  # set the button to Pitch 4
        self.app.addButton("BookPitch5", self.doSelectPitch, 6, 1)  # adds a button to the 6th row and 1st column
        self.app.setButton("BookPitch5", "Pitch 5")  # set the button to Pitch 5
        self.app.addButton("MakeBooking", self.doMakeBooking, 4, 3, 2, 2)  # adds a button to the 4th row and 3rd column with a col-span and row-span of 2
        self.app.setButton("MakeBooking", "Book Pitch")  # set the button to Book Pitch
        self.app.stopSubWindow()

        # BOOKING SUMMARY: this is the page that will display all the booking information
        #                  for the booking that the user has just made.
        self.app.startSubWindow("window_BookingSummary")
        self.app.setSize("600x300")  # sets the size of the sub-window to 600x300
        self.app.setSticky("W")  # moves everything to the west of the page
        self.app.addLabel("lb_BookingSummary", "Booking Summary", 0, 2)  # adds a label with the text Booking Summary to the 0th row and 2nd column
        self.app.addLabel("showBookingID", "BookingID :", 1, 0)  # adds a label with the text BookingID : to the 1st row and 0th column
        self.app.addLabel("UsersBookingID", " ", 1, 1)  # adds a label with the blank text to the 1st row and 1st column
        self.app.addLabel("showUsername", "Username :", 2, 0)  # adds a label with the text  Username : to the 2nd row and 0th column
        self.app.addLabel("UsersUsername", " ", 2, 1)  # adds a label with the blank text to the 2nd row and 1st column
        self.app.addLabel("ShowDate", "Date :", 3, 0)  # adds a label with the text Date : to the 3rd row and 0th column
        self.app.addLabel("UsersDate", " ", 3, 1)  # adds a label with the blank text to the 3rd row and 1st column
        self.app.addLabel("ShowTime", "Time :", 4, 0)  # adds a label with the text Time : to the 4th row and 0th column
        self.app.addLabel("UsersTime", " ", 4, 1)  # adds a label with the blank text to the 4th row and 1st column
        self.app.addLabel("ShowPitchNumber", "Pitch Number :", 5, 0)  # adds a label with the text Pitch Number : to the 5th row and 0th column
        self.app.addLabel("UsersPitchNumber", " ", 5, 1)  # adds a label with the blank text to the 5th row and 1st column
        self.app.addLabel("ShowTotalCost", "Total Cost :", 6, 0)  # adds a label with the text Total Cost : to the 6th row and 0th column
        self.app.addLabel("UsersTotalCost", " ", 6, 1)  # adds a label with the blank text to the 6th row and 1st column
        self.app.addButton("BookingSummaryToMainMenu", self.doBookingSummaryToMainMenu, 9, 2)  # adds a button to the 9th row and 2nd column
        self.app.setButton("BookingSummaryToMainMenu", "Main Menu")  # sets the button to Main Menu
        self.app.stopSubWindow()

    def loginValidation(self):
        self.attempts += 1  # increments the attempts variable by 1
        usernameEntered = self.app.getEntry("UsernameCheck")  # stores the username entered
        passwordEntered = self.app.getEntry("PasswordCheck")  # stores the password entered
        self.cur.execute("SELECT Username, Password FROM tbl_users WHERE Username = ? AND Password = ?",
                         (usernameEntered, passwordEntered))  # checks if the username entered is in the database
        validUser = self.cur.fetchone()  # stores the first value fetched by the SQL statement

        if type(validUser) is type(None):  # checks if the username and password entered are empty
            return self.checkAttempts()  # returns value returned by the checkAttempts function

        if validUser[0] == usernameEntered and validUser[1] == passwordEntered:  # checks if the username and password are correct
            # checks if the values retrieved from the SQL statement are the same as the users inputs
            self.attempts = 0  # sets the attempts =
            self.username = validUser[0]  # sets the username variable to the correct username entered by the user
            return True

        return self.checkAttempts()  # returns value returned by the checkAttempts function

    def checkAttempts(self):
        if self.attempts < 3:  # checks if the attempts are less than 3
            self.app.infoBox("ERROR",
                             "Username or Password is incorrect, " + str(
                                 3 - self.attempts) + " attempts remaining")  # displays an error box telling users how many attempts they have remaining
            return False
        else:
            self.app.infoBox("ERROR", "Too many failed attempts! Locking page.")  # displays an error box telling users the page is being locked
            self.disableWidgets()  # runs the disable widgets function
            self.updateTime()  # runs the updateTime function
            return False

    def disableWidgets(self):
        self.app.disableEntry("UsernameCheck")  # disables the UsernameCheck entry box
        self.app.disableEntry("PasswordCheck")  # disables the PasswordCheck entry box
        self.app.disableButton("SignIn")  # disables the SignIn button
        self.app.disableLink("Forgot Password")  # disables the Forgot Password link
        self.app.disableButton("Sign Up")  # disables the SignUp button

    def enableWidgets(self):
        self.app.enableEntry("UsernameCheck")  # enables the PasswordCheck entry box
        self.app.enableEntry("PasswordCheck")  # enables the PasswordCheck entry box
        self.app.enableButton("SignIn")  # enables the SignIn button
        self.app.enableLink("Forgot Password")  # enables the Forgot Password link
        self.app.enableButton("Sign Up")  # enables the SignUp button

    def formatTime(self):
        minutes = self.seconds // 60  # stores the value of the seconds variable DIV 60 in the minutes variable
        sec = self.seconds % 60  # stores the value of the seconds variable MOD 60 in the seconds variable
        return f"{minutes:02}:{sec:02}"  # Formats seconds into minutes:seconds format

    def updateTime(self):
        # Updates the timer countdown every second
        if self.seconds > 0:  # checks if the seconds variable is greater than 0
            self.seconds -= 1  # decrements the seconds variable by 1
            self.app.setLabel("timer", self.formatTime() + " left until unlock")  # displays the time left til unlock
            self.app.after(1000, self.updateTime)  # runs the updateTime function after 1000ms
        elif self.seconds == 0:  # checks if the seconds variable is equal to 0
            self.enableWidgets()  # runs the enable widgets function
            self.app.setLabel("timer", "")  # makes the timer invisible to users
            self.attempts = 0  # resets the attempts
            self.seconds = 10  # resets the seconds

    def doSignUp(self):
        self.app.hide()  # Hides the Main Log in page
        self.app.showSubWindow("window_CreateAnAccount")  # shows the Create An Account Sub-window

    def createAnAccountValidation(self):
        # gets all the entry box entries storing all the entered values in a variable
        firstnameEntered = self.app.getEntry("FirstnameEntry")  # gets the firstname entered
        surnameEntered = self.app.getEntry("SurnameEntry")  # gets the Surname entered and stores it in the surnameEntered variable
        usernameEntered = self.app.getEntry("UsernameEntry")  # gets the Username entered and stores it in the usernameEntered variable
        passwordEntered = self.app.getEntry("PasswordEntry")  # gets the Password entered and stores it in the passwordEntered variable
        # gets the Repeat Password entered and stores it in the repeatPassword Entered variable
        repeatPasswordEntered = self.app.getEntry("RepeatPasswordEntry")
        phoneNumberEntered = self.app.getEntry("PhoneNumberEntry")  # gets the Phone number entered and stores it in the phoneNumberEntered variable
        memorableWordEntered = self.app.getEntry("MemorableWordEntry")  # gets the Memorable word entered and stores it in the memorableWordEntered variable

        # checks if the entries are empty displaying an info box if any of them are empty
        if firstnameEntered == "" or surnameEntered == "" or usernameEntered == "" or passwordEntered == "" or repeatPasswordEntered == "" or memorableWordEntered == "":  # Checks if fields that are required are empty
            # shows user info box stating that all fields should be filled in
            self.app.infoBox("Create An Account", "Ensure that all required fields are filled in")
            return False
        else:
            # runs the validation function passing in every entry to the  function
            correctFields = self.checkCreateAccountFields(usernameEntered, passwordEntered, repeatPasswordEntered, firstnameEntered, surnameEntered,
                                                          phoneNumberEntered)
            # checks if the users entries are correct against my syntax
            if correctFields:
                userId = self.userId()  # generates a userID storing it in the userId variable
                self.cur.execute("INSERT INTO tbl_users VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (userId, usernameEntered, firstnameEntered, surnameEntered, passwordEntered, phoneNumberEntered,
                                  memorableWordEntered))  # inserts the users entries into the database
                self.con.commit()
                return True
            else:
                return False

    def checkCreateAccountFields(self, usernameEntered, passwordEntered, repeatPasswordEntered, firstnameEntered, surnameEntered, phoneNumberEntered):
        integers = 0
        capitals = 0
        self.cur.execute("SELECT Username FROM tbl_users WHERE Username = ?",
                         (usernameEntered,))  # checks if the username entered is in the database
        username = self.cur.fetchone()  # stores the first tuple returned

        if username is not None and username[0] is not None:  # checks if there was a value in the database that equals the entered username
            self.app.infoBox("Create An Account", "There is an existing account with this username")  # tells the user that this username already exists
            return False

        for char in passwordEntered:  # iterates through all the characters in the entered password
            if char.isdigit():  # checks if the character is an integer
                integers += 1  # if the character is an integer the integer variable is incremented
            elif char.isupper():  # checks if the character is a capital letter
                capitals += 1  # if the character is a capital letter the capital variable is incremented

        if len(passwordEntered) < 8 or len(
                passwordEntered) > 24 or integers < 2 or capitals < 1:  # checks if the password is between 8 and 24 characters, has at least 2 integers and at least 1 capital letter.
            # shows user info box that their password must have between 8 and 24 inclusive, have at least 2 integers and at least 1 capital letter
            self.app.infoBox("Create An Account", "Passwords must be between 8 and 24 inclusive, have at least 2 integers and at least 1 capital letter")
            return False

        if passwordEntered != repeatPasswordEntered:  # checks if the entered password is the same as the repeat password entered
            # shows user info box that their repeat password and pasword do not match
            self.app.infoBox("Create An Account", "Repeat password and Password do not match")
            return False

        if not firstnameEntered.isalpha() or not surnameEntered.isalpha():  # checks if the firstname and surname entered only contain letters
            # shows user info box saying that their username and surname must only contain letters
            self.app.infoBox("Create An Account", "Username and Surname must only contain letters")
            return False

        if phoneNumberEntered != "":  # checks if the phone number field is not empty
            if len(phoneNumberEntered) != 11 or phoneNumberEntered[:2] != "07":  # checks of the phone number is 11 digits long and starts with 06
                self.app.infoBox("Create An Account", "Phone numbers should be 11 digits long and start with 07")
                return False
        return True

    def userId(self):
        userNum = 100
        createUserId = "U" + str(userNum)  # concatenated the letter U with the userNUm
        self.cur.execute("SELECT UserID FROM tbl_users WHERE UserID = ?", (createUserId,))  # checks if the UserID entered is in the database
        existingUserID = self.cur.fetchone()
        while existingUserID is not None and existingUserID[0] is not None:  # does while the userID is existing in the database
            userNum += 1  # increments the userNum variable by 1
            createUserId = "U" + str(userNum)  # concatenated the letter U with the userNUm
            self.cur.execute("SELECT UserID FROM tbl_users WHERE UserID = ?", (createUserId,))  # checks if the username entered is in the database
            existingUserID = self.cur.fetchone()
        return createUserId

    def forgotPasswordValidation(self):
        username = self.app.getEntry("UsernameChecker")  # stores the users entry in the username variable
        memorableWord = self.app.getEntry("MemorableWordChecker")  # stores the users entry in the memorable word variable
        self.cur.execute("SELECT Password FROM tbl_users WHERE Username = ? AND MemorableWord = ?",
                         (username, memorableWord,))  # fetches the password that is in the same record as the users inputs
        password = self.cur.fetchone()  # stores the tuple returned in the password variable
        return password  # returns the password variable

    def doCreateAnAccountSubmit(self):
        # stores the result of a question box in the variable
        createAccountConfirmation = self.app.questionBox("Create An Account", "Are you sure you want to create an account?")
        if createAccountConfirmation:  # checks if the result was true
            validInfo = self.createAnAccountValidation()  # stores the result of the createAccountValidation function in the validInfo variable
            if validInfo:  # checks if the validInfo variable is True
                self.app.infoBox("Create An Account",
                                 "Your account has been created!")  # displays a pop-up box that says the account has been created
                self.app.clearEntry("FirstnameEntry")  # clears the FirstnameEntry
                self.app.clearEntry("SurnameEntry")  # clears the SurnameEntry
                self.app.clearEntry("UsernameEntry")  # clears the UsernameEntry
                self.app.clearEntry("PasswordEntry")  # clears the PasswordEntry
                self.app.clearEntry("RepeatPasswordEntry")  # clears the RepeatPasswordEntry
                self.app.clearEntry("PhoneNumberEntry")  # clears the PhoneNumberEntry
                self.app.clearEntry("MemorableWordEntry")  # clears the MemorableWordEntry

    def doCreateAccountToLogIn(self):
        self.app.hideSubWindow("window_CreateAnAccount")  # hides the Main Menu Sub-window
        self.app.show()  # shows the Main log in page
        self.app.clearEntry("FirstnameEntry")  # clears the FirstnameEntry
        self.app.clearEntry("SurnameEntry")  # clears the SurnameEntry
        self.app.clearEntry("UsernameEntry")  # clears the UsernameEntry
        self.app.clearEntry("PasswordEntry")  # clears the PasswordEntry
        self.app.clearEntry("RepeatPasswordEntry")  # clears the RepeatPasswordEntry
        self.app.clearEntry("PhoneNumberEntry")  # clears the PhoneNumberEntry
        self.app.clearEntry("MemorableWordEntry")  # clears the MemorableWordEntry

    def doGetPassword(self):
        returnedPassword = self.forgotPasswordValidation()  # stores the tuple returned by the function
        if returnedPassword is not None:  # checks if the tuple is not empty as that means the details entered were correct
            password = returnedPassword[0]  # stores the first value of the tuple in the password variable
            self.app.infoBox("Forgot Password", "Your Password is: " + password)  # displays a pop-up box that tells the user their password
        else:
            self.app.infoBox("Forgot Password",
                             "Memorable Word and Username do not match ")  # displays a pop-up box that tells the user their memorable word and password do not match

    def bookingValidation(self):
        bookingId = self.createBookingId()  # stores the bookingId created by the bookingId() function in the bookingId variable
        date = self.app.getOptionBox("Date: ")  # stores the date selected by the user in the option box in the date variable
        time = self.app.getSpinBox("Time: ")  # stores the time selected by the user in the spin box in the time variable
        formattedTime = times(time)
        self.cur.execute("SELECT Date, Time, PitchNumber FROM tbl_bookings WHERE Date = ? AND Time = ? AND PitchNumber = ?",
                         (date, formattedTime, self.pitchNum,))
        invalidBooking = self.cur.fetchone()
        if self.pitchNum is None:  # checks if the user has selected a pitch
            return "PITCH_NOT_SELECTED"

        if invalidBooking is not None:  # checks if the inputs selected by the user are existing as a booking within the database
            return "DOUBLE_BOOKED"
        else:
            self.cur.execute("INSERT INTO tbl_bookings (BookingID, PitchNumber, Date, Time, Price, Username) VALUES (?,?,?,?,?,?)",
                             (bookingId, self.pitchNum, date, formattedTime, self.pitchPrice, self.username))  # inserts the details into the tbl_bookings table
            self.con.commit()

            self.app.setLabel("UsersBookingID", bookingId)  # sets the label to the bookingId of the booking made
            self.app.setLabel("UsersUsername", self.username)  # sets the label to the users username
            self.app.setLabel("UsersDate", date)  # sets the label to the date of the booking made
            self.app.setLabel("UsersTime", time)  # sets the label to the time of the booking made
            self.app.setLabel("UsersPitchNumber", self.pitchNum)  # sets the label to the pitch number of the booking made
            self.app.setLabel("UsersTotalCost", self.pitchPrice)  # sets the label to the price of the pitch the user selected
            return "SUCCESS"

    def disable7aside(self):
        self.app.disableButton("BookPitch3")  # disables the BookPitch3 button
        self.app.disableButton("BookPitch4")  # disables the BookPitch4 button
        self.app.disableButton("BookPitch5")  # disables the BookPitch5 button

    def disable9aside(self):
        self.app.disableButton("BookPitch1")  # disables the BookPitch1 button
        self.app.disableButton("BookPitch2")  # disables the BookPitch2 button
        self.app.disableButton("BookPitch5")  # disables the BookPitch5 button

    def disable11aside(self):
        self.app.disableButton("BookPitch1")  # disables the BookPitch1 button
        self.app.disableButton("BookPitch2")  # disables the BookPitch2 button
        self.app.disableButton("BookPitch3")  # disables the BookPitch3 button
        self.app.disableButton("BookPitch4")  # disables the BookPitch4 button

    def enablePitches(self):
        self.app.enableButton("BookPitch1")  # enables the BookPitch1 button
        self.app.enableButton("BookPitch2")  # enables the BookPitch2 button
        self.app.enableButton("BookPitch3")  # enables the BookPitch3 button
        self.app.enableButton("BookPitch4")  # enables the BookPitch4 button
        self.app.enableButton("BookPitch5")  # enables the BookPitch5 button

    def createBookingId(self):
        bookingNum = 100  # sets the bookingNum variable to 100
        createBookingId = "B" + str(bookingNum)  # concatenated the letter B with the bookingNum
        self.cur.execute("SELECT BookingID FROM tbl_bookings WHERE BookingID = ?", (createBookingId,))  # checks if the bookingID entered is in the database
        existingBookingID = self.cur.fetchone()
        while existingBookingID is not None and existingBookingID[0] is not None:  # checks if the existingBookingID exists within the database
            bookingNum += 1  # increments the bookingNum
            createBookingId = "B" + str(bookingNum)  # concatenates the letter B with the bookingNum
            self.cur.execute("SELECT BookingID FROM tbl_bookings WHERE BookingID = ?", (createBookingId,))  # checks if the bookingID entered is in the database
            existingBookingID = self.cur.fetchone()
        return createBookingId

    def doViewBookingToMainMenu(self):
        self.app.hideSubWindow("window_ViewBooking")  # hides the ViewBooking Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the Main Menu page

    def retrieveBookingId(self):
        self.cur.execute("SELECT BookingID FROM tbl_bookings WHERE username = ?",
                         (self.username,))  # selects the bookingID from the table bookings variable where the username is equal to the users username
        bookingIds = self.cur.fetchall()
        if not bookingIds:  # checks if the bookingIds variable is empty
            return ["No bookings"]
        else:
            array = []
            for row in bookingIds:  # goes through every row in the bookingIds variable
                array.append(row[0])  # appends each value into the array
            return array  # returns the array

    def doViewBookings(self):
        self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
        self.app.showSubWindow("window_ViewBooking")  # shows the Cancel Booking Sub-window
        bookingIds = self.retrieveBookingId()
        self.app.changeOptionBox("Select a Booking ID :", bookingIds)  # changes the value in the option box to the values of the bookingIds variable

    def retrieveFutureBookingId(self):
        today = datetime.now().strftime("%Y-%m-%d")  # Gets today's date in YYYY-MM-DD format
        self.cur.execute("SELECT BookingID FROM tbl_bookings WHERE username = ? AND Date <= ?",
                         (self.username, today,))  # selects the bookingID from the table bookings variable where the username is equal to the users username
        bookingIds = self.cur.fetchall()
        if not bookingIds:  # checks if the bookingIds variable is empty
            return ["No bookings"]
        else:
            array = []  # sets the variable array to a blank array
            for row in bookingIds:  # goes through every row in the bookingIds variable
                array.append(row[0])  # appends each value into the array
            return array  # returns the array

    def doCancelBookingToMainMenu(self):
        self.app.hideSubWindow("window_CancelBooking")  # hides the Cancel Booking Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the Pitch Size Selection page

    def doCancelBooking(self):
        selectedBookingID = self.app.getOptionBox("Select booking you'd like to cancel :")  # gets the users selected bookingID
        if selectedBookingID == "No bookings":  # checks if the user has no bookings
            # shows the user an info box telling them that they have no bookings at the moment
            self.app.infoBox("Cancel Booking", "You have no bookings at the moment")
        else:
            cancelBookingConfirmation = self.app.questionBox("Cancel Booking",
                                                             "Are you sure you want to Cancel the Booking?")  # stores the result of a question box in the variable
            if cancelBookingConfirmation:  # checks if the result was true
                self.cur.execute("DELETE FROM tbl_bookings WHERE BookingID = ?",
                                 (selectedBookingID,))  # deletes the booking with the bookingID the user has selected
                self.con.commit()
                self.app.infoBox("Cancel Booking", "Your Booking has been canceled!")  # displays a pop-up box that says the account has been created
                updatedBookingIds = self.retrieveFutureBookingId()
                self.app.changeOptionBox("Select booking you'd like to cancel :", updatedBookingIds)

    def doCancelABooking(self):
        self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
        self.app.showSubWindow("window_CancelBooking")  # shows the Cancel Booking Sub-window
        bookingIds = self.retrieveFutureBookingId()
        self.app.changeOptionBox("Select booking you'd like to cancel :",
                                 bookingIds)  # changes the value in the option box to the values of the bookingIds variable

    def doMainMenuLogOut(self):
        LogOutConfirmation = self.app.questionBox("Main Menu", "Are you sure you want to Log out?")  # stores the result of a question box in the variable
        if LogOutConfirmation:  # checks if the result was true
            self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
            self.app.show()  # shows the Main log in page

    def doPitchSelection(self, name):
        if name == "7asideSelection":  # checks if the button name is 7asideSelection
            self.disable7aside()  # runs the disable7aside function
        elif name == "9asideSelection":  # checks if the button name is 9asideSelection
            self.disable9aside()  # runs the disable9aside function
        elif name == "11asideSelection":  # checks if the button name is 11asideSelection
            self.disable11aside()  # runs the disable11aside function
        self.app.hideSubWindow("window_PitchSizeSelection")  # hides the Pitch Size Selection Sub-window
        self.app.showSubWindow("window_Booking")  # shows the Booking Sub-window

    def doGetBookingInfo(self):
        selectedBookingID = self.app.getOptionBox(
            "Select a Booking ID :")  # Retrieves the users selection from the option box and stores it in selectedBookingID
        self.cur.execute("Select * FROM tbl_bookings WHERE BookingId = ?", (selectedBookingID,))
        bookingInfo = self.cur.fetchone()
        if selectedBookingID == "No bookings":  # checks if the Option Box has no BookingIds in it
            self.app.infoBox("View Booking", "You have no bookings at the moment")  # tells the user there is no information to give them
        else:
            self.app.infoBox("View Booking",
                             "Here is the booking information: "
                             "\n BookingID: " + bookingInfo[0] +  # displays the first index of the bookingInfo variable next to the text BookingID:
                             "\n Pitch Number: " + str(bookingInfo[1]) +  # displays the first index of the bookingInfo variable next to the text BookingID:
                             "\n Date: " + bookingInfo[2] +  # displays the first index of the bookingInfo variable next to the text BookingID:
                             "\n Time: " + bookingInfo[3] +  # displays the first index of the bookingInfo variable next to the text BookingID:
                             "\n Price: £" + str(bookingInfo[4]) + "0")  # displays the first index of the bookingInfo variable next to the text BookingID:

    def doMakeBooking(self):
        bookingConfirmation = self.app.questionBox("Booking",
                                                   "Are you sure you want to Make this booking?")  # stores the result of a question box in the variable
        if bookingConfirmation:  # checks if the result was true
            bookingResult = self.bookingValidation()
            if bookingResult == "SUCCESS":
                self.app.infoBox("Booking", "Booking Successful!")  # displays a pop-up box
                self.app.hideSubWindow("window_Booking")  # hides the Booking Sub-window
                self.app.showSubWindow("window_BookingSummary")  # shows the BookingSummary page
                self.enablePitches()  # enables the button widget
            elif bookingResult == "DOUBLE_BOOKED":
                self.app.infoBox("Booking", "There is already a booking at this date and time")  # tells the user that there is already a booking at this time
            elif bookingResult == "PITCH_NOT_SELECTED":
                self.app.infoBox("Booking", "Please select a pitch before making a booking.")

    def doBookingSummaryToMainMenu(self):
        self.app.hideSubWindow("window_BookingSummary")  # hides the BookingSummary Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the MainMenu page

    def doForgotPassword(self):
        self.app.hide()  # Hides the Main Log in page
        self.app.showSubWindow("window_ForgotPassword")  # shows the Forgot Password Sub-window

    def doBackToLogIn(self):
        self.app.hideSubWindow("window_ForgotPassword")  # hides the Forgot Password Sub-window
        self.app.show()  # shows the Main log in page

    def doBookAPitch(self):
        self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
        self.app.showSubWindow("window_PitchSizeSelection")  # shows the Pitch Size Selection Sub-window

    def doPitchSelectionToMainMenu(self):
        self.app.hideSubWindow("window_PitchSizeSelection")  # hides the Pitch Size Selection Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the Main Menu page

    def doBookingToPitchSizeSelection(self):
        self.enablePitches()
        self.app.hideSubWindow("window_Booking")  # hides the Booking Sub-window
        self.app.showSubWindow("window_PitchSizeSelection")  # shows the Pitch Size Selection page

    def doSelectPitch(self, name):
        if name == "BookPitch1":  # checks of the button name is BookPitch1
            self.pitchNum = "1"  # sets the pitchNum to 1
            self.pitchPrice = "50"  # set the pitchPrice to 50
        elif name == "BookPitch2":  # checks of the button name is BookPitch2
            self.pitchNum = "2"  # sets the pitchNum to 2
            self.pitchPrice = "50"  # set the pitchPrice to 50
        elif name == "BookPitch3":  # checks of the button name is BookPitch3
            self.pitchNum = "3"  # sets the pitchNum to 3
            self.pitchPrice = "75"  # set the pitchPrice to 75
        elif name == "BookPitch4":  # checks of the button name is BookPitch4
            self.pitchNum = "4"  # sets the pitchNum to 4
            self.pitchPrice = "75"  # set the pitchPrice to 75
        elif name == "BookPitch5":  # checks of the button name is BookPitch5
            self.pitchNum = "5"  # sets the pitchNum to 5
            self.pitchPrice = "100"  # set the pitchPrice to 100

    # checks if the buttons name is Sign In
    def doSignin(self):
        validateLogin = self.loginValidation()
        if validateLogin: # checks if the log in was valid
            self.app.hide()  # Hides the Main Log in page
            self.app.showSubWindow("window_MainMenu")  # shows the Main Menu Sub-window
            self.retrieveBookingId()
        self.app.clearEntry("UsernameCheck")  # clears the contents of the entry box with the label UsernameCheck
        self.app.clearEntry("PasswordCheck")  # clears the contents of the entry box with the label PasswordCheck

    def createDatabase(self):  # creates the databases and add the fields needed.
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS 'tbl_users' (
                        UserID TEXT NOT NULL PRIMARY KEY,
                        Username TEXT NOT NULL,
                        Firstname TEXT NOT NULL,
                        Surname TEXT NOT NULL,
                        Password TEXT NOT NULL,
                        PhoneNumber TEXT NOT NULL,
                        MemorableWord TEXT NOT NULL
            )""")

        self.cur.execute(""" CREATE TABLE IF NOT EXISTS 'tbl_bookings' (
                        BookingID TEXT NOT NULL PRIMARY KEY,
                        PitchNumber INTEGER NOT NULL,
                        Date DATE NOT NULL,
                        Time TIME NOT NULL,
                        Price FLOAT NOT NULL,
                        Username TEXT NOT NULL,
                        FOREIGN KEY (PitchNumber) REFERENCES tbl_pitches (PitchNumber)
            )""")

        self.cur.execute(""" CREATE TABLE IF NOT EXISTS 'tbl_pitches' (
                        PitchNumber INTEGER NOT NULL PRIMARY KEY,
                        PitchSize TEXT NOT NULL,
                        PitchPrice FLOAT NOT NULL
            )""")

        self.cur.execute(""" CREATE TABLE IF NOT EXISTS 'tbl_userBookings' (
                        UserBookingID TEXT NOT NULL PRIMARY KEY,
                        TIME TIME NOT NULL,
                        BookingID INTEGER NOT NULL,
                        UserID INTEGER NOT NULL,
                        FOREIGN KEY (BookingID) REFERENCES tbl_bookings (BookingID),
                        FOREIGN KEY (UserID) REFERENCES tbl_users (UserID)
    
            )""")

        self.con.commit()  # commit all the changes made

    def addExistingUsers(self):  # function that adds existing user data into database
        file = open("users.csv", "r")  # opens the csv file in read mode and saves it to the variable labeled file
        for line in file:  # goes through every line in the file
            line = line.strip()
            UserID, Username, Firstname, Surname, Password, PhoneNumber, MemorableWord = line.split(",")
            self.cur.execute("Insert INTO tbl_users VALUES (?,?,?,?,?,?,?)",
                             [UserID, Username, Firstname, Surname, Password, PhoneNumber, MemorableWord])
        self.con.commit()  # commit all the changes made

    def addExistingBookings(self):  # function that adds existing user data into database
        file = open("bookings.csv", "r")  # opens the csv file in read mode and saves it to the variable labeled file
        for line in file:  # goes through every line in the file
            line = line.strip()
            BookingID, PitchNumber, Date, Time, Price, Username = line.split(",")
            self.cur.execute("Insert INTO tbl_bookings VALUES (?,?,?,?,?,?)",
                             [BookingID, PitchNumber, Date, Time, Price, Username])
        self.con.commit()  # commit all the changes made

    def addExistingPitches(self):  # function that adds existing user data into database
        file = open("pitches.csv", "r")  # opens the csv file in read mode and saves it to the variable labeled file
        for line in file:  # goes through every line in the file
            line = line.strip()
            PitchNumber, PitchSize, PitchPrice = line.split(",")
            self.cur.execute("Insert INTO tbl_pitches VALUES (?,?,?)",
                             [PitchNumber, PitchSize, PitchPrice])
        self.con.commit()  # commit all the changes made


if __name__ == "__main__":
    BookingSoftware()
