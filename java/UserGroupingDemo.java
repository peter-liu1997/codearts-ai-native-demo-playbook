import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Case 01: code continuation from a natural-language method contract. */
public class UserGroupingDemo {
    record User(String name, Integer age) {}

    static Map<Integer, List<User>> groupUsersByAge(List<User> users) {
        if (users == null || users.isEmpty()) {
            return Collections.emptyMap();
        }
        Map<Integer, List<User>> grouped = new LinkedHashMap<>();
        for (User user : users) {
            if (user == null || user.age() == null || user.age() < 0) {
                continue;
            }
            grouped.computeIfAbsent(user.age(), ignored -> new ArrayList<>()).add(user);
        }
        return grouped;
    }

    public static void main(String[] args) {
        List<User> users = new ArrayList<>();
        users.add(new User("Alice", 28));
        users.add(null);
        users.add(new User("Bob", -1));
        users.add(new User("Carol", 28));
        users.add(new User("Dave", 35));
        Map<Integer, List<User>> grouped = groupUsersByAge(users);
        if (grouped.size() != 2 || grouped.get(28).size() != 2 || grouped.containsKey(-1)) {
            throw new AssertionError("groupUsersByAge contract failed");
        }
        System.out.println("PASS case 01: " + grouped);
    }
}

