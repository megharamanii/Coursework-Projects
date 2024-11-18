import p2app.events.regions as regions
import p2app.events.app as app


def search_region(conn, event):
    """A function to search for the region in the database"""
    cursor = conn.cursor()
    region_code = event.region_code()
    local_code = event.local_code()
    name = event.name()
    results = []

    try:
        if region_code and local_code and name:
            results = cursor.execute("SELECT * FROM region WHERE region_code = :1 AND local_code = :2 AND name = :3",
                                     (region_code, local_code, name)).fetchall()
        elif region_code and local_code:
            results = cursor.execute("SELECT * FROM region WHERE region_code = :1 AND local_code = :2",
                                     (region_code, local_code)).fetchall()
        elif region_code and name:
            results = cursor.execute("SELECT * FROM region WHERE region_code = :1 AND name = :2",
                                     (region_code, name)).fetchall()
        elif local_code and name:
            results = cursor.execute("SELECT * FROM region WHERE local_code = :1 AND name = :2",
                                     (local_code, name)).fetchall()
        elif region_code:
            results = cursor.execute("SELECT * FROM region WHERE region_code = ?", (region_code,)).fetchall()
        elif local_code:
            results = cursor.execute("SELECT * FROM region WHERE local_code = ?", (local_code,)).fetchall()
        elif name:
            results = cursor.execute("SELECT * FROM region WHERE name = ?", (name,)).fetchall()
        row = [regions.RegionSearchResultEvent(regions.Region(*result)) for result in results]
        yield from row
    except Exception as e:
        yield from app.ErrorEvent(f"Unexpected error has occurred, try again {e}")


def add_region(conn, event):
    """A function to add the region to the database"""
    cursor = conn.cursor()
    region = event.region()
    try:
        if region.region_code and region.local_code and region.name:
                # Check if continent_id exists in the database
                cursor.execute("SELECT COUNT(*) FROM continent WHERE continent_id = ?", (region.continent_id,))
                if cursor.fetchone()[0] == 0:
                    raise Exception("Continent id does not exist!")
                cursor.execute("SELECT COUNT(*) FROM country WHERE country_id = ?", (region.country_id,))
                if cursor.fetchone()[0] == 0:
                    raise Exception("Country id does not exist!")
                if region.wikipedia_link:
                    result = cursor.execute(
                        "INSERT INTO region (region_code, name, local_code, continent_id, country_id, wikipedia_link) "
                        "VALUES (?, ?, ?, ?, ?, ?)", (region.region_code, region.name, region.local_code,
                                                      region.continent_id, region.country_id, region.wikipedia_link))
                else:
                    result = cursor.execute(
                        "INSERT INTO region (region_code, name, local_code, continent_id, country_id, wikipedia_link) "
                        "VALUES (?, ?, ?, ?, ?, ?)", (region.region_code, region.name,
                                                      region.local_code, region.continent_id, region.country_id, ""))
                conn.commit()
                yield regions.SaveRegionEvent(result)
        else:
            raise Exception("Country id or Continent id does not exist!")
    except Exception as e:
        yield regions.SaveRegionFailedEvent(f"Something went wrong trying to insert!: {str(e)}")


def load_region(conn, event):
    """A function to load the region to the database"""
    cursor = conn.cursor()
    region_id = event.region_id()
    result = cursor.execute("SELECT * FROM region WHERE region_id = ?", (region_id,)).fetchone()
    return regions.RegionLoadedEvent(regions.Region(*result))


def update_region(conn, event):
    """A function to update the region in the database"""
    cursor = conn.cursor()
    region = event.region()
    cursor.execute("UPDATE region SET name =?, local_code=?, continent_id=?, country_id=?, wikipedia_link=?, region_code =? WHERE region_id = ?",
                   (region.name, region.local_code, region.continent_id, region.country_id, region.wikipedia_link,
                    region.region_code, region.region_id))
    conn.commit()
    return regions.RegionSavedEvent(region)
