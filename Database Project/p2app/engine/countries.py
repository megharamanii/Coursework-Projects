import p2app.events.countries as country_events

def search_country(conn, event):
    """A function to search for countries in the database"""
    cursor = conn.cursor()
    country_code = event.country_code()
    name = event.name()
    results = []
    if name:
        results = cursor.execute("SELECT * FROM country WHERE name = ?", (name,)).fetchall()
    elif country_code:
        results = cursor.execute("SELECT * FROM country WHERE country_code = ?", (country_code,)).fetchall()
    row = [country_events.CountrySearchResultEvent(country_events.Country(*result)) for result in results]
    yield from row


def add_country(conn, event):
    """A function to add a country to the database"""
    cursor = conn.cursor()
    countries = event.country()
    try:
        cursor.execute("SELECT 1 FROM continent WHERE continent_id = ?", (countries.continent_id,))
        continent_exists = cursor.fetchone()

        if continent_exists:
            if countries.country_code:
                if countries.wikipedia_link:
                    cursor.execute(
                        "INSERT INTO country (country_code, name, continent_id, wikipedia_link) "
                        "VALUES (?, ?, ?, ?)", (countries.country_code, countries.name,
                                                countries.continent_id, countries.wikipedia_link))
                else:
                    cursor.execute(
                        "INSERT INTO country (country_code, name, continent_id, wikipedia_link) "
                        "VALUES (?, ?, ?, ?)", (countries.country_code, countries.name,
                                                countries.continent_id, ""))
                conn.commit()
                country_id = cursor.lastrowid
                updated_country = countries._replace(country_id=country_id)
                yield country_events.CountrySavedEvent(updated_country)
            else:
                yield country_events.SaveCountryFailedEvent("Country code is required")
        else:
            yield country_events.SaveCountryFailedEvent("Invalid continent_id: does not exist in continent table")

    except Exception as e:
        yield country_events.SaveCountryFailedEvent("Something went wrong trying to insert!")


def load_country(conn, event):
    """A function to load the country to the database"""
    cursor = conn.cursor()
    country_id = event.country_id()
    result = cursor.execute("SELECT * FROM country WHERE country_id = ?", (country_id,)).fetchone()
    return country_events.CountryLoadedEvent(country_events.Country(*result))


def update_country(conn, event):
    """A function to update the country in the database"""
    cursor = conn.cursor()
    countries = event.country()
    if countries.country_code:
        if countries.wikipedia_link:
            cursor.execute("UPDATE country SET name = ?, continent_id = ?, country_code = ?, wikipedia_link= ? WHERE country_id = ?",
                  (countries.name, countries.continent_id, countries.country_code, countries.wikipedia_link,
                   countries.country_id))
        else:
            cursor.execute("UPDATE country SET name = ?, continent_id = ?, country_code = ?, wikipedia_link= ? WHERE country_id = ?",
                (countries.name, countries.continent_id, countries.country_code,"",countries.country_id))
        conn.commit()
    return country_events.CountrySavedEvent(countries)