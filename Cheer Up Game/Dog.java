package labs.lab5;
import java.util.Random;

public class Dog implements Encourager {

	public static final Random rand = new Random();
	@Override
	public String encourage() {
        return "Give wet sloppy kisses | Lay on your feet";
		
	}
}