package api

import (
	"database/sql"

	"github.com/gin-gonic/gin"
	db "github.com/vutranhoang1411/do_an_da_nganh/db/sqlc"
	"github.com/vutranhoang1411/do_an_da_nganh/token"
	"github.com/vutranhoang1411/do_an_da_nganh/util"
)
type Server struct{
	model db.Model
	router *gin.Engine
	maker token.Maker
	config util.Config
}

func NewServer(conn *sql.DB,config util.Config)*Server{
	server:=&Server{
		model: db.NewModel(conn),
	}
	server.config=config
	server.maker=token.NewPasetoMaker(config.TokenKey)
	server.router=gin.Default()
	
	///add route
	server.router.POST("/img",server.openLocker)
	server.router.POST("/user/create",server.createUser)
	server.router.POST("/user/login",server.loginUser)

	
	return server
}
func handleError(err error)gin.H{
	return gin.H{"error":err.Error()}
}
func (server *Server)Start(addr string)error{
	return server.router.Run(addr)
}