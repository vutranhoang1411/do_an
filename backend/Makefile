postgres:
	docker run --name doan_postgres12 -p 5432:5432  -e POSTGRES_USER=root -e POSTGRES_DB=do_an -e POSTGRES_PASSWORD=Hoang2002 -e TZ=Asia/Ho_Chi_Minh  -d postgres:12-alpine
dbup:
	migrate -path db/migration -database "postgresql://root:Hoang2002@localhost:5432/do_an?sslmode=disable" -verbose up
dbdown:
	migrate -path db/migration -database "postgresql://root:Hoang2002@localhost:5432/do_an?sslmode=disable" -verbose down
psql:
	docker exec -it doan_postgres12 psql -d do_an
PHONY:
	postgres dbup dbdown psql