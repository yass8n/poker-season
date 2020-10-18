import datetime

# Convert an integer into its ordinal representation::
#     make_ordinal(0)   => '0th'
#     make_ordinal(3)   => '3rd'
#     make_ordinal(122) => '122nd'
#     make_ordinal(213) => '213th'
def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

# convert a string of this format '%Y-%m-%d %H:%M:%S' into its date representation
def get_datetime_from_string(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')