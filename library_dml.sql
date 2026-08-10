USE LibraryDB;

-- *********** ADDING TUPLES FOR EACH RELATION HERE ***********
INSERT INTO Patron (patron_id, first_name, last_name, email, member_date) VALUES
(1, 'Ella', 'Potter', 'ella@email.com', '2026-04-01'),
(2, 'Wes', 'Phipps', 'wes@email.com', '2026-03-28'),
(3, 'Jaley', 'Grimm', 'jaley@email.com', '2026-02-10'),
(4, 'David', 'Lee', 'david.lee@email.com', '2026-01-20'),
(5, 'Emily', 'Clark', 'emily.clark@email.com', '2025-01-22'),
(6, 'Noah', 'Smith', 'noah.smith@email.com', '2024-01-25');


INSERT INTO Room (room_id, room_no, room_name, room_type, capacity, available) VALUES
(1, 100, 'Study Room A', 'Study', 4, TRUE),
(2, 102, 'Study Room B', 'Study', 6, TRUE),
(3, 300, 'Conference Room', 'Event', 50, TRUE),
(4, 15, 'Computer Lab', 'Lab', 25, TRUE),
(5, 201, 'Media Room', 'Media', 12, TRUE),
(6, 401, 'Class Room', 'Class', 30, TRUE),
(7, 403, 'Class Room', 'Class', 30, TRUE);


INSERT INTO SchoolEvent (event_id, room_id, event_name, event_type, event_date, start_time, end_time) VALUES
(1, 3, 'Spring Fair', 'Community', '2026-04-10', '10:00:00', '14:00:00'),
(2, 5, 'Film Discussion Night', 'Club', '2026-04-12', '18:00:00', '20:00:00'),
(3, 4, 'Coding Workshop', 'Educational', '2026-04-15', '15:00:00', '17:00:00'),
(4, 3, 'Poetry Reading', 'Literary', '2026-04-18', '17:30:00', '19:00:00'),
(5, 1, 'Study Session', 'Academic', '2026-04-20', '13:00:00', '14:30:00'),
(6, 6, 'Math 100', 'Class', '2026-04-21', '13:00:00', '14:15:00'),
(7, 7, 'Biology 300', 'Class', '2026-04-21', '13:00:00', '14:15:00');


INSERT INTO Reservation (reservation_id, patron_id, room_id, reservation_date, reservation_type, reservation_status, start_time, end_time) VALUES
(1, 1, 1, '2026-04-05', 'Study', 'Confirmed', '09:00:00', '11:00:00'),
(2, 2, 2, '2026-04-05', 'Group Study', 'Confirmed', '13:00:00', '15:00:00'),
(3, 3, 5, '2026-04-06', 'Media Use', 'Pending', '16:00:00', '18:00:00'),
(4, 4, 1, '2026-04-07', 'Tutoring Session', 'Confirmed', '10:00:00', '12:00:00'),
(5, 5, 3, '2026-04-08', 'Presentation Practice', 'Cancelled', '14:00:00', '16:00:00'),
(6, 6, 2, '2026-04-09', 'Study', 'Confirmed', '11:00:00', '12:30:00'),
(7, 1, 1, '2026-05-05', 'Study', 'Confirmed', '09:00:00', '10:30:00'),
(8, 1, 5, '2026-05-12', 'Media Use', 'Confirmed', '14:00:00', '16:00:00');


INSERT INTO Registration (reg_id, patron_id, event_id, reg_date, reg_status) VALUES
(1, 1, 1, '2026-04-01', 'Registered'),
(2, 2, 1, '2026-04-01', 'Registered'),
(3, 3, 2, '2026-04-02', 'Registered'),
(4, 4, 3, '2026-04-03', 'Waitlisted'),
(5, 5, 4, '2026-04-04', 'Registered'),
(6, 6, 5, '2026-04-05', 'Registered'),
(7, 1, 3, '2026-04-05', 'Registered'),
(8, 2, 4, '2026-04-06', 'Cancelled');


