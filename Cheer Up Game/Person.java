package labs.lab5;

public abstract class Person implements Comparable<Person> {

	private String name;
	private int age;

	/**
	 * 
	 * @param name no validity checks necessary -- assume all valid input
	 * @param age  no validity checks necessary -- assume all valid input
	 */
	public Person(String name, int age) {
		this.name = name;
		this.age = age;
	}


	public String getName() {
		return name;
	}


	public int getAge() {
		return age;
	}


	/**
	 * compares first by name (use String.compareTo), then by age
	 */
	@Override
	public int compareTo(Person otherPerson) {
		int nameComparison = this.name.compareTo(otherPerson.name);
    if (nameComparison != 0) {
        return nameComparison; 
    }
    return Integer.compare(this.age, otherPerson.age);
}



	@Override
	public String toString() {
		return "Name: " + name + ", Age: " + age;
	}

}