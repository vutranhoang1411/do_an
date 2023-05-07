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
	server.router.Static("/public/img","/home/hoangdeptrai/ki2nam3/do_an/backend/public/img")
	server.router.Use(CORSMiddleware())
	
	///add route
	server.router.POST("/api/create",server.createUser)
	server.router.POST("/api/login",server.loginUser)
	server.router.GET("/api/locker",server.getFreeLocker)

	authen_route:=server.router.Group("/api/user").Use(server.userAuthorization)
	authen_route.GET("",server.getUser)
	authen_route.POST("/locker",server.userRegisterLocker)
	authen_route.GET("/locker",server.getUserLocker)
	authen_route.POST("/img",server.updateImg)
	authen_route.POST("/payment",server.makePayment)
	authen_route.GET("/payment",server.getUserPayment)
	
	return server
}
func handleError(err error)gin.H{
	return gin.H{"error":err.Error()}
}
func (server *Server)Start(addr string)error{
	return server.router.Run(addr)
}