INSERT INTO Fee (fee_id, patron_id, fee_type, amount, fee_date, pay_status) VALUES
(1, 1, 'Late Fee', 5.00, '2026-03-28', 'Paid'),
(2, 2, 'Damage Fee', 15.00, '2026-03-30', 'Unpaid'),
(3, 3, 'Late Fee', 2.50, '2026-04-01', 'Paid'),
(4, 4, 'Late Fee', 7.00, '2026-04-02', 'Unpaid'),
(5, 5, 'Replacement Fee', 10.00, '2026-04-03', 'Paid'),
(6, 6, 'Replacement Fee', 25.00, '2026-04-04', 'Unpaid'),
(10, 1, 'Late Fee', 5.00, '2026-04-22', 'Unpaid'),
(11, 1, 'Damage Fee', 12.50, '2026-04-25', 'Unpaid');

INSERT INTO Material (material_id, title, blurb, material_type, genre, publish_date, availability) VALUES
(1, 'Just Mercy', 'Bryan Stevenson advocates as a lawyer through the Equal Justice Initiative for restorative justice', 'book', 'memoir', '2014-10-21', 'available'),
(2, 'And Then There Were None', 'Ten strangers trapped on an island must uncover a murderer as more and more of them are killed', 'book', 'mystery', '2004-05-03', 'available'),
(3, 'The House on Mango Street', 'The story of Esperanza Cordero as she grows up in a neightborhood in Chicago', 'book', 'realistic fiction', '2009-04-03', 'available'),
(4, 'The Hunger Games', 'Katniss Everdeen and her struggle to survive the Hunger Games after volunteering to save her sister', 'book', 'dystopian', '2008-10-14', 'available'),
(5, 'The Hunger Games', 'Katniss Everdeen and her struggle to survive the Hunger Games after volunteering to save her sister', 'book', 'dystopian', '2008-10-14', 'available'),
(6, 'Fences', 'Troy Maxson and his struggles with discrimination, family relationships, and his past are the focus of this play set in Pittsburgh', 'book', 'play', '1986-06-01', 'available'),
(7, 'The Wizard of Oz', 'Dorothy and Toto journey to Oz in order to find their way back home', 'film', 'fantasy', '1939-08-25', 'available'),
(8, 'The Martian', 'Mark Watney must survive on Mars after being left behind during an expedition', 'film', 'sci fi', '2015-10-02', 'available'),
(9, 'The Matrix', 'Thomas Anderson joins a rebellion to save humanity from the machines', 'film', 'sci fi', '1999-03-31', 'available'),
(10, 'The Dark Knight', 'Batman attempts to save Gotham from the Joker', 'film', 'superhero', '2008-07-18', 'available'),
(11, 'Challengers', 'Tashi, Art, and Patrick navigate changing relationship dynamics over the course of their tennis careers', 'film', 'sports', '2024-04-26', 'available'),
(12, 'Challengers', 'Tashi, Art, and Patrick navigate changing relationship dynamics over the course of their tennis careers', 'film', 'sports', '2024-04-26', 'available');


INSERT INTO Checkouts (due_date, return_date, checkout_date, patron_id, material_id) VALUES
('2026-07-01', NULL, '2026-04-01', 1, 3),
('2026-04-10', NULL, '2026-03-10', 3, 9),
('2023-02-01', '2023-01-20', '2023-01-01', 1, 4),
('2025-10-25', '2025-10-25', '2025-09-25', 1, 6),
('2025-10-25', '2025-10-25', '2025-09-25', 1, 2),
('2026-07-01', NULL, '2026-04-01', 1, 1),
('2026-06-11', NULL, '2026-04-11', 2, 5);

INSERT INTO Author (author_id, first_name, last_name) VALUES
(1, 'Bryan', 'Stevenson'),
(2, 'Agatha', 'Christie'),
(3, 'Sandra', 'Cisneros'),
(4, 'Suzanne', 'Collins'),
(5, 'August', 'Wilson');

