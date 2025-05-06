

SELECT
    Customer_ID,
    Industry,
    Signup_Date,
    EXTRACT(YEAR FROM Signup_Date) AS Signup_Year,
    Last_Interaction_Date
FROM `onpremtocloud`.`analytics_dataset`.`kenya_customers`