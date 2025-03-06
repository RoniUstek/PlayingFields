import sqlite3  # imports the SQL library.
from appJar import gui  # import gui from the self.app.ar library


class BookingSoftware:
    def __init__(self):
        self.app = gui("PlayingFields booking system")
        self.con = sqlite3.connect("pfDatabase.db")  # create my database and store it in the variable con.
        self.cur = self.con.cursor()  # set up the cursor value in my database and store it in the variable self.cur.
        self.attempts = 0
        self.seconds = 10
        self.running = False
        self.createInterface()
        self.app.go()

    def createInterface(self):
        # LOGIN PAGE: this is the initial starting page of the software,
        #             where users will be able to log into their account,
        #             go to the create an account page or the forgot password page
        self.app.addLabel("lb_Login", "Log In Page")
        self.app.setSize("600x300")  # Sets the size of the window to 600x300
        self.app.setSticky("W")
        self.app.addLabel("timer", "", 1, 3)
        self.app.addLabelEntry("UsernameCheck", 1, 0)
        self.app.setLabel("UsernameCheck", "Username *:")
        # Creates an entry box where the entered values are displayed as "*"
        self.app.addSecretLabelEntry("PasswordCheck", 2, 0)
        self.app.setLabel("PasswordCheck", "Password *:")
        self.app.addButton("SignIn", self.doSignin, 3, 0)
        self.app.setButton("SignIn", "Sign In")
        self.app.link("Forgot Password", self.doForgotPassword, 3, 1)  # Creates a hyperlink that acts as a button
        self.app.addLabel("lb_createAnAccount", "Dont have an account?", 5, 0)
        self.app.addButton("Sign Up", self.doSignUp, 6, 0)
        self.app.addLabel("lb_requiredFields", "Required Fields: *", 9, 0)

        # CREATE AN ACCOUNT PAGE: this is the page where users will enter all the required
        #                         information for them to create an account
        self.app.startSubWindow("window_CreateAnAccount")
        self.app.addLabel("lb_CreateAnAccount", "Create An Account")
        self.app.setSize("600x300")  # Sets the size of the window to 600x300
        self.app.setSticky("W")
        self.app.addLabelEntry("FirstnameEntry", 1, 0)
        self.app.setLabel("FirstnameEntry", "Firstname *:")
        self.app.addLabelEntry("SurnameEntry", 2, 0)
        self.app.setLabel("SurnameEntry", "Surname *:")
        self.app.addLabelEntry("UsernameEntry", 3, 0)
        self.app.setLabel("UsernameEntry", "Username *:")
        # Creates an entry box where the entered values are displayed as "*"
        self.app.addSecretLabelEntry("PasswordEntry", 4, 0)
        self.app.setLabel("PasswordEntry", "Password *:")
        self.app.addSecretLabelEntry("RepeatPasswordEntry", 5, 0)
        # Creates an entry box where the entered values are displayed as "*"
        self.app.setLabel("RepeatPasswordEntry", "Repeat Password *:")
        self.app.addLabelEntry("PhoneNumberEntry", 6, 0)
        self.app.setLabel("PhoneNumberEntry", "Phone Number :")
        self.app.addLabelEntry("MemorableWordEntry", 7, 0)
        self.app.setLabel("MemorableWordEntry", "Memorable Word *:")
        self.app.addButton("CreateAccountSubmit", self.doCreateAnAccountSubmit, 8, 0)
        self.app.setButton("CreateAccountSubmit", "Submit")
        self.app.addButton("CreateAccountToLogIn", self.doCreateAccountToLogIn, 9, 2)
        self.app.setButton("CreateAccountToLogIn", "Log In")
        self.app.addLabel("lb_requiredFields2", "Required Fields: *", 9, 0)
        self.app.stopSubWindow()

        # FORGOT PASSWORD PAGE: this is the page where users will use their memorable word to
        #                       retrieve their password if they have forgotten it
        self.app.startSubWindow("window_ForgotPassword")
        self.app.setSize("600x300")  # Sets the size of the window to 600x300
        self.app.setSticky("W")
        self.app.addLabel("lb_ForgotPassword", "ForgotPassword")
        self.app.addLabelEntry("UsernameChecker", 1, 0)
        self.app.setLabel("UsernameChecker", "Username *:")
        self.app.addLabelEntry("MemorableWordChecker", 2, 0)
        self.app.setLabel("MemorableWordChecker", "Memorable Word *:")
        self.app.addButton("GetPassword", self.doGetPassword, 3, 0)
        self.app.setButton("GetPassword", "Get Password")
        self.app.addLabel("lb_requiredFields3", "Required Fields: *", 9, 0)
        self.app.addButton("BackToLogIn", self.doBackToLogIn, 9, 2)
        self.app.setButton("BackToLogIn", "Log In")
        self.app.stopSubWindow()

        # MAIN MENU PAGE: this is the page that will allow users to access the Book a pitch page,
        #                 the Cancel booking page and the View bookings page,
        #                 they will also be able to log out of their account taking them back to the Log-in page
        self.app.startSubWindow("window_MainMenu")
        self.app.setSize("600x300")
        self.app.setSticky("W")
        self.app.addLabel("lb_MainMenu", "Main Menu", 0, 1)
        self.app.addButton("BookAPitch", self.doBookAPitch, 1, 1)
        self.app.setButton("BookAPitch", "Book A Pitch")
        self.app.addButton("CancelABooking", self.doCancelABooking, 2, 1)
        self.app.setButton("CancelABooking", "Cancel A Booking")
        self.app.addButton("ViewBookings", self.doViewBookings, 3, 1)
        self.app.setButton("ViewBookings", "View Bookings")
        self.app.addButton("MainMenuLogOut", self.doMainMenuLogOut, 0, 0)
        self.app.setButton("MainMenuLogOut", "Log Out")
        self.app.stopSubWindow()

        # PITCH SIZE SELECTION: this is the page that will start the booking process,
        #                       by allowing users to select the pitch size that they want
        self.app.startSubWindow("window_PitchSizeSelection")
        self.app.setSize("600x300")
        self.app.setSticky("W")
        self.app.addLabel("lb_PitchSizeSelection", "Pitch Size Selection", 0, 1)
        self.app.addButton("PitchSelectionToMainMenu", self.doPitchSelectionToMainMenu, 9, 2)
        self.app.setButton("PitchSelectionToMainMenu", "Main Menu")
        self.app.addButton("7asideSelection", self.doPitchSelection, 1, 0)
        self.app.setButton("7asideSelection", "7-aside")
        self.app.addButton("9asideSelection", self.doPitchSelection, 2, 0)
        self.app.setButton("9asideSelection", "9-aside")
        self.app.addButton("11asideSelection", self.doPitchSelection, 3, 0)
        self.app.setButton("11asideSelection", "11-aside")
        self.app.stopSubWindow()

        # CANCEL BOOKING : this is the page that will allow users to cancel a booking that they have made
        #                  if they wish to do so
        self.app.startSubWindow("window_CancelBooking")
        self.app.setSize("600x300")
        self.app.setSticky("W")
        self.app.addLabel("lb_CancelBooking", "Cancel Booking")
        self.app.addButton("CancelBookingToMainMenu", self.doCancelBookingToMainMenu, 9, 2)
        self.app.setButton("CancelBookingToMainMenu", "Main Menu")
        self.app.addLabelOptionBox("Select booking you'd like to cancel :", ["100", "101", "102", "103"], 3, 2)
        self.app.addButton("CancelBooking", self.doCancelBooking, 6, 2)
        self.app.setButton("CancelBooking", "Cancel Booking")
        self.app.stopSubWindow()

        # VIEW BOOKING: this is the page where users will be able to view all their previous and
        #              upcoming bookings
        self.app.startSubWindow("window_ViewBooking")
        self.app.setSize("600x300")
        self.app.setSticky("W")
        self.app.addLabel("lb_ViewBooking", "View Booking", 0, 2)
        self.app.addButton("ViewBookingToMainMenu", self.doViewBookingToMainMenu, 9, 2)
        self.app.setButton("ViewBookingToMainMenu", "Main Menu")
        self.app.addLabelOptionBox("Select a Booking ID :", ["100", "101", "102", "103"], 3, 2)
        self.app.addButton("GetBookingInfo", self.doGetBookingInfo, 6, 2)
        self.app.setButton("GetBookingInfo", "View Booking")
        self.app.stopSubWindow()

        # Booking: this is the page where users will be able to put all the details of the pitch they want to book
        #          as well as the date and time, allowing them to make a booking
        self.app.startSubWindow("window_Booking")
        self.app.setSize("600x300")
        self.app.setSticky("W")
        self.app.addLabel("lb_Booking", "Booking", 0, 1)
        self.app.addLabelOptionBox("Date: ", ["01/01/25", "02/01/25", "03/01/25", "04/01/25",
                                              "05/01/25", "06/01/25", "07/01/25", "08/01/25", "09/01/25", "10/01/25",
                                              "11/01/25",
                                              "12/01/25", "13/01/25", "14/01/25", "15/01/25", "16/01/25", "17/01/25",
                                              "18/01/25",
                                              "19/01/25", "20/01/25", "21/01/25", "22/01/25", "23/01/25", "24/01/25",
                                              "25/01/25",
                                              "26/01/25", "27/01/25", "28/01/25", "29/01/25", "30/01/25", "31/01/25"],
                                   1, 1)
        self.app.addLabelSpinBox("Time: ",
                                 ["8:00", "8:30", "9:00", "9:30", "10:00", "11:00", "11:30", "12:00", "12:30", "13:00",
                                  "13:30",
                                  "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00",
                                  "18:30",
                                  "19:30", "20:00"], 9, 1)
        self.app.addButton("BookingToPitchSizeSelection", self.doBookingToPitchSizeSelection, 9, 3)
        self.app.setButton("BookingToPitchSizeSelection", "Back")
        self.app.addButton("BookPitch1", self.buttonPress, 4, 1)
        self.app.setButton("BookPitch1", "Pitch 1 ")
        self.app.addButton("BookPitch2", self.buttonPress, 4, 2)
        self.app.setButton("BookPitch2", "Pitch 2")
        self.app.addButton("BookPitch3", self.buttonPress, 5, 1)
        self.app.setButton("BookPitch3", "Pitch 3")
        self.app.addButton("BookPitch4", self.buttonPress, 5, 2)
        self.app.setButton("BookPitch4", "Pitch 4")
        self.app.addButton("BookPitch5", self.buttonPress, 6, 1)
        self.app.setButton("BookPitch5", "Pitch 5")
        self.app.addButton("MakeBooking", self.doMakeBooking, 4, 3, 2, 2)
        self.app.setButton("MakeBooking", "Book Pitch")
        self.app.stopSubWindow()

        # BOOKING SUMMARY: this is the page that will display all the booking information
        self.app.startSubWindow("window_BookingSummary")
        self.app.setSize("600x300")
        self.app.setSticky("W")
        self.app.addLabel("lb_BookingSummary", "Booking Summary", 0, 2)
        self.app.addLabel("showBookingID", "BookingID :", 1, 0)
        self.app.addLabel("UsersBookingID", "bookingID", 1, 1)
        self.app.addLabel("showUsername", "Username :", 2, 0)
        self.app.addLabel("UsersUsername", "username", 2, 1)
        self.app.addLabel("ShowDate", "Date :", 3, 0)
        self.app.addLabel("UsersDate", "date", 3, 1)
        self.app.addLabel("ShowTime", "Time :", 4, 0)
        self.app.addLabel("UsersTime", "time", 4, 1)
        self.app.addLabel("ShowPitchNumber", "Pitch Number :", 5, 0)
        self.app.addLabel("UsersPitchNumber", "pitch number", 5, 1)
        self.app.addLabel("ShowTotalCost", "Total Cost :", 6, 0)
        self.app.addLabel("UsersTotalCost", "total cost", 6, 1)
        self.app.addButton("BookingSummaryToMainMenu", self.doBookingSummaryToMainMenu, 9, 2)
        self.app.setButton("BookingSummaryToMainMenu", "Main Menu")
        self.app.stopSubWindow()

    def loginValidation(self):
        self.attempts += 1
        usernameEntered = self.app.getEntry("UsernameCheck")  # stores the username entered
        passwordEntered = self.app.getEntry("PasswordCheck")  # stores the password entered
        self.cur.execute("SELECT Username, Password FROM tbl_users WHERE Username = ? AND Password = ?",
                         (usernameEntered, passwordEntered))  # checks if the username entered is in the database
        validUser = self.cur.fetchone()  # stores the first value fetched by the SQL statement

        if type(validUser) is type(None):  # checks if the username and password entered are empty
            return self.checkAttempts()

        if validUser[0] == usernameEntered and validUser[1] == passwordEntered:  # checks if the username and password are correct
            # checks if the values retrieved from the SQL statement are the same as the users inputs
            self.attempts = 0
            return True

        return self.checkAttempts()

    def checkAttempts(self):
        if self.attempts < 3:  # checks if the attempts are less than 3
            self.app.infoBox("ERROR",
                             "Username or Password is incorrect, " + str(
                                 3 - self.attempts) + " attempts remaining")  # displays an error box telling users how many attempts they have remaining
            return False
        else:
            self.app.infoBox("ERROR", "Too many failed attempts! Locking page.")  # displays an error box telling users the page is being locked
            self.disableWidgets()
            self.updateTime()
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
        minutes = self.seconds // 60
        sec = self.seconds % 60
        return f"{minutes:02}:{sec:02}"  # Formats seconds into minutes:seconds format

    def updateTime(self):
        # Updates the timer countdown every second
        if self.seconds > 0:
            self.seconds -= 1
            self.app.setLabel("timer", self.formatTime() + " left until unlock")
            self.app.after(1000, self.updateTime)  # runs the updateTime function after 1000ms
        elif self.seconds == 0:
            self.enableWidgets()
            self.app.setLabel("timer", "")  # makes the timer invisible to users
            self.attempts = 0  # resets the attempts
            self.seconds = 10  # resets the seconds

    def createAnAccountValidation(self):
        firstnameEntered = self.app.getEntry("FirstnameEntry")
        surnameEntered = self.app.getEntry("SurnameEntry")
        usernameEntered = self.app.getEntry("UsernameEntry")
        passwordEntered = self.app.getEntry("PasswordEntry")
        repeatPasswordEntered = self.app.getEntry("RepeatPasswordEntry")
        phoneNumberEntered = self.app.getEntry("PhoneNumberEntry")
        memorableWordEntered = self.app.getEntry("MemorableWordEntry")

        if firstnameEntered == "" or surnameEntered == "" or usernameEntered == "" or passwordEntered == "" or repeatPasswordEntered == "" or memorableWordEntered == "":  # Checks if fields that are required are empty
            self.app.infoBox("Create An Account", "Ensure that all required fields are filled in")
            return False
        else:
            correctFields = self.checkCreateAccountFields(usernameEntered, passwordEntered, repeatPasswordEntered, firstnameEntered, surnameEntered,
                                                          phoneNumberEntered)
            if correctFields:
                userId = self.userId()
                self.cur.execute("INSERT INTO tbl_users VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (userId, usernameEntered, firstnameEntered, surnameEntered, passwordEntered, phoneNumberEntered,
                                  memorableWordEntered))
                self.con.commit()
            return True

    def checkCreateAccountFields(self, usernameEntered, passwordEntered, repeatPasswordEntered, firstnameEntered, surnameEntered, phoneNumberEntered):
        integers = 0
        capitals = 0
        self.cur.execute("SELECT Username FROM tbl_users WHERE Username = ?",
                         (usernameEntered,))  # checks if the username entered is in the database
        username = self.cur.fetchone()  # stores the first tuple returned

        if username is not None and username[0] is not None:  # checks if there was a value in the database that equals the entered username
            self.app.infoBox("Create An Account", "There is an existing account with this username")  # tells the user that this username already exists
            return False

        for i in passwordEntered:  # iterates through all the characters in the entered password
            if i.isdigit():  # checks if the character is an integer
                integers += 1  # if the character is an integer the integer variable is incremented
            elif i.isupper():  # checks if the character is a capital letter
                capitals += 1  # if the character is a capital letter the capital variable is incremented

        if len(passwordEntered) < 8 or len(
                passwordEntered) > 24 or integers < 2 or capitals < 1:  # checks if the password is between 8 and 24 characters, has at least 2 integers and at least 1 capital letter.
            self.app.infoBox("Create An Account", "Passwords must be between 8 and 24 inclusive, have at least 2 integers and at least 1 capital letter")
            return False

        if passwordEntered != repeatPasswordEntered:
            self.app.infoBox("Create An Account", "Repeat password and Password do not match")
            return False

        if not firstnameEntered.isalpha() or not surnameEntered.isalpha():
            self.app.infoBox("Create An Account", "Username and Surname must only contain letters")
            return False

        if phoneNumberEntered != "":
            if len(phoneNumberEntered) != 11 or phoneNumberEntered[:2] != "07":
                self.app.infoBox("Create An Account", "Phone numbers should be 11 digits long and start with 07")
                return False
        return True

    def userId(self):
        userNum = 100
        createUserId = "U" + str(userNum)  # concatenated the letter U with the userNUm
        self.cur.execute("SELECT UserID FROM tbl_users WHERE UserID = ?", (createUserId,))  # checks if the username entered is in the database
        existingUserID = self.cur.fetchone()
        while existingUserID is not None and existingUserID[0] is not None:
            userNum += 1
            createUserId = "U" + str(userNum)
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

    def buttonPress(self, name):
        if name == "BookPitch1":
            pitchNum = 1

    def doCreateAnAccountSubmit(self):
        # stores the result of a question box in the variable
        createAccountConfirmation = self.app.questionBox("Create An Account", "Are you sure you want to create an account?")
        if createAccountConfirmation:  # checks if the result was true
            validInfo = self.createAnAccountValidation()
            if validInfo:
                self.app.infoBox("Create An Account",
                                 "Your account has been created!")  # displays a pop-up box that says the account has been created

    def doCreateAccountToLogIn(self):
        self.app.hideSubWindow("window_CreateAnAccount")  # hides the Main Menu Sub-window
        self.app.show()  # shows the Main log in page

    def doForgotPassword(self):
        self.app.hide()  # Hides the Main Log in page
        self.app.showSubWindow("window_ForgotPassword")  # shows the Forgot Password Sub-window

    def doGetPassword(self):
        returnedPassword = self.forgotPasswordValidation()  # stores the tuple returned by the function
        if returnedPassword is not None:  # checks if the tuple is not empty as that means the details entered were correct
            password = returnedPassword[0]  # stores the first value of the tuple in the password variable
            self.app.infoBox("Forgot Password", "Your Password is: " + password)  # displays a pop-up box that tells the user their password
        else:
            self.app.infoBox("Forgot Password",
                             "Memorable Word and password do not match ")  # displays a pop-up box that tells the user their memorable word and password do not match

    def doBackToLogIn(self):
        self.app.hideSubWindow("window_ForgotPassword")  # hides the Forgot Password Sub-window
        self.app.show()  # shows the Main log in page

    def doBookAPitch(self):
        self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
        self.app.showSubWindow("window_PitchSizeSelection")  # shows the Pitch Size Selection Sub-window

    def doCancelABooking(self):
        self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
        self.app.showSubWindow("window_CancelBooking")  # shows the Cancel Booking Sub-window

    def doViewBookings(self):
        self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
        self.app.showSubWindow("window_ViewBooking")  # shows the Cancel Booking Sub-window

    def doMainMenuLogOut(self):
        LogOutConfirmation = self.app.questionBox("Main Menu", "Are you sure you want to Log out?")  # stores the result of a question box in the variable
        if LogOutConfirmation:  # checks if the result was true
            self.app.hideSubWindow("window_MainMenu")  # hides the Main Menu Sub-window
            self.app.show()  # shows the Main log in page

    def doPitchSelectionToMainMenu(self):
        self.app.hideSubWindow("window_PitchSizeSelection")  # hides the Pitch Size Selection Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the Main Menu page

    def doPitchSelection(self):
        self.app.hideSubWindow("window_PitchSizeSelection")  # hides the Pitch Size Selection Sub-window
        self.app.showSubWindow("window_Booking")  # shows the Booking Sub-window

    def doViewBookingToMainMenu(self):
        self.app.hideSubWindow("window_ViewBooking")  # hides the ViewBooking Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the Main Menu page

    def doGetBookingInfo(self):
        selectedBookingID = self.app.getOptionBox(
            "Select a Booking ID :")  # Retrieves the users selection from the option box and stores it in selectedBookingID
        self.app.infoBox("View Booking", "Here is the booking information")  # displays a pop-up box

    def doCancelBooking(self):
        cancelBookingConfirmation = self.app.questionBox("Cancel Booking",
                                                         "Are you sure you want to Cancel the Booking?")  # stores the result of a question box in the variable
        if cancelBookingConfirmation:  # checks if the result was true
            self.app.infoBox("Cancel Booking", "Your Booking has been canceled!")  # displays a pop-up box that says the account has been created

    def doCancelBookingToMainMenu(self):
        self.app.hideSubWindow("window_CancelBooking")  # hides the Cancel Booking Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the Pitch Size Selection page

    def doBookingToPitchSizeSelection(self):
        self.app.hideSubWindow("window_Booking")  # hides the Booking Sub-window
        self.app.showSubWindow("window_PitchSizeSelection")  # shows the Pitch Size Selection page

    def doMakeBooking(self):
        bookingConfirmation = self.app.questionBox("Booking",
                                                   "Are you sure you want to Make this booking?")  # stores the result of a question box in the variable
        if bookingConfirmation:  # checks if the result was true
            self.app.infoBox("Booking", "Booking Successful!")  # displays a pop-up box
            self.app.hideSubWindow("window_Booking")  # hides the Booking Sub-window
            self.app.showSubWindow("window_BookingSummary")  # shows the BookingSummary page

    def doBookingSummaryToMainMenu(self):
        self.app.hideSubWindow("window_BookingSummary")  # hides the BookingSummary Sub-window
        self.app.showSubWindow("window_MainMenu")  # shows the MainMenu page

    def doSignUp(self):
        self.app.hide()  # Hides the Main Log in page
        self.app.showSubWindow("window_CreateAnAccount")  # shows the Create An Account Sub-window

    # checks if the buttons name is Sign In
    def doSignin(self):
        validateLogin = self.loginValidation()
        if validateLogin:
            self.app.hide()  # Hides the Main Log in page
            self.app.showSubWindow("window_MainMenu")  # shows the Main Menu Sub-window
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
