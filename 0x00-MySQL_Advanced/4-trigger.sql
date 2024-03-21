/*
Create trigger to decrease item quantity after adding a new order
*/
DELIMITER //
CREATE TRIGGER update_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
END;
//
DELIMITER ;