INSERT INTO Book (isbn, author_id, page_count, publisher) VALUES
(9780812984965, 1, 336, 'One World'),
(9780062073471, 2, 264, 'Harper Collins'),
(9780558644994, 3, 110, 'Knopf Doubleday Publishing Group'),
(9780545425117, 4, 374, 'Scholastic Press'),
(9780452264014, 5, 101, 'Plume');

INSERT INTO Book_ISBN_Connector(material_id, isbn) VALUES
(1, 9780812984965),
(2, 9780062073471),
(3, 9780558644994),
(4, 9780545425117),
(5, 9780545425117),
(6, 9780452264014);

INSERT INTO Director (director_id, first_name, last_name) VALUES
(1, 'Victor', 'Fleming'),
(2, 'Ridley', 'Scott'),
(3, 'Lana and Lilly', 'Wachowski'),
(5, 'Christopher', 'Nolan'),
(6, 'Luca', 'Guadagnino');

INSERT INTO Film (imdb_id, director_id, film_length, studio, rating, film_format) VALUES
('tt0032138', 1, 102, 'Metro-Goldwyn-Mayer', 'G', 'VHS'),
('tt3659388', 2, 141, '20th Century Fox', 'PG-13', 'DVD'),
('tt0133093', 3, 136, 'Warner Bros', 'R', 'DVD'),
('tt0468569', 5, 152, 'Warner Bros', 'PG-13', 'DVD'),
('tt16426418', 6, 131, 'Amazon MGM Studios', 'R', 'Blu-ray');

INSERT INTO Film_Connector (material_id, imdb_id) VALUES
(7, 'tt0032138'),
(8, 'tt3659388'),
(9, 'tt0133093'),
(10, 'tt0468569'),
(11, 'tt16426418'),
(12, 'tt16426418');

INSERT INTO Role (roleID, roleName, hourlyRate) VALUES
(1, 'Supervisor', 20.00),
(2, 'Manager', 18.50),
(3, 'Barista', 16.50),
(4, 'Cashier', 15.50),
(5, 'Librarian', 17.50);

INSERT INTO Staff (staffID, firstname, lastname, email, roleID) VALUES
(1, 'Alice', 'Smith', 'asmith@library.edu', 3),
(2, 'Ethan', 'Johnson', 'ejohnson@gmails.com', 4),
(3, 'Mildred', 'Brown', 'mbrown@library.edu', 5),
(4, 'Bill', 'White', 'bwhite@outlook.org', 1),
(5, 'Sarah', 'Nguyen', 'snguyen@msn.com', 2);

INSERT INTO Category(categoryID, categoryName, reorderNum) VALUES
(1, 'Hot Drink', 10),
(2, 'Cold Drink', 5),
(3, 'Pastry', 20),
(4, 'Snack', 13),
(5, 'Sandwich', 15);

INSERT INTO CafeItem (itemID, itemName, itemCost, itemPrice, categoryID, inStock) VALUES
(1, 'Hot Chocolate', 0.75, 2.50, 1, 40),
(2, 'Iced Latte', 1.00, 3.50, 2, 30),
(3, 'Blueberry Muffin', 1.25, 3.00, 3, 12),
(4, 'Ham Sandwich', 2.50, 5.50, 5, 30),
(5, 'Potato Chips', 1.50, 3.00, 4, 25);

INSERT INTO Availability (availableID, staffID, dayOfWeek, startTime, endTime) VALUES
(1, 1, 'Monday', '07:00:00', '15:00:00'),
(2, 2, 'Tuesday', '10:00:00', '18:00:00'),
(3, 3, 'Sunday', '08:00:00', '12:00:00'),
(4, 4, 'Friday', '06:00:00', '13:00:00'),
(5, 5, 'Wednesday', '07:00:00', '18:00:00');

