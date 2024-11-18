package labs.lab5;

public interface Ingestible {
	
	/**
	 * 
	 * @param player	the player who is ingesting the ingestible item
	 * @return			a string message describing what is being ingested and who is ingesting it
	 */
	String ingest(Player player);
}