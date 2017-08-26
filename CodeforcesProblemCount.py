import urllib.request
from bs4 import BeautifulSoup as soup

#Returns soup of given link.
def getParsedHTML(link):
    response = urllib.request.urlopen(link)
    html = response.read()
    pageSoup = soup(html, "html.parser")

    return pageSoup

#Returns number of submission pages of user.
def getNumberOfPages(pageSoup):
    numberOfPages = int(pageSoup.findAll("div", {"class" :"pagination"})[-1].ul.findAll("li")[-2].a.text)

    return numberOfPages

#Returns all the submissions of user on given page.
def getSubmissionsOnPage(username, pageNumber):
    pageSoup = getParsedHTML("http://codeforces.com/submissions/" + username + "/page/" + str(pageNumber))

    problemTable = pageSoup.findAll("table",{"class" :"status-frame-datatable"})[0]
    submissions = problemTable.findAll("tr")[1: ]

    return submissions

#Returns whether given submission is accepted or not.
def problemAccepted(submissionColumns):
    currentVerdict = ""

    singleProblem = submissionColumns[5]
    spans = singleProblem.findAll("span")
    spans = spans[0].findAll("span")

    if len(spans) != 0:
        currentVerdict = singleProblem.span.span.text

    return currentVerdict == "Accepted"

#Returns name of the submitted problem.
def getProblemName(submissionColumns):
    problemName = submissionColumns[3].a.text
    problemName = problemName[18 : -14]

    return problemName

username = input("Enter Username:")
pageSoup = getParsedHTML("http://codeforces.com/submissions/" + username)

submittedProblems = set()
numberOfPages = getNumberOfPages(pageSoup)

#Iterates throught all the pages and takes all the submissions on that page
#then iterates over each submission and if verdict is accepted adds problem name
#to submittedProblems set.
for i in range(1, numberOfPages + 1):
    submissions = getSubmissionsOnPage(username, i)
    for submission in submissions:
        submissionColumns = submission.findAll("td")

        if problemAccepted(submissionColumns):
            submittedProblems.add(getProblemName(submissionColumns))

#Prints number of successfully submitted problems and then lists name of each.
print("You Have Successfully Submitted: " + str(len(submittedProblems)) + " Problems")
for problemName in submittedProblems:
    print(problemName)
