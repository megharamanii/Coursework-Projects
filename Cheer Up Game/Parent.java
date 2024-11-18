package labs.lab5;

public class Parent extends Person implements Encourager {

	public Parent(String name, int age) {
		super(name, age);
	}


	@Override
	public String encourage() {
		return "Call on the phone | Say you're their favorite child";
	}

}