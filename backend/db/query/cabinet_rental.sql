-- name: CreateCabinetRental :one
insert into cabinet_locker_rentals(       
    CabinetID,    
    CustomerID,   
    rentdate,
    duration,  
    paymentMethod, 
    fee     
) values(
    $1,$2,$3,$4,$5,$6
) returning *;

