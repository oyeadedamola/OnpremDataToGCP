
  
    

    create or replace table `onpremtocloud`.`analytics_dataset`.`merged_transaction`
      
    
    

    OPTIONS()
    as (
      

  






    



    
        SELECT * FROM `onpremtocloud.analytics_dataset.merged_transaction`
        
            UNION ALL
        
    
        SELECT * FROM `onpremtocloud.analytics_dataset.ghana_transaction`
        
            UNION ALL
        
    
        SELECT * FROM `onpremtocloud.analytics_dataset.kenya_transaction`
        
            UNION ALL
        
    
        SELECT * FROM `onpremtocloud.analytics_dataset.nigeria_transaction`
        
    

    );
  