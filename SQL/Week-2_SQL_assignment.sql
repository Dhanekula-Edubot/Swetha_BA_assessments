create database swetha;
use swetha;

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    location VARCHAR(50)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    department_id INT,
    salary INT,
    performance_rating VARCHAR(20),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

INSERT INTO departments (department_id, department_name, location) VALUES
(1, 'Engineering', 'Bangalore'),
(2, 'HR', 'Hyderabad'),
(3, 'Finance', 'Mumbai'),
(4, 'Marketing', 'Delhi'),
(5, 'Sales', 'Chennai');

INSERT INTO employees (emp_id, name, department_id, salary, performance_rating) VALUES
(101, 'Anita Sharma', 1, 75000, 'Excellent'),
(102, 'Ravi Kumar', 2, 45000, 'Good'),
(103, 'Sneha Rao', 3, 55000, 'Average'),
(104, 'Arjun Verma', 4, 62000, 'Excellent'),
(105, 'Meena Das', 5, 38000, 'Below Average');

SELECT name, salary
FROM employees
WHERE salary > 50000;

SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;

SELECT d.department_name, COUNT(e.emp_id) AS total_employees
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name;

SELECT name
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

SELECT name, salary,
       CASE
           WHEN salary > 60000 THEN 'High'
           WHEN salary BETWEEN 40000 AND 60000 THEN 'Medium'
           ELSE 'Low'
       END AS salary_status
FROM employees;

DESCRIBE employees;
DESCRIBE departments;

SELECT * FROM employees;

ALTER TABLE employees
ADD COLUMN bonus INT;
SET SQL_SAFE_UPDATES = 0;

UPDATE employees
SET bonus = CASE
    WHEN performance_rating = 'Excellent' THEN 10000
    WHEN performance_rating = 'Good' THEN 5000
    ELSE 1000
END;
SET SQL_SAFE_UPDATES = 1;
SELECT * FROM employees;