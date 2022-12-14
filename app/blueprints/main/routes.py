
from flask import render_template, request
import requests
from .import bp as main
from flask_login import login_required


@main.route('/students', methods = ['GET'])
@login_required
def students():
    my_students = ['Scarlett', 'Aydee', 'Patrick', 'Armani', 'Jalen']
    
                                                # var_name in Jinja = var name in python
    return render_template('students.html.j2', students = my_students)


@main.route('/ergast', methods=['GET','POST'])
@login_required
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        round = request.form.get('round')
        url =  f'https://ergast.com/api/f1/{year}/{round}/driverStandings.json'
        response = requests.get(url)
        if not response.ok:
            error_string = 'We had an error'
            return render_template('ergast.html.j2', error=error_string)

        if not response.json()["MRData"]["StandingsTable"]["StandingsLists"]:
            error_string = "We had an error loading your data most likely because the year/round combo is not in the database"
            return render_template('ergast.html.j2', error=error_string)

        data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        new_data = []
        for racer in data:
            racer_dict={}
            racer_dict={
                "last_name":racer['Driver']['familyName'],
                "first_name":racer['Driver']['givenName'],
                "position":racer['position'],
                "wins":racer['wins'],
                "DOB":racer['Driver']['dateOfBirth'],
                "nationality":racer['Driver']['nationality'],
                "constructor":racer['Constructors'][0]['name']
            }
            new_data.append(racer_dict)
        
        return render_template('ergast.html.j2', racers=new_data)
    return render_template('ergast.html.j2')