INSERT INTO Shift (shiftID, staffID, shiftDate, startTime, endTime) VALUES
(1, 1, '2026-04-20', '08:00:00', '12:00:00'),
(2, 2, '2026-04-14', '08:00:00', '12:00:00'),
(3, 3, '2026-04-18', '10:00:00', '12:00:00'),
(4, 4, '2026-04-17', '08:00:00', '13:00:00'),
(5, 5, '2026-04-15', '08:00:00', '15:00:00');

INSERT INTO CafeOrder (orderID, orderDate, orderPayment, patron_id, staffID) VALUES
(1, '2026-04-13', 'paid', 1, 1),
(2, '2026-03-13', 'unpaid', 4, 2),
(3, '2026-04-10', 'paid', 3, 1),
(4, '2026-04-02', 'unpaid', 2, 5),
(5, '2026-03-23', 'paid', 3, 4);

INSERT INTO OrderItem (orderID, itemID, quantity) VALUES
(1, 1, 1),
(1, 3, 2),
(2, 4, 1),
(2, 1, 1),
(3, 5, 3);

-- *********** SELECT STATEMENTS TO DISPLAY EACH TABLE HERE ***********
SELECT * FROM Patron;
SELECT * FROM Room;
SELECT * FROM SchoolEvent;
SELECT * FROM Reservation;
SELECT * FROM Registration;
SELECT * FROM Fee;
SELECT * FROM Material;
SELECT * FROM Checkouts;
SELECT * FROM Author;
SELECT * FROM Book;
SELECT * FROM Book_ISBN_Connector;
SELECT * FROM Director;
SELECT * FROM Film;
SELECT * FROM Film_Connector;
SELECT * FROM Role;
SELECT * FROM Staff;
SELECT * FROM Category;
SELECT * FROM CafeItem;
SELECT * FROM Availability;
SELECT * FROM Shift;
SELECT * FROM CafeOrder;
SELECT * FROM OrderItem;

-- *********** QUERIES THAT MEET THE DELIVERABLE 5 REQUIREMENTS ***********

-- Search library books by book title (join)
SELECT m.title, a.first_name, a.last_name, m.genre, b.publisher, m.publish_date, b.page_count, b.isbn, m.availability, m.blurb
FROM Book b
JOIN Book_ISBN_Connector bc on b.isbn = bc.isbn
JOIN Material m on m.material_id = bc.material_id
JOIN Author a on b.author_id = a.author_id
WHERE m.title = "The Hunger Games";

-- Find names and email addresses and patron_ids of all patrons with checked out books using a subquery (subquery)
SELECT DISTINCT c.patron_id, p.first_name, p.last_name, p.email
FROM Checkouts c
JOIN  Patron p on c.patron_id = p.patron_id
WHERE c.return_date IS NULL
AND c.material_id IN (SELECT m.material_id FROM  Material m WHERE m.availability = 'checked out');

-- Counts Checked Out Materials (aggregate & join)
SELECT COUNT(*) AS num_checked_out
FROM Checkouts c
JOIN Material m ON c.material_id = m.material_id
WHERE c.return_date IS NULL;

-- View Unpaid Fees of Patrons(aggregate & join)
SELECT p.patron_id, p.first_name, p.last_name, p.email, COUNT(f.fee_id) AS number_of_unpaid_fees, SUM(f.amount) AS total_unpaid_fees
FROM Patron p
JOIN Fee f
    ON p.patron_id = f.patron_id
WHERE LOWER(f.pay_status) = 'unpaid'
GROUP BY p.patron_id, p.first_name, p.last_name, p.email
ORDER BY total_unpaid_fees DESC;

-- view upcoming reservations (view)
SELECT patron_id, room_no, reservation_date, start_time, end_time, reservation_type, reservation_status
FROM Patron_Reservation_View
WHERE patron_id = 1
  AND (
        reservation_date > CURDATE()
        OR (
            reservation_date = CURDATE()
            AND start_time >= CURTIME()
        )
      )
ORDER BY reservation_date, start_time;

