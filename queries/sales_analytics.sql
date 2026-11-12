-- 1. TOTAL CUSTOMERS
SELECT COUNT(*) AS total_customers
FROM customers;


-- 2. TOTAL PRODUCTS
SELECT COUNT(*) AS total_products
FROM products;


-- 3. TOTAL ORDERS
SELECT COUNT(*) AS total_orders
FROM orders;


-- 4. ORDER STATUS ANALYSIS
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status;


-- 5. TOTAL REVENUE
SELECT
    ROUND(SUM(oi.quantity * p.price), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed';


-- 6. MONTHLY REVENUE
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    ROUND(SUM(oi.quantity * p.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed'
GROUP BY month
ORDER BY month;


-- 7. TOP 5 SELLING PRODUCTS
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.product_id
ORDER BY units_sold DESC
LIMIT 5;


-- 8. REVENUE BY PRODUCT
SELECT
    p.product_name,
    SUM(oi.quantity * p.price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.product_id
ORDER BY revenue DESC;


-- 9. REVENUE BY CATEGORY
SELECT
    p.category,
    SUM(oi.quantity * p.price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- 10. TOP CUSTOMERS
SELECT
    c.customer_name,
    c.city,
    SUM(oi.quantity * p.price) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed'
GROUP BY c.customer_id
ORDER BY total_spending DESC
LIMIT 5;


-- 11. REVENUE BY CITY
SELECT
    c.city,
    SUM(oi.quantity * p.price) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed'
GROUP BY c.city
ORDER BY revenue DESC;


-- 12. PAYMENT METHOD ANALYSIS
SELECT
    payment_method,
    COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'Completed'
GROUP BY payment_method;


-- 13. AVERAGE ORDER VALUE
SELECT
    ROUND(AVG(order_total), 2) AS average_order_value
FROM (
    SELECT
        o.order_id,
        SUM(oi.quantity * p.price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.order_id
);


-- 14. REPEAT CUSTOMERS
SELECT
    c.customer_name,
    COUNT(o.order_id) AS completed_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Completed'
GROUP BY c.customer_id
HAVING COUNT(o.order_id) > 1;


-- 15. PRODUCTS NEVER SOLD
SELECT
    p.product_name
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE oi.product_id = p.product_id
    AND o.order_status = 'Completed'
);


-- 16. REVENUE CONTRIBUTION BY CATEGORY
WITH category_sales AS (
    SELECT
        p.category,
        SUM(oi.quantity * p.price) AS revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY p.category
)

SELECT
    category,
    revenue,
    ROUND(
        revenue * 100.0 / SUM(revenue) OVER (),
        2
    ) AS revenue_percentage
FROM category_sales
ORDER BY revenue DESC;