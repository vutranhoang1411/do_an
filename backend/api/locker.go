package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	db "github.com/vutranhoang1411/do_an_da_nganh/db/sqlc"
)

func (server *Server) getFreeLocker(ctx *gin.Context){
	locker_list,err:=server.model.GetAvailableCabinet(ctx)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err))
		return
	}
	ctx.JSON(http.StatusOK,map[string][]db.Cabinet{
		"available_locker":locker_list,
	})
}