-- *********** OTHER (EXTRA) QUERIES HERE ***********

-- View reservations with patron and room names
SELECT
    r.reservation_id,
    p.first_name,
    p.last_name,
    rm.room_name,
    r.reservation_date,
    r.reservation_type,
    r.reservation_status,
    r.start_time,
    r.end_time
FROM Reservation r
JOIN Patron p ON r.patron_id = p.patron_id
JOIN Room rm ON r.room_id = rm.room_id;

-- View event registrations with patron and event info
SELECT
    reg.reg_id,
    p.first_name,
    p.last_name,
    e.event_name,
    e.event_type,
    e.event_date,
    reg.reg_status
FROM Registration reg
JOIN Patron p ON reg.patron_id = p.patron_id
JOIN SchoolEvent e ON reg.event_id = e.event_id;

-- View fees owed by patrons
SELECT
    f.fee_id,
    p.first_name,
    p.last_name,
    f.fee_type,
    f.amount,
    f.fee_date,
    f.pay_status
FROM Fee f
JOIN Patron p ON f.patron_id = p.patron_id;

-- View book information in library collection including author info
SELECT m.title, a.first_name, a.last_name, m.genre, b.publisher, m.publish_date, b.page_count, b.isbn, m.availability, m.blurb
FROM Book b
JOIN Book_ISBN_Connector bc on b.isbn = bc.isbn
JOIN Material m on m.material_id = bc.material_id
JOIN Author a on b.author_id = a.author_id;

-- View film information in library collection including film info
SELECT m.title, d.first_name, d.last_name, f.film_length, m.genre, f.studio, m.publish_date, f.rating, f.film_format, m. availability, m.blurb
FROM Film f
JOIN Film_Connector fc on f.imdb_id = fc.imdb_id
JOIN Material m on m.material_id = fc.material_id
JOIN Director d on d.director_id = f.director_id;

-- View all available films in the library collection
SELECT m.title, d.first_name, d.last_name, f.film_length, m.genre, f.studio, m.publish_date, f.rating, f.film_format, m. availability, m.blurb
FROM Film f
JOIN Film_Connector fc on f.imdb_id = fc.imdb_id
JOIN Material m on m.material_id = fc.material_id
JOIN Director d on d.director_id = f.director_id
WHERE m.availability = 'available';

-- View all available books in the library collection
SELECT m.title, a.first_name, a.last_name, m.genre, b.publisher, m.publish_date, b.page_count, b.isbn, m.availability, m.blurb
FROM Book b
JOIN Book_ISBN_Connector bc on b.isbn = bc.isbn
JOIN Material m on m.material_id = bc.material_id
JOIN Author a on b.author_id = a.author_id
WHERE m.availability = 'available';

-- View all checked out films in the library collection
SELECT m.title, d.first_name, d.last_name, f.film_length, m.genre, f.studio, m.publish_date, f.rating, f.film_format, m. availability, m.blurb
FROM Film f
JOIN Film_Connector fc on f.imdb_id = fc.imdb_id
JOIN Material m on m.material_id = fc.material_id
JOIN Director d on d.director_id = f.director_id
WHERE m.availability = 'checked out';

-- View all checked out books in the library collection
SELECT m.title, a.first_name, a.last_name, m.genre, b.publisher, m.publish_date, b.page_count, b.isbn, m.availability, m.blurb
FROM Book b
JOIN Book_ISBN_Connector bc on b.isbn = bc.isbn
JOIN Material m on m.material_id = bc.material_id
JOIN Author a on b.author_id = a.author_id
WHERE m.availability = 'checked out';

-- View cafe orders with totals and payment status
SELECT
    co.orderID,
    co.orderDate,
    CONCAT(p.first_name, ' ', p.last_name) AS patron,
    CONCAT(s.firstname, ' ', s.lastname) AS staff,
    co.orderPayment
FROM CafeOrder co
JOIN Patron p ON co.patron_id = p.patron_id
JOIN Staff s ON co.staffID = s.staffID
ORDER BY co.orderDate DESC;

