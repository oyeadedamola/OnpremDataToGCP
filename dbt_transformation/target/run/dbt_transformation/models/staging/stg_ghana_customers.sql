

  create or replace view `onpremtocloud`.`analytics_dataset`.`stg_ghana_customers`
  OPTIONS()
  as 

SELECT
    Customer_ID,
    Industry,
    Signup_Date,
    EXTRACT(YEAR FROM Signup_Date) AS Signup_year,
    Last_Interaction_Date
FROM `onpremtocloud`.`analytics_dataset`.`ghana_customers`;

