import numpy as np
import pandas as pd
import configparser
import argparse

from tqdm.auto import tqdm

# TODO: Turn it into a panel dataset.

def generate_survey_data(
    seed, num_teams, num_grades, num_questions, num_months, team_bias, grade_bias
):
    """Generates simulated survey data based on provided configuration."""
    rng = np.random.default_rng(seed=seed)
    staff_per_team = {team: rng.integers(9, 12) for team in range(1, num_teams + 1)}
    rows = []
    columns = ["date", "employee_id", "team", "grade"] + [
        f"q{i}" for i in range(1, num_questions + 1)
    ]
    current_date = pd.to_datetime("2024-01-31")
    for _ in tqdm(range(num_months)):
        for team, n_staff in staff_per_team.items():
            for _ in range(n_staff):
                employee_id = rng.integers(1000, 9999)
                grade = rng.integers(1, num_grades + 1)
                responses = (
                    rng.integers(1, 6, size=num_questions)
                    + team_bias[team]
                    + grade_bias[grade]
                )
                responses = np.clip(responses, 1, 5)
                row = [current_date, employee_id, team, grade] + responses.tolist()
                rows.append(row)
        current_date = (current_date + pd.offsets.MonthEnd()).normalize()
    return pd.DataFrame(rows, columns=columns)


if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Simulate staff survey data")
    parser.add_argument(
        "--config", type=str, default="config.ini", help="Configuration file"
    )
    args = parser.parse_args()

    # Read configuration file
    config = configparser.ConfigParser()
    config.read(args.config)

    try:
        # Extract parameters and biases using lower case
        seed = config.getint("default", "seed")
        num_teams = config.getint("default", "teams")
        num_grades = config.getint("default", "grades")
        num_questions = config.getint("default", "questions")
        num_months = config.getint("default", "months")
        team_bias = {
            i: config.getint("bias", f"team{i}") for i in range(1, num_teams + 1)
        }
        grade_bias = {
            i: config.getint("bias", f"grade{i}") for i in range(1, num_grades + 1)
        }

        # Generate survey data
        df_survey = generate_survey_data(
            seed,
            num_teams,
            num_grades,
            num_questions,
            num_months,
            team_bias,
            grade_bias,
        )

        # Output the data
        print(df_survey.head())
        print(f"Total rows: {df_survey.shape[0]}")
        
        # Export the data
        out_name = "./data/survey.csv"
        df_survey.to_csv(out_name, index=False)
        print(f"Exported 'df_survey' as '{out_name}'.")

    except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
        print(f"Error reading configuration or invalid value: {e}")
