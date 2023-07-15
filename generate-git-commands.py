import csv

def generate_git_commands(input_file):
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file, delimiter='\t') # tab delimited
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            print(f'git clone https://github.com/{row[0]} ~/src/github.com/{row[0]}')

# Use the function
generate_git_commands('input.csv')
