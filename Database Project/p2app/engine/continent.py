import p2app.events.continents as continent_events

def search_continents(conn, event):
    """A function to search for continents in the database"""
    cursor = conn.cursor()
    continent_code = event.continent_code()
    name = event.name()
    if name:
        results = cursor.execute("SELECT * FROM continent WHERE name = ?", (name,)).fetchall()
    elif continent_code:
        results = cursor.execute("SELECT * FROM continent WHERE continent_code = ?", (continent_code,)).fetchall()
    else:
        results = []
    for result in results:
        continent = continent_events.Continent(result[0], result[1], result[2])
        yield continent_events.ContinentSearchResultEvent(continent)

def add_continent(conn, event):
    """A function to add a continent to the database"""
    cursor = conn.cursor()
    continent = event.continent()
    cursor.execute("INSERT INTO continent (continent_code, name) VALUES (?, ?)", (continent.continent_code,
                                                                                  continent.name))
    conn.commit()
    yield continent_events.ContinentSavedEvent(event.continent())


def load_continent(conn, event):
    """A function to load the continent to the database"""
    cursor = conn.cursor()
    continent_id = event.continent_id()
    results = cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (continent_id,)).fetchall()
    for result in results:
        continent = continent_events.Continent(result[0], result[1], result[2])
        return continent_events.ContinentLoadedEvent(continent)

def update_continent(conn, event):
    """A function to update the continent in the database"""
    cursor = conn.cursor()
    continent = event.continent()
    cursor.execute("UPDATE continent SET name=?, continent_code=? WHERE continent_id=?",
                   (continent.name, continent.continent_code, continent.continent_id))
    conn.commit()
    return continent_events.ContinentLoadedEvent(continent)
