import java.util.LinkedHashMap;
import java.util.Map;

/** Case 02: equivalent imperative and Stream refactorings. */
public class InventoryRefactorDemo {
    private final Map<String, Integer> inventoryMap;
    private final Map<String, String> categoryMap;

    InventoryRefactorDemo(Map<String, Integer> inventoryMap, Map<String, String> categoryMap) {
        this.inventoryMap = inventoryMap;
        this.categoryMap = categoryMap;
    }

    int calculateCategoryInventory(String category) {
        if (inventoryMap == null || categoryMap == null || category == null) {
            return 0;
        }
        int total = 0;
        for (Map.Entry<String, Integer> entry : inventoryMap.entrySet()) {
            Integer inventory = entry.getValue();
            if (inventory != null && category.equals(categoryMap.get(entry.getKey()))) {
                total += inventory;
            }
        }
        return total;
    }

    int calculateCategoryInventoryStream(String category) {
        if (inventoryMap == null || categoryMap == null || category == null) {
            return 0;
        }
        return inventoryMap.entrySet().stream()
                .filter(entry -> entry.getValue() != null)
                .filter(entry -> category.equals(categoryMap.get(entry.getKey())))
                .mapToInt(Map.Entry::getValue)
                .sum();
    }

    public static void main(String[] args) {
        Map<String, Integer> inventory = new LinkedHashMap<>();
        inventory.put("P-1", 10);
        inventory.put("P-2", null);
        inventory.put("P-3", 7);
        Map<String, String> categories = Map.of("P-1", "book", "P-2", "book", "P-3", "tool");
        InventoryRefactorDemo demo = new InventoryRefactorDemo(inventory, categories);
        int imperative = demo.calculateCategoryInventory("book");
        int stream = demo.calculateCategoryInventoryStream("book");
        if (imperative != 10 || stream != imperative) {
            throw new AssertionError("refactoring changed business behavior");
        }
        System.out.println("PASS case 02: imperative=" + imperative + ", stream=" + stream);
    }
}

