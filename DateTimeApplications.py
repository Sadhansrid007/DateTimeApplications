from datetime import date, datetime, timedelta

def get_day_of_week(day, month, year):
    try:
        dt = date(year, month, day)
    except ValueError:
        return None
    return dt.strftime("%A")

def calculate_age(birth_day, birth_month, birth_year):
    try:
        born = date(birth_year, birth_month, birth_day)
    except ValueError:
        return None
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age

def parse_date(input_str):
    """Parse a date string in DD MM YYYY or DD-MM-YYYY or DD/MM/YYYY formats."""
    for fmt in ("%d %m %Y", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(input_str, fmt).date()
        except ValueError:
            continue
    return None

def parse_datetime(input_str):
    """Parse a date-time string in DD MM YYYY HH:MM or DD-MM-YYYY HH:MM or with seconds."""
    for fmt in ("%d %m %Y %H:%M:%S",
                "%d %m %Y %H:%M",
                "%d-%m-%Y %H:%M:%S",
                "%d-%m-%Y %H:%M",
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(input_str, fmt)
        except ValueError:
            continue
    return None

def countdown_to_event(target_dt):
    now = datetime.now()
    delta = target_dt - now
    if delta.total_seconds() < 0:
        return None
    days = delta.days
    secs = delta.seconds
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    seconds = secs % 60
    return days, hours, minutes, seconds

def main():
    while True:
        print("\nSelect option:")
        print("1. Day of week calculator")
        print("2. Age calculator")
        print("3. Countdown to future event")
        print("4. Exit")
        choice = input("Enter 1/2/3/4: ").strip()

        if choice == '1':
            s = input("Enter date (DD MM YYYY): ").strip()
            parts = s.replace("-", " ").replace("/", " ").split()
            if len(parts) != 3:
                print("Invalid format. Please use DD MM YYYY.")
                continue
            d, m, y = map(int, parts)
            dow = get_day_of_week(d, m, y)
            if dow:
                print("Day of week:", dow)
            else:
                print("Invalid date.")
        elif choice == '2':
            s = input("Enter birthdate (DD MM YYYY): ").strip()
            parts = s.replace("-", " ").replace("/", " ").split()
            if len(parts) != 3:
                print("Invalid format. Please use DD MM YYYY.")
                continue
            d, m, y = map(int, parts)
            age = calculate_age(d, m, y)
            if age is not None:
                print("Your age is:", age)
            else:
                print("Invalid birthdate.")
        elif choice == '3':
            s = input("Enter event date (DD MM YYYY) optionally with time (HH:MM or HH:MM:SS),\n"
                      "for example: 25 12 2025 18:30 or 25-12-2025 18:30:00\n> ").strip()
            dt = parse_datetime(s) or ( lambda: None )()
            if dt is None:
                # try date only
                d = parse_date(s)
                if d is None:
                    print("Invalid date/time. Please try again.")
                    continue
                # assume time 00:00 if not given
                dt = datetime(d.year, d.month, d.day, 0, 0, 0)

            result = countdown_to_event(dt)
            if result is None:
                print("That date/time is in the past!")
            else:
                days, hours, minutes, seconds = result
                print(f"Time until event: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
        elif choice == '4':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice — please enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()

