DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS OrderDetails;
DROP TABLE IF EXISTS ProductCategories;

CREATE TABLE IF NOT EXISTS Users (
    user_id BIGINT UNSIGNED PRIMARY KEY
    , first_name VARCHAR(50)
    , last_name VARCHAR(50)
    , email VARCHAR(100) UNIQUE
    , phone VARCHAR(15)
    , registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , loyalty_status VARCHAR(10) CHECK (loyalty_status IN ('Gold', 'Silver', 'Bronze', 'None'))
);
CREATE TABLE  IF NOT EXISTS Products (
    product_id BIGINT UNSIGNED PRIMARY KEY
    , name VARCHAR(255)
    , description TEXT
    , category_id BIGINT
    , price DECIMAL(10, 2) CHECK (price > 0)
    , stock_quantity INT CHECK (stock_quantity > 0 AND stock_quantity = 0)
    , creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id BIGINT UNSIGNED PRIMARY KEY
    , user_id BIGINT UNSIGNED
    , order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , total_amount DECIMAL(10, 2) CHECK (total_amount > 0)
    , status VARCHAR(20) CHECK (status IN ('Pending', 'Completed'))
    , delivery_date TIMESTAMP
    , FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS OrderDetails (
    order_detail_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    , order_id BIGINT UNSIGNED
    , product_id BIGINT UNSIGNED
    , quantity INT
    , price_per_unit DECIMAL(10, 2) CHECK (price_per_unit > 0)
    , total_price DECIMAL(10, 2) CHECK (total_price > 0)
    , FOREIGN KEY  (order_id) REFERENCES Orders(order_id)
    , FOREIGN KEY (product_id) REFERENCES Products(product_id)
);


CREATE TABLE IF NOT EXISTS ProductCategories (
    category_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    , name VARCHAR(100)
    , parent_category_id BIGINT UNSIGNED
    , FOREIGN KEY (parent_category_id) REFERENCES ProductCategories(category_id)
);