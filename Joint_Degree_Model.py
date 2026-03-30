#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:21:55 2026

@author: georgiasilk
"""

import xpress as xp
import numpy as np 
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
# %%
import xpress as xp
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
# %%
programme_df = pd.read_csv('2024-5 DPT Data.csv', encoding="latin1")
courses_df = pd.read_csv("2024-5 Event Module Room.csv")
departments = [
    'School of Philosophy, Psychology and Language Sciences',
    'School of Economics',
    'School of Informatics',
    'School of Physics and Astronomy',
    'Business School'
]
programmes = ['Mathematics and Business BSc (Hons)',
              'Mathematics and Physics (BSc Hons)',
              'Economics and Mathematics (MA Hons)',
              'Computer Science and Mathematics (BSc Hons)',
              'Philosophy and Mathematics (MA Hons)'
              ]

needed = [
    '2024-25: UTMATHB : Y3 options : Business options', '2024-25: UTMATHB : Y4/5 : Approved Outside Courses',
    'ROU_H_UT International Business 4_10',

    'Economics Course Options for Joint Programmes Year 3 (A)', 'Topics in Microeconomics',
    'Essentials of Econometrics', 'Economics Course Options Year 3 (joint programmes)',
    'Economics Course Options Year 4 (joint programmes)',

    'Electromagnetism and Relativity', 'Undergraduate (School of Physics and Astronomy) Level 9 and 10  courses',
    'MathsPhysics : Y3 physics choice', 'MathsPhysics : Y4 Physics Projects',
    'Undergraduate (School of Physics and Astronomy) Level 10 and 11 courses',

    'Informatics Hons 3rd Year Group Project and Large Practical', 'Informatics Hons 3rd Year AI Courses',
    'Informatics Hons 3rd Year Joint Degree CS Courses', 'Informatics - Professional Issues',
    'Informatics Hons 4th Year Courses',

    'Year 3 Philosophy - History of Philosophy', 'Practical Philosophy', 'Theoretical Philosophy',
    'Philosophy Honours Year 4'
]
years = [3, 4]
programme_df = programme_df[programme_df['Programme Name'].isin(programmes)]
programme_df = programme_df[programme_df['Programme Year'].isin(years)]
courses_df = courses_df[courses_df['Module Department'].isin(departments)]
programme_df = programme_df[programme_df['Collection Name'].isin(needed)]
# %%
# Changes for economics
economics_course_change = (
    (courses_df[
         'Module Name'] == 'Advanced Mathematical Economics, Advanced Mathematical Economics, Advanced Mathematical Economics, Mathematical Microeconomics 1')
)
courses_df.loc[economics_course_change, 'Module Name'] = 'Advanced Mathematical Economics'

economics_course_change_1 = (
    (courses_df[
         'Module Name'] == 'Advanced Mathematical Economics, Advanced Mathematical Economics, Mathematical Microeconomics 1, Advanced Mathematical Economics')
)
courses_df.loc[economics_course_change_1, 'Module Name'] = 'Advanced Mathematical Economics'


def filtering(programme_name, module_department, startwith):
    prog = programme_df[programme_df['Programme Name'] == programme_name]
    cour = courses_df[courses_df['Module Department'] == module_department]
    all_courses = sorted(cour['Module Name'].unique())
    filtered = prog[~prog['Course Code'].str.startswith(startwith)]
    filtered_courses = sorted(filtered['Course Name'].unique())
    not_there = sorted(list(set(filtered_courses) - set(all_courses)))
    return all_courses, not_there


programme_df['Collection Name'].unique()
# %%
a_phy, n_phy = filtering('Mathematics and Physics (BSc Hons)', 'School of Physics and Astronomy', 'MAT')
for i in n_phy:
    for j in a_phy:
        l = [x.strip() for x in j.split(',')]
        if i in l:
            condition = ((courses_df['Module Name'] == j))
            courses_df.loc[condition, 'Module Name'] = i
# programme_df= programme_df[~programme_df['Course Name'].isin(['Statistical Mechanics','Thermodynamics'])]
condition = ((programme_df[
                  'Collection Name'] == 'Undergraduate (School of Physics and Astronomy) Level 9 and 10  courses') &
             (programme_df['Course Name'] == 'Thermal Physics'))
programme_df = programme_df[~condition]
# Informatics changes
a_inf, n_inf = filtering('Computer Science and Mathematics (BSc Hons)', 'School of Informatics', ('MAT', 'Lev'))

for i in n_inf:
    for j in a_inf:
        if i in j:
            condition = ((courses_df['Module Name'] == j))
            courses_df.loc[condition, 'Module Name'] = i

name = 'Speech Processing, Speech Processing (Hons)'

condition = ((courses_df['Module Name'] == name))
courses_df.loc[condition, 'Module Name'] = 'Speech Processing (Hons)'
# %%
a_phi, n_phi = filtering('Philosophy and Mathematics (MA Hons)',
                         'School of Philosophy, Psychology and Language Sciences', ('MAT'))

for i in n_phi:
    for j in a_phi:
        if i in j:
            condition = ((courses_df['Module Name'] == j))
            courses_df.loc[condition, 'Module Name'] = i
# Changing name of degree programmes
for degree in programmes:
    for year in years:
        condition = ((programme_df['Programme Name'] == degree) &
                     (programme_df['Programme Year'] == year))
        programme_df.loc[condition, 'Programme Name'] = degree + ': Year ' + str(year)

programmes = programme_df['Programme Name'].unique()
# Filtering unnecessary courses
n_phy_3 = filtering('Mathematics and Physics (BSc Hons): Year 3', 'School of Physics and Astronomy', ('Lev', 'MAT'))[1]
n_phy_4 = filtering('Mathematics and Physics (BSc Hons): Year 4', 'School of Physics and Astronomy', ('Lev', 'MAT'))[1]
n_bus_3 = filtering('Mathematics and Business BSc (Hons): Year 3', 'Business School', ('Lev', 'MAT'))[1]
n_bus_4 = filtering('Mathematics and Business BSc (Hons): Year 4', 'Business School', ('Lev', 'MAT'))[1]
n_phi_3 = \
filtering('Philosophy and Mathematics (MA Hons): Year 3', 'School of Philosophy, Psychology and Language Sciences',
          ('Lev', 'MAT'))[1]
n_phi_4 = \
filtering('Philosophy and Mathematics (MA Hons): Year 4', 'School of Philosophy, Psychology and Language Sciences',
          ('Lev', 'MAT'))[1]
not_required_courses = n_phy_3 + n_phy_4 + n_bus_3 + n_bus_4 + n_phi_3 + n_phi_4

programme_df = programme_df[
    ~programme_df['Course Name'].isin(not_required_courses)
]
# %%
# Fixing Reg Group Names
for degree in programmes:
    new = programme_df[programme_df['Programme Name'] == degree]
    groups = new['Collection Reg Group'].dropna().unique()
    for collection in groups:
        condition = (
                (programme_df['Programme Name'] == degree) &
                (programme_df['Collection Reg Group'] == collection)
        )
        programme_df.loc[condition, 'Collection Reg Group'] = degree + ', Group ' + str(collection)

condition = (
        (programme_df['Collection Reg Group'].isna()) &
        (programme_df['Programme Year'].isin([3, 4]))
)
programme_df.loc[condition, [
    'Collection Reg Group',
    'Collection Group Max',
    'Collection Group Min'
]] = programme_df.loc[condition, [
    'Collection Name',
    'Collection Max Value',
    'Collection Min Value'
]].values

condition_1 = ((programme_df['Collection Reg Group'] == 'Mathematics and Physics (BSc Hons): Year 3, Group A'))
programme_df.loc[condition_1, ['Collection Group Min', 'Collection Group Max']] = [0.0, 40.0]
condition_2 = ((programme_df['Collection Reg Group'] == 'Mathematics and Business BSc (Hons): Year 3, Group B'))
programme_df.loc[condition_2, ['Collection Group Min', 'Collection Group Max']] = [0, 60.0]
condition_3 = ((programme_df['Collection Reg Group'] == 'Philosophy and Mathematics (MA Hons): Year 3, Group B'))
programme_df.loc[condition_3, ['Collection Group Min', 'Collection Group Max']] = [40.0, 80.0]
condition_4 = ((programme_df['Collection Reg Group'] == 'Economics and Mathematics (MA Hons): Year 3, Group A'))
programme_df.loc[condition_4, ['Collection Group Min', 'Collection Group Max']] = [0.0, 20.0]
condition_5 = ((programme_df['Collection Reg Group'] == 'Mathematics and Physics (BSc Hons): Year 4, Group A'))
programme_df.loc[condition_5, ['Collection Group Min', 'Collection Group Max']] = [0.0, 20.0]
condition_6 = ((programme_df['Collection Reg Group'] == 'Mathematics and Physics (BSc Hons): Year 4, Group B'))
programme_df.loc[condition_6, ['Collection Group Min', 'Collection Group Max']] = [0.0, 40.0]
condition_7 = ((programme_df['Collection Reg Group'] == 'Mathematics and Business BSc (Hons): Year 4, Group A'))
programme_df.loc[condition_7, ['Collection Group Min', 'Collection Group Max']] = [40.0, 60.0]
condition_8 = ((programme_df['Collection Reg Group'] == 'Computer Science and Mathematics (BSc Hons): Year 4, Group A'))
programme_df.loc[condition_8, ['Collection Group Min', 'Collection Group Max']] = [0.0, 40.0]
condition_9 = ((programme_df['Collection Reg Group'] == 'Computer Science and Mathematics (BSc Hons): Year 4, Group B'))
programme_df.loc[condition_9, ['Collection Group Min', 'Collection Group Max']] = [0.0, 60.0]
# %%
courses_df = courses_df[courses_df['Event Type'].isin(['Lecture', 'Laboratory', 'Seminar'])]


# %%
def extract_programme_structure(programme_df):
    """
    Extract programme-specific information including collections and regression groups
    Returns a dictionary structure with collections and regression groups as dictionaries
    """
    # Get unique programmes
    programmes = programme_df['Programme Name'].unique().tolist()

    programme_data = {}

    for programme in programmes:
        prog_data = programme_df[programme_df['Programme Name'] == programme]

        # Get compulsory and optional courses for this programme
        compulsory_courses = prog_data[
            prog_data['Compulsory/Optional'] == 'Compulsory'
            ]['Course Name'].unique().tolist()

        optional_courses = prog_data[
            prog_data['Compulsory/Optional'] == 'Optional'
            ]['Course Name'].unique().tolist()

        # Get all courses for this programme
        all_courses = prog_data['Course Name'].unique().tolist()

        # Get collection information - store as dictionary
        collections = {}
        for _, row in prog_data.iterrows():
            collection_code = row.get('Collection Code')
            if pd.notna(collection_code) and collection_code != '':
                if collection_code not in collections:
                    collections[collection_code] = {
                        'name': row.get('Collection Name', ''),
                        'min_value': row.get('Collection Min Value', 0),
                        'max_value': row.get('Collection Max Value', 999),
                        'reg_group': row.get('Collection Reg Group', ''),
                        'courses': []
                    }
                # Add course to collection if not already there
                if row['Course Name'] not in collections[collection_code]['courses']:
                    collections[collection_code]['courses'].append(row['Course Name'])

        # Get regression group information - store as dictionary
        regression_groups = {}
        for _, row in prog_data.iterrows():
            reg_group = row.get('Collection Reg Group')
            if pd.notna(reg_group) and reg_group != '':
                if reg_group not in regression_groups:
                    regression_groups[reg_group] = {
                        'min_value': row.get('Collection Group Min', 0),
                        'max_value': row.get('Collection Group Max', 999),
                        'collections': []
                    }
                # Add collection to regression group if not already there
                collection_code = row.get('Collection Code')
                if pd.notna(collection_code) and collection_code != '':
                    if collection_code not in regression_groups[reg_group]['collections']:
                        regression_groups[reg_group]['collections'].append(collection_code)

        programme_data[programme] = {
            'compulsory_courses': compulsory_courses,
            'optional_courses': optional_courses,
            'all_courses': all_courses,
            'collections': collections,
            'regression_groups': regression_groups
        }

    return programme_data


programme_data = extract_programme_structure(programme_df)


# programme_data
# %%


def extract_timetable_info(courses_df, programmes_data):
    """
    Extract v parameter with dynamic duration per course
    """
    # Filter for all relevant courses
    all_relevant_courses = {"G1", "G2", "G3", "G4", 'G5', 'G6', 'G7', 'G8', 'O1', 'O2', 'O3', 'O4'}

    for programme in programmes_data:
        all_relevant_courses.update(programmes_data[programme]['compulsory_courses'])
        all_relevant_courses.update(programmes_data[programme]['optional_courses'])

    # Filter timetable data for relevant courses
    relevant_schedule = courses_df[courses_df['Module Name'].isin(all_relevant_courses)].copy()

    # Parse timeslot (format: "Monday 10:00")
    def parse_timeslot(timeslot):
        if pd.isna(timeslot):
            return None, None
        parts = str(timeslot).split()
        if len(parts) >= 2:
            day = parts[0]
            time_str = parts[1]
            hour = int(time_str.split(':')[0])
            return day, hour
        return None, None

    # Parse weeks (format like "1-11,13-24")
    def parse_weeks(weeks_str):
        if pd.isna(weeks_str):
            return []
        weeks = []
        for part in str(weeks_str).split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                weeks.extend(range(start, end + 1))
            else:
                weeks.append(int(part))
        return weeks

    # Map days to integers
    day_map = {
        'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
        'Friday': 5, 'Saturday': 6, 'Sunday': 7,
        'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7
    }

    # Create v parameter dictionary
    v = {}

    # For each course, build a dictionary of its scheduled events with durations
    for course in relevant_schedule['Module Name'].unique():
        course_schedule = relevant_schedule[relevant_schedule['Module Name'] == course]

        for _, row in course_schedule.iterrows():
            # Get timeslot
            day, start_hour = parse_timeslot(row['Timeslot'])
            if day is None:
                continue

            day_num = day_map.get(day, 0)
            if day_num == 0:
                print(f"Warning: Unknown day format: {day}")
                continue

            # Get duration from the Duration column
            duration = row['Duration (minutes)']
            if pd.isna(duration):
                # Fallback: use default based on event type
                event_type = row['Event Type']
                default_durations = {
                    'Lecture': 60,
                    'Workshop': 60,
                    'Tutorial': 60,
                    'Lab': 120,
                    'Seminar': 60
                }
                duration = default_durations.get(event_type, 60)

            # Calculate end hour (assuming duration is in minutes)
            # If duration is 60, end_hour = start_hour + 1
            # If duration is 90, end_hour = start_hour + 1.5 (we'll handle half-hours)
            # For simplicity, we'll treat hour slots as discrete and mark all hours covered
            duration_hours = duration / 60
            end_hour_float = start_hour + duration_hours

            # Determine which hour slots this event occupies
            # For integer hours, we can use integer hours
            occupied_hours = []
            current_hour = start_hour
            remaining_duration = duration

            while remaining_duration > 0:
                occupied_hours.append(current_hour)
                remaining_duration -= 60
                current_hour += 1

            # Alternative: if you want to handle half-hour slots more precisely
            # occupied_hours = [h for h in range(start_hour, start_hour + int(np.ceil(duration_hours)))]

            # Parse weeks
            weeks = parse_weeks(row['Weeks'])

            # Determine semester
            semester = row['Semester']
            if semester not in [1, 2]:
                # If semester is not 1 or 2, try to infer from weeks
                if weeks and max(weeks) <= 26:
                    semester = 1
                elif weeks and min(weeks) >= 27:
                    semester = 2
                else:
                    semester = 1

            campus = row['Campus']

            # For each week the course runs
            for week in weeks:
                # For each hour slot the course occupies
                for hour in occupied_hours:
                    # For each programme that includes this course
                    for programme in programmes_data:
                        if course in programmes_data[programme]['all_courses']:
                            v[(course, day_num, hour, week, programme, campus)] = 1
                        else:
                            v[(course, day_num, hour, week, programme, campus)] = 0

    return v


programmes_data = extract_programme_structure(programme_df)


# extract_timetable_info(courses_df, programmes_data)
# %%
def extract_days_hours_from_v(v):
    """
    Extract unique days and hours from v dictionary
    """
    if not v:
        # If v is empty, use default days and hours
        return [1, 2, 3, 4, 5], list(range(9, 17))  # Monday-Friday, 9am-5pm

    days = sorted(list(set([key[1] for key in v.keys()])))
    hours = sorted(list(set([key[2] for key in v.keys()])))

    # If no days/hours found, use defaults
    if not days:
        days = [1, 2, 3, 4, 5]
    if not hours:
        hours = list(range(9, 17))

    return days, hours


# Add this to your extract_all_parameters function
def extract_all_parameters(courses_df, programme_df):
    """
    Complete extraction including days and hours
    """

    # Step 1: Define Maths courses
    gateway_courses = ["G1", "G2", "G3", "G4", 'G5', 'G6', 'G7', 'G8']
    optional_courses = ['O1', 'O2', 'O3', 'O4']

    # Step 2: Extract programme structure
    programme_data = extract_programme_structure(programme_df)
    programmes = list(programme_data.keys())

    # Step 3: Extract timetable info
    v = extract_timetable_info(courses_df, programme_data)

    # Step 4: Extract days and hours from v
    # days, hours = extract_days_hours_from_v(v)
    days = [1, 2, 3, 4, 5]
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17]

    weeks = list(range(1, 53))  # E = {1, ..., 52}
    weeks_sem1 = list(range(9, 19))  # E_1 = {9, ..., 19}
    weeks_sem2 = list(range(26, 37))  # E_2 = {26, ..., 37}

    campuses = courses_df['Campus'].dropna().unique().tolist()

    # Build the complete parameter set
    parameters = {
        # Sets
        'G': gateway_courses,
        'O': optional_courses,
        'S': [1, 2],  # Semesters
        'D': days,  # Days extracted from timetable
        'H': hours,  # Hours extracted from timetable
        'W': [1, 2],  # Week parity
        'Q': programmes,
        'E': weeks,  # All weeks
        'E1': weeks_sem1,  # Semester 1 weeks
        'E2': weeks_sem2,  # Semester 2 weeks
        'K': campuses,  # Campuses
        # Parameters
        'R_g_L': 3,  # Fixed for gateway
        'R_g_W': 1,  # Fixed for gateway
        'R_g_F': 1,  # Fixed for gateway
        'R_o_L': 3,  # Fixed for optional
        'R_o_W': 1,  # Fixed for optional
        'C_g': 4,  # 4 gateway courses per semester
        'C_o': 2,  # 2 optional courses per semester
        'n_q': {programme: 40 for programme in programmes},  # 40 credits outside Maths
        'n_co': {},  # Credits for each course
        'v': v,

        # Programme-specific data
        'programme_data': programme_data,

        # Collection and regression groups
        'min_CL': {},
        'max_CL': {},
        'min_CR': {},
        'max_CR': {},
        'SC_cl': {},
        'SCL_cr': {}
    }

    # Extract credits (same as before)
    all_courses = set(gateway_courses + optional_courses)
    for programme in programmes:
        all_courses.update(programme_data[programme]['all_courses'])

    for course in all_courses:
        credit_info = programme_df[programme_df['Course Name'] == course]['SCQF Credits']
        if len(credit_info) > 0:
            credit_value = credit_info.iloc[0]
            if isinstance(credit_value, str):
                import re
                numbers = re.findall(r'\d+\.?\d*', credit_value)
                if numbers:
                    parameters['n_co'][course] = float(numbers[0])
                else:
                    parameters['n_co'][course] = 20.0
            else:
                parameters['n_co'][course] = float(credit_value)
        else:
            parameters['n_co'][course] = 20.0

    # Extract collection information
    for programme in programmes:
        prog_collections = programme_data[programme]['collections']
        for cl_id, cl_info in prog_collections.items():
            parameters['min_CL'][cl_id] = cl_info['min_value']
            parameters['max_CL'][cl_id] = cl_info['max_value']

            if cl_id not in parameters['SC_cl']:
                parameters['SC_cl'][cl_id] = []
            for course in cl_info['courses']:
                if course not in parameters['SC_cl'][cl_id]:
                    parameters['SC_cl'][cl_id].append(course)

    # Extract regression group information
    for programme in programmes:
        prog_reg_groups = programme_data[programme]['regression_groups']
        for rg_id, rg_info in prog_reg_groups.items():
            parameters['min_CR'][rg_id] = rg_info['min_value']
            parameters['max_CR'][rg_id] = rg_info['max_value']

            if rg_id not in parameters['SCL_cr']:
                parameters['SCL_cr'][rg_id] = []
            for cl in rg_info['collections']:
                if cl not in parameters['SCL_cr'][rg_id]:
                    parameters['SCL_cr'][rg_id].append(cl)

    # Print summary
    print(f"\nExtraction Summary:")
    print(f"  - Gateway courses: {len(parameters['G'])}")
    print(f"  - Optional courses: {len(parameters['O'])}")
    print(f"  - Programmes: {len(parameters['Q'])}")
    print(f"  - Days: {parameters['D']}")
    print(f"  - Hours: {parameters['H']}")
    print(f"  - Weeks: {len(parameters['E'])} (Sem1: {len(parameters['E1'])}, Sem2: {len(parameters['E2'])})")
    print(f"  - Campuses: {parameters['K']}")
    print(f"  - Collections: {len(parameters['SC_cl'])}")
    print(f"  - Regression groups: {len(parameters['SCL_cr'])}")
    print(f"  - Timetable entries: {len(parameters['v'])}")
    print(f"  - Courses with credits: {len(parameters['n_co'])}")

    return parameters


parameters = extract_all_parameters(courses_df, programme_df)


# %%
def create_model_data(parameters):
    """
    Convert extracted parameters into model-ready format
    """

    # Create mappings for indices
    course_to_idx = {course: idx for idx, course in enumerate(parameters['G'] + parameters['O'])}
    programme_to_idx = {prog: idx for idx, prog in enumerate(parameters['Q'])}

    # Create day and hour mappings
    # You'll need to extract actual days and hours from your timetable data
    days = sorted(list(set([key[1] for key in parameters['v'].keys() if len(key) > 1])))
    hours = sorted(list(set([key[2] for key in parameters['v'].keys() if len(key) > 2])))

    model_ready = {
        'G': parameters['G'],
        'O': parameters['O'],
        'S': parameters['S'],
        'D': days,
        'H': hours,
        'W': [1, 2],
        'Q': parameters['Q'],
        'E': parameters['E'],  # All weeks
        'E1': parameters['E1'],  # Semester 1 weeks
        'E2': parameters['E2'],  # Semester 2 weeks
        'K': parameters['K'],  # Campuses

        'R_g_L': parameters['R_g_L'],
        'R_g_W': parameters['R_g_W'],
        'R_g_F': parameters['R_g_F'],
        'R_o_L': parameters['R_o_L'],
        'R_o_W': parameters['R_o_W'],
        'C_g': parameters['C_g'],
        'C_o': parameters['C_o'],

        'min_CL': parameters['min_CL'],
        'max_CL': parameters['max_CL'],
        'min_CR': parameters['min_CR'],
        'max_CR': parameters['max_CR'],

        'n_co': parameters['n_co'],
        'n_q': parameters['n_q'],

        'CO_CO_q': {prog: parameters['programme_data'][prog]['compulsory_courses']
                    for prog in parameters['Q']},
        'CO_OP_q': {prog: parameters['programme_data'][prog]['optional_courses']
                    for prog in parameters['Q']},
        'CO_q': {prog: parameters['programme_data'][prog]['all_courses']
                 for prog in parameters['Q']},

        'SC_cl': parameters['SC_cl'],
        'SCL_cr': parameters['SCL_cr'],

        'v': parameters['v']
    }

    return model_ready


# %%
# Extract all parameters
parameters = extract_all_parameters(courses_df, programme_df)

# Convert to model-ready format
model_data = create_model_data(parameters)

# Now you can use model_data to build your Xpress model
print(f"Number of gateway courses: {len(model_data['G'])}")
print(f"Number of optional courses: {len(model_data['O'])}")
print(f"Number of programmes: {len(model_data['Q'])}")
print(f"Collection groups: {len(model_data['SC_cl'])}")
print(f"Regression groups: {len(model_data['SCL_cr'])}")

travel_data = [
    ("Bioquarter", "Bioquarter", 0),
    ("Central", "Bioquarter", 60),
    ("Easter Bush", "Bioquarter", 60),
    ("Holyrood", "Bioquarter", 60),
    ("King's Buildings", "Bioquarter", 60),
    ("Lauriston", "Bioquarter", 60),
    ("New College", "Bioquarter", 60),
    ("Western General", "Bioquarter", 60),
    ("Bioquarter", "Central", 60),
    ("Central", "Central", 0),
    ("Easter Bush", "Central", 60),
    ("Holyrood", "Central", 10),
    ("King's Buildings", "Central", 30),
    ("Lauriston", "Central", 10),
    ("New College", "Central", 10),
    ("Western General", "Central", 60),
    ("Bioquarter", "Easter Bush", 60),
    ("Central", "Easter Bush", 60),
    ("Easter Bush", "Easter Bush", 0),
    ("Holyrood", "Easter Bush", 60),
    ("King's Buildings", "Easter Bush", 60),
    ("Lauriston", "Easter Bush", 60),
    ("New College", "Easter Bush", 60),
    ("Western General", "Easter Bush", 60),
    ("Bioquarter", "Holyrood", 60),
    ("Central", "Holyrood", 10),
    ("Easter Bush", "Holyrood", 60),
    ("Holyrood", "Holyrood", 0),
    ("King's Buildings", "Holyrood", 30),
    ("Lauriston", "Holyrood", 10),
    ("New College", "Holyrood", 10),
    ("Western General", "Holyrood", 60),
    ("Bioquarter", "King's Buildings", 60),
    ("Central", "King's Buildings", 30),
    ("Easter Bush", "King's Buildings", 60),
    ("Holyrood", "King's Buildings", 30),
    ("King's Buildings", "King's Buildings", 0),
    ("Lauriston", "King's Buildings", 30),
    ("New College", "King's Buildings", 30),
    ("Western General", "King's Buildings", 60),
    ("Bioquarter", "Lauriston", 60),
    ("Central", "Lauriston", 10),
    ("Easter Bush", "Lauriston", 60),
    ("Holyrood", "Lauriston", 10),
    ("King's Buildings", "Lauriston", 30),
    ("Lauriston", "Lauriston", 0),
    ("New College", "Lauriston", 10),
    ("Western General", "Lauriston", 60),
    ("Bioquarter", "New College", 60),
    ("Central", "New College", 10),
    ("Easter Bush", "New College", 60),
    ("Holyrood", "New College", 10),
    ("King's Buildings", "New College", 30),
    ("Lauriston", "New College", 10),
    ("New College", "New College", 0),
    ("Western General", "New College", 60),
    ("Bioquarter", "Western General", 60),
    ("Central", "Western General", 60),
    ("Easter Bush", "Western General", 60),
    ("Holyrood", "Western General", 60),
    ("King's Buildings", "Western General", 60),
    ("Lauriston", "Western General", 60),
    ("New College", "Western General", 60),
    ("Western General", "Western General", 0)
]

# Create a dictionary for fast lookup
travel_time_dict = {}
for from_camp, to_camp, tt in travel_data:
    travel_time_dict[(from_camp, to_camp)] = tt

# ============= BUILD MODEL =============== #

def build_model_from_parameters(parameters):
    """
    Build the Xpress model for joint degrees (without pathway choices).
    """
    # Unpack parameters
    G = parameters['G']
    O = parameters['O']
    S = parameters['S']
    D = parameters['D']
    H = parameters['H']
    W = parameters['W']
    Q = parameters['Q']
    E = parameters['E']
    E1 = parameters['E1']
    E2 = parameters['E2']
    K = parameters['K']
    C_g = parameters['C_g']
    C_o = parameters['C_o']
    R_g_L = parameters['R_g_L']
    R_g_W = parameters['R_g_W']
    R_g_F = parameters['R_g_F']
    R_o_L = parameters['R_o_L']
    R_o_W = parameters['R_o_W']
    v = parameters['v']
    programme_data = parameters['programme_data']
    CO_CO_q = {prog: programme_data[prog]['compulsory_courses'] for prog in Q}
    CO_OP_q = {prog: programme_data[prog]['optional_courses'] for prog in Q}
    CO_q = {prog: programme_data[prog]['all_courses'] for prog in Q}
    SC_cl = parameters['SC_cl']
    SCL_cr = parameters['SCL_cr']
    min_CL = parameters['min_CL']
    max_CL = parameters['max_CL']
    min_CR = parameters['min_CR']
    max_CR = parameters['max_CR']
    n_co = parameters['n_co']
    n_q = parameters['n_q']
    QQ=Q+['math']

    # Soft constraint weights
    lambda_travel = 0.01
    lambda_clash = 0.1
    lambda_late     = 0.344249   # after 5pm
    lambda_lunch    = 0.112523   # lunch time
    lambda_isolated = 0.057430   # isolated class
    lambda_days     = 0.133207   # number of days
    lambda_wed      = 0.028978

    # Travel time dictionary
    global travel_time_dict

    # Constants based on actual hours
    late_hour = 17
    lunch_hours = [12, 13]
    isolated_hours = list(range(10, 17))
    wednesday_hours = list(range(13, 18))
    wed_idx = 3  # Wednesday is day index 3

    # Create problem
    p = xp.problem()

    # ==================== DECISION VARIABLES ====================
    print("Creating decision variables...")

    # Gateway variables
    x_L = {}
    x_W = {}
    x_F = {}
    for g in G:
        for d in D:
            for h in H:
                for s in S:
                    x_L[(g, d, h, s)] = xp.var(vartype=xp.binary, name=f"xL_{g}_{d}_{h}_{s}")
                    x_W[(g, d, h, s)] = xp.var(vartype=xp.binary, name=f"xW_{g}_{d}_{h}_{s}")
                    for w in W:
                        x_F[(g, d, h, s, w)] = xp.var(vartype=xp.binary, name=f"xF_{g}_{d}_{h}_{s}_{w}")

    # Optional maths variables
    y_L = {}
    y_W = {}
    for o in O:
        for d in D:
            for h in H:
                for s in S:
                    y_L[(o, d, h, s)] = xp.var(vartype=xp.binary, name=f"yL_{o}_{d}_{h}_{s}")
                    y_W[(o, d, h, s)] = xp.var(vartype=xp.binary, name=f"yW_{o}_{d}_{h}_{s}")

    # Semester assignment
    z = {(g, s): xp.var(vartype=xp.binary, name=f"z_{g}_{s}") for g in G for s in S}
    w_var = {(o, s): xp.var(vartype=xp.binary, name=f"w_{o}_{s}") for o in O for s in S}

    # Student choice for non‑maths courses
    a = {}
    for q in Q:
        for co in CO_q[q]:
            a[(q, co)] = xp.var(vartype=xp.binary, name=f"a_{q}_{co}")

    # Linearisation for product a * xL (travel)
    ind = {}
    for q in Q:
        for co in CO_q[q]:
            for g in G:
                for d in D:
                    for h in H:
                        for s in S:
                            ind[(q, co, g, d, h, s)] = xp.var(vartype=xp.binary, name=f"ind_{q}_{co}_{g}_{d}_{h}_{s}")

    # Linearisation for product a * a (travel between non‑maths)
    ch = {}
    for q in Q:
        for co in CO_q[q]:
            for co2 in CO_q[q]:
                if co < co2:
                    ch[(q, co, co2)] = xp.var(vartype=xp.binary, name=f"ch_{q}_{co}_{co2}")

    # Isolated class indicators
    is_isolated = {}
    for q in QQ:
        for d in D:
            for h in isolated_hours:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        is_isolated[(q, d, h, s, e)] = xp.var(vartype=xp.binary,
                                                              name=f"is_isolated_{q}_{d}_{h}_{s}_{e}")

    # Day‑used indicators
    b = {}
    for q in QQ:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    b[(q, d, s, e)] = xp.var(vartype=xp.binary, name=f"b_{q}_{d}_{s}_{e}")

    # Add all variables
    all_vars = (list(x_L.values()) + list(x_W.values()) + list(x_F.values()) +
                list(y_L.values()) + list(y_W.values()) +
                list(z.values()) + list(w_var.values()) +
                list(a.values()) +
                list(ind.values()) + list(ch.values()) +
                list(is_isolated.values()) + list(b.values()))
    p.addVariable(all_vars)

    # ==================== HARD CONSTRAINTS ====================
    print("Adding hard constraints...")
    constraint_count = 0
    constraint_list = []

    def add_constraint(expr, name):
        nonlocal constraint_count
        row = p.addConstraint(expr)
        constraint_list.append((row, name))
        constraint_count += 1

    def flatten_weeks(week_list):
        if not isinstance(week_list, (list, tuple)):
            return [week_list]
        flat = []
        for item in week_list:
            if isinstance(item, (list, tuple)):
                flat.extend(flatten_weeks(item))
            else:
                flat.append(item)
        return flat

    E_flat = flatten_weeks(E)
    E1_flat = flatten_weeks(E1)
    E2_flat = flatten_weeks(E2)

    # 1. Fortnightly workshops per gateway
    for g in G:
        add_constraint(xp.Sum(x_F[(g, d, h, s, w)] for d in D for h in H for s in S for w in W) == R_g_F,
                       f"Fortnightly_{g}")

    # 2. No multiple events per course in same slot
    for g in G:
        for d in D:
            for h in H:
                for s in S:
                    add_constraint(x_L[(g, d, h, s)] + x_W[(g, d, h, s)] +
                                   xp.Sum(x_F[(g, d, h, s, w)] for w in W) <= 1,
                                   f"CourseNoClash_G_{g}_{d}_{h}_{s}")
    for o in O:
        for d in D:
            for h in H:
                for s in S:
                    add_constraint(y_L[(o, d, h, s)] + y_W[(o, d, h, s)] <= 1,
                                   f"CourseNoClash_O_{o}_{d}_{h}_{s}")

    # 3. Global no‑clash per week (Maths only)
    for d in D:
        for h in H:
            for s in S:
                for w in W:
                    add_constraint(
                        xp.Sum(x_L[(g, d, h, s)] for g in G) +
                        xp.Sum(y_L[(o, d, h, s)]  for o in O) <= 1,
                        f"GlobalNoClash_{d}_{h}_{s}_{w}")

    # 4. Events limited to assigned semester
    for g in G:
        for d in D:
            for h in H:
                for s in S:
                    add_constraint(x_L[(g, d, h, s)] <= z[(g, s)],
                                   f"SemLimit_xL_{g}_{d}_{h}_{s}")
                    add_constraint(x_W[(g, d, h, s)] <= z[(g, s)],
                                   f"SemLimit_xW_{g}_{d}_{h}_{s}")
                    for w in W:
                        add_constraint(x_F[(g, d, h, s, w)] <= z[(g, s)],
                                       f"SemLimit_xF_{g}_{d}_{h}_{s}_{w}")
    for o in O:
        for d in D:
            for h in H:
                for s in S:
                    add_constraint(y_L[(o, d, h, s)] <= w_var[(o, s)],
                                   f"SemLimit_yL_{o}_{d}_{h}_{s}")
                    add_constraint(y_W[(o, d, h, s)] <= w_var[(o, s)],
                                   f"SemLimit_yW_{o}_{d}_{h}_{s}")

    # 5. Gateway course semester assignment
    for g in G:
        add_constraint(xp.Sum(z[(g, s)] for s in S) == 1, f"GateSemAssign_{g}")

    # 6. Optional course semester assignment
    for o in O:
        add_constraint(xp.Sum(w_var[(o, s)] for s in S) == 1, f"OptSemAssign_{o}")

    # 7. Exactly required number of courses per semester
    for s in S:
        add_constraint(xp.Sum(z[(g, s)] for g in G) == C_g, f"GateCount_{s}")
        add_constraint(xp.Sum(w_var[(o, s)] for o in O) == C_o, f"OptCount_{s}")

    # 8. Teaching event counts for gateway
    for g in G:
        for s in S:
            lect_count = R_g_L[g] if isinstance(R_g_L, dict) else R_g_L
            add_constraint(xp.Sum(x_L[(g, d, h, s)] for d in D for h in H) == lect_count * z[(g, s)],
                           f"GateLectures_{g}_{s}")
            workshop_count = R_g_W[g] if isinstance(R_g_W, dict) else R_g_W
            add_constraint(xp.Sum(x_W[(g, d, h, s)] for d in D for h in H) == workshop_count * z[(g, s)],
                           f"GateWorkshops_{g}_{s}")

    # 9. Teaching event counts for optional
    for o in O:
        for s in S:
            add_constraint(xp.Sum(y_L[(o, d, h, s)] for d in D for h in H) == R_o_L * w_var[(o, s)],
                           f"OptLectures_{o}_{s}")
            add_constraint(xp.Sum(y_W[(o, d, h, s)] for d in D for h in H) == R_o_W * w_var[(o, s)],
                           f"OptWorkshops_{o}_{s}")

    # 10. Collection credit requirements
    for cl_id in SC_cl:
        for q in Q:
            if cl_id in programme_data[q].get('collections', {}):
                collection_sum = xp.Sum(n_co[co] * a[(q, co)]
                                        for co in SC_cl[cl_id]
                                        if co in CO_q[q])
                add_constraint(collection_sum >= min_CL[cl_id],
                               f"CollectionMin_{cl_id}_{q}")
                add_constraint(collection_sum <= max_CL[cl_id],
                               f"CollectionMax_{cl_id}_{q}")

    # 11. Regression group credit requirements
    for rg_id in SCL_cr:
        for q in Q:
            if rg_id in programme_data[q].get('regression_groups', {}):
                reg_sum = xp.Sum(n_co[co] * a[(q, co)]
                                 for cl_id in SCL_cr[rg_id]
                                 for co in SC_cl[cl_id]
                                 if co in CO_q[q])
                add_constraint(reg_sum >= min_CR[rg_id],
                               f"RegGroupMin_{rg_id}_{q}")
                add_constraint(reg_sum <= max_CR[rg_id],
                               f"RegGroupMax_{rg_id}_{q}")

    # 12. Compulsory courses must be taken
    for q in Q:
        for co in CO_CO_q[q]:
            add_constraint(a[(q, co)] == 1, f"Compulsory_{q}_{co}")

    # 13. Minimum credits outside Maths
    for q in Q:
        outside_credits = xp.Sum(n_co[co] * a[(q, co)]
                                 for co in CO_q[q]
                                 if co not in G and co not in O)
        add_constraint(outside_credits >= n_q[q], f"OutsideCredits_{q}")

    # 14. No clashes with compulsory courses per curriculum (using xL directly)
    for q in Q:
        for d in D:
            for h in H:
                for s in S:
                    weeks = E1_flat if s == 1 else E2_flat if s == 2 else E_flat
                    for e in weeks:
                        if isinstance(e, (list, tuple)): continue
                        for k in K:
                            gateway_sum = xp.Sum(x_L[(g, d, h, s)] for g in G)
                            compulsory_terms = []
                            for co in CO_CO_q[q]:
                                key = (co, d, h, e, q, k)
                                val = v.get(key, 0)
                                if val > 0:
                                    compulsory_terms.append(a[(q, co)] * val)
                            if compulsory_terms:
                                compulsory_sum = xp.Sum(compulsory_terms)
                                add_constraint(gateway_sum + compulsory_sum <= 1,
                                               f"ClashComp_{q}_{d}_{h}_{s}_{e}_{k}")

    # 15. No clashes with optional courses per curriculum (using xL directly)
    for q in Q:
        for d in D:
            for h in H:
                for s in S:
                    weeks = E1_flat if s == 1 else E2_flat if s == 2 else E_flat
                    for e in weeks:
                        if isinstance(e, (list, tuple)): continue
                        for k in K:
                            gateway_sum = xp.Sum(x_L[(g, d, h, s)] for g in G)
                            optional_terms = []
                            for co in CO_OP_q[q]:
                                key = (co, d, h, e, q, k)
                                val = v.get(key, 0)
                                if val > 0:
                                    optional_terms.append(a[(q, co)] * val)
                            if optional_terms:
                                optional_sum = xp.Sum(optional_terms)
                                add_constraint(gateway_sum + optional_sum <= 1,
                                               f"ClashOpt_{q}_{d}_{h}_{s}_{e}_{k}")

    # 16. Linearisation for ind (product a * xL)
    for q in Q:
        for co in CO_q[q]:
            for g in G:
                for d in D:
                    for h in H:
                        for s in S:
                            vv = ind[(q, co, g, d, h, s)]
                            add_constraint(vv <= a[(q, co)], f"Ind1_{q}_{co}_{g}_{d}_{h}_{s}")
                            add_constraint(vv <= x_L[(g, d, h, s)], f"Ind2_{q}_{co}_{g}_{d}_{h}_{s}")
                            add_constraint(vv >= a[(q, co)] + x_L[(g, d, h, s)] - 1,
                                           f"Ind3_{q}_{co}_{g}_{d}_{h}_{s}")

    # 17. Linearisation for ch (product a * a)
    for q in Q:
        for co in CO_q[q]:
            for co2 in CO_q[q]:
                if co < co2:
                    vv = ch[(q, co, co2)]
                    add_constraint(vv <= a[(q, co)], f"Ch1_{q}_{co}_{co2}")
                    add_constraint(vv <= a[(q, co2)], f"Ch2_{q}_{co}_{co2}")
                    add_constraint(vv >= a[(q, co)] + a[(q, co2)] - 1, f"Ch3_{q}_{co}_{co2}")

    # ==================== SOFT CONSTRAINT AUXILIARY ====================
        # q_math = the pure mathematics curriculum
    q_math = "math"
    # QQ= Q.append(q_math)
    # print('QQ:',QQ)
        # P[(q,d,h,s,e)] will store the event-presence expression
    P = {}

        # --- Pure Mathematics curriculum ---
    for d in D:
            for h in H:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        P[(q_math, d, h, s, e)] = (
                                xp.Sum(
                                    x_L[(g, d, h, s)]

                                    for g in G
                                ) +
                                xp.Sum(
                                    y_L[(o, d, h, s)] for o in O
                                )
                        )

        # --- Joint curricula ---
    for q in Q:
            if q == q_math:
                continue

            for d in D:
                for h in H:
                    for s in S:
                        for e in E1 + E2:
                            P[(q, d, h, s, e)] = (
                                    xp.Sum(x_L[(g, d, h, s)] for g in G) +
                                    xp.Sum(
                                        v.get((co, d, h, e, q, k), 0) * a[(q, co)]
                                        for co in CO_q[q]
                                        for k in K
                                    )
                            )

    # 18. Isolated classes (for hours in isolated_hours)
    for q in QQ:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    for h in isolated_hours:
                        p_curr = P[(q, d, h, s, e)]
                        p_next = P[(q, d, h + 1, s, e)] if h + 1 in H else 0
                        p_prev = P[(q, d, h - 1, s, e)] if h - 1 in H else 0
                        add_constraint(is_isolated[(q, d, h, s, e)] >= p_curr - p_next - p_prev,
                                       f"IsolatedGe_{q}_{d}_{h}_{s}_{e}")
                        add_constraint(is_isolated[(q, d, h, s, e)] <= p_curr,
                                       f"IsolatedLe_{q}_{d}_{h}_{s}_{e}")

    # 19. Days used (all hours)
    for q in QQ:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    total_day = xp.Sum(P[(q, d, h, s, e)] for h in H)
                    add_constraint(b[(q, d, s, e)] <= total_day, f"DaysLe_{q}_{d}_{s}_{e}")
                    add_constraint(total_day <= len(H) * b[(q, d, s, e)], f"DaysGe_{q}_{d}_{s}_{e}")

    # ==================== OBJECTIVE ====================
    print("Building objective...")

    # Normalisation constants (maximum possible values for raw counts over a semester)
    weeks_per_sem = len(E1)          # 26
    N_late  = len(S) * len(D) * weeks_per_sem          # 2 * 5 * 26 = 260
    N_lunch = len(S) * len(D) * 2 * weeks_per_sem      # 2 * 5 * 2 * 26 = 520
    N_isol  = len(S) * len(D) * 7 * weeks_per_sem      # 2 * 5 * 7 * 26 = 1820
    N_days  = len(S) * len(D) * weeks_per_sem          # 260
    N_wed   = len(S) * 5 * weeks_per_sem               # 2 * 5 * 26 = 260
    N_clash= len(S) * weeks_per_sem * 3*2
    max_travel_weekly = 660  # or compute from data
    max_travel_sem = max_travel_weekly * len(E1) * len(S)
    scale_travel = lambda_travel / max_travel_sem
    # Scale raw expressions by lambda / N
    scale_late     = lambda_late / N_late
    scale_lunch    = lambda_lunch / N_lunch
    scale_isolated = lambda_isolated / N_isol
    scale_days     = lambda_days / N_days
    scale_wed      = lambda_wed / N_wed
    scale_clash=lambda_clash / N_clash
    # Travel time
    travel_obj = 0
    # Term 1: Maths → non‑maths (ind with co at h+1)
    for q in Q:
        for co in CO_q[q]:
            for g in G:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        for d in D:
                            for h in H:
                                if h + 1 not in H: continue
                                for k in K:
                                    val = v.get((co, d, h + 1, e, q, k), 0)
                                    if val > 0:
                                        travel_obj += travel_time_dict.get(('King\'s Buildings', k), 60) * val * ind[
                                            (q, co, g, d, h, s)]
    # Term 2: Non‑maths → Maths (ind with co at h)
    for q in Q:
        for co in CO_q[q]:
            for g in G:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        for d in D:
                            for h in H:
                                if h + 1 not in H: continue
                                for k in K:
                                    val = v.get((co, d, h, e, q, k), 0)
                                    if val > 0:
                                        travel_obj += travel_time_dict.get((k, 'King\'s Buildings'), 60) * val * ind[
                                            (q, co, g, d, h + 1, s)]
    # Term 3: Non‑maths ↔ non‑maths (using ch)
    for q in Q:
        for co in CO_q[q]:
            for co2 in CO_q[q]:
                if co < co2:
                    for s in S:
                        weeks = E1 if s == 1 else E2
                        for e in weeks:
                            for d in D:
                                for h in H:
                                    if h + 1 not in H: continue
                                    for k in K:
                                        for k2 in K:
                                            val1 = v.get((co, d, h, e, q, k), 0)
                                            val2 = v.get((co2, d, h + 1, e, q, k2), 0)
                                            if val1 > 0 and val2 > 0:
                                                travel_obj += travel_time_dict.get((k, k2), 60) * val1 * val2 * ch[
                                                    (q, co, co2)]

    # Clashes between optional maths and non‑maths courses
    clash_obj = 0
    for q in Q:
        for co in CO_q[q]:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    for d in D:
                        for h in H:
                            optional_maths = xp.Sum(y_L[(o, d, h, s)] for o in O)
                            nonmaths = xp.Sum(a[(q, co)] * v.get((co, d, h, e, q, k), 0) for co in CO_q[q] for k in K)
                            clash_obj += optional_maths * nonmaths

    # Late, lunch, Wednesday objectives
    late_obj = 0
    lunch_obj = 0
    wed_obj = 0
    for q in QQ:
        for s in S:
            weeks = E1 if s == 1 else E2
            for e in weeks:
                for d in D:
                    late_obj += P[(q, d, late_hour, s, e)]
                    for h in lunch_hours:
                        lunch_obj += P[(q, d, h, s, e)]
                    if d == wed_idx:
                        for h in wednesday_hours:
                            wed_obj += P[(q, d, h, s, e)]

    # Isolated objective
    isolated_obj = 0
    for q in QQ:
        for d in D:
            for h in isolated_hours:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        isolated_obj += is_isolated[(q, d, h, s, e)]

    # Days objective
    days_obj = 0
    for q in QQ:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    days_obj += b[(q, d, s, e)]

    objective = (scale_late * late_obj +
                 scale_lunch * lunch_obj +
                 scale_isolated * isolated_obj +
                 scale_days * days_obj +
                 scale_wed * wed_obj +
                 scale_travel * travel_obj +
                 scale_clash * clash_obj)

    p.setObjective(objective, sense=xp.minimize)

    print(f"Total constraints added: {constraint_count}")

    var_dicts = {
        'xL': x_L, 'xW': x_W, 'xF': x_F,
        'yL': y_L, 'yW': y_W,
        'z': z, 'w': w_var,
        'a': a,
        'ind': ind, 'ch': ch,
        'is_isolated': is_isolated, 'b': b
    }
    return p, constraint_list, var_dicts
build_model_from_parameters(parameters)

# ============= SOLVE MODEL =============== #
def solve_model(parameters):
        from xpress import InterfaceError

        model, constraint_list, var_dicts = build_model_from_parameters(parameters)
        row_to_name = {r: name for r, name in constraint_list}

        model.setControl('outputlog', 1)
        model.setControl('miprelstop', 0.2)  # 20% gap
        model.setControl('maxtime', 7200)
        model.solve()

        status_string = model.getProbStatusString()
        print("\nSolution status:", status_string)

        if "optimal" in status_string or "Feasible" in status_string:
            print("Feasible solution found!")
            # Retrieve only the variables needed for output and plotting
            needed = ['z', 'w', 'a', 'xL', 'xW', 'xF', 'yL', 'yW']
            var_sol = {}
            for name in needed:
                if name in var_dicts:
                    var_sol[name] = {k: model.getSolution(v) for k, v in var_dicts[name].items()}
            # Retrieve xL for plotting (optional)
            var_sol['xL'] = {k: model.getSolution(v) for k, v in var_dicts['xL'].items()}
            results = analyze_solution(model, parameters, var_sol)
            return model, results, var_sol
        else:
            print("Model is infeasible!")
            print("\nComputing IIS...")

            model.iisfirst(1)

            rows = None
            bounds = None

            try:
                rows = model.attributes.iisrows
                bounds = model.attributes.iisbnds
            except (InterfaceError, AttributeError):
                pass

            if rows is None:
                try:
                    rows = model.getiisrows()
                    bounds = model.getiisbnds()
                except AttributeError:
                    pass

            if rows is None:
                model.write("iis.ilp")
                print("IIS written to 'iis.ilp'. Please open this file to inspect the constraints.")
                return model, None, None

            print(f"\nFound {len(rows)} constraints in the IIS.")
            if rows:
                print("Constraints in IIS:")
                for row_idx in rows:
                    if row_idx in row_to_name:
                        print(f"  - {row_to_name[row_idx]} (row {row_idx})")
                    else:
                        print(f"  - Row {row_idx} (no name stored)")

            print(f"\nFound {len(bounds)} variable bounds in the IIS.")
            if bounds:
                print("Variable bounds in IIS:")
                for col_idx, lower, upper in bounds:
                    var_name = model.getVarName(col_idx)
                    print(f"  - {var_name}: lower={lower}, upper={upper}")

            model.write("iis.ilp")
            print("\nIIS written to 'iis.ilp'. You can open this file to see the exact constraints.")

            return model, None, None

def analyze_solution(model, parameters, var_sol):
    """
    Analyze and display the solution using variable solution dictionaries.
    """
    results = {
        'gateway_schedule': {},      # gateway -> semester(s)
        'optional_schedule': {},     # optional -> semester(s)
        'course_selection': {}       # curriculum -> list of chosen non‑maths courses
    }

    # Gateway semester assignment (z)
    for (g, s), val in var_sol['z'].items():
        if val > 0.5:
            if g not in results['gateway_schedule']:
                results['gateway_schedule'][g] = []
            results['gateway_schedule'][g].append(s)

    # Optional course semester assignment (w)
    for (o, s), val in var_sol['w'].items():
        if val > 0.5:
            if o not in results['optional_schedule']:
                results['optional_schedule'][o] = []
            results['optional_schedule'][o].append(s)

    # Non‑maths course selection per curriculum (a)
    for (q, co), val in var_sol['a'].items():
        if val > 0.5:
            if q not in results['course_selection']:
                results['course_selection'][q] = []
            results['course_selection'][q].append(co)

    return results

def print_results(results):
    if results is None:
        print("No results to display")
        return

    print("\n" + "=" * 50)
    print("SOLUTION RESULTS")
    print("=" * 50)

    print("\nGateway Course Schedule:")
    for g, sems in results['gateway_schedule'].items():
        print(f"  {g}: Semester(s) {sems}")

    print("\nOptional Course Schedule:")
    for o, sems in results['optional_schedule'].items():
        print(f"  {o}: Semester(s) {sems}")

    print("\nNon‑Maths Course Selections per Curriculum:")
    for q, courses in results['course_selection'].items():
        print(f"  {q}: {courses}")

    print("\nFeasibility Status:")
    print("  Model is feasible - all constraints satisfied.")
# Assuming you have already run your extraction steps
# parameters = extract_all_parameters(courses_df, programme_df)

model, results, var_sol = solve_model(parameters)
print_results(results)

# ============ IMPROVE NONMATHS SELECTION =========== #

def improve_nonmaths_selection(parameters, model, var_sol, time_limit=300):
    """
    Decomposition heuristic for non-maths course selection.
    Fixes gateway + optional maths timetable and re-optimises only 'a' variables.
    """
    import xpress as xp
    from xpress import problem

    G = parameters['G']
    O = parameters['O']
    S = parameters['S']
    D = parameters['D']
    H = parameters['H']
    Q = parameters['Q']
    E1 = parameters['E1']
    E2 = parameters['E2']
    K = parameters['K']
    v = parameters['v']
    programme_data = parameters['programme_data']
    CO_CO_q = {prog: programme_data[prog]['compulsory_courses'] for prog in Q}
    CO_q = {prog: programme_data[prog]['all_courses'] for prog in Q}
    SC_cl = parameters['SC_cl']
    SCL_cr = parameters['SCL_cr']
    min_CL = parameters['min_CL']
    max_CL = parameters['max_CL']
    min_CR = parameters['min_CR']
    max_CR = parameters['max_CR']
    n_co = parameters['n_co']
    n_q = parameters['n_q']

    # Soft weights - must match build_model_from_parameters
    lambda_travel = 0.01
    lambda_clash = 0.1
    lambda_late = 0.344249
    lambda_lunch = 0.112523
    lambda_isolated = 0.057430
    lambda_days = 0.133207
    lambda_wed = 0.028978

    weeks_per_sem = len(E1)
    N_late = len(S) * len(D) * weeks_per_sem
    N_lunch = len(S) * len(D) * 2 * weeks_per_sem
    N_isol = len(S) * len(D) * 7 * weeks_per_sem
    N_days = len(S) * len(D) * weeks_per_sem
    N_wed = len(S) * 5 * weeks_per_sem
    N_clash = len(S) * weeks_per_sem * 3 * 2
    max_travel_sem = 660 * weeks_per_sem * len(S)

    scale_late = lambda_late / N_late
    scale_lunch = lambda_lunch / N_lunch
    scale_isolated = lambda_isolated / N_isol
    scale_days = lambda_days / N_days
    scale_wed = lambda_wed / N_wed
    scale_travel = lambda_travel / max_travel_sem
    scale_clash = lambda_clash / N_clash

    # Current solution
    xL_sol = var_sol.get('xL', {})

    yL_sol = var_sol.get('yL', {})
    yW_sol = var_sol.get('yW', {})
    a_sol = var_sol.get('a', {})

    isolated_hours = list(range(10, 17))
    lunch_hours = [12, 13]
    wed_idx = 3
    wednesday_hours = list(range(13, 18))

    for q in Q:
        print(f"Improving non-maths selection for: {q}")

        sub = problem(f"Sub_{q}")

        # === Variables ===
        a_vars = {co: xp.var(vartype=xp.binary, name=f"a_{q}_{co}") for co in CO_q[q]}
        sub.addVariable(list(a_vars.values()))

        # Linearisation ch for non-maths <-> non-maths travel
        nonmath_courses = [co for co in CO_q[q] if co not in G and co not in O]
        ch_vars = {}
        for i, co1 in enumerate(nonmath_courses):
            for co2 in nonmath_courses[i+1:]:
                ch_vars[(co1, co2)] = xp.var(vartype=xp.binary, name=f"ch_{q}_{co1}_{co2}")
        sub.addVariable(list(ch_vars.values()))

        for co1, co2 in ch_vars:
            sub.addConstraint(ch_vars[(co1, co2)] <= a_vars[co1])
            sub.addConstraint(ch_vars[(co1, co2)] <= a_vars[co2])
            sub.addConstraint(ch_vars[(co1, co2)] >= a_vars[co1] + a_vars[co2] - 1)

        # === Hard Constraints ===
        # 1. Compulsory
        for co in CO_CO_q.get(q, []):
            sub.addConstraint(a_vars[co] == 1)

        # 2. Collections
        for cl_id, courses_in_cl in SC_cl.items():
            if cl_id in programme_data[q].get('collections', {}):
                coll_sum = xp.Sum(n_co.get(co, 20) * a_vars[co]
                                  for co in courses_in_cl if co in a_vars)
                sub.addConstraint(coll_sum >= min_CL.get(cl_id, 0))
                sub.addConstraint(coll_sum <= max_CL.get(cl_id, 999))

        # 3. Regression groups
        for rg_id, cl_list in SCL_cr.items():
            if rg_id in programme_data[q].get('regression_groups', {}):
                reg_sum = xp.Sum(n_co.get(co, 20) * a_vars[co]
                                 for cl_id in cl_list
                                 for co in SC_cl.get(cl_id, []) if co in a_vars)
                sub.addConstraint(reg_sum >= min_CR.get(rg_id, 0))
                sub.addConstraint(reg_sum <= max_CR.get(rg_id, 999))

        # 4. Minimum outside credits
        outside = xp.Sum(n_co.get(co, 20) * a_vars[co]
                         for co in CO_q[q] if co not in G and co not in O)
        sub.addConstraint(outside >= n_q.get(q, 40))

        # 5. No clashes with fixed maths timetable + no self-clashes among non-maths
        for d in D:
            for h in H:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        # Fixed occupancy from gateway + optional maths
                        gateway_occ = any(xL_sol.get((g, d, h, s), 0) > 0.5 for g in G)


                        fixed_occ = 1 if (gateway_occ) else 0

                        nonmath_expr = xp.Sum(a_vars[co] * v.get((co, d, h, e, q, k), 0)
                                              for co in CO_q[q] for k in K)

                        sub.addConstraint(nonmath_expr <= 1 - fixed_occ)
                        sub.addConstraint(nonmath_expr <= 1)   # no two non-maths in same slot

        # === P for soft constraints ===
        P = {}
        for d in D:
            for h in H:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        fixed_part = (any(xL_sol.get((g,d,h,s),0)>0.5 for g in G) )

                        nonmath_part = xp.Sum(a_vars[co] * v.get((co, d, h, e, q, k), 0)
                                              for co in CO_q[q] for k in K)
                        P[(d, h, s, e)] = (1 if fixed_part else 0) + nonmath_part

        # Isolated and Days variables
        is_isolated_var = {(d, h, s, e): xp.var(vartype=xp.binary, name=f"iso_{d}_{h}_{s}_{e}")
                           for d in D for h in isolated_hours
                           for s in S for e in (E1 if s==1 else E2)}
        sub.addVariable(list(is_isolated_var.values()))

        b_var = {(d, s, e): xp.var(vartype=xp.binary, name=f"b_{d}_{s}_{e}")
                 for d in D for s in S for e in (E1 if s==1 else E2)}
        sub.addVariable(list(b_var.values()))

        # Constraints for isolated and days
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    for h in isolated_hours:
                        p_curr = P.get((d, h, s, e), 0)
                        p_next = P.get((d, h+1, s, e), 0)
                        p_prev = P.get((d, h-1, s, e), 0)
                        sub.addConstraint(is_isolated_var[(d,h,s,e)] >= p_curr - p_next - p_prev)
                        sub.addConstraint(is_isolated_var[(d,h,s,e)] <= p_curr)

                    total_day = xp.Sum(P.get((d, hh, s, e), 0) for hh in H)
                    sub.addConstraint(b_var[(d,s,e)] <= total_day)
                    sub.addConstraint(total_day <= len(H) * b_var[(d,s,e)])

        # === Objective ===
        travel_obj = 0
        clash_obj = 0
        late_obj = lunch_obj = wed_obj = 0
        isolated_obj = xp.Sum(list(is_isolated_var.values()))   # FIXED: list()
        days_obj = xp.Sum(list(b_var.values()))                 # FIXED: list()

        # Travel: Gateway <-> non-maths
        for d in D:
            for h in H:
                if h + 1 not in H: continue
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        for g in G:
                            # Gateway at h → non-maths at h+1
                            if xL_sol.get((g, d, h, s), 0) > 0.5:
                                for co in nonmath_courses:
                                    for k in K:
                                        val = v.get((co, d, h+1, e, q, k), 0)
                                        if val > 0:
                                            travel_obj += travel_time_dict.get(("King's Buildings", k), 60) * val * a_vars[co]

                            # non-maths at h → Gateway at h+1
                            if xL_sol.get((g, d, h+1, s), 0) > 0.5:
                                for co in nonmath_courses:
                                    for k in K:
                                        val = v.get((co, d, h, e, q, k), 0)
                                        if val > 0:
                                            travel_obj += travel_time_dict.get((k, "King's Buildings"), 60) * val * a_vars[co]

        # non-maths <-> non-maths travel
        for (co1, co2), chv in ch_vars.items():
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    for d in D:
                        for h in H:
                            if h + 1 not in H: continue
                            for k1 in K:
                                for k2 in K:
                                    v1 = v.get((co1, d, h, e, q, k1), 0)
                                    v2 = v.get((co2, d, h+1, e, q, k2), 0)
                                    if v1 > 0 and v2 > 0:
                                        travel_obj += travel_time_dict.get((k1, k2), 60) * v1 * v2 * chv

        # Clash with optional maths
        for s in S:
            weeks = E1 if s == 1 else E2
            for e in weeks:
                for d in D:
                    for h in H:
                        opt_maths = any(yL_sol.get((o, d, h, s), 0) > 0.5 for o in O)
                        if opt_maths:
                            nonmath_expr = xp.Sum(a_vars[co] * v.get((co, d, h, e, q, k), 0)
                                                  for co in nonmath_courses for k in K)
                            clash_obj += nonmath_expr

        # Late, lunch, wednesday
        for s in S:
            weeks = E1 if s == 1 else E2
            for e in weeks:
                for d in D:
                    if 17 in H:
                        late_obj += P.get((d, 17, s, e), 0)
                    for hh in lunch_hours:
                        if hh in H:
                            lunch_obj += P.get((d, hh, s, e), 0)
                    if d == wed_idx:
                        for hh in wednesday_hours:
                            if hh in H:
                                wed_obj += P.get((d, hh, s, e), 0)

        sub_obj = (scale_late * late_obj +
                   scale_lunch * lunch_obj +
                   scale_isolated * isolated_obj +
                   scale_days * days_obj +
                   scale_wed * wed_obj +
                   scale_travel * travel_obj +
                   scale_clash * clash_obj)

        sub.setObjective(sub_obj, sense=xp.minimize)

        # Solve
        sub.setControl('timelimit', time_limit)
        sub.setControl('outputlog', 0)
        sub.solve()

        status = sub.getProbStatusString()
        if "optimal" in status or "Feasible" in status:
            for co in CO_q[q]:
                new_val = sub.getSolution(a_vars[co])
                var_sol['a'][(q, co)] = new_val
            print(f"   → Updated a for {q} (status: {status})")
        else:
            print(f"   → No improvement for {q} (status: {status})")

    return var_sol
def compute_total_objective(parameters, var_sol):
    """
    Computes the total objective value from the solution dictionaries
    for the current model (all gateways mandatory, no ta variables).
    """
    G = parameters['G']
    O = parameters['O']
    S = parameters['S']
    D = parameters['D']
    H = parameters['H']
    W = parameters['W']
    Q = parameters['Q']
    E1 = parameters['E1']
    E2 = parameters['E2']
    K = parameters['K']
    v = parameters['v']
    n_co = parameters['n_co']          # not directly used here but kept for consistency
    programme_data = parameters['programme_data']
    CO_q = {prog: programme_data[prog]['all_courses'] for prog in Q}

    # Soft weights (must match exactly what you use in build_model_from_parameters)
    lambda_travel = 0.01
    lambda_clash = 0.1
    lambda_late = 0.344249
    lambda_lunch = 0.112523
    lambda_isolated = 0.057430
    lambda_days = 0.133207
    lambda_wed = 0.028978

    weeks_per_sem = len(E1)
    N_late = len(S) * len(D) * weeks_per_sem
    N_lunch = len(S) * len(D) * 2 * weeks_per_sem
    N_isol = len(S) * len(D) * 7 * weeks_per_sem
    N_days = len(S) * len(D) * weeks_per_sem
    N_wed = len(S) * 5 * weeks_per_sem
    N_clash = len(S) * weeks_per_sem * 3 * 2
    max_travel_sem = 660 * weeks_per_sem * len(S)

    scale_late = lambda_late / N_late
    scale_lunch = lambda_lunch / N_lunch
    scale_isolated = lambda_isolated / N_isol
    scale_days = lambda_days / N_days
    scale_wed = lambda_wed / N_wed
    scale_travel = lambda_travel / max_travel_sem
    scale_clash = lambda_clash / N_clash

    # Extract solution dictionaries
    xL_sol = var_sol.get('xL', {})
    xW_sol = var_sol.get('xW', {})
    xF_sol = var_sol.get('xF', {})
    yL_sol = var_sol.get('yL', {})
    yW_sol = var_sol.get('yW', {})
    a_sol = var_sol.get('a', {})
    ind_sol = var_sol.get('ind', {})   # linearisation a * xL
    ch_sol = var_sol.get('ch', {})     # linearisation a * a

    # Helper to check if a gateway event is active in a slot (considering fortnightly)
    def is_gateway_active(g, d, h, s, e):
        lect = xL_sol.get((g, d, h, s), 0) > 0.5
        work = xW_sol.get((g, d, h, s), 0) > 0.5
        parity = 1 if e % 2 == 1 else 2
        fortn = xF_sol.get((g, d, h, s, parity), 0) > 0.5
        return lect or work or fortn

    # ------------------------------------------------------------------
    # 1. Travel time objective
    # ------------------------------------------------------------------
    travel_obj = 0.0

    # Term 1 & 2: Gateway <-> non-maths (using ind)
    for q in Q:
        for co in CO_q[q]:
            if co in G or co in O:
                continue
            for g in G:
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        for d in D:
                            for h in H:
                                if h + 1 not in H:
                                    continue
                                # Maths at h → non-maths at h+1
                                ind_val = ind_sol.get((q, co, g, d, h, s), 0)
                                if ind_val > 0.5:
                                    val = v.get((co, d, h + 1, e, q, k), 0) if 'k' in locals() else 0
                                    for k in K:
                                        val = v.get((co, d, h + 1, e, q, k), 0)
                                        if val > 0:
                                            travel_obj += travel_time_dict.get(("King's Buildings", k), 60) * ind_val

                                # non-maths at h → Maths at h+1
                                ind_val2 = ind_sol.get((q, co, g, d, h + 1, s), 0)
                                if ind_val2 > 0.5:
                                    for k in K:
                                        val = v.get((co, d, h, e, q, k), 0)
                                        if val > 0:
                                            travel_obj += travel_time_dict.get((k, "King's Buildings"), 60) * ind_val2

    # Term 3: non-maths <-> non-maths (using ch)
    for q in Q:
        nonmath = [co for co in CO_q[q] if co not in G and co not in O]
        for i, co1 in enumerate(nonmath):
            for co2 in nonmath[i+1:]:
                ch_val = ch_sol.get((q, co1, co2), 0)
                if ch_val <= 0.5:
                    continue
                for s in S:
                    weeks = E1 if s == 1 else E2
                    for e in weeks:
                        for d in D:
                            for h in H:
                                if h + 1 not in H:
                                    continue
                                for k1 in K:
                                    for k2 in K:
                                        v1 = v.get((co1, d, h, e, q, k1), 0)
                                        v2 = v.get((co2, d, h + 1, e, q, k2), 0)
                                        if v1 > 0 and v2 > 0:
                                            travel_obj += travel_time_dict.get((k1, k2), 60) * v1 * v2 * ch_val

    # ------------------------------------------------------------------
    # 2. Clash between optional maths and non-maths
    # ------------------------------------------------------------------
    clash_obj = 0.0
    for q in Q:
        for s in S:
            weeks = E1 if s == 1 else E2
            for e in weeks:
                for d in D:
                    for h in H:
                        # Optional maths in this slot
                        opt_math = (any(yL_sol.get((o, d, h, s), 0) > 0.5 for o in O) or
                                    any(yW_sol.get((o, d, h, s), 0) > 0.5 for o in O))
                        if not opt_math:
                            continue

                        # Non-maths in this slot
                        nonmath_count = 0
                        for co in CO_q[q]:
                            if co in G or co in O:
                                continue
                            if a_sol.get((q, co), 0) > 0.5:
                                for k in K:
                                    if v.get((co, d, h, e, q, k), 0) > 0:
                                        nonmath_count += 1
                                        break
                        clash_obj += nonmath_count   # since opt_math is 0 or 1

    # ------------------------------------------------------------------
    # 3. Late, lunch, Wednesday, isolated, days
    # ------------------------------------------------------------------
    late_obj = lunch_obj = wed_obj = isolated_obj = days_obj = 0.0

    q_math = "math"
    QQ = Q + [q_math]

    for q in QQ:
        for s in S:
            weeks = E1 if s == 1 else E2
            for e in weeks:
                for d in D:
                    for h in H:
                        # Compute P(q, d, h, s, e)
                        if q == q_math:
                            p_val = (sum(xL_sol.get((g, d, h, s), 0) for g in G) +
                                     sum(yL_sol.get((o, d, h, s), 0) for o in O) +
                                     sum(xW_sol.get((g, d, h, s), 0) for g in G) +
                                     sum(yW_sol.get((o, d, h, s), 0) for o in O))
                            # fortnightly contribution approximated (conservative)
                            parity = 1 if e % 2 == 1 else 2
                            p_val += sum(xF_sol.get((g, d, h, s, parity), 0) for g in G)
                        else:
                            gateway_part = sum(1 for g in G if is_gateway_active(g, d, h, s, e))
                            nonmath_part = 0
                            for co in CO_q[q]:
                                if co in G or co in O:
                                    continue
                                if a_sol.get((q, co), 0) > 0.5:
                                    for k in K:
                                        if v.get((co, d, h, e, q, k), 0) > 0:
                                            nonmath_part += 1
                                            break
                            p_val = gateway_part + nonmath_part

                        # Count soft violations
                        if h == 17:
                            late_obj += p_val
                        if h in [12, 13]:
                            lunch_obj += p_val
                        if d == 3 and h in range(13, 18):
                            wed_obj += p_val

                        # Isolated (we approximate using solution of is_isolated if available)
                        if 10 <= h <= 16:
                            iso_key = (q, d, h, s, e)
                            isolated_obj += var_sol.get('is_isolated', {}).get(iso_key, 0)

                    # Days used
                    day_key = (q, d, s, e)
                    days_obj += var_sol.get('b', {}).get(day_key, 0)

    # ------------------------------------------------------------------
    # Final objective
    # ------------------------------------------------------------------
    total_obj = (scale_late * late_obj +
                 scale_lunch * lunch_obj +
                 scale_isolated * isolated_obj +
                 scale_days * days_obj +
                 scale_wed * wed_obj +
                 scale_travel * travel_obj +
                 scale_clash * clash_obj)

    # ------------------------------------------------------------------
    # Unnormalised objectives
    # ------------------------------------------------------------------ 

    unnorm_obj = [(late_obj, "Late"), (lunch_obj, "Lunch"), (isolated_obj, "Isolated"), (days_obj, "Days"), (wed_obj, "Wednesday"), (travel_obj, "Travel"), (clash_obj, "Clash")]

    return total_obj, unnorm_obj

var_sol_improved = improve_nonmaths_selection(parameters, model, var_sol, time_limit=3600)
# Compare

improved_objective, unnormalised_objectives = compute_total_objective(parameters, var_sol_improved)

print("Improved objective (approximate): ", improved_objective)
print("Unnormalised objectives: ", unnormalised_objectives)


def plot_curriculum_timetable(q, semester, var_sol, parameters,
                              week=None,
                              day_names=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                              hour_range=(9, 18),
                              figsize=(12, 6),
                              only_nonmaths_weeks=False):
    """
    Plot timetable for curriculum q using solution dictionaries.
    - If week is None: heatmap of weeks occupied (color intensity = number of weeks).
    - If only_nonmaths_weeks=True: restricts to weeks where non‑maths courses occur.
    - If a specific week is given: binary occupancy with labels.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # Unpack data
    G = parameters['G']
    if q not in parameters['programme_data']:
        print(f"Curriculum '{q}' not found in programme_data.")
        return
    CO_q = parameters['programme_data'][q]['all_courses']
    v = parameters['v']
    D = parameters['D']
    H = parameters['H']
    E1 = parameters['E1']
    E2 = parameters['E2']
    K = parameters['K']

    # Solution dictionaries
    xL_sol = var_sol['xL']
    a_sol = var_sol['a']

    # All weeks in the semester
    all_weeks = E1 if semester == 1 else E2

    # Determine which weeks to include
    if only_nonmaths_weeks:
        weeks_with_nonmaths = set()
        # For each week, check if any non‑maths course has an event at any day/hour
        for e in all_weeks:
            found = False
            for d in D:
                for h in H:
                    for co in CO_q:
                        if co not in G and co not in parameters['O']:
                            if a_sol.get((q, co), 0) > 0.5:
                                for k in K:
                                    if v.get((co, d, h, e, q, k), 0) > 0:
                                        found = True
                                        break
                            if found:
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                weeks_with_nonmaths.add(e)
        weeks = sorted(weeks_with_nonmaths)
        if not weeks:
            print(f"No weeks with non‑maths events for {q} in semester {semester}.")
            return
        print(f"Weeks with non‑maths events: {weeks}")
    else:
        weeks = all_weeks

    # Map days to indices
    day_map = {d: i for i, d in enumerate(day_names)}
    day_index_to_name = {i+1: day_names[i] for i in range(len(day_names))}

    hours = list(range(hour_range[0], hour_range[1]+1))
    n_hours = len(hours)
    n_days = len(day_names)

    # Prepare occupancy grid
    if week is None:
        occupancy = np.zeros((n_days, n_hours))
        sample_course = [[None for _ in hours] for _ in day_names]
    else:
        occupancy = np.zeros((n_days, n_hours), dtype=bool)
        labels = [[[] for _ in hours] for _ in day_names]

    # Loop over days, hours, weeks
    for d in D:
        day_name = day_index_to_name.get(d)
        if day_name is None:
            continue
        day_idx = day_map[day_name]
        for h in hours:
            if h not in H:
                continue
            hour_idx = h - hour_range[0]
            if hour_idx < 0 or hour_idx >= n_hours:
                continue
            for e in weeks:
                # Gateway events
                gateway = any(xL_sol.get((g, d, h, semester), 0) > 0.5 for g in G)

                # Non‑maths events
                nonmaths = False
                course_found = None
                for co in CO_q:
                    if co not in G and co not in parameters['O']:
                        if a_sol.get((q, co), 0) > 0.5:
                            for k in K:
                                if v.get((co, d, h, e, q, k), 0) > 0:
                                    nonmaths = True
                                    course_found = co
                                    break
                    if nonmaths:
                        break

                if gateway or nonmaths:
                    if week is None:
                        occupancy[day_idx, hour_idx] += 1
                        if nonmaths and course_found:
                            sample_course[day_idx][hour_idx] = course_found
                        elif gateway and sample_course[day_idx][hour_idx] is None:
                            sample_course[day_idx][hour_idx] = "Gateway"
                    else:
                        if e == week:
                            occupancy[day_idx, hour_idx] = True
                            label_parts = []
                            if gateway:
                                label_parts.append("Gateway")
                            if nonmaths:
                                label_parts.append("Non-Maths")
                            labels[day_idx][hour_idx].append("\n".join(label_parts))

    # Plot
    fig, ax = plt.subplots(figsize=figsize)
    if week is None:
        im = ax.imshow(occupancy, cmap='YlOrRd', aspect='auto',
                       vmin=0, vmax=occupancy.max() if occupancy.max() > 0 else 1)
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Number of weeks occupied')
        # Annotate cells with course name and count
        for i in range(n_days):
            for j in range(n_hours):
                if occupancy[i, j] > 0:
                    count = int(occupancy[i, j])
                    course = sample_course[i][j] or ""
                    # Shorten long course names
                    if len(course) > 12:
                        course = course[:9] + "..."
                    text = f"{course}\n({count} wk)" if course else f"{count} wk"
                    ax.text(j, i, text, ha='center', va='center',
                            fontsize=8, color='black', weight='bold')
    else:
        im = ax.imshow(occupancy, cmap='Blues', aspect='auto', vmin=0, vmax=1)
        for i in range(n_days):
            for j in range(n_hours):
                if occupancy[i, j]:
                    text = '\n'.join(labels[i][j])
                    ax.text(j, i, text, ha='center', va='center',
                            fontsize=8, color='black', weight='bold')

    ax.set_xticks(range(n_hours))
    ax.set_xticklabels([f'{h}:00' for h in hours])
    ax.set_yticks(range(n_days))
    ax.set_yticklabels(day_names)
    ax.set_xlabel('Hour')
    ax.set_ylabel('Day')
    title = f"Timetable for {q} – Semester {semester}"
    if week:
        title += f", Week {week}"
    else:
        title += " (all weeks combined)"
        if only_nonmaths_weeks:
            title += " – only weeks with non‑maths courses"
    ax.set_title(title)
    ax.set_xticks(np.arange(-0.5, n_hours, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_days, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    plt.tight_layout()
    plt.show()
# Heatmap for weeks with non‑maths events
# plot_curriculum_timetable('Mathematics and Business BSc (Hons)', semester=1,
#                           var_sol=var_sol, parameters=parameters)
# plot_curriculum_timetable('Mathematics and Business BSc (Hons)', semester=2,
#                           var_sol=var_sol, parameters=parameters)
# # Specific week (week 10) if it has non‑maths
# plot_curriculum_timetable('Mathematics and Business BSc (Hons)', semester=1, week=10,
#                           var_sol=var_sol, parameters=parameters, only_nonmaths_weeks=True)

# After solving, var_sol contains the solution
for q in parameters['Q']:
        for sem in [1, 2]:
            # Heatmap for all weeks
            plot_curriculum_timetable(q, sem, var_sol, parameters)
            # Optionally, a specific week (e.g., week 10)
            # plot_curriculum_timetable(q, sem, var_sol, parameters, week=10)

# Plot Mathematics Timetables            
def plot_maths_timetable(semester, var_sol, parameters,
                         week=None,
                         day_names=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                         hour_range=(9, 18),
                         figsize=(12, 6)):
    """
    Plot timetable for the mathematics curriculum (gateway + optional maths).
    Uses xL, xW, xF, yL, yW solution dictionaries.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # Unpack needed data
    G = parameters['G']
    O = parameters['O']
    D = parameters['D']
    H = parameters['H']
    E1 = parameters['E1']
    E2 = parameters['E2']
    W = parameters['W']          # week parity set [1,2]

    # Get solution dictionaries
    xL_sol = var_sol.get('xL', {})
    xW_sol = var_sol.get('xW', {})
    xF_sol = var_sol.get('xF', {})
    yL_sol = var_sol.get('yL', {})
    yW_sol = var_sol.get('yW', {})

    # All weeks in the semester
    all_weeks = E1 if semester == 1 else E2

    # Determine which weeks to include (if week is given, only that week)
    if week is not None:
        weeks = [week] if week in all_weeks else []
        if not weeks:
            print(f"Week {week} not in semester {semester} weeks.")
            return
    else:
        weeks = all_weeks

    # Map day numbers to indices
    day_map = {d: i for i, d in enumerate(day_names)}
    day_index_to_name = {i+1: day_names[i] for i in range(len(day_names))}

    hours = list(range(hour_range[0], hour_range[1]+1))
    n_hours = len(hours)
    n_days = len(day_names)

    # Prepare occupancy grid
    if week is None:
        occupancy = np.zeros((n_days, n_hours))
        sample_course = [[None for _ in hours] for _ in day_names]
    else:
        occupancy = np.zeros((n_days, n_hours), dtype=bool)
        labels = [[[] for _ in hours] for _ in day_names]

    # Loop over days, hours, weeks
    for d in D:
        day_name = day_index_to_name.get(d)
        if day_name is None:
            continue
        day_idx = day_map[day_name]
        for h in hours:
            if h not in H:
                continue
            hour_idx = h - hour_range[0]
            if hour_idx < 0 or hour_idx >= n_hours:
                continue
            for e in weeks:
                # Determine week parity (1=odd, 2=even)
                parity = 1 if e % 2 == 1 else 2

                # Gateway events
                gate_lect = any(xL_sol.get((g, d, h, semester), 0) > 0.5 for g in G)
                gate_work = any(xW_sol.get((g, d, h, semester), 0) > 0.5 for g in G)
                gate_fort = any(xF_sol.get((g, d, h, semester, parity), 0) > 0.5 for g in G)

                gateway = gate_lect or gate_work or gate_fort

                # Optional maths events
                opt_lect = any(yL_sol.get((o, d, h, semester), 0) > 0.5 for o in O)
                opt_work = any(yW_sol.get((o, d, h, semester), 0) > 0.5 for o in O)

                optional = opt_lect or opt_work

                if gateway or optional:
                    if week is None:
                        occupancy[day_idx, hour_idx] += 1
                        # Store representative course name (first non‑null)
                        if optional:
                            # find first optional course
                            for o in O:
                                if yL_sol.get((o, d, h, semester), 0) > 0.5 or yW_sol.get((o, d, h, semester), 0) > 0.5:
                                    sample_course[day_idx][hour_idx] = f"O{o}"
                                    break
                        elif gateway:
                            for g in G:
                                if xL_sol.get((g, d, h, semester), 0) > 0.5:
                                    sample_course[day_idx][hour_idx] = f"G{g}L"
                                    break
                                if xW_sol.get((g, d, h, semester), 0) > 0.5:
                                    sample_course[day_idx][hour_idx] = f"G{g}W"
                                    break
                                if xF_sol.get((g, d, h, semester, parity), 0) > 0.5:
                                    sample_course[day_idx][hour_idx] = f"G{g}F"
                                    break
                    else:
                        if e == week:
                            occupancy[day_idx, hour_idx] = True
                            label_parts = []
                            if gateway:
                                label_parts.append("Gateway")
                            if optional:
                                label_parts.append("Optional")
                            labels[day_idx][hour_idx].append("\n".join(label_parts))

    # Plot
    fig, ax = plt.subplots(figsize=figsize)
    if week is None:
        im = ax.imshow(occupancy, cmap='YlOrRd', aspect='auto',
                       vmin=0, vmax=occupancy.max() if occupancy.max() > 0 else 1)
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Number of weeks occupied')
        # Annotate cells with course name and count
        for i in range(n_days):
            for j in range(n_hours):
                if occupancy[i, j] > 0:
                    count = int(occupancy[i, j])
                    course = sample_course[i][j] or ""
                    if len(course) > 12:
                        course = course[:9] + "..."
                    text = f"{course}\n({count} wk)" if course else f"{count} wk"
                    ax.text(j, i, text, ha='center', va='center',
                            fontsize=8, color='black', weight='bold')
    else:
        im = ax.imshow(occupancy, cmap='Blues', aspect='auto', vmin=0, vmax=1)
        for i in range(n_days):
            for j in range(n_hours):
                if occupancy[i, j]:
                    text = '\n'.join(labels[i][j])
                    ax.text(j, i, text, ha='center', va='center',
                            fontsize=8, color='black', weight='bold')

    ax.set_xticks(range(n_hours))
    ax.set_xticklabels([f'{h}:00' for h in hours])
    ax.set_yticks(range(n_days))
    ax.set_yticklabels(day_names)
    ax.set_xlabel('Hour')
    ax.set_ylabel('Day')
    title = f"Mathematics Timetable – Semester {semester}"
    if week:
        title += f", Week {week}"
    else:
        title += " (all weeks combined)"
    ax.set_title(title)
    ax.set_xticks(np.arange(-0.5, n_hours, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_days, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    plt.tight_layout()
    plt.show()
plot_maths_timetable(semester=1, var_sol=var_sol, parameters=parameters)
plot_maths_timetable(semester=2, var_sol=var_sol, parameters=parameters)