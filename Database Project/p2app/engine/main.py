# p2app/engine/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

import sqlite3
import p2app.engine.continent
import p2app.engine.countries
import p2app.engine.region
import p2app.events.continents
import p2app.events.countries
import p2app.events.regions

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        pass


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.
        # Quit initiated
        if isinstance(event, p2app.events.app.QuitInitiatedEvent):
            yield self.quit_initiated_event()
        # Open database
        elif isinstance(event, p2app.events.database.OpenDatabaseEvent):
            p = event.path()
            if not str(p).endswith(".db") and not str(p).endswith(".sqlite"):
                yield p2app.events.database.DatabaseOpenFailedEvent(
                    "Invalid file type. Please use a .db or .sqlite file.")
                return
            try:
                self.conn = sqlite3.connect(p)
                yield p2app.events.database.DatabaseOpenedEvent(p)
            except Exception as e:
                yield p2app.events.database.DatabaseOpenFailedEvent(str(e))

            # Close Database
        elif isinstance(event, p2app.events.database.CloseDatabaseEvent):
            try:
                self.conn.close()
                yield p2app.events.database.DatabaseClosedEvent()
            except Exception as e:
                yield p2app.events.app.ErrorEvent(str(e))

            # CONTINENT
            # Search for continents
        elif isinstance(event, p2app.events.continents.StartContinentSearchEvent):
            yield from p2app.engine.continent.search_continents(self.conn, event)
            # Add Continent
        elif isinstance(event, p2app.events.continents.SaveNewContinentEvent):
            yield from p2app.engine.continent.add_continent(self.conn, event)
            # Update Continent
        elif isinstance(event, p2app.events.continents.SaveContinentEvent):
            yield p2app.engine.continent.update_continent(self.conn, event)
            # Load Continent
        elif isinstance(event, p2app.events.continents.LoadContinentEvent):
            yield p2app.engine.continent.load_continent(self.conn, event)

            # COUNTRY
            # Search for countries
        elif isinstance(event, p2app.events.countries.StartCountrySearchEvent):
            yield from p2app.engine.countries.search_country(self.conn, event)
            # Add Country
        elif isinstance(event, p2app.events.countries.SaveNewCountryEvent):
            yield from p2app.engine.countries.add_country(self.conn, event)
            # Update Country
        elif isinstance(event, p2app.events.countries.SaveCountryEvent):
            yield p2app.engine.countries.update_country(self.conn, event)
            # Load Country
        elif isinstance(event, p2app.events.countries.LoadCountryEvent):
            yield p2app.engine.countries.load_country(self.conn, event)

            # REGION
            # Search for Region
        elif isinstance(event, p2app.events.regions.StartRegionSearchEvent):
            yield from p2app.engine.region.search_region(self.conn, event)
            # Add Region
        elif isinstance(event, p2app.events.regions.SaveNewRegionEvent):
            yield from p2app.engine.region.add_region(self.conn, event)
            # Update Region
        elif isinstance(event, p2app.events.regions.SaveRegionEvent):
            yield p2app.engine.region.update_region(self.conn, event)
            #Load Region
        elif isinstance(event, p2app.events.regions.LoadRegionEvent):
            yield p2app.engine.region.load_region(self.conn, event)


    def quit_initiated_event(self):
        """A function to check if the user has quit the program"""
        return p2app.events.EndApplicationEvent()