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
		ctx.JSON(http.StatusUnauthorized,handleError(fmt.Errorf("No token provided")))
	}
	payload,err:=server.maker.VerifyToken(authorization)
	if err!=nil{
		ctx.JSON(http.StatusUnauthorized,handleError(err))
	}
	ctx.Set("user_info",payload)
}