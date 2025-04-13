# Get birth month function
def get_birth_month():
    month_lookup = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    while True:
        user_input = input("Enter your birth month (1-12 or Jan-Dec): ").strip().lower()

        # Try converting to integer
        if user_input.isdigit():
            month_num = int(user_input)
            if 1 <= month_num <= 12:
                print(f"Valid input: Month number {month_num}")
                return month_num
            else:
                print("Please enter a number between 1 and 12.")
                
        # Try matching to 3-letter month
        elif user_input[:3] in month_lookup:
            month_num = month_lookup[user_input[:3]]
            print(f"Valid input: Month abbreviation '{user_input[:3].title()}' -> Month number {month_num}")
            return month_num
        
        else:
            print("Invalid input. Please enter a number (1–12) or the first three letters of a month (e.g., Jan, Feb, Mar).")