-- View of Items in each cafe order
SELECT
    co.orderID,
    ci.itemName,
    oi.quantity,
    ci.itemPrice,
    (oi.quantity * ci.itemPrice) AS lineTotal
FROM OrderItem oi
JOIN CafeOrder co ON oi.orderID = co.orderID
JOIN CafeItem ci ON oi.itemID = ci.itemID
ORDER BY co.orderID;

-- View of total items sold by cafe item
SELECT
    ci.itemName,
    SUM(oi.quantity) AS totalSold
FROM OrderItem oi
JOIN CafeItem ci ON oi.itemID = ci.itemID
GROUP BY ci.itemID
ORDER BY totalSold DESC;

-- View of staff availability by day
SELECT
    CONCAT(s.firstname, ' ', s.lastname) AS staff,
    a.dayOfWeek,
    a.startTime,
    a.endTime
FROM Availability a
JOIN Staff s ON a.staffID = s.staffID
ORDER BY a.dayOfWeek, a.startTime;

-- View of Cafe Data
SELECT
    co.orderID,
    co.orderDate,
    p.first_name,
    p.last_name,
    s.firstname AS staff_first,
    s.lastname AS staff_last,
    ci.itemName,
    oi.quantity,
    ci.itemPrice
FROM CafeOrder co
JOIN Patron p ON co.patron_id = p.patron_id
JOIN Staff s ON co.staffID = s.staffID
JOIN OrderItem oi ON co.orderID = oi.orderID
JOIN CafeItem ci ON oi.itemID = ci.itemID;

-- View staff shifts with staff names
SELECT
    sh.shiftID,
    sh.shiftDate,
    sh.startTime,
    sh.endTime,
    CONCAT(s.firstname, ' ', s.lastname) AS staff
FROM Shift sh
JOIN Staff s ON sh.staffID = s.staffID
ORDER BY sh.shiftDate, sh.startTime;


-- *********** CODE TO TEST TRIGGERS HERE ***********

-- Testing trigger to block checkouts of books that are already checked out
SELECT * FROM Checkouts;
INSERT INTO Checkouts (due_date, return_date, checkout_date, patron_id, material_id) VALUES
('2026-10-01', NULL, '2026-08-01', 1, 1);
SELECT * FROM Checkouts;

SELECT *
FROM Patron_Reservation_View
WHERE patron_id = 1;

INSERT INTO Fee (fee_id, patron_id, fee_type, amount, fee_date, pay_status) VALUES
(7, 1, 'Late Fee', 5.00, '2026-03-28', 'unpaid'),
(8, 1, 'Late Fee', 5.00, '2026-03-28', 'unpaid'),
(9, 1, 'Late Fee', 5.00, '2026-03-28', 'unpaid');
SELECT get_unpaid_fee_total(1) AS unpaid_fee_total;


-- ***** TEST handle_inventory_on_order TRIGGER *****
-- Check stock BEFORE
SELECT itemID, inStock
FROM CafeItem
WHERE itemID = 3;

-- This should trigger the failure logic
INSERT INTO OrderItem (orderID, itemID, quantity)
VALUES (1, 3, 20);

-- Check if anything was inserted
SELECT *
FROM OrderItem
WHERE itemID = 3 AND quantity = 20;

-- Check stock AFTER
SELECT itemID, inStock
FROM CafeItem
WHERE itemID = 3;

-- ***** TEST apply_late_fees PROCEDURE *****
-- Show overdue, unreturned checkouts BEFORE
SELECT patron_id, material_id, due_date
FROM Checkouts
WHERE return_date IS NULL
  AND due_date < CURDATE();

-- Call the procedure
CALL apply_late_fees();

-- Verify late fees were added
SELECT patron_id, fee_type, amount, fee_date, pay_status
FROM Fee
WHERE fee_type = 'Late Fee'
ORDER BY fee_date DESC;
