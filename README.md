# Studentski servis

### What is it?

A small and unfinished app I did as one of the school projects. It is not finished in the sense that there are still some functionalities I thought of, but still haven't implemented. But I did implement everything that was required, and after submitting it I never quite felt like coming back to it. That being said, there are a few things that are there just for the sake of those requirements and serve no real purpose, like mapping and file reading/writing.

### What's in there?

#### 1. Server.py

Server side/School administration app *(to be separated)* through which professors can look up students and their info, schedule an exam, or change students' grades.

Staff is required to sign in with credentials that are, for now, hard-coded. After signing in, they can choose one of the three options. Each of them in one way or another fetches some data from the database or updates the tables in the case of scheduling exams and changing students' grades.

#### 2. Klijent.py

It is a client-side of the app, where students can check their info and grades, and also check upcoming exams and apply to take them.

The student is supposed to first sign in using their unique student ID. It sends a request to the server which checks if the said student exists in the database. If so, it gathers and then sends back the information about the student and his subjects. The table then populates with the information received from the server.

The student is able to see upcoming exams for each subject in a separate tab. *(to be finished)* It allows the student to apply by simply selecting a subject and pressing a button.

#### 3. DB.db

Dummy database with dummy tables and dummy data, with sole purpose of testing the app
