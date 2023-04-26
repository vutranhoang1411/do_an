package api

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

var (

)
func (server *Server)userAuthorization(ctx *gin.Context){
	authorization:=ctx.GetHeader("authorization")
	if len(authorization)==0{
		ctx.JSON(http.StatusUnauthorized,handleError(fmt.Errorf("no token provided")))
		ctx.Abort()
		return
	}
	payload,err:=server.maker.VerifyToken(authorization)
	if err!=nil{
		ctx.JSON(http.StatusUnauthorized,handleError(err))
		ctx.Abort()
		return
	}
	ctx.Set("user_info",payload.Email)
}
func CORSMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {

        c.Header("Access-Control-Allow-Origin", "*")
        c.Header("Access-Control-Allow-Credentials", "true")
        c.Header("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
        c.Header("Access-Control-Allow-Methods", "POST,HEAD,PATCH, OPTIONS, GET, PUT")

        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(200)
            return
        }

        c.Next()
    }
}