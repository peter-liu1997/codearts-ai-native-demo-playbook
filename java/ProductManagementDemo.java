import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Case 03: dependency-free reproduction of controller/service/repository layers. */
public class ProductManagementDemo {
    record Product(long id, String name, double price, int stock) {
        Product {
            if (name == null || name.isBlank()) throw new IllegalArgumentException("name is required");
            if (price < 0 || stock < 0) throw new IllegalArgumentException("price and stock must be non-negative");
        }
    }

    static final class ProductRepository {
        private final Map<Long, Product> store = new LinkedHashMap<>();
        private long nextId = 1;

        synchronized List<Product> findAll() { return new ArrayList<>(store.values()); }
        synchronized Optional<Product> findById(long id) { return Optional.ofNullable(store.get(id)); }
        synchronized Product save(String name, double price, int stock) {
            Product product = new Product(nextId++, name, price, stock);
            store.put(product.id(), product);
            return product;
        }
        synchronized boolean delete(long id) { return store.remove(id) != null; }
    }

    static final class ProductService {
        private final ProductRepository repository;
        ProductService(ProductRepository repository) { this.repository = repository; }
        List<Product> listProducts() { return repository.findAll(); }
        Optional<Product> getProduct(long id) { return repository.findById(id); }
        Product createProduct(String name, double price, int stock) { return repository.save(name, price, stock); }
        boolean deleteProduct(long id) { return repository.delete(id); }
    }

    static final class ProductController {
        private final ProductService service;
        ProductController(ProductService service) { this.service = service; }
        Map<String, Object> list() { return Map.of("success", true, "data", service.listProducts()); }
        Map<String, Object> find(long id) {
            Optional<Product> product = service.getProduct(id);
            Map<String, Object> response = new LinkedHashMap<>();
            response.put("success", product.isPresent());
            response.put("data", product.orElse(null));
            return response;
        }
        Map<String, Object> create(String name, double price, int stock) { return Map.of("success", true, "data", service.createProduct(name, price, stock)); }
        Map<String, Object> delete(long id) { return Map.of("success", service.deleteProduct(id)); }
    }

    static ProductController buildController() {
        return new ProductController(new ProductService(new ProductRepository()));
    }

    public static void main(String[] args) {
        ProductController controller = buildController();
        Map<String, Object> created = controller.create("AI 开发套件", 299.0, 12);
        if (!Boolean.TRUE.equals(created.get("success")) || ((List<?>) controller.list().get("data")).size() != 1) {
            throw new AssertionError("project-level CRUD failed");
        }
        System.out.println("PASS case 03: " + controller.list());
    }
}
