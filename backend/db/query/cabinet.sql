-- name: GetCabinetByID :one
select * from cabinet where ID=$1;

-- name: GetCabinetForRent :one
select * from cabinet where ID=$1 FOR UPDATE;

-- name: GetAvailableCabinet :many
select * from cabinet where avail=true;

-- name: GetUserCabinet :many
select * from cabinet where userID=$1;

-- name: RentCabinet :exec
update cabinet set userID=$1, start=NOW(), avail=false where ID=$2;

-- name: UnrentCabinet :exec
update cabinet set userID=null,start=null,avail=true where ID=$1;

-- name: UpdateCabinetOpen :one
update cabinet set open=true where ID=$1 returning *;

-- name: UpdateCabinetClose :one
update cabinet set open=false where ID=$1 returning *;