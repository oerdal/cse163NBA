def format_year(year):
    start_year = str(year - 1)
    end_year = str(year)[-2:]
    fmt_year = start_year + '-' + end_year
    return fmt_year
