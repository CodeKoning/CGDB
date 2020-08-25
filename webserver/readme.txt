Corporate Governance Database - A Database Schema & Relations Project

This allows a user to peruse a few of the most valuable companies in the Fortune 500, see who their founders and governors are and see where they attended university. They can peruse by clicking hyperlinks or by searching any of the entities in the database by entering their name in the search field at the top of the page. The goal is to inform the user by showing them the how closely related many of these people are, by showing that many of them attend the same univesities, hold the same degrees and even serve on the boards of multiple companies at the same time.

**NOTES**

Searching currently does not support partial or misspelled entries. Please enter the exact search query by entering the names of any of the following entities:

Executives
Companies
Universities

To see the most extensive information in this currently "in progress" state please navigate to the index page and select from one of these companies.

Microsoft
Amazon
Facebook

These companies have the most comprehensive information at the moment and Microsoft and Amazon will exhibit the subsidiary_of relationship the best.

The same can be said for these universities:

Harvard
University of Pennsylvania
Stanford

All of the relations and entities are displayed on the following pages:

Index
- companies
- executives
- universities

Companies(id)
- companies
- officers
- directors
- member_of
- works in
- governed_boards
- overseen_committee
- founded_by

Executives(id)
- executives
- founded_by

Universities(id)
- universities
- executives
- education

I think the most interesting pages so far are the companies and universities pages. The user can see the bird's eye view of a company's officers, board members, committees etc, which they can then click to see more information about on other pages. The universities page shows all of the graduates in the database from that university and their degrees which shows how frequent these institutions are patronized by those in the upper echelons of these companies. In later iterations the user will be able to see how integrated so many of these companies and their founders and where they went to school.

