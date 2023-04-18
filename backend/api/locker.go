package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func (server *Server) getFreeLocker(ctx *gin.Context){
	locker_list,err:=server.model.GetAvailableCabinet(ctx)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err))
		return
	}
	ctx.JSON(http.StatusOK,locker_list)
}
