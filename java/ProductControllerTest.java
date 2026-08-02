import java.util.List;
import java.util.Map;

/** Case 04: generated controller tests without a third-party test runner. */
public class ProductControllerTest {
    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    public static void main(String[] args) {
        ProductManagementDemo.ProductController controller = ProductManagementDemo.buildController();
        Map<String, Object> created = controller.create("企业云沙箱", 599.0, 8);
        require(Boolean.TRUE.equals(created.get("success")), "create should succeed");
        require(((List<?>) controller.list().get("data")).size() == 1, "list should contain one product");
        require(Boolean.TRUE.equals(controller.find(1).get("success")), "find existing product");
        require(!Boolean.TRUE.equals(controller.find(999).get("success")), "missing product should not succeed");
        require(Boolean.TRUE.equals(controller.delete(1).get("success")), "delete existing product");
        require(((List<?>) controller.list().get("data")).isEmpty(), "list should be empty after delete");
        System.out.println("PASS case 04: 6 controller scenarios");
    }
}

