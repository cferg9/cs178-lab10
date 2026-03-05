# Lab10.py
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Recipes')  # table name


# -------------------------------
# CREATE
# -------------------------------
def create_recipe():
    try:
        name = input("Enter recipe name: ").strip()
        cuisine = input("Enter cuisine type: ").strip()
        prep_time = input("Enter prep time (e.g., 30 mins): ").strip()

        table.put_item(
            Item={
                "Name": name,
                "Cuisine": cuisine,
                "Prep Time": prep_time  # <-- use exact attribute name
            }
        )
        print(f"Recipe '{name}' created successfully.")
    except:
        print("error in creating recipe")


# -------------------------------
# READ (all recipes)
# -------------------------------
def print_all_recipes():
    try:
        response = table.scan()
        items = response.get("Items", [])
        if not items:
            print("No recipes found.")
            return
        for recipe in items:
            print_recipe(recipe)
    except:
        print("error in reading recipes")


def print_recipe(recipe):
    print(f"Name: {recipe.get('Name')}")
    print(f"Cuisine: {recipe.get('Cuisine')}")
    print(f"Prep Time: {recipe.get('Prep Time')}")  # <-- exact attribute
    print()


# -------------------------------
# UPDATE
# -------------------------------
def update_recipe():
    try:
        name = input("Enter the name of the recipe to update: ").strip()
        cuisine = input("Enter new cuisine type: ").strip()
        prep_time = input("Enter new prep time: ").strip()

        table.update_item(
            Key={"Name": name},
            UpdateExpression="SET Cuisine = :c, #pt = :p",
            ExpressionAttributeNames={"#pt": "Prep Time"},  # <-- handle space
            ExpressionAttributeValues={
                ':c': cuisine,
                ':p': prep_time
            },
            ConditionExpression=Attr("Name").eq(name)  # ensure recipe exists
        )
        print(f"Recipe '{name}' updated successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("error: recipe does not exist")
        else:
            print("error in updating recipe")
    except:
        print("error in updating recipe")


# -------------------------------
# DELETE
# -------------------------------
def delete_recipe():
    try:
        name = input("Enter the name of the recipe to delete: ").strip()
        table.delete_item(
            Key={"Name": name},
            ConditionExpression=Attr("Name").eq(name)  # ensure recipe exists
        )
        print(f"Recipe '{name}' deleted successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("error: recipe does not exist")
        else:
            print("error in deleting recipe")
    except:
        print("error in deleting recipe")


# -------------------------------
# QUERY
# -------------------------------
def query_recipe():
    try:
        search_name = input("Enter the name to search for: ").strip()
        response = table.scan(
            FilterExpression=Attr("Name").contains(search_name)
        )
        items = response.get("Items", [])
        if not items:
            print(f"No recipes found matching '{search_name}'.")
            return
        for recipe in items:
            print_recipe(recipe)
    except:
        print("error in querying recipes")


# -------------------------------
# MAIN MENU
# -------------------------------
def main():
    while True:
        print("\nRecipe Menu:")
        print("1. Create recipe")
        print("2. Read all recipes")
        print("3. Update recipe")
        print("4. Delete recipe")
        print("5. Query recipe")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()
        if choice == '1':
            create_recipe()
        elif choice == '2':
            print_all_recipes()
        elif choice == '3':
            update_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == '5':
            query_recipe()
        elif choice == '6':
            print("Exiting recipe manager.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
