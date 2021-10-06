import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import random
np.random.seed(42)

# Default Params....
# INITIAL_MAX_STUDENTS = 11_000
# INITIAL_STUDENTS_APPLYING = 21_000
# INITIAL_MAX_STUDENTS_ADMITTED = 2750
# TRANSFER_STUDENT_APPS_PER_YEAR = 1600
# TRANSFER_STUDENT_ACCEPTANCE_RATE = 0.738
# ACCEPTANCE_RATE = 0.673
# ACCEPTED_WHO_ATTEND = 0.2
# GRADUATION_RATE = 0.74


# timestemps are 1 year at a time
YEARS = 20


def model_students_through_uvm(years_to_simulate):
    INITIAL_MAX_STUDENTS = 100
    INITIAL_STUDENTS_APPLYING = 100
    TRANSFER_STUDENT_APPS_PER_YEAR = 50
    TRANSFER_STUDENT_ACCEPTANCE_RATE = 0.23
    ACCEPTANCE_RATE = 0.6
    ACCEPTED_WHO_ATTEND = 0.22
    GRADUATION_RATE = 0.3
    FAILURE_RATE = 1 - GRADUATION_RATE

    lost_students = []
    graduated_students = []
    current_total_students = []
    gained_students = []

    current_max_students = INITIAL_MAX_STUDENTS
    students_applied = INITIAL_STUDENTS_APPLYING
    transfer_students = TRANSFER_STUDENT_APPS_PER_YEAR

    for year in range(years_to_simulate):
        delta_new_students = students_applied * ACCEPTANCE_RATE * ACCEPTED_WHO_ATTEND
        delta_graduated_students = (current_max_students / 4) * GRADUATION_RATE
        delta_lost_students = (current_max_students / 4) * FAILURE_RATE
        delta_new_students += transfer_students * TRANSFER_STUDENT_ACCEPTANCE_RATE
        delta_new_students += np.random.randint(-600, 600)  # noise

        current_max_students -= delta_lost_students
        current_max_students += delta_new_students
        current_max_students -= delta_graduated_students

        lost_students.append(delta_lost_students)
        graduated_students.append(delta_graduated_students)
        current_total_students.append(current_max_students)
        gained_students.append(delta_new_students)

    timesteps = [i for i in range(years_to_simulate)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timesteps, y=current_total_students, mode='lines', name='Total Students Enrolled', marker_color='red'))
    fig.add_trace(go.Scatter(x=timesteps, y=gained_students, mode='lines', name='Gained Students per Year', marker_color='green'))
    fig.add_trace(go.Scatter(x=timesteps, y=lost_students, mode='lines', name='Lost Students per Year (dropped/failed out)', marker_color='blue'))
    fig.add_trace(go.Scatter(x=timesteps, y=graduated_students, mode='lines', name='Graduated Students per Year', marker_color='purple'))
    fig.update_xaxes(title='Timestamp (year)')
    fig.update_yaxes(title='Number of Students')
    fig.update_layout(title='UVM Undergraduate Student Population')
    print('Params:')
    print(f'initial_max_students={INITIAL_MAX_STUDENTS}')
    print(f'students_applied={INITIAL_STUDENTS_APPLYING}')
    print(f'transfers_per_year={TRANSFER_STUDENT_APPS_PER_YEAR}')
    print(f'transfer_acceptance_rate={TRANSFER_STUDENT_ACCEPTANCE_RATE}')
    print(f'acceptance_rate={ACCEPTANCE_RATE}')
    print(f'accepted_who_actually_attend_rate={ACCEPTED_WHO_ATTEND}')
    print(f'graduation_rate={GRADUATION_RATE}')
    print(f'failure_rate={FAILURE_RATE}')
    fig.show()


def main():
    model_students_through_uvm(YEARS)


if __name__ == '__main__':
    main()