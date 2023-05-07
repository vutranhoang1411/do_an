package main

import (
	"database/sql"
	"log"

	"github.com/vutranhoang1411/do_an_da_nganh/api"
	"github.com/vutranhoang1411/do_an_da_nganh/util"
	_ "github.com/lib/pq"
)

func main(){
	config,err:=util.LoadConfig(".")
	if err!=nil{
		log.Fatal(err)
	}
	conn,err:=sql.Open(config.DBDriver,config.DBSource)
	if err!=nil{
		log.Fatal(err)
	}
	server:=api.NewServer(conn,config)
	server.Start(config.HttpServerAddress)
}