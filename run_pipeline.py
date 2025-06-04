import warnings
from bs4 import GuessedAtParserWarning

warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

from my_project.data import process_musicals

if __name__ == "__main__":
    input_file = "data/movies.csv"
    critic_file = "data/critic_reviews.csv"
    output_file = "output/output_musicals.csv"

    process_musicals(input_file, output_file, critic_file)
