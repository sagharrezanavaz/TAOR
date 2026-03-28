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

def change_name(name):
    n = len(name)
    a = name[:(n-7)//2]
    #print(a)
    b = name[(n-7)//2 + 2:]
    #print(b)
    c = name[:(n-7)//2 +5]
    d = name[(n-7)//2 +5+2:]
    if '(UG)' in a:
        return a
    elif '(UG)' in b:
        return b
    elif '(UG)' in c:
        return c
    elif '(UG)' in c:
        return d
    else:
        split = name.split(',')
        a = split[0]
        b = split[1]
        if '(UG)' in a:
            return a
        elif '(UG)' in b:
            return b
        else:
            return "Error"
departments_needed = ['School of Mathematics','School of Philosophy, Psychology and Language Sciences','School of Economics','School of Informatics',
                      'School of Physics and Astronomy',
                      'Business School']
collections_needed = ['Economics Course Options for Joint Programmes Year 3 (A)',
       'Economics Course Options Year 3 (joint programmes)',
       'Economics and Maths Dissertation',
       'Economics Course Options Year 4 (joint programmes)',
       'Topics in Microeconomics', 'Essentials of Econometrics','MathPhy : Mathematics Projects',
       'MathsPhysics : Y4 Physics Projects',
       'Undergraduate (School of Physics and Astronomy) Level 10 and 11 courses',
       'Electromagnetism and Relativity',
       'MathsPhysics : Y3 physics choice',
       'Undergraduate (School of Physics and Astronomy) Level 9 and 10  courses',
       'MathsBusiness : Y4 Projects',
       '2024-25: UTMATHB : Y4/5 : Approved Outside Courses',
       'ROU_H_UT International Business 4_10',
       'Strategic Management',
       '2024-25: UTMATHB : Y3 options : Business options',
       'Informatics Hons 3rd Year Group Project and Large Practical',
       'Informatics Hons 3rd Year AI Courses',
       'Informatics Hons 3rd Year Joint Degree CS Courses',
       'Informatics - Professional Issues',
       'Honours Project (Informatics)',
       'Informatics Hons 4th Year Courses',
        'Year 3 Philosophy - History of Philosophy',
       'Practical Philosophy', 'Theoretical Philosophy',
       'Philosophy Honours Year 4']
programmes_needed = ['Mathematics and Business BSc (Hons)',
                     #'Mathematics and Physics (BSc Hons)',
                     'Economics and Mathematics (MA Hons)','Computer Science and Mathematics (BSc Hons)',
              'Philosophy and Mathematics (MA Hons)']

courses_df = pd.read_csv("2024-5 Event Module Room.csv")
courses_df = courses_df[courses_df["Module Department"].isin(departments_needed)]
courses_df = courses_df[courses_df["Event Type"]=="Lecture"]
programme_df = pd.read_csv('2024-5 DPT Data.csv',encoding = "latin1")

programme_df = programme_df[programme_df["Programme Year"].isin([3])]
programme_df = programme_df[programme_df["Programme Name"].isin(programmes_needed)]
programme_df = programme_df[programme_df["Collection Name"].isin(collections_needed)]

ug_indices = courses_df[
    (courses_df["Module Department"]=="School of Informatics") & 
    (courses_df['Module Name'].str.contains('\(UG\)', na=False))
].index

# Apply the change_name function to those specific rows
courses_df.loc[ug_indices, 'Module Name'] = courses_df.loc[ug_indices, 'Module Name'].apply(change_name)
#programme_df = programme_df[programme_df['Collection Reg Group']!="Physics 3 A"]

# Year 3
#Informatics 
condition_inf_A3 = (
    (programme_df['Collection Reg Group'] == 'A') & 
    (programme_df['Programme School Name'] == 'School of Informatics') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_inf_A3, 'Collection Reg Group'] = 'School of Informatics 3 A'

#Economics
condition_eco_A3 = (
    (programme_df['Collection Reg Group'] == 'A') & 
    (programme_df['Programme School Name'] == 'School of Economics') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_eco_A3, 'Collection Reg Group'] = 'Economics 3 A'

#Philosophy
condition_phi_B3 = (
    (programme_df['Collection Reg Group'] == 'B') & 
    (programme_df['Programme School Name'] == 'School of Philosophy, Psychology and Language Sciences') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_phi_B3, 'Collection Reg Group'] = 'Philosophy 3 B'

#Business
condition_bus_B3 = (
    (programme_df['Collection Reg Group'] == 'B') & 
    (programme_df['Programme Name'] == 'Mathematics and Business BSc (Hons)') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_bus_B3, 'Collection Reg Group'] = 'Business 3 B'

#Physics
#condition_phy_A3 = (
 #   (programme_df['Collection Reg Group'] == 'A') & 
  #  (programme_df['Programme Name'] == 'Mathematics and Physics (BSc Hons)') & 
   # (programme_df['Programme Year'] == 3)
#)
#programme_df.loc[condition_phy_A3, 'Collection Reg Group'] = 'Physics 3 A'

#Physics
#condition_bounds_phy_A3 = (
 #   (programme_df['Collection Reg Group'] == 'Physics 3 A') & 
  #  (programme_df['Programme Name'] == 'Mathematics and Physics (BSc Hons)') & 
   # (programme_df['Programme Year'] == 3)
#)
#programme_df.loc[condition_bounds_phy_A3, 'Collection Group Min'] = 20.0
#programme_df.loc[condition_bounds_phy_A3, 'Collection Group Max'] = 40.0

#Business
condition_bounds_bus_B3 = (
    (programme_df['Collection Reg Group'] == 'Business 3 B') & 
    (programme_df['Programme Name'] == 'Mathematics and Business BSc (Hons)') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_bounds_bus_B3, 'Collection Group Min'] = 0.0
programme_df.loc[condition_bounds_bus_B3, 'Collection Group Max'] = 60.0

#Philosophy
condition_bounds_phi_B3 = (
    (programme_df['Collection Reg Group'] == 'Philosophy 3 B') & 
    (programme_df['Programme School Name'] == 'School of Philosophy, Psychology and Language Sciences') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_bounds_phi_B3, 'Collection Group Min'] = 40.0
programme_df.loc[condition_bounds_phi_B3, 'Collection Group Max'] = 80.0

#Economics
condition_bounds_eco_A3 = (
    (programme_df['Collection Reg Group'] == 'Economics 3 A') & 
    (programme_df['Programme School Name'] == 'School of Economics') & 
    (programme_df['Programme Year'] == 3)
)
programme_df.loc[condition_bounds_eco_A3, 'Collection Group Min'] = 0.0
programme_df.loc[condition_bounds_eco_A3, 'Collection Group Max'] = 20.0

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
#programme_data

def extract_timetable_info(courses_df, programmes_data):
    """
    Extract v parameter with dynamic duration per course
    """
    # Filter for all relevant courses
    all_relevant_courses = {"G1","G2","G3","G4",'G5','G6','G7','G8','O1','O2','O3','O4'}
    
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
#extract_timetable_info(courses_df, programmes_data)

def extract_days_hours_from_v(v):
    """
    Extract unique days and hours from v dictionary
    """
    if not v:
        # If v is empty, use default days and hours
        return [1, 2, 3, 4, 5], list(range(9, 18))  # Monday-Friday, 9am-5pm
    
    days = sorted(list(set([key[1] for key in v.keys()])))
    hours = sorted(list(set([key[2] for key in v.keys()])))
    
    # If no days/hours found, use defaults
    if not days:
        days = [1, 2, 3, 4, 5]
    if not hours:
        hours = list(range(9, 18))
    
    return days, hours

# Add this to your extract_all_parameters function
def extract_all_parameters(courses_df, programme_df):
    """
    Complete extraction including days and hours
    """
    
    # Step 1: Define Maths courses
    gateway_courses = ["G1","G2","G3","G4",'G5','G6','G7','G8']
    optional_courses = ['O1','O2','O3','O4']
    
    # Step 2: Extract programme structure
    programme_data = extract_programme_structure(programme_df)
    programmes = list(programme_data.keys())
    
    # Step 3: Extract timetable info
    v = extract_timetable_info(courses_df, programme_data)
    
    # Step 4: Extract days and hours from v
    days, hours = extract_days_hours_from_v(v)

    weeks = list(range(1, 53))  # E = {1, ..., 52}
    weeks_sem1 = list(range(1, 27))  # E_1 = {1, ..., 26}
    weeks_sem2 = list(range(27, 53))  # E_2 = {27, ..., 52}

    campuses = courses_df['Campus'].dropna().unique().tolist()
    
    # Build the complete parameter set
    parameters = {
        # Sets
        'G': gateway_courses,
        'O': optional_courses,
        'S': [1, 2],  # Semesters
        'D': days,    # Days extracted from timetable
        'H': hours,   # Hours extracted from timetable
        'W': [1, 2],  # Week parity
        'Q': programmes,
        'E': weeks,           # All weeks
        'E1': weeks_sem1,     # Semester 1 weeks
        'E2': weeks_sem2,     # Semester 2 weeks
        'K': campuses,        # Campuses
        # Parameters
        'R_g_L': 3,  # Fixed for gateway
        'R_g_W': 1,  # Fixed for gateway
        'R_g_F': 1,  # Fixed for gateway
        'R_o_L': 3,  # Fixed for optional
        'R_o_W': 1,  # Fixed for optional
        'C_g': 4,    # 4 gateway courses per semester
        'C_o': 2,    # 2 optional courses per semester
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
parameters = extract_all_parameters(courses_df,programme_df)
#extract_all_parameters(courses_df,programme_df)

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
        'E': parameters['E'],      # All weeks
        'E1': parameters['E1'],    # Semester 1 weeks
        'E2': parameters['E2'],    # Semester 2 weeks
        'K': parameters['K'],      # Campuses
        
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

def build_model_from_parameters(parameters):
    """
    Build the Xpress model using the extracted parameters
    """
    
    # Unpack parameters
    G = parameters['G']  # Gateway courses
    O = parameters['O']  # Optional courses
    S = parameters['S']  # Semesters
    D = parameters['D']  # Days
    H = parameters['H']  # Hours
    W = parameters['W']  # Week parity
    Q = parameters['Q']  # Programmes
    E = parameters['E']      # All weeks
    E1 = parameters['E1']    # Semester 1 weeks
    E2 = parameters['E2']    # Semester 2 weeks
    K = parameters['K']      # Campuses
    
    # Constants
    C_g = parameters['C_g']  # 4 gateway courses per semester
    C_o = parameters['C_o']  # 2 optional courses per semester
    
    # Teaching event counts
    R_g_L = parameters['R_g_L']  # Lectures per gateway (could be dict or int)
    R_g_W = parameters['R_g_W']  # Weekly workshops per gateway
    R_g_F = parameters['R_g_F']  # Fortnightly workshops per gateway
    R_o_L = parameters['R_o_L']  # Lectures per optional
    R_o_W = parameters['R_o_W']  # Workshops per optional
    
    # Timetable data
    v = parameters['v']  # Scheduled events for mandatory courses
    
    # Programme-specific data
    programme_data = parameters['programme_data']
    CO_CO_q = {prog: programme_data[prog]['compulsory_courses'] for prog in Q}
    CO_OP_q = {prog: programme_data[prog]['optional_courses'] for prog in Q}
    CO_q = {prog: programme_data[prog]['all_courses'] for prog in Q}
    
    # Collection and regression group data
    SC_cl = parameters['SC_cl']
    SCL_cr = parameters['SCL_cr']
    min_CL = parameters['min_CL']
    max_CL = parameters['max_CL']
    min_CR = parameters['min_CR']
    max_CR = parameters['max_CR']
    
    # Credit data
    n_co = parameters['n_co']
    n_q = parameters['n_q']
    
    # Create problem
    p = xp.problem()
    
    # ==================== DECISION VARIABLES ====================
    print("Creating decision variables...")
    
    # Gateway course variables
    x_L = {}
    x_W = {}
    x_F = {}
    
    for g in G:
        for d in D:
            for h in H:
                for s in S:
                    x_L[(g, d, h, s)] = xp.var(vartype=xp.binary, 
                                                 name=f"xL_{g}_{d}_{h}_{s}")
                    x_W[(g, d, h, s)] = xp.var(vartype=xp.binary, 
                                                 name=f"xW_{g}_{d}_{h}_{s}")
                    for w in W:
                        x_F[(g, d, h, s, w)] = xp.var(vartype=xp.binary, 
                                                       name=f"xF_{g}_{d}_{h}_{s}_{w}")
    
    # Optional course variables
    y_L = {}
    y_W = {}
    
    for o in O:
        for d in D:
            for h in H:
                for s in S:
                    y_L[(o, d, h, s)] = xp.var(vartype=xp.binary, 
                                                name=f"yL_{o}_{d}_{h}_{s}")
                    y_W[(o, d, h, s)] = xp.var(vartype=xp.binary, 
                                                name=f"yW_{o}_{d}_{h}_{s}")
    
    # Course assignment variables
    z = {(g, s): xp.var(vartype=xp.binary, name=f"z_{g}_{s}") 
         for g in G for s in S}
    w_var = {(o, s): xp.var(vartype=xp.binary, name=f"w_{o}_{s}") 
             for o in O for s in S}
    
    # Student course choice variables
    a = {}
    
    
    for q in Q:
        for co in CO_q[q]:
            a[(q, co)] = xp.var(vartype=xp.binary, name=f"a_{q}_{co}")
    
    
    # Add all variables to problem
    all_vars = (list(x_L.values()) + list(x_W.values()) + list(x_F.values()) +
                list(y_L.values()) + list(y_W.values()) +
                list(z.values()) + list(w_var.values()) +
                list(a.values()))
    
    p.addVariable(all_vars)
    
    print("Creating event presence expressions...")
    
    P = {}
    for q in Q:
        for d in D:
            for h in H:
                for s in S:
                    weeks = E1 if s == 1 else E2                    
                    for e in weeks:
                        expr = 0
                        
                        # Gateway events (shared across programmes)
                        expr += xp.Sum(x_L[(g,d,h,s)] + x_W[(g,d,h,s)] for g in G)
                        expr += xp.Sum(x_F[(g,d,h,s,w)] for g in G for w in W)
                        
                        # Optional maths
                        expr += xp.Sum(y_L[(o,d,h,s)] + y_W[(o,d,h,s)] for o in O)
                        
                        # Non-maths courses (programme-specific)
                        for co in CO_q[q]:
                            for k in K:
                                expr += a[(q,co)] * v.get((co,d,h,e,q,k), 0)
                                
                        P[(q,d,h,s,e)] = expr
                        
    print("Creating soft constraint variables...")
    
    late = {}
    lunch = {}
    isol = {}
    day_used = {}
    
    for q in Q:
        for s in S:
            weeks = E1 if s == 1 else E2
            
            for e in weeks:
                for d in D:
                    day_used[(q,d,s,e)] = xp.var(vartype=xp.binary, name=f"day_{q}_{d}_{s}_{e}")
                    
                    for h in H:
                        late[(q,d,h,s,e)] = xp.var(vartype=xp.binary, name=f"late_{q}_{d}_{h}_{s}_{e}")
                        lunch[(q,d,h,s,e)] = xp.var(vartype=xp.binary, name=f"lunch_{q}_{d}_{h}_{s}_{e}")
                        
                        if 1 <= h <= 7:
                            isol[(q,d,h,s,e)] = xp.var(vartype=xp.binary, name=f"isol_{q}_{d}_{h}_{s}_{e}")
    
    p.addVariable(list(late.values()) + list(lunch.values()) + 
              list(isol.values()) + list(day_used.values()))
    
    # ==================== CONSTRAINTS ====================
    print("Adding constraints...")
    constraint_count = 0
    
    # Helper function to add constraint with name
    def add_constraint(expr, name):
        """Add constraint with name"""
        p.addConstraint(expr)
        return name
    
    # CONSTRAINT 1: Each gateway course has exactly one fortnightly workshop
    print("Adding constraint 1: Fortnightly workshops per gateway...")
    for g in G:
        cons = xp.Sum(x_F[(g, d, h, s, w)] for d in D for h in H for s in S for w in W) == R_g_F
        p.addConstraint(cons)
        constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 2: A course cannot have more than one event in the same time slot
    print("Adding constraint 2: No multiple events in same time slot...")
    
    # For gateway courses
    for g in G:
        for d in D:
            for h in H:
                for s in S:
                    cons = (x_L[(g, d, h, s)] + x_W[(g, d, h, s)] + 
                           xp.Sum(x_F[(g, d, h, s, w)] for w in W) <= 1)
                    p.addConstraint(cons)
                    constraint_count += 1
    print(constraint_count)
    # For optional courses
    for o in O:
        for d in D:
            for h in H:
                for s in S:
                    cons = y_L[(o, d, h, s)] + y_W[(o, d, h, s)] <= 1
                    p.addConstraint(cons)
                    constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 3: No clashes for students in any week (any combination condition)
    print("Adding constraint 3: No student clashes in any week...")
    for d in D:
        for h in H:
            for s in S:
                for w in W:
                    cons = (xp.Sum(x_L[(g, d, h, s)] + x_W[(g, d, h, s)] for g in G) +
                           xp.Sum(y_L[(o, d, h, s)] + y_W[(o, d, h, s)] for o in O) +
                           xp.Sum(x_F[(g, d, h, s, w)] for g in G) <= 1)
                    p.addConstraint(cons)
                    
                    constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 4: Events can only occur in the semester the course is assigned to
    print("Adding constraint 4: Events limited to assigned semester...")
    
    # For gateway courses
    for g in G:
        for d in D:
            for h in H:
                for s in S:
                    cons1 = x_L[(g, d, h, s)] <= z[(g, s)]
                    cons2 = x_W[(g, d, h, s)] <= z[(g, s)]
                    p.addConstraint(cons1)
                    p.addConstraint(cons2)
                    constraint_count += 2
                    for w in W:
                        cons3 = x_F[(g, d, h, s, w)] <= z[(g, s)]
                        p.addConstraint(cons3)
                        constraint_count += 1
    print(constraint_count)
    # For optional courses
    for o in O:
        for d in D:
            for h in H:
                for s in S:
                    cons1 = y_L[(o, d, h, s)] <= w_var[(o, s)]
                    cons2 = y_W[(o, d, h, s)] <= w_var[(o, s)]
                    p.addConstraint(cons1)
                    p.addConstraint(cons2)
                    constraint_count += 2
    print(constraint_count)
    # CONSTRAINT 5: Gateway course assignment to semesters
    print("Adding constraint 5: Gateway course semester assignment...")
    for g in G:
        cons = xp.Sum(z[(g, s)] for s in S) == 1
        p.addConstraint(cons)
        constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 6: Optional course assignment to semesters
    print("Adding constraint 6: Optional course semester assignment...")
    for o in O:
        cons = xp.Sum(w_var[(o, s)] for s in S) == 1
        p.addConstraint(cons)
        constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 7: Exactly required number of courses per semester
    print("Adding constraint 7: Course count per semester...")
    for s in S:
        cons1 = xp.Sum(z[(g, s)] for g in G) == C_g
        cons2 = xp.Sum(w_var[(o, s)] for o in O) == C_o
        p.addConstraint(cons1)
        p.addConstraint(cons2)
        constraint_count += 2
    print(constraint_count)
    # CONSTRAINT 8: Correct number of teaching events for gateway courses
    print("Adding constraint 8: Teaching events count for gateway...")
    for g in G:
        for s in S:
            # Lectures
            lect_count = R_g_L[g] if isinstance(R_g_L, dict) else R_g_L
            cons = xp.Sum(x_L[(g, d, h, s)] for d in D for h in H) == lect_count * z[(g, s)]
            p.addConstraint(cons)
            
            # Weekly workshops
            workshop_count = R_g_W[g] if isinstance(R_g_W, dict) else R_g_W
            cons = xp.Sum(x_W[(g, d, h, s)] for d in D for h in H) == workshop_count * z[(g, s)]
            p.addConstraint(cons)
            constraint_count += 2
    print(constraint_count)
    # CONSTRAINT 9: Correct number of teaching events for optional courses
    print("Adding constraint 9: Teaching events count for optional...")
    for o in O:
        for s in S:
            cons = xp.Sum(y_L[(o, d, h, s)] for d in D for h in H) == R_o_L * w_var[(o, s)]
            p.addConstraint(cons)
            constraint_count +=1
            cons = xp.Sum(y_W[(o, d, h, s)] for d in D for h in H) == R_o_W * w_var[(o, s)]
            p.addConstraint(cons)
            constraint_count += 1

    print(constraint_count)
    # CONSTRAINT 10: Collection credit requirements
    print("Adding constraint 10: Collection credit requirements...")
    for cl_id in SC_cl:
        for q in Q:
            # Check if this collection exists for this programme
            if cl_id in programme_data[q].get('collections', {}):
                collection_sum = xp.Sum(n_co[co] * a[(q, co)] 
                                       for co in SC_cl[cl_id] 
                                       if co in CO_q[q])
                cons1 = collection_sum >= min_CL[cl_id]
                
                cons2 = collection_sum <= max_CL[cl_id]
                
                p.addConstraint(cons1)
                constraint_count+= 1
                print(cl_id,constraint_count,min_CL[cl_id])
                
                p.addConstraint(cons2)
                constraint_count += 1
                print(cl_id,constraint_count,max_CL[cl_id])
                
    print(constraint_count)
    # CONSTRAINT 11: Regression group credit requirements
    print("Adding constraint 11: Regression group credit requirements...")
    for rg_id in SCL_cr:
        for q in Q:
            if rg_id in programme_data[q].get('regression_groups', {}):
                reg_sum = xp.Sum(n_co[co] * a[(q, co)] 
                                for cl_id in SCL_cr[rg_id]
                                for co in SC_cl[cl_id]
                                if co in CO_q[q])
                cons1 = reg_sum >= min_CR[rg_id]
                print(rg_id, constraint_count)
                p.addConstraint(cons1)
                constraint_count += 1
                cons2 = reg_sum <= max_CR[rg_id]
                print(rg_id, constraint_count)
                p.addConstraint(cons2)
                constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 12: No compulsory course should collide with gateway courses
    print("Adding constraint 12: No collisions with compulsory courses...")
    clash_count = 0
    
    for q in Q:
        for d in D:
            for h in H:
                for s in S:
                    # Get weeks for this semester
                    if s == 1:
                        weeks = E1
                    elif s == 2:
                        weeks = E2
                    else:
                        weeks = E
                    
                    # Ensure weeks is a list of integers
                    if isinstance(weeks, list) and len(weeks) > 0:
                        for e in weeks:  # e should be integer week number
                            for k in K:
                                # Sum over gateway courses at this time slot
                                gateway_sum = xp.Sum(x_L[(g, d, h, s)] for g in G)
                                
                                # Sum over optional courses that are taken and have scheduled events
                                optional_sum = xp.Sum(
                                    a[(q, o)] * v.get((o, d, h, e, q, k), 0) 
                                    for o in O 
                                    if o in CO_OP_q.get(q, [])
                                )
                                
                                # No clash constraint
                                cons = gateway_sum + optional_sum <= 1
                                p.addConstraint(cons)
                                clash_count += 1
    
    constraint_count += clash_count
    print(constraint_count)
    # CONSTRAINT 13: Student course selection - compulsory courses must be taken
    print("Adding constraint 13: Compulsory course selection...")
    for q in Q:
        for co in CO_CO_q[q]:
            cons = a[(q, co)] == 1
            p.addConstraint(cons)
            constraint_count += 1
    print(constraint_count)
    # CONSTRAINT 15: Minimum credits outside Mathematics
    print("Adding constraint 14: Minimum credits outside Maths...")
    print('fegrg4t')
    for q in Q:
        outside_credits = xp.Sum(n_co[co] * a[(q, co)] 
                                for co in CO_q[q] 
                                if co not in G and co not in O)
        cons = outside_credits >= n_q[q]
        p.addConstraint(cons)
        constraint_count += 1
        print(q, constraint_count)
        
    print(constraint_count)   
    print("Adding constraint 15: Gateway and compulsory clash avoiding")
    def flatten_weeks(week_list):
        """Flatten nested week lists into a single list of integers"""
        if not isinstance(week_list, (list, tuple)):
            return [week_list]
        
        flat_list = []
        for item in week_list:
            if isinstance(item, (list, tuple)):
                flat_list.extend(flatten_weeks(item))
            else:
                flat_list.append(item)
        return flat_list
    
    # Create flattened week lists
    E_flat = flatten_weeks(E)
    E1_flat = flatten_weeks(E1)
    E2_flat = flatten_weeks(E2)
    
    # Now add the constraint with flattened weeks
    clash_count = 0
    
    for q in Q:
        for d in D:
            for h in H:
                for s in S:
                    # Get weeks for this semester (now flattened)
                    if s == 1:
                        weeks = E1_flat
                    elif s == 2:
                        weeks = E2_flat
                    else:
                        weeks = E_flat
                    
                    # Iterate through each individual week
                    for e in weeks:
                        # Ensure e is a single integer
                        if isinstance(e, (list, tuple)):
                            print(f"Warning: e is still a list: {e}, skipping")
                            continue
                        
                        for k in K:
                            # Sum over all gateway courses' lectures at this time slot
                            gateway_sum = xp.Sum(x_L[(g, d, h, s)] for g in G)
                            
                            # Sum over all compulsory courses that have scheduled events at this time
                            compulsory_terms = []
                            for co in CO_CO_q[q]:
                                # Create the key for v dictionary
                                key = (co, d, h, e, q, k)
                                # Get the value from v or 0 if not present
                                val = v.get(key, 0)
                                if val > 0:  # Only add if there's a scheduled event
                                    compulsory_terms.append(a[(q, co)] * val)
                            
                            if compulsory_terms:  # Only add constraint if there are terms
                                compulsory_sum = xp.Sum(compulsory_terms)
                                # Ensure the total doesn't exceed 1
                                cons = gateway_sum + compulsory_sum <= 1
                                p.addConstraint(cons)
                                clash_count += 1
    
    constraint_count += clash_count
          
    
    
    print(constraint_count)
    print("Adding constraint 16: Minimum 40 credits outside Maths")
    for q in Q:
        # Sum credits from all courses in the curriculum that are NOT Maths courses
        outside_maths_credits = xp.Sum(
            n_co[co] * a[(q, co)] 
            for co in CO_q[q]  # All courses in this programme
            if co not in G and co not in O  # Exclude gateway and optional (Maths) courses
        )
        
        # Require at least 40 credits
        cons = outside_maths_credits >= 40
        p.addConstraint(cons)
        constraint_count += 1
    print(constraint_count)
    print("Adding constraint 17: Compulsory courses should be taken in each curriculum")
    for q in Q:
        for co in CO_CO_q[q]:  # Compulsory courses for this programme
            cons = a[(q, co)] == 1
            p.addConstraint(cons)
            print(cons)
            constraint_count += 1
    print(constraint_count)
    
    # ==================== SOFT CONSTRAINTS ====================
    
    # SOFT CONSTRAINT 1: Late classes
    max_h = max(H)
    
    for q in Q:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    cons = P[(q,d,max_h,s,e)] <= late[(q,d,max_h,s,e)]
                    p.addConstraint(cons)
                    
    # SOFT CONSTRAINT 2: Lunch hours
    for q in Q:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                for e in weeks:
                    for h in [3,4]:
                        if h in H:
                            cons = P[(q,d,h,s,e)] <= lunch[(q,d,h,s,e)]
                            p.addConstraint(cons)
                            
    # SOFT CONSTRAINT 3: Isolated lectures
    for q in Q:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                
                for e in weeks:
                    for h in H:
                        if h in range(1,8) and (h-1 in H) and (h+1 in H):
                            
                            cons1 = isol[(q,d,h,s,e)] >= (
                                P[(q,d,h,s,e)] 
                                - P[(q,d,h+1,s,e)] 
                                - P[(q,d,h-1,s,e)]
                            )
                            
                            cons2 = isol[(q,d,h,s,e)] <= P[(q,d,h,s,e)]
                            
                            p.addConstraint(cons1)
                            p.addConstraint(cons2)
                            
    # SOFT CONSTRAINT 4: Number of days
    for q in Q:
        for d in D:
            for s in S:
                weeks = E1 if s == 1 else E2
                
                for e in weeks:
                    total = xp.Sum(P[(q,d,h,s,e)] for h in H)
                    
                    p.addConstraint(day_used[(q,d,s,e)] <= total)
                    p.addConstraint(total <= len(H) * day_used[(q,d,s,e)])
                    
    # SOFT CONSTRAINT 5: Wednesday afternoon
    #WED = 3
    
    #wed_penalty = []
    
    #for q in Q:
        #for s in S:
            #weeks = E1 if s == 1 else E2
            
            #for e in weeks:
                #if WED in D:
                    #for h in H:
                        #wed_penalty.append(P[(q, WED, h, s, e)])
                        
    print("Setting objective...")
    
    #wed_expr = xp.Sum(wed_penalty) if len(wed_penalty) > 0 else 0
    
    lambda_late = 1
    lambda_lunch = 1
    lambda_isol = 1
    lambda_days = 1
    #lambda_wed = O
    
    objective = (
        lambda_late * xp.Sum(late[q,d,h,s,e] for (q,d,h,s,e) in late) +
        lambda_lunch * xp.Sum(lunch[q,d,h,s,e] for (q,d,h,s,e) in lunch) +
        lambda_isol * xp.Sum(isol[q,d,h,s,e] for (q,d,h,s,e) in isol) +
        lambda_days * xp.Sum(day_used[q,d,s,e] for (q,d,s,e) in day_used)# +
        #lambda_wed * wed_expr
    )

    p.setObjective(objective, sense=xp.minimize)
    
    return p

build_model_from_parameters(parameters)

def solve_model(parameters):
    model = build_model_from_parameters(parameters)
    
    model.setControl('outputlog', 1)
    
    print("\nSolving model...")
    model.solve()
    
    status_string = model.getProbStatusString()
    print("\nSolution status:", status_string)
    
    # Check status using string
    if ("optimal" in status_string) or ("Feasible" in status_string):
        print("Feasible solution found!")
        
        sol = model.getSolution()
        results = analyze_solution(model, parameters, sol)
        
        return model, results       
    
    else:
        print("Model is infeasible!")
        
        print("\nComputing IIS...")
        model.iisfirst(1)
        model.iisnext()
        
        rows = model.getiisrows()
        
        print("\nConstraints causing infeasibility:")
        for r in rows:
            print(f"Row {r}: {model.getRowName(r)}")
        
        model.write("iis.ilp")
        print("\nIIS written to iis.ilp")
        
        return model, None

def analyze_solution(model, parameters, sol):
    """
    Analyze and display the solution
    """
    results = {
        'gateway_schedule': {},
        'optional_schedule': {},
        'course_selection': {}
    }
    
    # Get all variables
    vars_dict = {var.name: var for var in model.getVariable()}
    
    # Find which gateway courses run in which semester
    for (g, s), var in parameters.get('z_vars', {}).items():
        if sol[var] > 0.5:
            if g not in results['gateway_schedule']:
                results['gateway_schedule'][g] = []
            results['gateway_schedule'][g].append(s)
    
    # Find which optional courses run in which semester
    for (o, s), var in parameters.get('w_vars', {}).items():
        if sol[var] > 0.5:
            if o not in results['optional_schedule']:
                results['optional_schedule'][o] = []
            results['optional_schedule'][o].append(s)
    
    return results

def print_results(results):
    """
    Print the results
    """
    if results is None:
        print("No results to display")
        return
    
    print("\n" + "="*50)
    print("SOLUTION RESULTS")
    print("="*50)
    
    print("\nGateway Course Schedule:")
    for g, sems in results['gateway_schedule'].items():
        print(f"  {g}: Semester(s) {sems}")
    
    print("\nOptional Course Schedule:")
    for o, sems in results['optional_schedule'].items():
        print(f"  {o}: Semester(s) {sems}")
    
    # Count how many gateway courses each programme can take
    print("\nFeasibility Status:")
    print("  Model is feasible - joint students can take all gateway courses")
    print("  while meeting their mandatory course requirements.")
    
# Assuming you have already run your extraction steps
# parameters = extract_all_parameters(courses_df, programme_df)

# Build and solve the model
model, results = solve_model(parameters)

# Print results
print_results(results)

