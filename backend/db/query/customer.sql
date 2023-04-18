-- name: GetCustomer :one
select * from customer
where ID = $1;

-- name: GetCustomerByEmail :one
select * from customer
where email = $1;

-- name: CreateCustomer :one
insert into customer(
    name,
    email,
    password
)values(
    $1,$2,$3
) RETURNING *;


-- name: UpdateUserPhoto :exec
update customer set photo=$1 where email=$2;
