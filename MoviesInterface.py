# name: YOUR NAME HERE
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    """
    Prompt the user for movie information and add it to the DynamoDB table.
    """

    title = input("Enter movie title: ").strip()
    genre = input("Enter genre: ").strip()
    year = input("Enter release year: ").strip()

    table.put_item(
        Item={
            "Title": title,
            "Genre": genre,
            "Year": year
        }
    )

    print(f"Movie '{title}' added successfully.")

def print_all_movies():
    """Scan the entire Movies table and print each item."""
    
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print(movie)


def main():
    print("===== Reading from DynamoDB =====\n")
    print_all_movies()


if __name__ == "__main__":
    main()

def update_rating():
    try:
        title = input("What is the movie title? ")
        rating = int(input("What is the rating (integer): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print(f"Rating {rating} added for '{title}'")
    except Exception:
        print("error in updating movie rating")



def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    try:
        title = input("Enter the movie title to delete: ").strip()

        # Check if the movie exists
        response = table.get_item(Key={"Title": title})
        if "Item" not in response:
            print(f"Movie '{title}' not found in the database.")
            return

        # Delete the movie
        table.delete_item(Key={"Title": title})
        print(f"Movie '{title}' has been deleted.")

        # Optional: confirm deletion by listing remaining movies
        all_movies = table.scan().get('Items', [])
        print("\nCurrent movies in the database:")
        for movie in all_movies:
            print(movie["Title"])

    except Exception:
        print("Error deleting movie")

def query_movie():
    """
    Prompt the user for a movie title and print the average rating.
    Handles cases where the movie doesn't exist or has no ratings.
    """
    try:
        title = input("Enter the movie title to query: ").strip()
        response = table.get_item(Key={"Title": title})
        movie = response.get("Item")

        if not movie:
            print("movie not found")
            return

        ratings_list = movie.get("Ratings", [])
        if not ratings_list:
            print("movie has no ratings")
            return

        average = sum(ratings_list) / len(ratings_list)
        print(f"Average rating for '{title}' is {average:.2f}")

    except Exception:
        print("error querying movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
