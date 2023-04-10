""" Tests for GUI Survey"""
import tkinter as tk

# import SurveyApp class from the survey_app module
from surveyGUI import SurveyApp


def main():
    # create a new instance of the SurveyApp class
    survey = SurveyApp(tk.Tk())

    # run the GUI survey
    survey.run()


# call the main function to start the program
if __name__ == '__main__':
    main()
