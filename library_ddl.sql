CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- *********** CREATING TABLES HERE ***********
CREATE TABLE Patron (
    patron_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    member_date DATE NOT NULL
);

CREATE TABLE Room (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_no INT NOT NULL,
    room_name VARCHAR(100) NOT NULL,
    room_type VARCHAR(50),
    capacity INT,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Reservation (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    patron_id INT NOT NULL,
    room_id INT NOT NULL,
    reservation_date DATE,
    reservation_type VARCHAR(50),
    reservation_status VARCHAR(50),
    start_time TIME,
    end_time TIME,
	FOREIGN KEY (patron_id) REFERENCES Patron(patron_id) ON DELETE CASCADE,
	FOREIGN KEY (room_id) REFERENCES Room(room_id)
);

CREATE TABLE SchoolEvent (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(50),
    event_date DATE,
    start_time TIME,
    end_time TIME,
	FOREIGN KEY (room_id) REFERENCES Room(room_id)
);

CREATE TABLE Registration (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    patron_id INT NOT NULL,
    event_id INT NOT NULL,
    reg_date DATE,
    reg_status VARCHAR(50),
	FOREIGN KEY (patron_id) REFERENCES Patron(patron_id) ON DELETE CASCADE,
	FOREIGN KEY (event_id) REFERENCES SchoolEvent(event_id),
    UNIQUE (patron_id, event_id)
);

CREATE TABLE Fee (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    patron_id INT NOT NULL,
    fee_type VARCHAR(50),
    amount DECIMAL(10,2) NOT NULL,
    fee_date DATE,
    pay_status VARCHAR(50),
	FOREIGN KEY (patron_id) REFERENCES Patron(patron_id) ON DELETE CASCADE
);

CREATE TABLE Material (
	material_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    blurb VARCHAR(250),
    material_type VARCHAR(50),
    genre VARCHAR(50),
    publish_date DATE,
    availability VARCHAR(50) CHECK (availability IN ('checked out', 'available'))
);

CREATE TABLE Checkouts (
	due_date DATE,
    return_date DATE,
    checkout_date DATE,
    patron_id INT NOT NULL,
    material_id INT NOT NULL,
	PRIMARY KEY (patron_id, material_id, checkout_date),
    FOREIGN KEY (patron_id) REFERENCES Patron(patron_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    CHECK (return_date >= checkout_date),
    CHECK (due_date > checkout_date)
);

CREATE TABLE CheckoutRequest (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    request_date DATE NOT NULL,
    request_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    patron_id INT NOT NULL,
    material_id INT NOT NULL,
    FOREIGN KEY (patron_id) REFERENCES Patron(patron_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    CHECK (request_status IN ('pending', 'accepted', 'denied'))
);

CREATE TABLE Author (
	author_id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE Director (
	director_id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE Book (
    author_id INT NOT NULL,
    page_count INT,
    isbn BIGINT PRIMARY KEY,
    publisher VARCHAR(100),
    FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

CREATE TABLE Book_ISBN_Connector (
	material_id INT NOT NULL PRIMARY KEY,
    isbn BIGINT,
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    FOREIGN KEY (isbn) REFERENCES Book(isbn)
);

CREATE TABLE Film (
    imdb_id VARCHAR(50) NOT NULL PRIMARY KEY,
    director_id INT NOT NULL,
    film_length INT,
    studio VARCHAR(100),
    rating VARCHAR(50),
    film_format VARCHAR(50),
    FOREIGN KEY (director_id) REFERENCES Director(director_id)
);

CREATE TABLE Film_Connector (
	material_id INT NOT NULL PRIMARY KEY,
    imdb_id VARCHAR(50),
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    FOREIGN KEY (imdb_id) REFERENCES Film(imdb_id)
);

CREATE TABLE Role(
	roleID INT AUTO_INCREMENT PRIMARY KEY,
    roleName VARCHAR(50) NOT NULL UNIQUE,
    hourlyRate DECIMAL(6, 2) NOT NULL CHECK (hourlyRate >= 0)
);

CREATE TABLE Staff(
	staffID INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    roleID INT NOT NULL,
    FOREIGN KEY (roleID) REFERENCES Role(roleID)
);

CREATE TABLE Category(
	categoryID INT AUTO_INCREMENT PRIMARY KEY,
    categoryName VARCHAR(50) NOT NULL UNIQUE,
    reorderNum INT NOT NULL CHECK(reorderNum >= 0)
);

CREATE TABLE CafeItem (
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(100) NOT NULL,
    itemCost DECIMAL(6,2) NOT NULL CHECK (itemCost >= 0),
    itemPrice DECIMAL(6,2) NOT NULL CHECK (itemPrice >= 0),
    categoryID INT NOT NULL,
    inStock INT NOT NULL CHECK (inStock >= 0),
    FOREIGN KEY (categoryID) REFERENCES Category (categoryID)
);

CREATE TABLE CafeOrder (
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    orderDate DATE NOT NULL,
    orderPayment ENUM('paid', 'unpaid') NOT NULL,
    patron_id INT NOT NULL,
    staffID INT NOT NULL,
    FOREIGN KEY (patron_id) REFERENCES Patron(patron_id) ON DELETE CASCADE,
    FOREIGN KEY (staffID) REFERENCES Staff(staffID)
);

CREATE TABLE OrderItem (
    orderID INT NOT NULL,
    itemID INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (orderID, itemID),
    FOREIGN KEY (orderID) REFERENCES CafeOrder(orderID) ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES CafeItem(itemID)
);

CREATE TABLE Availability (
    availableID INT AUTO_INCREMENT PRIMARY KEY,
    staffID INT NOT NULL,
    dayOfWeek ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
    startTime TIME NOT NULL,
    endTime TIME NOT NULL,
    CHECK (startTime < endTime),
    FOREIGN KEY (staffID) REFERENCES Staff(staffID)
);

CREATE TABLE Shift (
    shiftID INT AUTO_INCREMENT PRIMARY KEY,
    staffID INT NOT NULL,
    shiftDate DATE NOT NULL,
    startTime TIME NOT NULL,
    endTime TIME NOT NULL,
    CHECK (startTime < endTime),
    FOREIGN KEY (staffID) REFERENCES Staff(staffID)
);

-- *********** ADDING TRIGGERS HERE ***********
DELIMITER |

CREATE TRIGGER prevent_checkout_of_unavailable_materials
BEFORE INSERT ON Checkouts
FOR EACH ROW
BEGIN
	IF (SELECT availability FROM Material WHERE material_id = NEW.material_id) = 'checked out' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'You cannot check out a material that is already checked out.';
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE TRIGGER sync_material_checkouts
AFTER INSERT ON Checkouts
FOR EACH ROW
BEGIN
	IF NEW.return_date IS NULL THEN
		UPDATE Material
		SET availability = 'checked out'
		WHERE material_id = NEW.material_id;
	END IF;
END |

DELIMITER ;

DELIMITER |

CREATE TRIGGER sync_material_returns
AFTER UPDATE ON Checkouts
FOR EACH ROW
BEGIN
	IF NEW.return_date IS NOT NULL THEN
		UPDATE Material
        SET availability = 'available'
        WHERE material_id = NEW.material_id;
	END IF;
END |


DELIMITER $$

CREATE TRIGGER handle_inventory_on_order
BEFORE INSERT ON OrderItem
FOR EACH ROW
BEGIN
    DECLARE currentStock INT;

    -- Get current stock
    SELECT inStock
    INTO currentStock
    FROM CafeItem
    WHERE itemID = NEW.itemID;

    -- If not enough stock, force a CHECK constraint failure
    IF currentStock < NEW.quantity THEN
        SET NEW.quantity = -1;
    ELSE
        -- Otherwise, reduce inventory
        UPDATE CafeItem
        SET inStock = inStock - NEW.quantity
        WHERE itemID = NEW.itemID;
    END IF;
END $$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER prevent_overlapping_reservations
BEFORE INSERT ON Reservation
FOR EACH ROW
BEGIN

    IF EXISTS (
        SELECT 1
        FROM Reservation
        WHERE room_id = NEW.room_id
          AND reservation_date = NEW.reservation_date
          AND start_time < NEW.end_time
          AND NEW.start_time < end_time
    ) THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'You can not have multiple reservations for the same room at same time and day.';

    END IF;
END $$

DELIMITER ;

-- *********** ADDING VIEWS HERE ***********
CREATE VIEW Patron_Material_View AS
SELECT
    material_type,
    title,
    genre,
    availability
FROM Material;

CREATE VIEW Patron_Reservation_View AS
SELECT
    p.patron_id,
    rm.room_no,
    r.reservation_date,
    r.start_time,
    r.end_time,
    r.reservation_type,
    r.reservation_status
FROM Reservation r
JOIN Patron p
    ON r.patron_id = p.patron_id
JOIN Room rm
    ON r.room_id = rm.room_id;

-- *********** ADDING FUNCTION HERE ***********

DELIMITER $$

CREATE FUNCTION get_unpaid_fee_total(input_patron_id INT)
RETURNS DECIMAL(10,2)
READS SQL DATA
BEGIN
    DECLARE total_unpaid DECIMAL(10,2);

    SELECT SUM(amount)
    INTO total_unpaid
    FROM Fee
    WHERE patron_id = input_patron_id
      AND LOWER(pay_status) = 'unpaid';

    RETURN total_unpaid;
END $$

DELIMITER ;

-- *********** ADDING PROCEDURE HERE ***********
DELIMITER $$

CREATE PROCEDURE apply_late_fees()
BEGIN
    INSERT INTO Fee (patron_id, fee_type, amount, fee_date, pay_status)
    SELECT
        c.patron_id,
        'Late Fee',
        5.00,
        CURDATE(),
        'unpaid'
    FROM Checkouts c
    WHERE c.return_date IS NULL
      AND c.due_date < CURDATE();
END $$

DELIMITER ;
